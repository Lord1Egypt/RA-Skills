import pytest
import argparse
import sys
from datetime import date
from database_handler import DatabaseHandler
from data_parser import DataParser
from calculate_stats import StatCalculator
from cli import stats, portfolio

@pytest.fixture
def staleness_test_db(tmp_path):
    # Set up a test database with synthetic, mock data
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
    
    # Pre-populate asset_prices with price from 2026-01-02
    cur = db.get_cursor()
    cur.execute("INSERT OR REPLACE INTO asset_prices (asset_id, price_date, price, source) VALUES (1, '2026-01-02', 10.0, 'external')")
    db.commit()
    
    stat_calc = StatCalculator(db)
    stat_calc.calculate_stats(apy_mode='mwrr')
    
    return db_file

def test_stats_staleness_warning(staleness_test_db, capsys):
    # Valuation date '2026-03-01' is 58 days after price date '2026-01-02' (> 30 days)
    args = argparse.Namespace(
        database=str(staleness_test_db),
        account='1111',
        period='default',
        deposits='current',
        accumulated=False,
        update_prices='never',
        update_all=False,
        force=False,
        apy_mode='mwrr',
        as_of='2026-03-01',
        start_date=None,
        end_date=None,
        format='table',
        quiet=False
    )
    
    stats(args)
    captured = capsys.readouterr()
    
    # Check that warning is written to stderr
    assert "WARNING: Mock Asset A priced from 2026-01-02" in captured.err
    assert "days stale" in captured.err

def test_stats_staleness_quiet(staleness_test_db, capsys):
    # Same as above, but with quiet=True
    args = argparse.Namespace(
        database=str(staleness_test_db),
        account='1111',
        period='default',
        deposits='current',
        accumulated=False,
        update_prices='never',
        update_all=False,
        force=False,
        apy_mode='mwrr',
        as_of='2026-03-01',
        start_date=None,
        end_date=None,
        format='table',
        quiet=True
    )
    
    stats(args)
    captured = capsys.readouterr()
    
    # Check that warning is suppressed
    assert "WARNING" not in captured.err

def test_portfolio_staleness_warning(staleness_test_db, capsys):
    # Valuation date '2026-03-01' is 58 days after price date '2026-01-02' (> 30 days)
    args = argparse.Namespace(
        database=str(staleness_test_db),
        account='1111',
        as_of='2026-03-01',
        start_date=None,
        end_date=None,
        apy_mode='mwrr',
        format='table',
        quiet=False
    )
    
    portfolio(args)
    captured = capsys.readouterr()
    
    # Check that warning is written to stderr
    assert "WARNING: Mock Asset A priced from 2026-01-02" in captured.err
    assert "days stale" in captured.err

def test_portfolio_staleness_quiet(staleness_test_db, capsys):
    # Same as above, but with quiet=True
    args = argparse.Namespace(
        database=str(staleness_test_db),
        account='1111',
        as_of='2026-03-01',
        start_date=None,
        end_date=None,
        apy_mode='mwrr',
        format='table',
        quiet=True
    )
    
    portfolio(args)
    captured = capsys.readouterr()
    
    # Check that warning is suppressed
    assert "WARNING" not in captured.err

def test_no_staleness_warning_for_sold_assets(tmp_path, capsys):
    # Set up test database where asset is bought and fully sold
    csv_content = """Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat
2026-01-01;1111;Insättning;Deposit;-;-;10000;0;SEK;;-
2026-01-02;1111;Köp;Mock Asset A;100;10;-1000;0;SEK;MOCKA;-
2026-01-10;1111;Sälj;Mock Asset A;-100;12;1200;0;SEK;MOCKA;-
"""
    csv_file = tmp_path / "sold_staleness_test.csv"
    csv_file.write_text(csv_content, encoding="utf-8")
    
    db_file = tmp_path / "test_sold_staleness.db"
    db = DatabaseHandler(db_file)
    
    parser = DataParser(db)
    parser.add_data(str(csv_file))
    parser.process_transactions()
    
    # Pre-populate asset_prices with price from 2026-01-02
    cur = db.get_cursor()
    cur.execute("INSERT OR REPLACE INTO asset_prices (asset_id, price_date, price, source) VALUES (1, '2026-01-02', 10.0, 'external')")
    db.commit()
    
    stat_calc = StatCalculator(db)
    stat_calc.calculate_cohort_stats(apy_mode='mwrr')
    
    args = argparse.Namespace(
        database=str(db_file),
        account='1111',
        period='default',
        deposits='current',
        accumulated=False,
        update_prices='never',
        update_all=False,
        force=False,
        apy_mode='mwrr',
        as_of='2026-03-01',
        start_date=None,
        end_date=None,
        format='table',
        quiet=False
    )
    
    stats(args)
    captured = capsys.readouterr()
    
    # Check that warning is NOT written to stderr for sold asset
    assert "WARNING: Mock Asset A" not in captured.err

