import pytest
import math
from datetime import date
from unittest.mock import patch, MagicMock
from database_handler import DatabaseHandler
from data_parser import DataParser
from scripts.risk_calculator import RiskCalculator, generate_monthly_dates, clear_riksbanken_cache


@pytest.fixture(autouse=True)
def _clear_rate_cache():
    """Clear the Riksbanken rate cache between tests so mocked requests.get
    call counts are deterministic."""
    clear_riksbanken_cache()
    yield
    clear_riksbanken_cache()


@pytest.fixture
def risk_scenario_db(tmp_path):
    """
    Scenario for testing risk metrics:
    - 2020-01-15: Deposit 10000
    - 2020-01-16: Buy Asset A (100 shares at 100 SEK)
    """
    csv_content = """Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat
2020-01-15;1111;Insättning;Deposit;-;-;10000;0;SEK;;-
2020-01-16;1111;Köp;Asset A;100;100;-10000;0;SEK;TESTA;-
"""
    csv_file = tmp_path / "risk_scenario.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    db_file = tmp_path / "test_risk.db"
    db = DatabaseHandler(db_file)
    parser = DataParser(db)
    parser.add_data(str(csv_file))
    parser.process_transactions()
    
    # Manually inject asset prices for month ends:
    # 2020-01-31: Price 110 SEK
    # 2020-02-29: Price 121 SEK
    # 2020-03-31: Price 96.8 SEK
    db.connect()
    cur = db.get_cursor()
    cur.execute("INSERT OR REPLACE INTO asset_prices (asset_id, price_date, price, source) VALUES (1, '2020-01-31', 110.0, 'external')")
    cur.execute("INSERT OR REPLACE INTO asset_prices (asset_id, price_date, price, source) VALUES (1, '2020-02-29', 121.0, 'external')")
    cur.execute("INSERT OR REPLACE INTO asset_prices (asset_id, price_date, price, source) VALUES (1, '2020-03-31', 96.8, 'external')")
    db.commit()
    db.disconnect()
    
    return db


def test_generate_monthly_dates():
    start = date(2020, 1, 5)
    end = date(2020, 3, 15)
    dates = generate_monthly_dates(start, end)
    
    # Expected: day before start's month end (i.e. prev month end: 2019-12-31)
    # plus month ends for Jan, Feb, and end date 2020-03-15
    assert dates == [
        date(2019, 12, 31),
        date(2020, 1, 31),
        date(2020, 2, 29),
        date(2020, 3, 15)
    ]


@patch("scripts.risk_calculator.requests.get")
def test_risk_calculator_metrics(mock_get, risk_scenario_db):
    # Mock Riksbanken to return 2%
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = [{"date": "2020-03-01", "value": 2.0}]
    mock_get.return_value = mock_resp
    
    calculator = RiskCalculator(
        db=risk_scenario_db,
        accounts="1111",
        from_date="2020-01-01",
        to_date="2020-03-31",
        beta_ticker=None,
        interpolate=True
    )
    
    metrics = calculator.calculate(portfolio_apy=-0.1451)
    
    # Portfolio values at:
    # 2019-12-31 (t_0): 0
    # 2020-01-31 (t_1): 100 shares * 110 = 11000
    # 2020-02-29 (t_2): 100 shares * 121 = 12100
    # 2020-03-31 (t_3): 100 shares * 96.8 = 9680
    
    # Cash flow: 10000 deposit on 2020-01-15 (period 1 only)
    #
    # Modified Dietz returns:
    # Period 1 (31 days): v_start=0, v_end=11000, cf=10000 on Jan 15
    #   weighted_cf = 10000 * (Jan31 - Jan15) / 31 = 10000 * 16/31
    #   r1 = (11000 - 0 - 10000) / (10000 * 16/31) = 1000 / 5161.29 = 0.19375
    # Period 2 (29 days): v_start=11000, v_end=12100, cf=0
    #   r2 = (12100 - 11000) / 11000 = 0.10
    # Period 3 (31 days): v_start=12100, v_end=9680, cf=0
    #   r3 = (9680 - 12100) / 12100 = -0.20
    # Returns series: [0.19375, 0.10, -0.20]
    
    # Mean of returns: (0.19375 + 0.10 - 0.20) / 3 = 0.03125
    # Variance: ((0.1625)^2 + (0.06875)^2 + (-0.23125)^2) / 2 = 0.042305
    # Monthly Stddev = sqrt(0.042305) = 0.20568
    # Annualized Stddev = 0.20568 * sqrt(12) = 0.7125
    
    # Sharpe Ratio:
    # risk_free_rate = 0.02
    # overall_return = -0.1451 (-14.51%) supplied by caller
    # Sharpe = (-0.1451 - 0.02) / 0.7125 = -0.2317
    
    # Max Drawdown:
    # Cumulative index: [1.0, 1.19375, 1.3131, 1.0505]
    # Peak = 1.3131 at Feb 29, Trough = 1.0505 at Mar 31
    # Max Drawdown = (1.3131 - 1.0505) / 1.3131 = 0.20 (20%)
    
    assert abs(metrics['annualized_stddev'] - 0.7125) < 0.001
    assert abs(metrics['sharpe_ratio'] - (-0.2317)) < 0.01
    assert abs(metrics['max_drawdown'] - 0.20) < 0.001
    assert metrics['max_drawdown_peak'] == date(2020, 2, 29)
    assert metrics['max_drawdown_trough'] == date(2020, 3, 31)
    
    # Verify Riksbanken was called with correct parameters
    mock_get.assert_called_once()
    args, kwargs = mock_get.call_args
    assert "SECBREPOEFF" in args[0]
    assert "2020-01-01" in args[0]
    assert "2020-03-31" in args[0]


@patch("scripts.risk_calculator.requests.get")
def test_riksbanken_rate_fallback(mock_get, risk_scenario_db):
    # Mock Riksbanken API failure (connection error or HTTP error)
    mock_get.side_effect = Exception("Connection error")
    
    calculator = RiskCalculator(
        db=risk_scenario_db,
        accounts="1111",
        from_date="2020-01-01",
        to_date="2020-03-31",
        beta_ticker=None,
        interpolate=True
    )
    
    metrics = calculator.calculate(portfolio_apy=-0.1451)
    
    # Should fall back to 2.0%
    assert metrics['risk_free_rate'] == 0.02
    assert abs(metrics['sharpe_ratio'] - (-0.2317)) < 0.01


@patch("scripts.risk_calculator.requests.get")
def test_beta_calculation(mock_get, risk_scenario_db):
    # We call calculate twice: once for Riksbanken, once for Yahoo Finance chart
    # Mock Riksbanken response
    mock_riksbanken_resp = MagicMock()
    mock_riksbanken_resp.status_code = 200
    mock_riksbanken_resp.json.return_value = [{"date": "2020-03-01", "value": 0.0}]
    
    # Mock Yahoo Finance response
    # Timestamps correspond to 2019-12-31, 2020-01-31, 2020-02-29, 2020-03-31
    import time
    ts_0 = int(time.mktime(date(2019, 12, 31).timetuple()))
    ts_1 = int(time.mktime(date(2020, 1, 31).timetuple()))
    ts_2 = int(time.mktime(date(2020, 2, 29).timetuple()))
    ts_3 = int(time.mktime(date(2020, 3, 31).timetuple()))
    
    mock_yahoo_resp = MagicMock()
    mock_yahoo_resp.status_code = 200
    mock_yahoo_resp.json.return_value = {
        "chart": {
            "result": [
                {
                    "timestamp": [ts_0, ts_1, ts_2, ts_3],
                    "indicators": {
                        "quote": [{"close": [100.0, 105.0, 110.25, 99.225]}]  # returns: [0.05, 0.05, -0.10]
                    }
                }
            ]
        }
    }
    
    # Side effects for Riksbanken first, then Yahoo Finance
    mock_get.side_effect = [mock_riksbanken_resp, mock_yahoo_resp]
    
    calculator = RiskCalculator(
        db=risk_scenario_db,
        accounts="1111",
        from_date="2020-01-01",
        to_date="2020-03-31",
        beta_ticker="^OMXSPI",
        interpolate=True
    )
    
    metrics = calculator.calculate(portfolio_apy=-0.1451)
    
    # Port returns (Modified Dietz): [0.19375, 0.10, -0.20], mean: 0.03125
    # Bench returns: [0.05, 0.05, -0.10], mean: 0.0
    
    # Covariance:
    # ((0.19375 - 0.03125) * 0.05 + (0.10 - 0.03125) * 0.05 + (-0.20 - 0.03125) * (-0.10)) / 2
    # = (0.008125 + 0.0034375 + 0.023125) / 2 = 0.01734375
    
    # Var(bench):
    # ((0.05 - 0)**2 + (0.05 - 0)**2 + (-0.10 - 0)**2) / 2
    # = (0.0025 + 0.0025 + 0.01) / 2 = 0.0075
    
    # Beta = Covariance / Var(bench) = 0.01734375 / 0.0075 = 2.3125
    
    assert metrics['beta'] is not None
    assert abs(metrics['beta'] - 2.3125) < 0.01


@pytest.fixture
def cf_dominated_scenario_db(tmp_path):
    """
    Scenario that reproduces the cf-dominated first-period blow-up (task #2/#71):
        - 2020-01-15: Deposit 100, buy 1 share @ 100
        - 2020-02-10: Deposit 10000 (cash, no purchase)
        - 2020-02-29 price = 50 (asset drops)

    Period 2 (Jan 31 -> Feb 29) has:
        v_start = 100   (1 share @ 100)
        v_end   = 10050 (1 share @ 50 + 10000 cash)
        cf      = 10000 on Feb 10

    Under simple Dietz the return is (10050 - 100 - 10000) / 100 = -500%,
    which would push max_drawdown below -100% and inflate stddev. The fix is
    Modified Dietz: the cash flow is time-weighted by how much of the period
    it was invested, so weighted_cf = 10000 * 19/29 = 6551.72 and the return
    becomes (10050 - 100 - 10000) / (100 + 6551.72) ~= -0.75%. The drawdown
    index is also floored at 1e-9 so max_drawdown can never exceed 100%.
    """
    csv_content = """Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat
2020-01-15;1111;Insättning;Deposit;-;-;100;0;SEK;;-
2020-01-16;1111;Köp;Asset A;1;100;-100;0;SEK;TESTA;-
2020-02-10;1111;Insättning;Deposit;-;-;10000;0;SEK;;-
"""
    csv_file = tmp_path / "cf_dominated.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    db_file = tmp_path / "test_cf_dominated.db"
    db = DatabaseHandler(db_file)
    parser = DataParser(db)
    parser.add_data(str(csv_file))
    parser.process_transactions()

    db.connect()
    cur = db.get_cursor()
    cur.execute("INSERT OR REPLACE INTO asset_prices (asset_id, price_date, price, source) VALUES (1, '2020-01-31', 100.0, 'external')")
    cur.execute("INSERT OR REPLACE INTO asset_prices (asset_id, price_date, price, source) VALUES (1, '2020-02-29', 50.0, 'external')")
    cur.execute("INSERT OR REPLACE INTO asset_prices (asset_id, price_date, price, source) VALUES (1, '2020-03-31', 55.0, 'external')")
    db.commit()
    db.disconnect()

    return db


@patch("scripts.risk_calculator.requests.get")
def test_modified_dietz_handles_cash_flow_dominated_period(mock_get, cf_dominated_scenario_db):
    """Regression test: a large cash flow into a small starting balance must
    not produce an impossible return. Modified Dietz time-weights the cash
    flow so the return stays bounded.

    Scenario (from cf_dominated_scenario_db):
      2020-01-15: Deposit 100, buy 1 share @ 100
      2020-02-10: Deposit 10000 (cash, no purchase)
      Prices:     Jan 31 = 100, Feb 29 = 50, Mar 31 = 55

    Period 2 (Jan 31 -> Feb 29, 29 days):
      v_start = 100 (1 share @ 100)
      v_end   = 10050 (1 share @ 50 + 10000 cash)
      cf      = 10000 on Feb 10 (19 days before period end)
      Simple Dietz:   r = (10050 - 100 - 10000) / 100 = -50% (misleading)
      Modified Dietz: weighted_cf = 10000 * 19/29 = 6551.72
                      r = (10050 - 100 - 10000) / (100 + 6551.72) = -0.75%
    """
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = [{"date": "2020-03-01", "value": 2.0}]
    mock_get.return_value = mock_resp

    calculator = RiskCalculator(
        db=cf_dominated_scenario_db,
        accounts="1111",
        from_date="2020-01-01",
        to_date="2020-03-31",
        beta_ticker=None,
        interpolate=True,
    )
    metrics = calculator.calculate(portfolio_apy=-0.5)

    # Modified Dietz keeps the return bounded; no impossible drawdowns.
    assert metrics['max_drawdown'] <= 1.0, "max_drawdown must be <= 100%"
    assert metrics['max_drawdown'] >= 0.0, "max_drawdown must be non-negative"
    # Stddev must be plausible (the old simple-Dietz -50% outlier is gone).
    assert metrics['annualized_stddev'] < 0.1, (
        f"stddev should be small with Modified Dietz, "
        f"got {metrics['annualized_stddev']}"
    )
