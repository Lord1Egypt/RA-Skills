import pytest

from database_handler import DatabaseHandler
from data_parser import SpecialCases, DataParser

@pytest.fixture(scope='function')
def db(tmp_path):
    # Create a temporary SQLite database in the tmp_path directory
    db_file = tmp_path / "test_asset_data.db"
    return DatabaseHandler(str(db_file))

@pytest.fixture(scope='function')
def special_cases():
    return SpecialCases("./test/data/special_cases_test.json")

def test_data_adder_init(db,special_cases):
    # Create DataAdder object
    data_adder = DataParser(db,special_cases)
    assert data_adder is not None
    # Create DataAdder object without special cases
    data_adder = DataParser(db)
    assert data_adder is not None

def test_data_adder_add_data(db,special_cases):
    # Create DataAdder object
    data_adder = DataParser(db,special_cases)
    # Add data to database
    rows_added = data_adder.add_data("./test/data/small_data.csv")
    # Check that the correct number of rows were added
    assert rows_added == 8
    # Check that the correct number of rows are in the database
    db.connect()
    assert db.get_db_stats(["Transactions"])["Transactions"] == rows_added
    db.disconnect()

    # Add the same data again
    new_rows_added = data_adder.add_data("./test/data/small_data.csv")
    # Check that no rows were added
    assert new_rows_added == 0

    # Add some overlapping data
    new_rows_added = data_adder.add_data("./test/data/small_data_plus.csv")
    # Check that the correct number of rows were added
    assert new_rows_added == 6

    # Check that the correct number of rows are in the database
    db.connect()
    assert db.get_db_stats(["Transactions"])["Transactions"] == rows_added+new_rows_added
    db.disconnect()

def test_data_adder_new_format(db):
    # Test that the new CSV format (with Transaktionsvaluta column) is parsed correctly
    data_adder = DataParser(db)
    rows_added = data_adder.add_data("./test/data/new_format_data.csv")
    # Check that all 5 rows were added
    assert rows_added == 5
    # Check database row count
    db.connect()
    assert db.get_db_stats(["Transactions"])["Transactions"] == rows_added
    # Check that currency and courtage were mapped correctly for first row
    cur = db.conn.cursor()
    row = cur.execute("SELECT currency, courtage FROM transactions ORDER BY date DESC LIMIT 1").fetchone()
    assert row[0] == "SEK"
    assert row[1] == 0.0
    db.disconnect()

    # Add same data again — should add 0 rows (dedup check)
    new_rows_added = data_adder.add_data("./test/data/new_format_data.csv")
    assert new_rows_added == 0

def test_data_adder_group_dedup_splits_first(db, tmp_path):
    # Setup test CSV paths
    splits_csv = tmp_path / "splits.csv"
    combined_csv = tmp_path / "combined.csv"
    
    # Write split transactions (0.7951 + 0.0286 = 0.8237)
    splits_csv.write_text(
        "Datum;Konto;Typ;Värdepapper;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat\n"
        "2026-04-29;Test Account;Köp;Avanza Zero;0,7951;523,97;-416,61;;SEK;SE0001718388;\n"
        "2026-04-29;Test Account;Köp;Avanza Zero;0,0286;523,97;-14,99;;SEK;SE0001718388;\n",
        encoding="utf-8"
    )
    
    # Write combined transaction (0.8237)
    combined_csv.write_text(
        "Datum;Konto;Typ;Värdepapper;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat\n"
        "2026-04-29;Test Account;Köp;Avanza Zero;0,8237;523,97;-431,59;;SEK;SE0001718388;\n",
        encoding="utf-8"
    )
    
    data_adder = DataParser(db)
    
    # 1. Add splits first
    rows_added = data_adder.add_data(str(splits_csv))
    assert rows_added == 2
    
    # 2. Add combined (should be skipped)
    new_rows_added = data_adder.add_data(str(combined_csv))
    assert new_rows_added == 0
    
    db.connect()
    assert db.get_db_stats(["Transactions"])["Transactions"] == 2
    db.disconnect()

def test_data_adder_group_dedup_combined_first(db, tmp_path):
    # Setup test CSV paths
    splits_csv = tmp_path / "splits.csv"
    combined_csv = tmp_path / "combined.csv"
    
    # Write split transactions (0.7951 + 0.0286 = 0.8237)
    splits_csv.write_text(
        "Datum;Konto;Typ;Värdepapper;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat\n"
        "2026-04-29;Test Account;Köp;Avanza Zero;0,7951;523,97;-416,61;;SEK;SE0001718388;\n"
        "2026-04-29;Test Account;Köp;Avanza Zero;0,0286;523,97;-14,99;;SEK;SE0001718388;\n",
        encoding="utf-8"
    )
    
    # Write combined transaction (0.8237)
    combined_csv.write_text(
        "Datum;Konto;Typ;Värdepapper;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat\n"
        "2026-04-29;Test Account;Köp;Avanza Zero;0,8237;523,97;-431,59;;SEK;SE0001718388;\n",
        encoding="utf-8"
    )
    
    data_adder = DataParser(db)
    
    # 1. Add combined first
    rows_added = data_adder.add_data(str(combined_csv))
    assert rows_added == 1
    
    # 2. Add splits (should be skipped)
    new_rows_added = data_adder.add_data(str(splits_csv))
    assert new_rows_added == 0
    
    db.connect()
    assert db.get_db_stats(["Transactions"])["Transactions"] == 1
    db.disconnect()
