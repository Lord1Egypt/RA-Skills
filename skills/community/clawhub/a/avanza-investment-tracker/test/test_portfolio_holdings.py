import pytest
from datetime import date
import argparse
import json
from database_handler import DatabaseHandler
from data_parser import DataParser
from calculate_stats import StatCalculator
from cli import portfolio

@pytest.fixture
def holdings_test_db(tmp_path):
    # Set up database with:
    # Account 1111:
    # 2026-01-01: Deposit 20000 SEK
    # 2026-01-02: Buy Asset A (100 shares @ 100 SEK = 10000 SEK)
    # 2026-01-03: Buy Asset B (50 shares @ 100 SEK = 5000 SEK)
    # Account 2222:
    # 2026-01-01: Deposit 10000 SEK
    # 2026-01-02: Buy Asset C (100 shares @ 100 SEK = 10000 SEK)
    
    csv_content = """Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat
2026-01-01;1111;Insättning;Deposit;-;-;20000;0;SEK;;-
2026-01-02;1111;Köp;Asset A;100;100;-10000;0;SEK;TESTA;-
2026-01-03;1111;Köp;Asset B;50;100;-5000;0;SEK;TESTB;-
2026-01-01;2222;Insättning;Deposit;-;-;10000;0;SEK;;-
2026-01-02;2222;Köp;Asset C;100;100;-10000;0;SEK;TESTC;-
"""
    csv_file = tmp_path / "holdings_test.csv"
    csv_file.write_text(csv_content, encoding="utf-8")
    
    db_file = tmp_path / "test_portfolio_holdings.db"
    db = DatabaseHandler(db_file)
    
    parser = DataParser(db)
    parser.add_data(str(csv_file))
    parser.process_transactions()
    
    # Calculate stats so cohort_assets is populated
    stat_calc = StatCalculator(db)
    stat_calc.calculate_stats(apy_mode='mwrr')
    
    return db_file

def test_portfolio_holdings_text(holdings_test_db, capsys):
    # Set prices
    db = DatabaseHandler(holdings_test_db)
    cur = db.get_cursor()
    cur.execute("UPDATE assets SET latest_price = 120.0, latest_price_date = '2026-01-15' WHERE asset = 'Asset A'")
    cur.execute("UPDATE assets SET latest_price = 80.0, latest_price_date = '2026-01-15' WHERE asset = 'Asset B'")
    cur.execute("UPDATE assets SET latest_price = 150.0, latest_price_date = '2026-01-15' WHERE asset = 'Asset C'")
    
    cur.execute("INSERT OR REPLACE INTO asset_prices (asset_id, price_date, price, source) VALUES (1, '2026-01-15', 120.0, 'external')")
    cur.execute("INSERT OR REPLACE INTO asset_prices (asset_id, price_date, price, source) VALUES (2, '2026-01-15', 80.0, 'external')")
    cur.execute("INSERT OR REPLACE INTO asset_prices (asset_id, price_date, price, source) VALUES (3, '2026-01-15', 150.0, 'external')")
    db.commit()
    
    # Run stats calculation to refresh values
    stat_calc = StatCalculator(db)
    stat_calc.calculate_stats(apy_mode='mwrr')
    
    # Test portfolio overview for account 1111 in text mode
    # Asset A market value: 100 * 120 = 12000 SEK
    # Asset B market value: 50 * 80 = 4000 SEK
    # Total asset value: 16000 SEK
    # Allocations: Asset A = 75.0%, Asset B = 25.0%
    # Cash: 20000 - 10000 - 5000 = 5000 SEK
    
    args = argparse.Namespace(
        database=str(holdings_test_db),
        account='1111',
        format='text',
        apy_mode='mwrr',
        as_of=None
    )
    
    portfolio(args)
    captured = capsys.readouterr()
    
    output = captured.out
    assert "Account 1111" in output
    assert "Holdings:" in output
    assert "Asset A" in output
    assert "12,000 SEK" in output
    assert "75.0%" in output
    assert "Asset B" in output
    assert "4,000 SEK" in output
    assert "25.0%" in output
    assert "Total" in output
    assert "16,000 SEK" in output
    assert "100.0%" in output
    
    # Ensure Asset C (account 2222) is NOT in the output for account 1111
    assert "Asset C" not in output

def test_portfolio_holdings_json(holdings_test_db, capsys):
    # Set prices (same as above)
    db = DatabaseHandler(holdings_test_db)
    cur = db.get_cursor()
    cur.execute("UPDATE assets SET latest_price = 120.0, latest_price_date = '2026-01-15' WHERE asset = 'Asset A'")
    cur.execute("UPDATE assets SET latest_price = 80.0, latest_price_date = '2026-01-15' WHERE asset = 'Asset B'")
    db.commit()
    
    stat_calc = StatCalculator(db)
    stat_calc.calculate_stats(apy_mode='mwrr')
    
    args = argparse.Namespace(
        database=str(holdings_test_db),
        account='1111',
        format='json',
        apy_mode='mwrr',
        as_of=None
    )
    
    portfolio(args)
    captured = capsys.readouterr()
    
    data = json.loads(captured.out)
    assert data['account'] == '1111'
    assert 'holdings' in data
    
    holdings = data['holdings']
    assert len(holdings) == 2
    
    # First holding (highest market value: Asset A)
    assert holdings[0]['asset'] == 'Asset A'
    assert holdings[0]['amount'] == 100.0
    assert holdings[0]['price'] == 120.0
    assert holdings[0]['market_value'] == 12000.0
    assert holdings[0]['allocation_percent'] == 75.0
    
    # Second holding
    assert holdings[1]['asset'] == 'Asset B'
    assert holdings[1]['amount'] == 50.0
    assert holdings[1]['price'] == 80.0
    assert holdings[1]['market_value'] == 4000.0
    assert holdings[1]['allocation_percent'] == 25.0


def test_portfolio_nickname_resolution(holdings_test_db, capsys):
    db = DatabaseHandler(holdings_test_db)
    cur = db.get_cursor()
    
    # Add nickname "Fixed Income" for account 1111
    cur.execute("INSERT OR REPLACE INTO accounts (account_id, nickname) VALUES ('1111', 'Fixed Income')")
    
    # Set prices so there's non-zero values
    cur.execute("UPDATE assets SET latest_price = 120.0, latest_price_date = '2026-01-15' WHERE asset = 'Asset A'")
    cur.execute("UPDATE assets SET latest_price = 80.0, latest_price_date = '2026-01-15' WHERE asset = 'Asset B'")
    db.commit()
    
    stat_calc = StatCalculator(db)
    stat_calc.calculate_stats(apy_mode='mwrr')
    
    # Test that querying by nickname "fixed income" (case-insensitive) resolves to account 1111
    args = argparse.Namespace(
        database=str(holdings_test_db),
        account='fixed income',
        format='text',
        apy_mode='mwrr',
        as_of=None
    )
    
    portfolio(args)
    captured = capsys.readouterr()
    
    output = captured.out
    assert "Account 1111" in output
    assert "Fixed Income" in output
    assert "Asset A" in output
    assert "12,000 SEK" in output

