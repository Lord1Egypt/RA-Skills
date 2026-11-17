import pytest
from datetime import date
import argparse
import os
from database_handler import DatabaseHandler
from data_parser import DataParser
from cli import export_transactions

@pytest.fixture
def export_test_db(tmp_path):
    # Setup test database using Avanza CSV import
    csv_content = """Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat
2026-01-01;1111;Insättning;Deposit;-;-;20000;0;SEK;;-
2026-01-01;2222;Insättning;Deposit;-;-;10000;0;SEK;;-
2026-01-02;1111;Köp;Asset A;10,5;100;-1050;9,9;SEK;TESTA;-
2026-01-03;2222;Köp;Asset B;50;100;-5000;-;SEK;TESTB;-
"""
    csv_file = tmp_path / "export_import_test.csv"
    csv_file.write_text(csv_content, encoding="utf-8")
    
    db_file = tmp_path / "test_export.db"
    db = DatabaseHandler(db_file)
    
    parser = DataParser(db)
    parser.add_data(str(csv_file))
    parser.process_transactions()
    
    return db_file

def test_export_transactions_csv(export_test_db, tmp_path):
    export_file = tmp_path / "exported.csv"
    
    args = argparse.Namespace(
        database=str(export_test_db),
        account='all',
        output=str(export_file)
    )
    
    # Run export
    status = export_transactions(args)
    assert status == 0
    assert export_file.exists()
    
    # Read export content
    lines = export_file.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 5 # header + 4 transactions
    
    assert lines[0] == "Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat"
    
    # Verify first row: Insättning (zero numbers should be formatted as "-")
    parts = lines[1].split(';')
    assert parts[0] == "2026-01-01"
    assert parts[1] == "1111"
    assert parts[2] == "Insättning"
    assert parts[3] == "Deposit"
    assert parts[4] == "-" # amount 0.0 -> "-"
    assert parts[5] == "-" # price 0.0 -> "-"
    assert parts[6] == "20000" # total 20000.0 -> "20000"
    assert parts[7] == "-" # courtage 0.0 -> "-"
    assert parts[8] == "SEK"
    assert parts[9] == ""
    assert parts[10] == "-"
    
    # Verify third row: Köp with float values (decimals should use comma)
    parts = lines[3].split(';')
    assert parts[0] == "2026-01-02"
    assert parts[1] == "1111"
    assert parts[2] == "Köp"
    assert parts[3] == "Asset A"
    assert parts[4] == "10,5" # 10.5 -> "10,5"
    assert parts[5] == "100" # 100.0 -> "100"
    assert parts[6] == "-1050" # -1050.0 -> "-1050"
    assert parts[7] == "9,9" # 9.9 -> "9,9"
    assert parts[8] == "SEK"
    assert parts[9] == "TESTA"
    assert parts[10] == "-"

def test_export_account_filtering(export_test_db, tmp_path):
    export_file = tmp_path / "exported_filtered.csv"
    
    # Add nickname "First" for account 1111
    db = DatabaseHandler(export_test_db)
    cur = db.get_cursor()
    cur.execute("INSERT OR REPLACE INTO accounts (account_id, nickname) VALUES ('1111', 'First')")
    db.commit()
    
    args = argparse.Namespace(
        database=str(export_test_db),
        account='First', # Using display name filtering
        output=str(export_file)
    )
    
    # Run export
    status = export_transactions(args)
    assert status == 0
    assert export_file.exists()
    
    lines = export_file.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 3 # header + 2 transactions (account 2222 is filtered out)
    assert "2222" not in export_file.read_text(encoding="utf-8")

def test_export_round_trip(export_test_db, tmp_path):
    export_file = tmp_path / "exported_roundtrip.csv"
    
    # 1. Export original DB
    args_export = argparse.Namespace(
        database=str(export_test_db),
        account='all',
        output=str(export_file)
    )
    assert export_transactions(args_export) == 0
    
    # 2. Import into a new empty database
    new_db_file = tmp_path / "new_import.db"
    new_db = DatabaseHandler(new_db_file)
    
    parser = DataParser(new_db)
    parser.add_data(str(export_file))
    
    # Verify count and data in new database
    cur_orig = DatabaseHandler(export_test_db).get_cursor()
    orig_txs = cur_orig.execute("SELECT date, account, transaction_type, asset_name, amount, price, total, courtage, currency, isin FROM transactions ORDER BY date ASC, rowid ASC").fetchall()
    
    cur_new = new_db.get_cursor()
    new_txs = cur_new.execute("SELECT date, account, transaction_type, asset_name, amount, price, total, courtage, currency, isin FROM transactions ORDER BY date ASC, rowid ASC").fetchall()
    
    assert len(new_txs) == len(orig_txs)
    for orig, new in zip(orig_txs, new_txs):
        assert orig == new
