import pytest
from unittest.mock import patch, MagicMock
from datetime import date
from database_handler import DatabaseHandler
from data_parser import DataParser
from calculate_stats import StatCalculator


def test_retroactive_migration(tmp_path):
    """
    Test that retroactive migration query works correctly to populate asset_prices.
    """
    db_file = str(tmp_path / "test_migration.db")
    db = DatabaseHandler(db_file)
    db.connect()
    
    # Manually insert assets and processed transactions directly
    cur = db.get_cursor()
    cur.execute("INSERT INTO assets (asset) VALUES ('Asset A')")
    cur.execute("INSERT INTO assets (asset) VALUES ('Asset B')")
    asset_a_id = cur.execute("SELECT asset_id FROM assets WHERE asset = 'Asset A'").fetchone()[0]
    asset_b_id = cur.execute("SELECT asset_id FROM assets WHERE asset = 'Asset B'").fetchone()[0]
    
    # Insert processed transactions
    cur.execute("""
        INSERT INTO transactions (date, account, transaction_type, asset_name, amount, price, total, courtage, currency, isin, processed)
        VALUES ('2023-01-01', '1111', 'Köp', 'Asset A', 10, 100, -1000, 0, 'SEK', 'TESTA', 1)
    """)
    cur.execute("""
        INSERT INTO transactions (date, account, transaction_type, asset_name, amount, price, total, courtage, currency, isin, processed)
        VALUES ('2023-01-02', '1111', 'Sälj', 'Asset A', -5, 120, 600, 0, 'SEK', 'TESTA', 1)
    """)
    cur.execute("""
        INSERT INTO transactions (date, account, transaction_type, asset_name, amount, price, total, courtage, currency, isin, processed)
        VALUES ('2023-01-03', '1111', 'Tillgångsinsättning', 'Asset B', 5, 50, 0, 0, 'SEK', 'TESTB', 1)
    """)
    
    # Insert unprocessed and non-matching type transactions (should not be migrated)
    cur.execute("""
        INSERT INTO transactions (date, account, transaction_type, asset_name, amount, price, total, courtage, currency, isin, processed)
        VALUES ('2023-01-04', '1111', 'Köp', 'Asset A', 10, 150, -1500, 0, 'SEK', 'TESTA', 0)
    """)
    cur.execute("""
        INSERT INTO transactions (date, account, transaction_type, asset_name, amount, price, total, courtage, currency, isin, processed)
        VALUES ('2023-01-05', '1111', 'Ränta', 'Asset A', 0, 10, 10, 0, 'SEK', 'TESTA', 1)
    """)
    
    db.commit()
    
    # Drop the asset_prices table so we can trigger retroactive migration afresh
    cur.execute("DROP TABLE IF EXISTS asset_prices")
    db.commit()
    
    # Re-run create_tables() which triggers retroactive migration
    db.create_tables()
    
    # Verify migration results
    prices = cur.execute("SELECT asset_id, price_date, price, source FROM asset_prices ORDER BY price_date").fetchall()
    
    # Only the three processed transactions of valid types should be migrated
    assert len(prices) == 3
    
    # First: Köp Asset A at 100 on 2023-01-01
    assert prices[0][0] == asset_a_id
    assert str(prices[0][1]) == "2023-01-01"
    assert prices[0][2] == 100.0
    assert prices[0][3] == "transaction"
    
    # Second: Sälj Asset A at 120 on 2023-01-02
    assert prices[1][0] == asset_a_id
    assert str(prices[1][1]) == "2023-01-02"
    assert prices[1][2] == 120.0
    assert prices[1][3] == "transaction"
    
    # Third: Tillgångsinsättning Asset B at 50 on 2023-01-03
    assert prices[2][0] == asset_b_id
    assert str(prices[2][1]) == "2023-01-03"
    assert prices[2][2] == 50.0
    assert prices[2][3] == "transaction"


def test_parser_price_recording(tmp_path):
    """
    Test that when DataParser processes new transactions,
    it records the prices in the asset_prices table.
    """
    db_file = tmp_path / "test_parser.db"
    csv_file = tmp_path / "test_data.csv"
    
    csv_content = """Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat
2023-01-01;1111;Insättning;Deposit;-;-;10000;0;SEK;;-
2023-01-02;1111;Köp;Asset A;10;100;-1000;0;SEK;TESTA;-
2023-01-03;1111;Köp;Asset A;5;120;-600;0;SEK;TESTA;-
2023-01-04;1111;Sälj;Asset A;-5;150;750;0;SEK;TESTA;-
2023-01-05;1111;Tillgångsinsättning;Asset B;10;50;0;0;SEK;TESTB;-
"""
    csv_file.write_text(csv_content, encoding="utf-8")
    
    db = DatabaseHandler(str(db_file))
    parser = DataParser(db)
    parser.add_data(str(csv_file))
    parser.process_transactions()
    
    db.connect()
    cur = db.get_cursor()
    
    # Verify that asset_prices was populated during processing
    rows = cur.execute("""
        SELECT a.asset, ap.price_date, ap.price, ap.source
        FROM asset_prices ap
        JOIN assets a ON ap.asset_id = a.asset_id
        ORDER BY ap.price_date ASC
    """).fetchall()
    
    assert len(rows) == 4
    
    # 2023-01-02 Köp Asset A at 100
    assert rows[0] == ("Asset A", date(2023, 1, 2), 100.0, "transaction")
    # 2023-01-03 Köp Asset A at 120
    assert rows[1] == ("Asset A", date(2023, 1, 3), 120.0, "transaction")
    # 2023-01-04 Sälj Asset A at 150
    assert rows[2] == ("Asset A", date(2023, 1, 4), 150.0, "transaction")
    # 2023-01-05 Tillgångsinsättning Asset B at 50
    assert rows[3] == ("Asset B", date(2023, 1, 5), 50.0, "transaction")


def test_cohort_value_resolution(tmp_path):
    """
    Test that cohort_value correctly resolves prices using historical asset_prices
    when as_of_date is provided.
    """
    db_file = tmp_path / "test_cohort.db"
    db = DatabaseHandler(str(db_file))
    db.connect()
    cur = db.get_cursor()
    
    # Create asset and cohort asset
    cur.execute("INSERT INTO assets (asset, latest_price) VALUES ('Asset A', 200.0)")
    asset_id = cur.execute("SELECT asset_id FROM assets WHERE asset = 'Asset A'").fetchone()[0]
    
    # Insert cohort_data and cohort_assets
    cur.execute("""
        INSERT INTO cohort_data (month, account, deposit, active_base, capital)
        VALUES ('2023-01-01', '1111', 1000.0, 1000.0, 0.0)
    """)
    cur.execute("""
        INSERT INTO cohort_assets (month, asset_id, account, amount, average_price)
        VALUES ('2023-01-01', ?, '1111', 10, 100.0)
    """, (asset_id,))
    
    # Insert price history:
    # On 2023-01-15, price was 100
    # On 2023-02-15, price was 150
    # On 2023-03-15, price was 180
    cur.execute("INSERT INTO asset_prices (asset_id, price_date, price, source) VALUES (?, '2023-01-15', 100.0, 'transaction')", (asset_id,))
    cur.execute("INSERT INTO asset_prices (asset_id, price_date, price, source) VALUES (?, '2023-02-15', 150.0, 'transaction')", (asset_id,))
    cur.execute("INSERT INTO asset_prices (asset_id, price_date, price, source) VALUES (?, '2023-03-15', 180.0, 'transaction')", (asset_id,))
    db.commit()
    
    db.interpolate = False
    parser = DataParser(db)
    
    # 1. Without as_of_date, uses latest_price (200.0)
    val_latest = parser.cohort_value(date(2023, 1, 1), '1111')
    assert val_latest == 2000.0  # 10 shares * 200.0
    
    # 2. As of 2023-01-20, closest price on or before is 100.0 (from 2023-01-15)
    val_jan = parser.cohort_value(date(2023, 1, 1), '1111', as_of_date=date(2023, 1, 20))
    assert val_jan == 1000.0  # 10 shares * 100.0
    
    # 3. As of 2023-02-28, closest price on or before is 150.0 (from 2023-02-15)
    val_feb = parser.cohort_value(date(2023, 1, 1), '1111', as_of_date=date(2023, 2, 28))
    assert val_feb == 1500.0  # 10 shares * 150.0
    
    # 4. As of 2023-01-01 (before any price in history), flat-carry the first
    #    known price (100.0 from 2023-01-15) backwards. Do NOT fall back to
    #    latest_price — that is a current value and would leak a future price
    #    into a historical valuation.
    val_before = parser.cohort_value(date(2023, 1, 1), '1111', as_of_date=date(2023, 1, 1))
    assert val_before == 1000.0  # 10 shares * 100.0 (first known price)


@patch('requests.post')
def test_update_prices_records_history(mock_post, tmp_path):
    """
    Test that update_prices records fetched prices in the asset_prices table.
    """
    db_file = tmp_path / "test_updater.db"
    db = DatabaseHandler(str(db_file))
    db.connect()
    cur = db.get_cursor()
    
    # Insert held asset
    cur.execute("INSERT INTO assets (asset, amount) VALUES ('Asset A', 10)")
    asset_id = cur.execute("SELECT asset_id FROM assets WHERE asset = 'Asset A'").fetchone()[0]
    db.commit()
    
    # Mock Avanza search API response
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "hits": [
            {
                "price": {
                    "last": "123,45"
                }
            }
        ]
    }
    mock_post.return_value = mock_resp
    
    stat_calc = StatCalculator(db)
    stat_calc.update_prices(force=True)
    
    # Check that it updated asset_prices table
    prices = cur.execute("SELECT asset_id, price_date, price, source FROM asset_prices").fetchall()
    assert len(prices) == 1
    assert prices[0][0] == asset_id
    assert prices[0][2] == 123.45
    assert prices[0][3] == "external"


def test_historical_price_superseding_and_resolution(tmp_path):
    """
    Test that historical prices resolved during a withdrawal are:
    1. Correctly superseded by more recent transaction prices for an asset.
    2. Correctly applied (affecting the cohort valuation) for assets with no newer transactions.
    """
    db_file = tmp_path / "test_fake_prices.db"
    csv_file = tmp_path / "test_data.csv"
    
    # Write test CSV with transactions
    csv_content = """Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat
2020-01-15;1111;Insättning;Deposit;-;-;20000;0;SEK;;-
2020-01-16;1111;Köp;Asset A;100;100;-10000;0;SEK;TESTA;-
2020-01-16;1111;Köp;Asset B;100;100;-10000;0;SEK;TESTB;-
2021-01-15;1111;Sälj;Asset A;-50;200;10000;0;SEK;TESTA;-
2021-01-16;1111;Uttag;;-;-;-10000;0;SEK;;-
"""
    csv_file.write_text(csv_content, encoding="utf-8")
    
    def run_with_fake_prices(fake_prices=None):
        if db_file.exists():
            db_file.unlink()
        db = DatabaseHandler(str(db_file))
        db.interpolate = False
        parser = DataParser(db)
        parser.add_data(str(csv_file))
        
        db.connect()
        cur = db.get_cursor()
        
        # Step through transactions manually up to withdrawal, then inject fake prices
        cur.execute("SELECT *, rowid FROM transactions ORDER BY date ASC, rowid ASC")
        txs = cur.fetchall()
        for tx in txs:
            tx_type = tx[2]
            if tx_type == "Insättning":
                parser.handle_deposit(tx)
            elif tx_type == "Köp":
                parser.handle_purchase(tx)
            elif tx_type == "Sälj":
                parser.handle_sale(tx)
            elif tx_type == "Tillgångsinsättning":
                parser.handle_asset_deposit(tx)
            elif tx_type == "Uttag":
                if fake_prices:
                    for asset_name, p_date, p_val in fake_prices:
                        (asset_id,) = cur.execute("SELECT asset_id FROM assets WHERE asset = ?", (asset_name,)).fetchone()
                        cur.execute(
                            "INSERT OR REPLACE INTO asset_prices (asset_id, price_date, price, source) VALUES (?, ?, ?, 'external')",
                            (asset_id, p_date, p_val)
                        )
                    db.commit()
                parser.handle_withdrawal(tx)
                
        cur.execute("SELECT active_base FROM cohort_data WHERE month = '2020-01-31'")
        active_base = cur.fetchone()[0]
        
        cur.close()
        parser._data_cur = None
        parser._transaction_cur = None
        db.disconnect()
        return active_base

    # 1. Baseline Case: active_base drops from 20000 to 13333.33 (since Asset A = 50*200=10k, Asset B = 100*100=10k, Cash = 10k)
    ab_baseline = run_with_fake_prices()
    assert abs(ab_baseline - 13333.3333) < 1e-2
    
    # 2. Case A: Inject fake price for Asset A (999.0) on 2020-06-01.
    # Since Asset A has a newer transaction price (200.0) on 2021-01-15, the fake price should be superseded.
    # Resulting active_base must be identical to baseline.
    ab_case_a = run_with_fake_prices([("Asset A", "2020-06-01", 999.0)])
    assert abs(ab_case_a - ab_baseline) < 1e-4
    
    # 3. Case B: Inject fake price for Asset B (50.0) on 2020-06-01.
    # Since Asset B has no newer transaction price, the fake price is resolved and reduces its valuation,
    # which alters the active_base reduction.
    ab_case_b = run_with_fake_prices([("Asset B", "2020-06-01", 50.0)])
    assert abs(ab_case_b - ab_baseline) > 1.0
    assert abs(ab_case_b - 12000.0) < 1e-2


@patch('requests.get')
@patch('requests.post')
def test_update_prices_detailed_fetching(mock_post, mock_get, tmp_path):
    """
    Test that update_prices fetches detailed date and price information for
    funds, stocks, and certificates, and falls back to today's date on failure.
    """
    db_file = tmp_path / "test_updater_detail.db"
    db = DatabaseHandler(str(db_file))
    db.connect()
    cur = db.get_cursor()
    
    # Insert 4 assets: a Fund, a Stock, a Certificate, and a Fallback asset
    cur.execute("INSERT INTO assets (asset, amount) VALUES ('Avanza Global', 10)")
    cur.execute("INSERT INTO assets (asset, amount) VALUES ('AstraZeneca', 5)")
    cur.execute("INSERT INTO assets (asset, amount) VALUES ('Valour Ethereum', 2)")
    cur.execute("INSERT INTO assets (asset, amount) VALUES ('Fallback Asset', 1)")
    db.commit()
    
    fund_id = cur.execute("SELECT asset_id FROM assets WHERE asset = 'Avanza Global'").fetchone()[0]
    stock_id = cur.execute("SELECT asset_id FROM assets WHERE asset = 'AstraZeneca'").fetchone()[0]
    cert_id = cur.execute("SELECT asset_id FROM assets WHERE asset = 'Valour Ethereum'").fetchone()[0]
    fallback_id = cur.execute("SELECT asset_id FROM assets WHERE asset = 'Fallback Asset'").fetchone()[0]
    
    # Mock search API response based on the asset query
    def mock_post_side_effect(url, headers=None, json=None, timeout=None):
        query = json.get("query")
        resp = MagicMock()
        resp.status_code = 200
        if query == "Avanza Global":
            resp.json.return_value = {
                "hits": [{
                    "type": "FUND",
                    "orderBookId": "878733",
                    "price": {"last": "250,00"}
                }]
            }
        elif query == "AstraZeneca":
            resp.json.return_value = {
                "hits": [{
                    "type": "STOCK",
                    "orderBookId": "5431",
                    "price": {"last": "1800,00"}
                }]
            }
        elif query == "Valour Ethereum":
            resp.json.return_value = {
                "hits": [{
                    "type": "CERTIFICATE",
                    "orderBookId": "1208273",
                    "price": {"last": "16,00"}
                }]
            }
        else: # Fallback Asset search hit
            resp.json.return_value = {
                "hits": [{
                    "type": "UNKNOWN",
                    "orderBookId": "9999",
                    "price": {"last": "50,00"}
                }]
            }
        return resp
        
    mock_post.side_effect = mock_post_side_effect
    
    # Mock get API response for detailed endpoints
    def mock_get_side_effect(url, headers=None, timeout=None):
        resp = MagicMock()
        if "fund-reference/reference/878733" in url:
            resp.status_code = 200
            resp.json.return_value = {
                "nav": 257.91,
                "navDate": "2026-07-03T00:00:00"
            }
        elif "market-guide/stock/5431" in url:
            resp.status_code = 200
            resp.json.return_value = {
                "quote": {
                    "last": 1863.0,
                    "updated": 1783094400643 # 2026-07-03
                }
            }
        elif "market-guide/certificate/1208273" in url:
            resp.status_code = 200
            resp.json.return_value = {
                "quote": {
                    "last": 16.80,
                    "updated": 1783094400561 # 2026-07-03
                }
            }
        else:
            resp.status_code = 404
        return resp
        
    mock_get.side_effect = mock_get_side_effect
    
    stat_calc = StatCalculator(db)
    stat_calc.update_prices(force=True)
    
    # Verify fund details recorded correctly
    fund_price = cur.execute("SELECT price, price_date FROM asset_prices WHERE asset_id = ? AND source = 'external'", (fund_id,)).fetchone()
    assert fund_price is not None
    assert fund_price[0] == 257.91
    assert str(fund_price[1]) == "2026-07-03"
    
    # Verify stock details recorded correctly
    stock_price = cur.execute("SELECT price, price_date FROM asset_prices WHERE asset_id = ? AND source = 'external'", (stock_id,)).fetchone()
    assert stock_price is not None
    assert stock_price[0] == 1863.0
    assert str(stock_price[1]) == "2026-07-03"
    
    # Verify certificate details recorded correctly
    cert_price = cur.execute("SELECT price, price_date FROM asset_prices WHERE asset_id = ? AND source = 'external'", (cert_id,)).fetchone()
    assert cert_price is not None
    assert cert_price[0] == 16.80
    assert str(cert_price[1]) == "2026-07-03"
    
    # Verify fallback asset recorded correctly with today's date
    today = date.today()
    fallback_price = cur.execute("SELECT price, price_date FROM asset_prices WHERE asset_id = ? AND source = 'external'", (fallback_id,)).fetchone()
    assert fallback_price is not None
    assert fallback_price[0] == 50.0
    assert fallback_price[1] == today


def test_parse_date_bound():
    from cli import parse_date_bound
    # Test YYYY
    assert parse_date_bound("2022", is_start_bound=True) == date(2022, 1, 1)
    assert parse_date_bound("2022", is_start_bound=False) == date(2022, 12, 31)
    
    # Test YYYY-MM
    assert parse_date_bound("2022-02", is_start_bound=True) == date(2022, 2, 1)
    assert parse_date_bound("2022-02", is_start_bound=False) == date(2022, 2, 28)
    assert parse_date_bound("2024-02", is_start_bound=False) == date(2024, 2, 29) # Leap year
    
    # Test YYYY-MM-DD
    assert parse_date_bound("2022-06-15", is_start_bound=True) == date(2022, 6, 15)
    assert parse_date_bound("2022-06-15", is_start_bound=False) == date(2022, 6, 15)
    
    # Test None/empty
    assert parse_date_bound(None) is None
    assert parse_date_bound("") is None
    
    # Test invalid
    with pytest.raises(ValueError):
        parse_date_bound("invalid")


def test_stats_date_range_filtering(tmp_path):
    db_file = tmp_path / "test_filter_stats.db"
    db = DatabaseHandler(str(db_file))
    db.connect()
    db.create_tables()
    
    # Initialize per-account tables
    stat_calc = StatCalculator(db)
    stat_calc._ensure_per_account_tables()
    
    # Setup mock tables and stats data
    cur = db.get_cursor()
    db.reset_table("account_cohort_stats")
    
    # Insert cohort stats rows for various months
    data = [
        ('A1', '2021-01-31', 100.0, 0.0, 110.0, 10.0, 0.0, 10.0, 10.0, 0.0, 10.0, 5.0, 100.0, 100.0, 110.0, 10.0, 10.0),
        ('A1', '2021-06-30', 200.0, 0.0, 220.0, 20.0, 0.0, 20.0, 10.0, 0.0, 10.0, 6.0, 300.0, 300.0, 330.0, 30.0, 30.0),
        ('A1', '2022-01-31', 500.0, 0.0, 550.0, 50.0, 0.0, 50.0, 10.0, 0.0, 10.0, 7.0, 800.0, 800.0, 880.0, 80.0, 80.0),
        ('A1', '2022-12-31', 1000.0, 0.0, 1100.0, 100.0, 0.0, 100.0, 10.0, 0.0, 10.0, 8.0, 1800.0, 1800.0, 1980.0, 180.0, 180.0)
    ]
    
    for row in data:
        cur.execute("""
            INSERT INTO account_cohort_stats (
                account, month, deposit, withdrawal, value,
                total_gainloss, realized_gainloss, unrealized_gainloss,
                total_gainloss_per, realized_gainloss_per, unrealized_gainloss_per,
                annual_per_yield, acc_net_deposit, acc_deposit, acc_value,
                acc_unrealized_gainloss, acc_total_gainloss
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, row)
    db.commit()
    
    stat_calc = StatCalculator(db)
    
    # Test filtering with start_date and end_date
    res_filtered = stat_calc.get_stats(
        accounts=['A1'], period='month', deposits='all',
        start_date=date(2021, 6, 1), end_date=date(2022, 6, 1)
    )
    
    # Should only return '2021-06-30' and '2022-01-31'
    assert len(res_filtered) == 2
    assert res_filtered[0][0] == date(2021, 6, 30)
    assert res_filtered[1][0] == date(2022, 1, 31)
    
    # Test get_accumulated with start_date and end_date
    acc_filtered = stat_calc.get_accumulated(
        accounts=['A1'], period='month', deposits='all',
        start_date=date(2022, 1, 1)
    )
    # Should return '2022-01-31' and '2022-12-31'
    assert len(acc_filtered) == 2
    assert acc_filtered[0][0] == date(2022, 1, 31)
    assert acc_filtered[1][0] == date(2022, 12, 31)
    db.disconnect()


@patch("requests.post")
def test_update_prices_only_held_by_default(mock_post, tmp_path):
    db_file = tmp_path / "test_held_assets.db"
    db = DatabaseHandler(str(db_file))
    db.connect()
    db.create_tables()
    
    cur = db.get_cursor()
    # Insert assets: A (held, amount = 10), B (not held, amount = 0)
    cur.execute("INSERT INTO assets (asset, amount) VALUES ('Asset Held', 10.0)")
    cur.execute("INSERT INTO assets (asset, amount) VALUES ('Asset Unheld', 0.0)")
    db.commit()
    
    resp = MagicMock()
    resp.status_code = 200
    resp.json.return_value = {"hits": []}
    mock_post.return_value = resp
    
    stat_calc = StatCalculator(db)
    
    # By default, update_prices should only request 'Asset Held'
    stat_calc.update_prices(force=True)
    
    # Check calls to mock_post
    called_queries = [call.kwargs['json']['query'] for call in mock_post.call_args_list]
    assert "Asset Held" in called_queries
    assert "Asset Unheld" not in called_queries
    
    # Clear mock
    mock_post.reset_mock()
    
    # With update_all=True, it should request both
    stat_calc.update_prices(force=True, update_all=True)
    called_queries = [call.kwargs['json']['query'] for call in mock_post.call_args_list]
    assert "Asset Held" in called_queries
    assert "Asset Unheld" in called_queries
    
    db.disconnect()




