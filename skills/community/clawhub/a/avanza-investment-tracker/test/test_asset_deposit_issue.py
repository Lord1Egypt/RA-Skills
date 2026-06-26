import pytest
import sqlite3
import csv
from database_handler import DatabaseHandler
from data_parser import DataParser, SpecialCases

@pytest.fixture
def asset_deposit_db(tmp_path):
    db_base = str(tmp_path / "test_asset_deposit")
    db_file = db_base + ".db"
    
    # Create DB schema
    db = DatabaseHandler(db_base)
    db.connect()
    db.create_tables()
    db.disconnect()
    
    # Needs special cases to apply custom purchase price for Asset 2
    special_cases_file = tmp_path / "special_cases.json"
    special_cases_file.write_text("""
    [
        {
            "condition": [
                {
                    "index": 1,
                    "value": "2222222"
                },
                {
                    "index": 3,
                    "value": "Asset 2"
                }
            ],
            "replacement": [
                {
                    "index": 5,
                    "value": "10.0"
                }
            ]
        }
    ]
    """)
    special_cases = SpecialCases(str(special_cases_file))
    
    # Create transactions with Tillgångsinsättning
    csv_file = tmp_path / "asset_deposits.csv"
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Datum","Konto","Typ av transaktion","Värdepapper/beskrivning","Antal","Kurs","Belopp","Transaktionsvaluta","Courtage","Valutakurs","Instrumentvaluta","ISIN","Resultat"])
        
        # Scenario 1 (Asset 1): Price=0, fallback to sale total (amount 100, price 0)
        writer.writerow(["2019-02-12","1111111","Tillgångsinsättning","Asset 1","100","0","0","SEK","-","-","SEK","SE000000001","-"])
        # Scenario 2 (Asset 2): Price=0, but we will have a special case giving it a price (amount 50, price 0, special case: 10)
        writer.writerow(["2019-02-12","2222222","Tillgångsinsättning","Asset 2","50","0","0","SEK","-","-","SEK","SE000000002","-"])
        # Scenario 3 (Asset 3): Price>0, standard processing (amount 20, price 50)
        writer.writerow(["2019-02-12","3333333","Tillgångsinsättning","Asset 3","20","50","0","SEK","-","-","SEK","SE000000003","-"])
        
        # Later sales
        writer.writerow(["2019-04-08","1111111","Sälj","Asset 1","-100","12.5","1250","SEK","-","-","SEK","SE000000001","1250"])
        writer.writerow(["2019-04-08","2222222","Sälj","Asset 2","-50","12","600","SEK","-","-","SEK","SE000000002","600"])
        writer.writerow(["2019-04-08","3333333","Sälj","Asset 3","-20","60","1200","SEK","-","-","SEK","SE000000003","1200"])
        
    db_handler = DatabaseHandler(db_file)
    parser = DataParser(db_handler, special_cases)
    parser.add_data(str(csv_file))
    db_handler.connect()
    parser.process_transactions()
    db_handler.disconnect()
    
    return db_file

def test_tillgangsinsattning_processing(asset_deposit_db):
    """
    Tests that Tillgångsinsättning cost basis is handled correctly:
    1. Special case price applies when provided
    2. Fallback retroactive deposit applies when price=0 and no special case
    3. Standard CSV price applies when price>0 and no special case
    """
    with sqlite3.connect(asset_deposit_db) as conn:
        cursor = conn.cursor()
        
        # 1. Fallback scenario (Asset 1)
        # Should retroactively deposit 1250 in 2019-02-28 (when the asset was deposited)
        cursor.execute("SELECT active_base FROM cohort_data WHERE account='1111111' AND month='2019-02-28'")
        res1 = cursor.fetchone()
        
        # 2. Special case scenario (Asset 2)
        cursor.execute("SELECT active_base FROM cohort_data WHERE account='2222222' AND month='2019-02-28'")
        res2 = cursor.fetchone()
        
        # 3. Standard scenario (Asset 3)
        cursor.execute("SELECT active_base FROM cohort_data WHERE account='3333333' AND month='2019-02-28'")
        res3 = cursor.fetchone()

        # Check Asset 1 (Fallback) -> Base should be 1250
        assert res1, "Month stat for 1111111 should exist"
        assert res1[0] == 1250.0, "Retroactive deposit fallback should result in 1250 deposit"

        # Check Asset 2 (Special Case) -> Base should be 50 * 10 = 500
        assert res2, "Month stat for 2222222 should exist"
        assert res2[0] == 500.0, "Special case custom price (10) should result in 500 deposit"
        
        # Check Asset 3 (Standard) -> Base should be 20 * 50 = 1000
        assert res3, "Month stat for 3333333 should exist"
        assert res3[0] == 1000.0, "Standard CSV price (50) should result in 1000 deposit"
