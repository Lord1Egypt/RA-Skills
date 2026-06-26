import pytest

from database_handler import DatabaseHandler
from data_parser import DataParser


@pytest.fixture
def database_transfer_deferral(tmp_path):
    """
    Out-of-order internal transfers: Transfer IN arrives before paired OUT,
    and a sell is needed before the second OUT can be processed.
    All 8 transactions should be processed via deferred retry logic.
    """
    db_file = tmp_path / "test_asset_data.db"
    parser = DataParser(DatabaseHandler(db_file))
    parser.add_data("./test/data/transfer_deferral.csv")
    return DatabaseHandler(db_file)


@pytest.fixture
def database_transfer_proper_order(tmp_path):
    """
    Same scenario as transfer_deferral but with transactions in natural order
    (OUT before IN, dependencies satisfied before they are needed).
    No deferral required — baseline that must always pass.
    """
    db_file = tmp_path / "test_asset_data.db"
    parser = DataParser(DatabaseHandler(db_file))
    parser.add_data("./test/data/transfer_proper_order.csv")
    return DatabaseHandler(db_file)


def test_process_data__transfer_deferral(database_transfer_deferral):
    """
    Verifies that out-of-order internal transfers are correctly deferred and
    retried once sufficient capital/assets become available.

    Expected final state:
    - All 8 transactions processed
    - Account 1111: 25 SEK capital  (100 deposit - 100 out + 175 in - 150 withdraw)
    - Account 2222: 25 SEK capital  (100 in - 100 purchase + 200 sell - 175 out)
    - No Asset A held
    """
    parser = DataParser(database_transfer_deferral)
    database_transfer_deferral.connect()
    unprocessed = database_transfer_deferral.get_db_stat("Unprocessed")

    parser.process_transactions()

    assert database_transfer_deferral.get_db_stat("Processed") == unprocessed
    assert database_transfer_deferral.get_db_stat("Unprocessed") == 0

    cur = database_transfer_deferral.get_cursor()

    capital_1111 = cur.execute(
        "SELECT SUM(capital) FROM cohort_data WHERE account = '1111'"
    ).fetchone()[0] or 0.0
    capital_2222 = cur.execute(
        "SELECT SUM(capital) FROM cohort_data WHERE account = '2222'"
    ).fetchone()[0] or 0.0
    asset_amount = cur.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM cohort_assets"
    ).fetchone()[0]

    assert abs(capital_1111 - 25.0) < 0.01, f"Account 1111 capital should be 25, got {capital_1111}"
    assert abs(capital_2222 - 25.0) < 0.01, f"Account 2222 capital should be 25, got {capital_2222}"
    assert abs(asset_amount) < 0.001, f"No assets should be held, got {asset_amount}"


def test_process_data__transfer_proper_order(database_transfer_proper_order):
    """
    Verifies the same scenario with transactions in correct order processes
    cleanly without needing deferral. Same expected final state as the deferral test.
    """
    parser = DataParser(database_transfer_proper_order)
    database_transfer_proper_order.connect()
    unprocessed = database_transfer_proper_order.get_db_stat("Unprocessed")

    parser.process_transactions()

    assert database_transfer_proper_order.get_db_stat("Processed") == unprocessed
    assert database_transfer_proper_order.get_db_stat("Unprocessed") == 0

    cur = database_transfer_proper_order.get_cursor()

    capital_1111 = cur.execute(
        "SELECT SUM(capital) FROM cohort_data WHERE account = '1111'"
    ).fetchone()[0] or 0.0
    capital_2222 = cur.execute(
        "SELECT SUM(capital) FROM cohort_data WHERE account = '2222'"
    ).fetchone()[0] or 0.0
    asset_amount = cur.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM cohort_assets"
    ).fetchone()[0]

    assert abs(capital_1111 - 25.0) < 0.01, f"Account 1111 capital should be 25, got {capital_1111}"
    assert abs(capital_2222 - 25.0) < 0.01, f"Account 2222 capital should be 25, got {capital_2222}"
    assert abs(asset_amount) < 0.001, f"No assets should be held, got {asset_amount}"
