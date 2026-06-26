import pytest

from database_handler import DatabaseHandler
from data_parser import DataParser, AssetDeficit, SpecialCases

# Define all datasets to be used that should pass
passing_datasets = [
    "./test/data/small_data.csv", 
    "./test/data/listing_change.csv", 
    "./test/data/reordered_data.csv",
    "./test/data/asset_deposit.csv",
    "./test/data/interest_fees.csv",
    "./test/data/fraction_writeoff.csv",
    "./test/data/new_transaction_types.csv"]

# Parametrize the fixture
# Indirect parametrization allows us to use different datasets for the same fixture
@pytest.fixture
def databases(tmp_path, request):
    # Create a temporary SQLite database in the tmp_path directory
    db_file = tmp_path / "test_asset_data.db"
    # Create DataAdder object
    data_adder = DataParser(DatabaseHandler(db_file), SpecialCases("./test/data/special_cases_test.json"))
    # Add data to database
    # The dataset used is specified in the test function that uses this fixture
    data_adder.add_data(request.param)
    return DatabaseHandler(db_file)

# Create a temporary SQLite database in the tmp_path directory using the small dataset
# Special cases are not handled, creating a small deficit in the database
@pytest.fixture
def database_small_deficit(tmp_path):
    # Create a temporary SQLite database in the tmp_path directory
    db_file = tmp_path / "test_asset_data.db"
    # Create DataAdder object
    data_adder = DataParser(DatabaseHandler(db_file))
    # Add data to database
    data_adder.add_data("./test/data/small_data.csv")
    return DatabaseHandler(db_file)

@pytest.fixture
def database_small_wrong_accounts(tmp_path):
    # Create a temporary SQLite database in the tmp_path directory
    db_file = tmp_path / "test_asset_data.db"
    # Create DataAdder object
    data_adder = DataParser(DatabaseHandler(db_file), SpecialCases("./test/data/special_cases_test.json"))
    # Add data to database
    data_adder.add_data("./test/data/small_data_wrong_accounts.csv")
    return DatabaseHandler(db_file)

@pytest.fixture
def database_cohort_aggregation(tmp_path):
    """
    Creates a database with a specific scenario for testing the cohort_cash_flows aggregation:
    - 2020-01-15: Deposit 1000 SEK (using >10th to bypass the month offset logic)
    - 2021-05-15: Withdraw 100 SEK
    - 2021-05-20: Withdraw 200 SEK
    - 2021-05-25: Withdraw 50 SEK
    All three withdrawals occur in the same month and draw from the same cohort,
    so they should be aggregated into one row summing to -350 SEK.
    """
    csv_content = """Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat
2020-01-15;1111;Insättning;Deposit;-;-;1000;0;SEK;;-
2021-05-15;1111;Uttag;;-;-;-100;0;SEK;;-
2021-05-20;1111;Uttag;;-;-;-200;0;SEK;;-
2021-05-25;1111;Uttag;;-;-;-50;0;SEK;;-
"""
    csv_file = tmp_path / "cohort_aggregation.csv"
    csv_file.write_text(csv_content, encoding="utf-8")
    
    db_file = tmp_path / "test_cohort_aggregation.db"
    db = DatabaseHandler(db_file)
    
    parser = DataParser(db)
    parser.add_data(str(csv_file))
    
    return db, parser

@pytest.mark.parametrize("databases", passing_datasets, indirect=True)
def test_data_parser__parse(databases):
    # Create DataParser object
    data_parser = DataParser(databases, SpecialCases("./test/data/special_cases_test.json"))
    # Connect to database and get number of unprocessed transactions
    databases.connect()
    unprocessed = databases.get_db_stat("Unprocessed" )
    # Process transactions
    data_parser.process_transactions()
    # Check that all previously unprocessed transactions are now processed
    assert databases.get_db_stat("Processed" ) == unprocessed
    assert databases.get_db_stat("Unprocessed" ) == 0

@pytest.mark.parametrize("databases", passing_datasets, indirect=True)
def test_data_parser__double_parse(databases):
    # Create DataParser object
    data_parser = DataParser(databases, SpecialCases("./test/data/special_cases_test.json"))
    # Connect to database and get number of unprocessed transactions
    databases.connect()
    unprocessed = databases.get_db_stat("Unprocessed" )
    # Process transactions
    data_parser.process_transactions()
    # Process transactions again, since all are processed nothing should happen
    data_parser.process_transactions()
    # Check that all previously unprocessed transactions are now processed
    assert databases.get_db_stat("Processed" ) == unprocessed
    assert databases.get_db_stat("Unprocessed" ) == 0

@pytest.mark.parametrize("databases", passing_datasets, indirect=True)
def test_data_parser__reset(databases):
    # Create DataParser object
    data_parser = DataParser(databases, SpecialCases("./test/data/special_cases_test.json"))
    # Connect to database and get number of unprocessed transactions
    databases.connect()
    unprocessed = databases.get_db_stat("Unprocessed" )
    # Process transactions
    data_parser.process_transactions()
    # Check that all previously unprocessed transactions are now processed
    assert databases.get_db_stat("Processed" ) == unprocessed
    assert databases.get_db_stat("Unprocessed" ) == 0
    # Reset the database
    data_parser.reset_processed_transactions()
    # Check that all previously processed transactions are now unprocessed
    assert databases.get_db_stat("Processed" ) == 0
    assert databases.get_db_stat("Unprocessed" ) == unprocessed

@pytest.mark.parametrize("databases", passing_datasets, indirect=True)
def test_data_parser__reparse(databases):
    # Create DataParser object
    data_parser = DataParser(databases, SpecialCases("./test/data/special_cases_test.json"))
    # Connect to database and get number of unprocessed transactions
    databases.connect()
    unprocessed = databases.get_db_stat("Unprocessed" )
    # Process transactions
    data_parser.process_transactions()
    # Check that all previously unprocessed transactions are now processed
    assert databases.get_db_stat("Processed" ) == unprocessed
    assert databases.get_db_stat("Unprocessed" ) == 0
    # Reset the database
    data_parser.reset_processed_transactions()
    # Check that all previously processed transactions are now unprocessed
    assert databases.get_db_stat("Processed" ) == 0
    assert databases.get_db_stat("Unprocessed" ) == unprocessed
    # Test that all transactions can be processed again
    data_parser.process_transactions()
    assert databases.get_db_stat("Processed" ) == unprocessed
    assert databases.get_db_stat("Unprocessed" ) == 0


def test_data_parser__wrong_accounts(database_small_wrong_accounts):
    # Create DataParser object
    data_parser = DataParser(database_small_wrong_accounts)
    # Connect to database and get number of unprocessed transactions
    database_small_wrong_accounts.connect()
    unprocessed = database_small_wrong_accounts.get_db_stat("Unprocessed" )
    # Process transactions, since there is a deficit, an exception should be raised
    with pytest.raises(AssetDeficit):
        data_parser.process_transactions()
    # Check that all previously unprocessed transactions are still unprocessed
    assert database_small_wrong_accounts.get_db_stat("Processed" ) == 0
    assert database_small_wrong_accounts.get_db_stat("Unprocessed" ) == unprocessed

def test_cohort_cash_flows_aggregation(database_cohort_aggregation):
    db, parser = database_cohort_aggregation
    
    # Process transactions
    parser.process_transactions()
    
    db.connect()
    cur = db.get_cursor()
    
    # Query the cohort_cash_flows table
    rows = cur.execute(
        "SELECT cohort_month, account, transaction_month, amount FROM cohort_cash_flows"
    ).fetchall()
    
    # There should be exactly one row summing all three withdrawals from May 2021
    assert len(rows) == 1
    
    cohort_month, account, transaction_month, amount = rows[0]
    
    # Validating the aggregated results
    assert str(cohort_month) == "2020-01-31"
    assert account == "1111"
    assert str(transaction_month) == "2021-05-31"
    assert amount == -350.0  # -100 - 200 - 50 = -350