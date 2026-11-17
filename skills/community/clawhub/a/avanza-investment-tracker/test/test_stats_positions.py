import pytest
import argparse
import json
import sys
from datetime import date
from database_handler import DatabaseHandler
from data_parser import DataParser
from calculate_stats import StatCalculator
from cli import stats, portfolio

@pytest.fixture
def stats_positions_test_db(tmp_path):
    # Set up test database with synthetic transactions
    csv_content = """Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat
2025-01-01;1111;Insättning;Deposit;-;-;10000;0;SEK;;-
2025-01-02;1111;Köp;Mock Fund A;10;100;-1000;0;SEK;MOCKA;-
2025-06-01;1111;Insättning;Deposit;-;-;5000;0;SEK;;-
2025-06-02;1111;Köp;Mock Fund B;5;200;-1000;0;SEK;MOCKB;-
"""
    csv_file = tmp_path / "stats_positions.csv"
    csv_file.write_text(csv_content, encoding="utf-8")
    
    db_file = tmp_path / "test_stats_positions.db"
    db = DatabaseHandler(db_file)
    
    parser = DataParser(db)
    parser.add_data(str(csv_file))
    parser.process_transactions()
    
    # Pre-populate asset prices for both assets at different times
    cur = db.get_cursor()
    # Prices on 2025-01-02
    cur.execute("INSERT OR REPLACE INTO asset_prices (asset_id, price_date, price, source) VALUES (1, '2025-01-02', 100.0, 'external')")
    # Prices on 2025-06-02
    cur.execute("INSERT OR REPLACE INTO asset_prices (asset_id, price_date, price, source) VALUES (2, '2025-06-02', 200.0, 'external')")
    # Prices as of 2025-12-31 (Fund A grew to 150, Fund B grew to 250)
    cur.execute("INSERT OR REPLACE INTO asset_prices (asset_id, price_date, price, source) VALUES (1, '2025-12-31', 150.0, 'external')")
    cur.execute("INSERT OR REPLACE INTO asset_prices (asset_id, price_date, price, source) VALUES (2, '2025-12-31', 250.0, 'external')")
    db.commit()
    
    stat_calc = StatCalculator(db)
    stat_calc.calculate_stats(apy_mode='mwrr')
    
    return db_file

def test_stats_positions(stats_positions_test_db, capsys):
    args = argparse.Namespace(
        database=str(stats_positions_test_db),
        account='1111',
        period='default',
        deposits='current',
        accumulated=False,
        update_prices='never',
        update_all=False,
        force=False,
        apy_mode='mwrr',
        as_of='2025-12-31',
        cohorts_start=None,
        cohorts_end=None,
        from_date=None,
        to=None,
        positions=True,
        summary=False,
        format='table',
        quiet=True
    )
    
    stats(args)
    captured = capsys.readouterr()
    
    # Verify both cohorts (Dec 2024 and May 2025) are printed with their holdings
    assert "Dec 2024" in captured.out
    assert "Mock Fund A" in captured.out
    assert "May 2025" in captured.out
    assert "Mock Fund B" in captured.out

def test_stats_summary_only(stats_positions_test_db, capsys):
    args = argparse.Namespace(
        database=str(stats_positions_test_db),
        account='1111',
        period='default',
        deposits='current',
        accumulated=False,
        update_prices='never',
        update_all=False,
        force=False,
        apy_mode='mwrr',
        as_of='2025-12-31',
        cohorts_start=None,
        cohorts_end=None,
        from_date=None,
        to=None,
        positions=False,
        summary=True,
        format='table',
        quiet=True
    )
    
    stats(args)
    captured = capsys.readouterr()
    
    # Cohort breakdown should be suppressed in summary mode
    assert "Dec 2024" not in captured.out
    assert "Summary — all cohorts" in captured.out
    assert "Total Deposited:" in captured.out
    assert "Current Value:" in captured.out

def test_stats_summary_positions_json(stats_positions_test_db, capsys):
    args = argparse.Namespace(
        database=str(stats_positions_test_db),
        account='1111',
        period='default',
        deposits='current',
        accumulated=False,
        update_prices='never',
        update_all=False,
        force=False,
        apy_mode='mwrr',
        as_of='2025-12-31',
        cohorts_start=None,
        cohorts_end=None,
        from_date=None,
        to=None,
        positions=True,
        summary=True,
        format='json',
        quiet=True
    )
    
    stats(args)
    captured = capsys.readouterr()
    
    data = json.loads(captured.out)
    assert 'deposits' in data
    assert 'current_value' in data
    assert 'holdings' in data
    assert len(data['holdings']) == 2
    assert data['holdings'][0]['asset'] == "Mock Fund A"
    assert data['holdings'][1]['asset'] == "Mock Fund B"

def test_portfolio_alias(stats_positions_test_db, capsys):
    args = argparse.Namespace(
        database=str(stats_positions_test_db),
        account='1111',
        as_of='2025-12-31',
        cohorts_start=None,
        cohorts_end=None,
        from_date=None,
        to=None,
        apy_mode='mwrr',
        format='json',
        quiet=True
    )
    
    portfolio(args)
    captured = capsys.readouterr()
    
    data = json.loads(captured.out)
    assert 'holdings' in data
    assert len(data['holdings']) == 2

def test_cohorts_filtering(stats_positions_test_db, capsys):
    # Only show cohorts starting from 2025-05-01
    args = argparse.Namespace(
        database=str(stats_positions_test_db),
        account='1111',
        period='default',
        deposits='current',
        accumulated=False,
        update_prices='never',
        update_all=False,
        force=False,
        apy_mode='mwrr',
        as_of='2025-12-31',
        cohorts_start='2025-05-01',
        cohorts_end=None,
        from_date=None,
        to=None,
        positions=False,
        summary=False,
        format='table',
        quiet=True
    )
    
    stats(args)
    captured = capsys.readouterr()
    
    assert "Dec 2024" not in captured.out
    assert "May 2025" in captured.out

def test_period_valuation(stats_positions_test_db, capsys):
    # Calculate performance specifically between 2025-06-01 and 2025-12-31
    args = argparse.Namespace(
        database=str(stats_positions_test_db),
        account='1111',
        period='default',
        deposits='current',
        accumulated=False,
        update_prices='never',
        update_all=False,
        force=False,
        apy_mode='mwrr',
        as_of=None,
        cohorts_start=None,
        cohorts_end=None,
        from_date='2025-06-01',
        to='2025-12-31',
        positions=False,
        summary=False,
        format='json',
        quiet=True
    )
    
    stats(args)
    captured = capsys.readouterr()
    
    data = json.loads(captured.out)
    # Check that performance is filtered
    assert len(data) > 0

def test_multi_account_stats_preserves_multiple_cohorts(stats_positions_test_db):
    # Setup StatCalculator and query multi-account stats
    from calculate_stats import StatCalculator
    from database_handler import DatabaseHandler
    
    db = DatabaseHandler(str(stats_positions_test_db))
    stat_calc = StatCalculator(db)
    
    # We query for both accounts ('1111' and '2222')
    res = stat_calc.get_stats(accounts=['1111', '2222'], period='month', deposits='all')
    
    # We should have cohorts from both accounts, meaning at least 2 cohort months
    assert len(res) >= 2

def test_dynamic_label_valuation(stats_positions_test_db, capsys):
    # Setup stats namespace with from_date='2025-06-01' and to='2025-12-31' in table format
    args = argparse.Namespace(
        database=str(stats_positions_test_db),
        account='1111',
        period='default',
        deposits='current',
        accumulated=False,
        update_prices='never',
        update_all=False,
        force=False,
        apy_mode='mwrr',
        as_of=None,
        cohorts_start=None,
        cohorts_end=None,
        from_date='2025-06-01',
        to='2025-12-31',
        positions=False,
        summary=False,
        format='table',
        quiet=True,
        no_interpolation=True
    )
    stats(args)
    captured = capsys.readouterr()
    
    # Dec 2024 is the first cohort month in the test database.
    # It existed before the June 2025 window, so it should display "Start Value: 10000".
    assert "Dec 2024" in captured.out
    assert "Start Value: 10000" in captured.out
    
    # May 2025 is the second cohort month, which also has its deposit on 2025-06-01 included in the start snapshot, so it shows "Start Value: 5000".
    assert "May 2025" in captured.out
    assert "Start Value: 5000" in captured.out


def test_cohort_shorthand_filtering(stats_positions_test_db, capsys):
    # Test --cohort YYYY-MM
    args1 = argparse.Namespace(
        database=str(stats_positions_test_db),
        account='1111',
        period='default',
        deposits='current',
        accumulated=False,
        update_prices='never',
        update_all=False,
        force=False,
        apy_mode='mwrr',
        as_of=None,
        cohort='2024-12',  # filters to Dec 2024 cohort
        cohorts_start=None,
        cohorts_end=None,
        from_date=None,
        to=None,
        positions=False,
        summary=False,
        format='table',
        quiet=True
    )
    stats(args1)
    captured1 = capsys.readouterr()
    assert "Dec 2024" in captured1.out
    assert "May 2025" not in captured1.out

    # Test --cohort YYYY
    args2 = argparse.Namespace(
        database=str(stats_positions_test_db),
        account='1111',
        period='default',
        deposits='current',
        accumulated=False,
        update_prices='never',
        update_all=False,
        force=False,
        apy_mode='mwrr',
        as_of=None,
        cohort='2025',  # filters to 2025 cohorts (May 2025)
        cohorts_start=None,
        cohorts_end=None,
        from_date=None,
        to=None,
        positions=False,
        summary=False,
        format='table',
        quiet=True
    )
    stats(args2)
    captured2 = capsys.readouterr()
    # Dec 2024 is NOT in 2025 and should be grouped under 2024
    assert "2024" not in captured2.out
    # May 2025 is in 2025 and should be grouped under 2025
    assert "2025" in captured2.out

    # Test mutual exclusivity with cohorts_start
    args3 = argparse.Namespace(
        database=str(stats_positions_test_db),
        account='1111',
        period='default',
        deposits='current',
        accumulated=False,
        update_prices='never',
        update_all=False,
        force=False,
        apy_mode='mwrr',
        as_of=None,
        cohort='2025',
        cohorts_start='2025-01-01',
        cohorts_end=None,
        from_date=None,
        to=None,
        positions=False,
        summary=False,
        format='table',
        quiet=True
    )
    assert stats(args3) == 1  # Should return error code 1


def test_multi_account_stats_apy_with_end_date(tmp_path):
    from datetime import date
    from database_handler import DatabaseHandler
    from data_parser import DataParser
    from calculate_stats import StatCalculator

    csv_content = """Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat
2025-01-01;1111;Insättning;Deposit;-;-;10000;0;SEK;;-
2025-01-02;1111;Köp;Mock Fund A;10;100;-1000;0;SEK;MOCKA;-
2025-01-01;2222;Insättning;Deposit;-;-;5000;0;SEK;;-
2025-01-02;2222;Köp;Mock Fund A;5;100;-500;0;SEK;MOCKA;-
"""
    csv_file = tmp_path / "test_multi_apy.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    db_file = tmp_path / "test_multi_apy.db"
    db = DatabaseHandler(db_file)

    parser = DataParser(db)
    parser.add_data(str(csv_file))
    parser.process_transactions()

    cur = db.get_cursor()
    cur.execute("INSERT OR REPLACE INTO asset_prices (asset_id, price_date, price, source) VALUES (1, '2025-01-02', 100.0, 'external')")
    cur.execute("INSERT OR REPLACE INTO asset_prices (asset_id, price_date, price, source) VALUES (1, '2025-06-30', 150.0, 'external')")
    cur.execute("UPDATE assets SET latest_price = 150.0, latest_price_date = '2025-06-30' WHERE asset_id = 1")
    db.commit()

    # Pre-populate stats
    stat_calc = StatCalculator(db)
    # We run stats calculation as of 2025-06-30
    stat_calc.calculate_cohort_stats(apy_mode='mwrr', today=date(2025, 6, 30))
    stat_calc.calculate_year_stats(apy_mode='mwrr', today=date(2025, 6, 30))

    # Test get_stats with end_date=2025-06-30
    res_with_end = stat_calc.get_stats(
        accounts=['1111', '2222'],
        period='year',
        deposits='all',
        end_date=date(2025, 6, 30)
    )

    # Test get_stats with end_date=None (defaults to system today)
    res_without_end = stat_calc.get_stats(
        accounts=['1111', '2222'],
        period='year',
        deposits='all',
        end_date=None
    )

    assert len(res_with_end) > 0
    assert len(res_without_end) > 0

    apy_with = res_with_end[0][10]
    apy_without = res_without_end[0][10]

    # APY with past end_date (2025-06-30) should use 2025-06-30 as today, which is ~180 days from cohort start.
    # APY without end_date will use system today, which is in 2026 (~540+ days).
    # Since the position grew (from 100 to 150), HPR is positive, so the shorter holding period (2025-06-30)
    # should yield a higher APY.
    assert apy_with > apy_without
    assert apy_with != 0.0
    assert apy_without != 0.0



