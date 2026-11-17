import sys
sys.path.insert(0, "..")
import sqlite3
import pytest
from datetime import date
from database_handler import DatabaseHandler
from data_parser import DataParser
from calculate_stats import StatCalculator

@pytest.fixture
def apy_test_db(tmp_path):
    # Set up a database with:
    # 2020-01-01: Deposit 10000 SEK (Account 1111)
    # 2020-01-02: Buy Asset A (100 shares @ 100 SEK = 10000 SEK)
    # 2020-07-01: Deposit 5000 SEK (Account 1111)
    # 2020-07-02: Buy Asset A (50 shares @ 100 SEK = 5000 SEK)
    csv_content = """Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat
2020-01-01;1111;Insättning;Deposit;-;-;10000;0;SEK;;-
2020-01-02;1111;Köp;Asset A;100;100;-10000;0;SEK;TESTA;-
2020-07-01;1111;Insättning;Deposit;-;-;5000;0;SEK;;-
2020-07-02;1111;Köp;Asset A;50;100;-5000;0;SEK;TESTA;-
"""
    csv_file = tmp_path / "apy_test.csv"
    csv_file.write_text(csv_content, encoding="utf-8")
    
    db_file = tmp_path / "test_account_apy.db"
    db = DatabaseHandler(db_file)
    
    parser = DataParser(db)
    parser.add_data(str(csv_file))
    parser.process_transactions()
    
    return db

def test_account_apy_mwrr(apy_test_db):
    # Set asset price for Asset A to 120 SEK as of 2020-12-31
    cur = apy_test_db.get_cursor()
    cur.execute("UPDATE assets SET latest_price = 120.0, latest_price_date = '2020-12-31'")
    cur.execute("INSERT OR REPLACE INTO asset_prices (asset_id, price_date, price, source) VALUES (1, '2020-12-31', 120.0, 'external')")
    apy_test_db.commit()
    
    stat_calc = StatCalculator(apy_test_db)
    # Run stats calculation
    stat_calc.calculate_stats(apy_mode='mwrr')
    
    # 1. MWRR calculation over the year
    # End date: 2020-12-31 (365 days from 2020-01-01)
    # Deposits: 10000 (day 0), 5000 (day 182)
    # Valuation: 150 shares * 120 SEK = 18000 SEK
    # Net invested: 15000
    # Gain: 3000
    # Weight for CF2: (365 - 182)/365 = 183/365 ≈ 0.50137
    # Denominator = 10000 * 1.0 + 5000 * 0.50137 = 12506.85
    # HPR = 3000 / 12506.85 ≈ 0.23987
    # APY ≈ 23.99%
    apy, total_days = stat_calc.calculate_account_apy('1111', apy_mode='mwrr', end_date=date(2020, 12, 31))
    
    assert total_days == 365
    assert apy is not None
    assert 23.9 <= apy <= 24.1
    
def test_account_apy_twrr(apy_test_db):
    cur = apy_test_db.get_cursor()
    cur.execute("UPDATE assets SET latest_price = 120.0, latest_price_date = '2020-12-31'")
    cur.execute("INSERT OR REPLACE INTO asset_prices (asset_id, price_date, price, source) VALUES (1, '2020-12-31', 120.0, 'external')")
    apy_test_db.commit()
    
    stat_calc = StatCalculator(apy_test_db)
    stat_calc.calculate_stats(apy_mode='twrr')
    
    apy, total_days = stat_calc.calculate_account_apy('1111', apy_mode='twrr', end_date=date(2020, 12, 31))
    assert apy is not None
    assert 19.8 <= apy <= 20.2


@pytest.fixture
def partial_year_db(tmp_path):
    # Single deposit early in the year, evaluated mid-year — reproduces the
    # July 1 start_date heuristic explosion from issue #77.
    # Dates after day-10 so allocate_to_month buckets them into Jan 2020
    # (transactions on day <= 10 roll back to the prior month).
    # 2020-01-15: Deposit 10000 SEK (Account 1111)
    # 2020-01-16: Buy Asset A (100 shares @ 100 SEK = 10000 SEK)
    csv_content = """Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat
2020-01-15;1111;Insättning;Deposit;-;-;10000;0;SEK;;-
2020-01-16;1111;Köp;Asset A;100;100;-10000;0;SEK;TESTA;-
"""
    csv_file = tmp_path / "partial_year.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    db_file = tmp_path / "test_partial_year.db"
    db = DatabaseHandler(db_file)

    parser = DataParser(db)
    parser.add_data(str(csv_file))
    parser.process_transactions()

    # 5% gain: 100 shares @ 105 SEK = 10500 SEK vs 10000 invested
    cur = db.get_cursor()
    cur.execute("UPDATE assets SET latest_price = 105.0, latest_price_date = '2020-07-22'")
    cur.execute("INSERT OR REPLACE INTO asset_prices (asset_id, price_date, price, source) VALUES (1, '2020-07-22', 105.0, 'external')")
    db.commit()
    return db


def test_yearly_apy_partial_year_no_explosion(partial_year_db):
    # Evaluate on 2020-07-22 — 21 days after the old July 1 heuristic start.
    # With the bug, total_days=21 and APY = 1.05^(365/21)-1 ~= 130%.
    # With the deposit-weighted start (Jan 15), total_days=189 and
    # APY = 1.05^(365/189)-1 ~= 9.9%.
    stat_calc = StatCalculator(partial_year_db)
    stat_calc.calculate_cohort_stats(apy_mode='twrr', today=date(2020, 7, 22))
    stat_calc.calculate_year_stats(apy_mode='twrr', today=date(2020, 7, 22))

    cur = partial_year_db.get_cursor()
    cur.execute("SELECT annual_per_yield FROM account_year_stats WHERE account = '1111' AND strftime('%Y', year) = '2020'")
    row = cur.fetchone()
    assert row is not None, "No yearly stats row for 2020"
    apy = row[0]

    assert apy is not None
    # Must be a reasonable annualized figure, not the explosive ~130%.
    assert 8.0 <= apy <= 11.0


def test_deposit_weighted_year_start_helper():
    # Direct unit test for the deposit-weighted start date helper.
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE transactions (
        date DATE, account TEXT, transaction_type TEXT, asset_name TEXT,
        amount REAL, price REAL, total REAL, courtage REAL,
        currency TEXT, isin TEXT, processed INT)""")
    fallback = date(2020, 7, 1)

    # 10000 on 2020-01-01, 5000 on 2020-07-01.
    # Weighted day-of-year = (10000*1 + 5000*183)/15000 = 61.67 -> day 62.
    # 2020 is a leap year: day 62 = March 2.
    cur.executemany(
        "INSERT INTO transactions (date, account, transaction_type, total) VALUES (?,?,?,?)",
        [("2020-01-01", "1111", "Insättning", 10000.0),
         ("2020-07-01", "1111", "Insättning", 5000.0)])

    start = StatCalculator._deposit_weighted_year_start("2020", ["1111"], cur, fallback)
    assert start == date(2020, 3, 2)

    # Single deposit -> weighted start is that deposit's date.
    cur.execute("DELETE FROM transactions")
    cur.execute("INSERT INTO transactions (date, account, transaction_type, total) VALUES (?,?,?,?)",
                ("2020-04-15", "1111", "Autogiroinsättning", 3000.0))
    start = StatCalculator._deposit_weighted_year_start("2020", ["1111"], cur, fallback)
    assert start == date(2020, 4, 15)

    # No deposits -> fallback.
    cur.execute("DELETE FROM transactions")
    start = StatCalculator._deposit_weighted_year_start("2020", ["1111"], cur, fallback)
    assert start == fallback
    conn.close()


def test_deposit_weighted_cohort_start_helper():
    # Unit test for the monthly cohort deposit-weighted start date helper.
    # Verifies the allocate_to_month bucketing (cutoff day 10) and weighting.
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE transactions (
        date DATE, account TEXT, transaction_type TEXT, asset_name TEXT,
        amount REAL, price REAL, total REAL, courtage REAL,
        currency TEXT, isin TEXT, processed INT)""")
    fallback = date(2020, 6, 15)

    def insert(d, total):
        cur.execute("INSERT INTO transactions (date, account, transaction_type, total) VALUES (?,?,?,?)",
                    (d, "1111", "Insättning", total))

    # June cohort (month=2020-06-30): funded by day>10 of Jun + day<=10 of Jul.
    # Two deposits: 10000 on Jun 23 (day 175), 5000 on Jun 29 (day 181).
    # Weighted = (10000*175 + 5000*181)/15000 = 177.0 -> Jun 25.
    insert("2020-06-23", 10000.0)
    insert("2020-06-29", 5000.0)
    start = StatCalculator._deposit_weighted_cohort_start(date(2020, 6, 30), ["1111"], cur, fallback)
    assert start == date(2020, 6, 25)

    # Deposit on day <= 10 of the next month (Jul 5) still allocates to June.
    cur.execute("DELETE FROM transactions")
    insert("2020-07-05", 3000.0)
    start = StatCalculator._deposit_weighted_cohort_start(date(2020, 6, 30), ["1111"], cur, fallback)
    assert start == date(2020, 7, 5)

    # Deposit on Jul 11 (day>10 of Jul) allocates to July, NOT June -> fallback.
    cur.execute("DELETE FROM transactions")
    insert("2020-07-11", 3000.0)
    start = StatCalculator._deposit_weighted_cohort_start(date(2020, 6, 30), ["1111"], cur, fallback)
    assert start == fallback

    # Deposit on Jun 10 (day<=10 of Jun) allocates to May, NOT June -> fallback.
    cur.execute("DELETE FROM transactions")
    insert("2020-06-10", 3000.0)
    start = StatCalculator._deposit_weighted_cohort_start(date(2020, 6, 30), ["1111"], cur, fallback)
    assert start == fallback

    # December cohort crosses year boundary: range end is Jan 10 of next year.
    cur.execute("DELETE FROM transactions")
    insert("2021-01-05", 3000.0)
    start = StatCalculator._deposit_weighted_cohort_start(date(2020, 12, 31), ["1111"], cur, fallback)
    assert start == date(2021, 1, 5)
    conn.close()


@pytest.fixture
def partial_month_db(tmp_path):
    # Single deposit mid-June, evaluated ~4 weeks later — exercises the monthly
    # deposit-weighted start date. The deposit on Jun 23 (day > 10) allocates
    # to the June cohort; the truer start date (Jun 23, not the 15th) means
    # the annualized figure is HIGHER (capital at risk for fewer days).
    csv_content = """Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat
2020-06-23;1111;Insättning;Deposit;-;-;10000;0;SEK;;-
2020-06-24;1111;Köp;Asset A;100;100;-10000;0;SEK;TESTA;-
"""
    csv_file = tmp_path / "partial_month.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    db_file = tmp_path / "test_partial_month.db"
    db = DatabaseHandler(db_file)

    parser = DataParser(db)
    parser.add_data(str(csv_file))
    parser.process_transactions()

    # 5% gain: 100 shares @ 105 SEK = 10500 vs 10000 invested.
    cur = db.get_cursor()
    cur.execute("UPDATE assets SET latest_price = 105.0, latest_price_date = '2020-07-22'")
    cur.execute("INSERT OR REPLACE INTO asset_prices (asset_id, price_date, price, source) VALUES (1, '2020-07-22', 105.0, 'external')")
    db.commit()
    return db


def test_monthly_apy_uses_real_deposit_date(partial_month_db):
    # Evaluate on 2020-07-22.
    # Deposit-weighted start (Jun 23): 29 days at risk -> APY = 1.05^(365/29)-1 ~= 84.8%.
    # Old 15th-of-month heuristic (Jun 15): 37 days -> APY ~= 61.8%.
    # The higher value is the truer one: the money was only at risk for 29 days.
    stat_calc = StatCalculator(partial_month_db)
    stat_calc.calculate_cohort_stats(apy_mode='twrr', today=date(2020, 7, 22))

    cur = partial_month_db.get_cursor()
    cur.execute("SELECT annual_per_yield FROM account_cohort_stats WHERE account = '1111'")
    row = cur.fetchone()
    assert row is not None, "No monthly stats row"
    apy = row[0]

    assert apy is not None
    # Reflects the real deposit date (Jun 23), not the 15th heuristic.
    assert 83.0 <= apy <= 87.0
