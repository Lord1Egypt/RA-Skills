import pytest

from database_handler import DatabaseHandler

@pytest.fixture(scope='function')
def db_handler(tmp_path) -> DatabaseHandler:
    # Create a temporary SQLite database in the tmp_path directory
    db_file = tmp_path / "test_asset_data.db"
    return DatabaseHandler(str(db_file))

def test_database_handler__init(db_handler):
    assert db_handler is not None
    assert len(db_handler.tables) > 0

def test_database_handler__connect(db_handler):
    db_handler.connect()
    assert db_handler.conn is not None
    db_handler.disconnect()
    assert db_handler.conn is None

def test_database_hanler__get_cursor(db_handler):
    # Test that get_cursor() returns a cursor object even when the database is not connected
    cursor1 = db_handler.get_cursor()
    assert cursor1 is not None

    # Test that get_cursor() returns a cursor object when the database is already connected
    cursor2 = db_handler.get_cursor()
    assert cursor2 is not None

# Test that the database handler can return stats correctly
def test_database_handler__get_db_stats(db_handler):
    db_handler.connect()
    stats = db_handler.get_db_stats(["Transactions", "Unprocessed", "Processed", "Assets", "Capital", "Tables"])
    assert stats["Transactions"] == 0
    assert stats["Unprocessed"] == 0
    assert stats["Processed"] == 0
    assert stats["Assets"] == 0
    assert stats["Capital"] == 0
    assert stats["Tables"] == len(db_handler.tables)
    db_handler.disconnect()

# Test that the database handler can return stats correctly
def test_database_handler__get_db_stat(db_handler):
    db_handler.connect()
    assert db_handler.get_db_stat("Transactions") == 0
    assert db_handler.get_db_stat("Unprocessed") == 0
    assert db_handler.get_db_stat("Processed") == 0
    assert db_handler.get_db_stat("Assets") == 0
    assert db_handler.get_db_stat("Capital") == 0
    assert db_handler.get_db_stat("Tables") == len(db_handler.tables)
    db_handler.disconnect()

# Test that the database handler can reset the tables correctly
def test_database_handler__reset_table(db_handler):
    db_handler.connect()
    # Add a row to the transactions table
    cursor = db_handler.get_cursor()
    cursor.execute("INSERT INTO transactions(date, account, transaction_type,asset_name,amount,price,total,courtage,currency,isin) VALUES(?,?,?,?,?,?,?,?,?,?);",(1,2,3,4,5,6,7,8,9,10))
    db_handler.conn.commit()
    # Get the number of rows in the transactions table
    original_rows = db_handler.get_db_stat("Transactions")
    # Reset the tables a different table
    db_handler.reset_table("assets")
    # Check that the number of rows is the same
    assert db_handler.get_db_stat("Transactions") == original_rows
    # Reset the correct table
    rowcount = db_handler.reset_table("transactions")
    # Check that the new number of rows is less than the original number of rows
    assert db_handler.get_db_stat("Transactions") < original_rows
    # Check that the number of reset rows is the same as the original number of rows
    assert rowcount == original_rows
    # Check that the number of rows is 0
    assert db_handler.get_db_stat("Transactions") == 0
    db_handler.disconnect()

# Test that the database handler returns an error when trying to reset a table that does not exist
def test_database_handler__reset_table_nonexistant(db_handler):
    db_handler.connect()
    # Add a row to the transactions table
    cursor = db_handler.get_cursor()
    cursor.execute("INSERT INTO transactions(date, account, transaction_type,asset_name,amount,price,total,courtage,currency,isin) VALUES(?,?,?,?,?,?,?,?,?,?);",(1,2,3,4,5,6,7,8,9,10))
    db_handler.conn.commit()
    # Reset the tables a table that does not exist
    with pytest.raises(Exception):
        db_handler.reset_table("nonexistant_table")
    # Check that the number of rows is the same
    assert db_handler.get_db_stat("Transactions") == 1

# Test that the database handler can reset all tables correctly
def test_database_handler__reset_all_tables(db_handler):
    db_handler.connect()
    # Add a row to the transactions table
    cursor = db_handler.get_cursor()
    cursor.execute("INSERT INTO transactions(date, account, transaction_type,asset_name,amount,price,total,courtage,currency,isin) VALUES(?,?,?,?,?,?,?,?,?,?);",(1,2,3,4,5,6,7,8,9,10))
    db_handler.conn.commit()
    # Get the number of rows in the transactions table
    db_handler.get_db_stat("Transactions")
    # Reset the tables
    db_handler.reset_tables()
    # Check that the number of rows is 0
    assert db_handler.get_db_stat("Transactions") == 0
    db_handler.disconnect()