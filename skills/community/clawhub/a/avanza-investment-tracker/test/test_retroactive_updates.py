import sys
sys.path.insert(0, "..")
import pytest
import json
from datetime import date
from database_handler import DatabaseHandler
from data_parser import DataParser, SpecialCases

@pytest.fixture
def base_db(tmp_path):
    # Set up a database with:
    # 2020-01-01: Deposit 10000 SEK (Account 1111)
    # 2020-01-02: Buy Asset A (100 shares @ 100 SEK)
    csv_content = """Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat
2020-01-01;1111;Insättning;Deposit;-;-;10000;0;SEK;;-
2020-01-02;1111;Köp;Asset A;100;100;-10000;0;SEK;TESTA;-
"""
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(csv_content, encoding="utf-8")
    
    db_file = tmp_path / "test_retroactive.db"
    db = DatabaseHandler(db_file)
    
    parser = DataParser(db)
    parser.add_data(str(csv_file))
    parser.process_transactions()
    
    return db

def test_special_cases_retroactive_application(tmp_path, base_db):
    # Set up a special case JSON file that overrides price of Asset A buy to 120.0
    special_cases_content = [
        {
            "condition": [
                {
                    "index": 3,
                    "value": "Asset A"
                },
                {
                    "index": 2,
                    "value": "Köp"
                }
            ],
            "replacement": [
                {
                    "index": 5,
                    "value": "120.0"
                }
            ]
        }
    ]
    sc_file = tmp_path / "special_cases.json"
    sc_file.write_text(json.dumps(special_cases_content), encoding="utf-8")
    
    # Instantiate DataParser with special cases
    special_cases = SpecialCases(str(sc_file))
    parser = DataParser(base_db, special_cases)
    
    # Run reset (which sets processed = 0)
    parser.reset_processed_transactions()
    
    # Verify that the transaction in database initially has price = 100
    cur = base_db.get_cursor()
    price_before = cur.execute("SELECT price FROM transactions WHERE transaction_type = 'Köp'").fetchone()[0]
    assert price_before == 100.0
    
    # Process transactions - this should trigger re-application of special cases and update price to 120.0
    parser.process_transactions()
    
    # Verify that the database transaction price was updated to 120.0
    price_after = cur.execute("SELECT price FROM transactions WHERE transaction_type = 'Köp'").fetchone()[0]
    assert price_after == 120.0

def test_historical_price_fallback(tmp_path):
    # Set up a database with:
    # 2020-01-01: Tillgångsinsättning (Asset deposit) with price = 0
    csv_content = """Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat
2020-01-01;1111;Tillgångsinsättning;Asset B;10;0;0;0;SEK;TESTB;-
"""
    csv_file = tmp_path / "test_fallback.csv"
    csv_file.write_text(csv_content, encoding="utf-8")
    
    db_file = tmp_path / "test_fallback.db"
    db = DatabaseHandler(db_file)
    
    # Pre-populate asset_prices table with a price for Asset B
    # Let's first register Asset B in assets table
    cur = db.get_cursor()
    cur.execute("INSERT INTO assets (asset) VALUES ('Asset B')")
    asset_id = cur.execute("SELECT asset_id FROM assets WHERE asset = 'Asset B'").fetchone()[0]
    # Insert a price as of 2020-01-02 (closest price to 2020-01-01)
    cur.execute("INSERT INTO asset_prices (asset_id, price_date, price, source) VALUES (?, '2020-01-02', 150.0, 'external')", (asset_id,))
    db.commit()
    
    # Now import and process the transaction
    parser = DataParser(db)
    parser.add_data(str(csv_file))
    
    # Verify that before processing, transaction price is 0
    price_before = cur.execute("SELECT price FROM transactions WHERE transaction_type = 'Tillgångsinsättning'").fetchone()[0]
    assert price_before == 0.0
    
    # Process the transaction - it should look up the price in asset_prices and update to 150.0
    parser.process_transactions()
    
    # Verify transaction price is updated to 150.0
    price_after = cur.execute("SELECT price FROM transactions WHERE transaction_type = 'Tillgångsinsättning'").fetchone()[0]
    assert price_after == 150.0
    
    # Verify cohort data active base is updated correctly (10 shares * 150 SEK = 1500 SEK)
    active_base = cur.execute("SELECT active_base FROM cohort_data WHERE account = '1111'").fetchone()[0]
    assert active_base == 1500.0
