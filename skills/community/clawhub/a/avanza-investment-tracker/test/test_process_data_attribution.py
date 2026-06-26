import pytest

from database_handler import DatabaseHandler
from data_parser import DataParser


@pytest.fixture
def database_attribution_single_account(tmp_path):
    """
    Single account: deposit 110, buy asset for 100, sell for 200, withdraw 210.
    All activity in one account — attribution should be clean.
    """
    db_file = tmp_path / "test_asset_data.db"
    parser = DataParser(DatabaseHandler(db_file))
    parser.add_data("./test/data/transfer_attribution_single_account.csv")
    return DatabaseHandler(db_file)


@pytest.fixture
def database_attribution_two_accounts(tmp_path):
    """
    Two accounts: 1111 deposits 100 and buys asset, 2222 deposits 10.
    Asset sold for 200 in 1111, 100 transferred to 2222, then both accounts withdraw.
    The 100 SEK transferred was originally deposited in the same month as the asset purchase —
    it should remain attributed to that month even after moving to a different account.
    """
    db_file = tmp_path / "test_asset_data.db"
    parser = DataParser(DatabaseHandler(db_file))
    parser.add_data("./test/data/transfer_attribution_two_accounts.csv")
    return DatabaseHandler(db_file)


def test_process_data__attribution_single_account(database_attribution_single_account):
    """
    Single account baseline: all gain correctly attributed to the deposit month.

    Expected cohort_data:
      - One row: deposit=110, withdrawal=210, gain=100
      - No orphan rows (rows with withdrawal > 0 but deposit == 0)
    """
    parser = DataParser(database_attribution_single_account)
    database_attribution_single_account.connect()
    unprocessed = database_attribution_single_account.get_db_stat("Unprocessed")

    parser.process_transactions()

    assert database_attribution_single_account.get_db_stat("Processed") == unprocessed
    assert database_attribution_single_account.get_db_stat("Unprocessed") == 0

    cur = database_attribution_single_account.get_cursor()

    rows = cur.execute(
        "SELECT month, account, deposit, capital, withdrawal FROM cohort_data ORDER BY month, account"
    ).fetchall()

    total_deposit = sum(r[2] for r in rows)
    total_withdrawal = sum(r[4] for r in rows)
    orphan_rows = [r for r in rows if r[4] > 0.01 and r[2] < 0.01]

    assert abs(total_deposit - 110.0) < 0.01, f"Total deposit should be 110, got {total_deposit}"
    assert abs(total_withdrawal - 210.0) < 0.01, f"Total withdrawal should be 210, got {total_withdrawal}"
    assert len(orphan_rows) == 0, f"No orphan withdrawal rows expected, got: {orphan_rows}"


def test_process_data__attribution_two_accounts(database_attribution_two_accounts):
    """
    Two accounts: gain should be attributed to the original deposit month,
    regardless of the capital moving to a different account via internal transfer.

    Expected cohort_data:
      - Total deposit = 110 SEK
      - Total withdrawal = 210 SEK
      - No orphan rows (rows with withdrawal > 0 but deposit == 0)
        i.e. the 100 SEK transferred to 2222 should NOT create a new month row
        with deposit=0 — it should remain attributed to its original deposit month.
    """
    parser = DataParser(database_attribution_two_accounts)
    database_attribution_two_accounts.connect()
    unprocessed = database_attribution_two_accounts.get_db_stat("Unprocessed")

    parser.process_transactions()

    assert database_attribution_two_accounts.get_db_stat("Processed") == unprocessed
    assert database_attribution_two_accounts.get_db_stat("Unprocessed") == 0

    cur = database_attribution_two_accounts.get_cursor()

    rows = cur.execute(
        "SELECT month, account, deposit, capital, withdrawal FROM cohort_data ORDER BY month, account"
    ).fetchall()

    total_deposit = sum(r[2] for r in rows)
    total_withdrawal = sum(r[4] for r in rows)
    orphan_rows = [r for r in rows if r[4] > 0.01 and r[2] < 0.01]

    assert abs(total_deposit - 110.0) < 0.01, f"Total deposit should be 110, got {total_deposit}"
    assert abs(total_withdrawal - 210.0) < 0.01, f"Total withdrawal should be 210, got {total_withdrawal}"
    assert len(orphan_rows) == 0, \
        f"Orphan withdrawal rows found — transferred capital lost its original month attribution: {orphan_rows}"
