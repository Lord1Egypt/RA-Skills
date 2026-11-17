import pytest
import argparse
from datetime import date
from database_handler import DatabaseHandler
from data_parser import DataParser
from calculate_stats import StatCalculator
from cli import stats

@pytest.fixture
def test_db(tmp_path):
    db_file = tmp_path / "test_interpolation.db"
    db = DatabaseHandler(str(db_file))
    db.connect()
    db.create_tables()
    
    # Insert a mock asset
    cur = db.get_cursor()
    cur.execute("INSERT OR REPLACE INTO assets (asset_id, asset, amount, latest_price, latest_price_date) VALUES (1, 'Mock Asset A', 10, 100.0, '2026-01-11')")
    
    # Insert price points: Jan 1st -> 100, Jan 11th -> 110
    cur.execute("INSERT OR REPLACE INTO asset_prices (asset_id, price_date, price, source) VALUES (1, '2026-01-01', 100.0, 'external')")
    cur.execute("INSERT OR REPLACE INTO asset_prices (asset_id, price_date, price, source) VALUES (1, '2026-01-11', 110.0, 'external')")
    db.commit()
    return db

def test_exact_match(test_db):
    price, is_interp, gap, price_date = test_db.get_price(1, "2026-01-01")
    assert price == 100.0
    assert not is_interp
    assert gap == 0
    assert price_date == date(2026, 1, 1)

def test_linear_interpolation(test_db):
    # Jan 6th is midpoint between Jan 1st and Jan 11th
    price, is_interp, gap, price_date = test_db.get_price(1, "2026-01-06")
    assert price == 105.0
    assert is_interp
    assert gap == 10
    assert price_date == date(2026, 1, 6)

def test_disabled_interpolation(test_db):
    # Interpolation disabled -> should fall back to Jan 1st price of 100.0 and return its date
    price, is_interp, gap, price_date = test_db.get_price(1, "2026-01-06", interpolate=False)
    assert price == 100.0
    assert not is_interp
    assert gap is None
    assert price_date == date(2026, 1, 1)

def test_extrapolation_before_first(test_db):
    # Clear latest_price to test fallback to first known price in asset_prices
    cur = test_db.get_cursor()
    cur.execute("UPDATE assets SET latest_price = NULL WHERE asset_id = 1")
    test_db.commit()

    # Before Jan 1st -> flat extrapolation to first price (100.0)
    price, is_interp, gap, price_date = test_db.get_price(1, "2025-12-25")
    assert price == 100.0
    assert not is_interp
    assert price_date == date(2026, 1, 1)

def test_extrapolation_after_last(test_db):
    # After Jan 11th -> latest_price from assets is 100.0
    price, is_interp, gap, price_date = test_db.get_price(1, "2026-01-15")
    assert price == 100.0
    assert not is_interp
    assert price_date == date(2026, 1, 11)

    # If assets table doesn't have latest_price, should fall back to last known in asset_prices (110.0)
    cur = test_db.get_cursor()
    cur.execute("UPDATE assets SET latest_price = NULL WHERE asset_id = 1")
    test_db.commit()
    
    price, is_interp, gap, price_date = test_db.get_price(1, "2026-01-15")
    assert price == 110.0
    assert not is_interp
    assert price_date == date(2026, 1, 11)

def test_fallback_zero_price_points(test_db):
    cur = test_db.get_cursor()
    cur.execute("DELETE FROM asset_prices WHERE asset_id = 1")
    cur.execute("UPDATE assets SET latest_price = NULL, average_price = 140.0 WHERE asset_id = 1")
    test_db.commit()

    # No price points -> fallback to average_price
    price, is_interp, gap, price_date = test_db.get_price(1, "2026-01-06")
    assert price == 140.0
    assert not is_interp

@pytest.fixture
def cli_test_db(tmp_path):
    csv_content = """Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat
2026-01-01;1111;Insättning;Deposit;-;-;10000;0;SEK;;-
2026-01-02;1111;Köp;Mock Asset A;100;10;-1000;0;SEK;MOCKA;-
"""
    csv_file = tmp_path / "staleness_test.csv"
    csv_file.write_text(csv_content, encoding="utf-8")
    
    db_file = tmp_path / "test_staleness.db"
    db = DatabaseHandler(db_file)
    
    parser = DataParser(db)
    parser.add_data(str(csv_file))
    parser.process_transactions()
    
    # Sparse prices: Jan 2nd -> 10.0, Jan 12th -> 20.0
    cur = db.get_cursor()
    cur.execute("INSERT OR REPLACE INTO asset_prices (asset_id, price_date, price, source) VALUES (1, '2026-01-02', 10.0, 'external')")
    cur.execute("INSERT OR REPLACE INTO asset_prices (asset_id, price_date, price, source) VALUES (1, '2026-01-12', 20.0, 'external')")
    db.commit()
    
    stat_calc = StatCalculator(db)
    stat_calc.calculate_stats(apy_mode='mwrr')
    
    return db_file

def test_cli_default_interpolation_no_warning(cli_test_db, capsys):
    # Valuation date '2026-01-07' which falls between 2026-01-02 and 2026-01-12.
    # By default, it will interpolate. No warnings should print.
    args = argparse.Namespace(
        database=str(cli_test_db),
        account='1111',
        period='default',
        deposits='current',
        accumulated=False,
        update_prices='never',
        update_all=False,
        force=False,
        apy_mode='mwrr',
        as_of='2026-01-07',
        start_date=None,
        end_date=None,
        format='table',
        quiet=False,
        no_interpolation=False
    )
    
    stats(args)
    captured = capsys.readouterr()
    assert "WARNING" not in captured.err

def test_cli_no_interpolation_with_warning(cli_test_db, capsys):
    # Valuation date '2026-02-15'.
    # Target date is 2026-02-15.
    # With no_interpolation, it falls back to last known price on Jan 12th.
    # The gap between 2026-02-15 and 2026-01-12 is 34 days (> 30 days threshold).
    # Since no_interpolation=True, a warning should print.
    args = argparse.Namespace(
        database=str(cli_test_db),
        account='1111',
        period='default',
        deposits='current',
        accumulated=False,
        update_prices='never',
        update_all=False,
        force=False,
        apy_mode='mwrr',
        as_of='2026-02-15',
        start_date=None,
        end_date=None,
        format='table',
        quiet=False,
        no_interpolation=True
    )
    
    stats(args)
    captured = capsys.readouterr()
    assert "WARNING: Mock Asset A priced from 2026-01-12, 34 days stale" in captured.err
