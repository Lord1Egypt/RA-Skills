import pytest
from database_handler import DatabaseHandler
from data_parser import DataParser
from calculate_stats import StatCalculator


@pytest.fixture
def twrr_scenario_db(tmp_path):
    """
    Scenario for testing TWRR active_base reduction:
    - Deposit 10000, buy asset at 100
    - Asset doubles to 200
    - Sell half, withdraw 10000 (half of 20000 cohort value)
    - active_base should be reduced by 50% (R = 10000/20000 = 0.5)
    - Remaining: 50 shares at latest_price 200 = 10000
    - active_base = 5000, value = 10000, TWRR return = 10000/5000 = 2.0
    """
    csv_content = """Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat
2020-01-15;1111;Insättning;Deposit;-;-;10000;0;SEK;;-
2020-01-16;1111;Köp;Asset A;100;100;-10000;0;SEK;TESTA;-
2021-01-15;1111;Sälj;Asset A;-50;200;10000;0;SEK;TESTA;-
2021-01-16;1111;Uttag;;-;-;-10000;0;SEK;;-
"""
    csv_file = tmp_path / "twrr_scenario.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    db_file = tmp_path / "test_twrr.db"
    db = DatabaseHandler(db_file)
    parser = DataParser(db)
    parser.add_data(str(csv_file))
    parser.process_transactions()
    return db


def test_twrr_active_base_tracking(twrr_scenario_db):
    """
    Test that active_base is correctly initialized and reduced proportionally on withdrawal.
    """
    twrr_scenario_db.connect()
    cur = twrr_scenario_db.get_cursor()

    rows = cur.execute(
        "SELECT month, deposit, active_base, capital FROM cohort_data ORDER BY month"
    ).fetchall()

    assert len(rows) == 1
    month, deposit, active_base, capital = rows[0]

    # Deposit was 10000, after withdrawal active_base should be ~5000
    assert deposit == 10000.0
    assert abs(active_base - 5000.0) < 1.0, f"Expected active_base ~5000, got {active_base}"


def test_twrr_closed_return_snapshot(twrr_scenario_db):
    """
    Test that closed_return is stored when a position is fully closed.
    """
    twrr_scenario_db.connect()
    cur = twrr_scenario_db.get_cursor()
    
    # closed_return should be NULL since position is still open (50 shares remain)
    row = cur.execute("SELECT closed_return FROM cohort_data").fetchone()
    assert row[0] is None, "Open position should not have closed_return"


@pytest.fixture
def twrr_closed_db(tmp_path):
    """
    Scenario for testing TWRR on fully closed positions:
    - Deposit 10000, buy asset at 100 (100 shares)
    - Asset doubles to 200
    - Sell all 100 shares at 200 = 20000
    - Withdraw 20000
    - Position fully closed, total return = 2.0x
    """
    csv_content = """Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat
2020-01-15;1111;Insättning;Deposit;-;-;10000;0;SEK;;-
2020-01-16;1111;Köp;Asset A;100;100;-10000;0;SEK;TESTA;-
2021-01-15;1111;Sälj;Asset A;-100;200;20000;0;SEK;TESTA;-
2021-01-16;1111;Uttag;;-;-;-20000;0;SEK;;-
"""
    csv_file = tmp_path / "twrr_closed.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    db_file = tmp_path / "test_twrr_closed.db"
    db = DatabaseHandler(db_file)
    parser = DataParser(db)
    parser.add_data(str(csv_file))
    parser.process_transactions()
    return db


def test_twrr_closed_position_has_return(twrr_closed_db):
    """
    Test that fully closed positions store closed_return and produce nonzero TWRR APY.
    """
    twrr_closed_db.connect()
    cur = twrr_closed_db.get_cursor()
    
    row = cur.execute("SELECT closed_return FROM cohort_data").fetchone()
    assert row[0] is not None, "Closed position should have closed_return"
    assert abs(row[0] - 2.0) < 0.1, f"Expected closed_return ~2.0, got {row[0]}"
    
    # Stats with TWRR should show nonzero APY
    stat_calc = StatCalculator(twrr_closed_db)
    stat_calc.calculate_stats(apy_mode='twrr')
    stats = stat_calc.get_stats(accounts=["1111"], period="month", deposits="all", apy_mode='twrr')
    
    cohort = stats[0]
    apy = cohort[10]
    assert apy is not None and apy > 5, f"Expected positive TWRR APY for closed position, got {apy}%"


def test_twrr_apy_open_position(twrr_scenario_db):
    """
    Test that TWRR APY uses active_base for open positions.
    value/active_base = 10000/5000 = 2.0 (100% total return).
    """
    stat_calculator = StatCalculator(twrr_scenario_db)
    stat_calculator.calculate_stats()

    stats = stat_calculator.get_stats(accounts=["1111"], period="month", deposits="all")

    cohort = next((s for s in stats if s[0].year == 2020 and s[0].month == 1), None)
    assert cohort is not None

    deposit = cohort[1]
    withdrawal = cohort[2]
    value = cohort[3]
    apy = cohort[10]

    assert deposit == 10000.0
    assert withdrawal == 10000.0
    # Value should be ~10000 (50 shares * 200 latest_price)
    assert value > 9000, f"Expected value ~10000, got {value}"
    # APY should be positive and substantial (100% return over ~5 years, annualized)
    assert apy > 10, f"Expected significant positive APY, got {apy}%"
