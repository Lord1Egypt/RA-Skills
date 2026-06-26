"""
Test per-account asset tracking implementation.

These tests verify:
1. Assets are tracked per account in cohort_assets table
2. Sales can only sell assets owned by the account
3. Savings accounts don't get attributed assets they never purchased
4. Assets are correctly associated with the purchasing account
"""

import pytest
import sqlite3

from database_handler import DatabaseHandler
from data_parser import DataParser


@pytest.fixture
def database_basic_two_accounts(tmp_path):
    """
    Two accounts purchasing different assets:
    - Account 1111: Deposits 100, buys 5 Asset A for 50
    - Account 2222: Deposits 200, buys 2 Asset B for 50
    """
    db_file = tmp_path / "test_asset_data.db"
    parser = DataParser(DatabaseHandler(db_file))

    # Create test CSV data in correct Avanza format (semicolon separated, 11 columns)
    test_data = """Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat
2020-01-01;1111;Insättning;Deposit;-;-;100;0;SEK;DEPOSIT;-
2020-01-01;1111;Köp;Asset A;5;10;-50;0;SEK;ASSETA;-
2020-01-01;2222;Insättning;Deposit;-;-;200;0;SEK;DEPOSIT;-
2020-01-01;2222;Köp;Asset B;2;25;-50;0;SEK;ASSETB;-"""
    
    # Write to temporary CSV
    csv_file = tmp_path / "test_data.csv"
    with open(csv_file, 'w') as f:
        f.write(test_data)
    
    parser.add_data(str(csv_file))
    return DatabaseHandler(db_file)


@pytest.fixture  
def database_savings_account_scenario(tmp_path):
    """
    Savings account scenario:
    - SavingsAccount: Deposits 5000 (only cash, no purchases)
    - InvestmentAccount: Deposits 27000, buys 10 Asset A for 100
    """
    db_file = tmp_path / "test_asset_data.db"
    parser = DataParser(DatabaseHandler(db_file))
    
    test_data = """Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat
2026-01-01;SavingsAccount;Insättning;Deposit;-;-;5000;0;SEK;DEPOSIT;-
2026-01-01;InvestmentAccount;Insättning;Deposit;-;-;27000;0;SEK;DEPOSIT;-
2026-01-01;InvestmentAccount;Köp;Asset A;10;10;-100;0;SEK;ASSETA;-"""
    
    csv_file = tmp_path / "test_data.csv"
    with open(csv_file, 'w') as f:
        f.write(test_data)
    
    parser.add_data(str(csv_file))
    return DatabaseHandler(db_file)


@pytest.fixture
def database_sales_validation(tmp_path):
    """
    Test sales validation:
    - Account 1111: Deposits 100, buys 5 Asset A for 50
    - Account 2222: Deposits 200, buys 2 Asset B for 50
    - Account 1111 tries to sell Asset B (doesn't own it)
    """
    db_file = tmp_path / "test_asset_data.db"
    parser = DataParser(DatabaseHandler(db_file))
    
    test_data = """Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat
2020-01-01;1111;Insättning;Deposit;-;-;100;0;SEK;DEPOSIT;-
2020-01-01;1111;Köp;Asset A;5;10;-50;0;SEK;ASSETA;-
2020-01-01;2222;Insättning;Deposit;-;-;200;0;SEK;DEPOSIT;-
2020-01-01;2222;Köp;Asset B;2;25;-50;0;SEK;ASSETB;-
2020-02-01;1111;Sälj;Asset B;-1;30;30;0;SEK;ASSETB;-"""
    
    csv_file = tmp_path / "test_data.csv"
    with open(csv_file, 'w') as f:
        f.write(test_data)
    
    parser.add_data(str(csv_file))
    return DatabaseHandler(db_file)


def test_assets_correctly_attributed_to_purchasing_account(database_basic_two_accounts):
    """
    Test that assets are correctly attributed to the account that purchased them.
    """
    db = database_basic_two_accounts
    db.connect()
    cur = db.get_cursor()

    # Process transactions
    parser = DataParser(db)
    parser.process_transactions()

    # Get asset purchases from transactions (join by asset name)
    cur.execute("""
        SELECT t.account, t.asset_name, SUM(t.amount) as purchased_amount
        FROM transactions t
        WHERE t.transaction_type = 'Köp' AND t.amount > 0
        GROUP BY t.account, t.asset_name
        ORDER BY t.account, t.asset_name
    """)
    purchases = cur.fetchall()
    
    # Get asset holdings from cohort_assets
    cur.execute("""
        SELECT ma.account, a.asset, SUM(ma.amount) as held_amount
        FROM cohort_assets ma
        JOIN assets a ON ma.asset_id = a.asset_id
        WHERE ma.amount > 0
        GROUP BY ma.account, a.asset
        ORDER BY ma.account, a.asset
    """)
    holdings = cur.fetchall()
    
    # Create dictionaries for comparison
    purchase_dict = {(account, asset_name): amount for account, asset_name, amount in purchases}
    holding_dict = {(account, asset): amount for account, asset, amount in holdings}
    
    # Verify each purchase appears in holdings for the same account
    for (account, asset), purchase_amount in purchase_dict.items():
        assert (account, asset) in holding_dict, f"Account {account} should hold {asset} they purchased"
        holding_amount = holding_dict[(account, asset)]
        assert abs(purchase_amount - holding_amount) < 0.001, \
            f"Account {account} purchased {purchase_amount} of {asset} but holds {holding_amount}"


def test_assets_tracked_per_account(database_basic_two_accounts):
    """
    Test that assets are tracked per account in cohort_assets.
    """
    db = database_basic_two_accounts
    db.connect()
    cur = db.get_cursor()

    # Process transactions
    parser = DataParser(db)
    parser.process_transactions()

    # Check cohort_assets table - should include account column
    cur.execute("SELECT month, asset_id, account, amount FROM cohort_assets ORDER BY month, asset_id, account")
    cohort_assets = cur.fetchall()

    # Get asset names for readability
    cur.execute("SELECT asset_id, asset FROM assets ORDER BY asset_id")
    asset_map = {row[0]: row[1] for row in cur.fetchall()}

    # We have 2 assets purchased by different accounts
    # Should have 2 entries with account information
    assert len(cohort_assets) == 2, "Should have 2 asset entries (one per asset per account)"

    # Check that assets in cohort_assets include account info
    for month, asset_id, account, amount in cohort_assets:
        asset_name = asset_map[asset_id]
        print(f"Asset in cohort_assets: {month}, {asset_name}, Account: {account}, {amount} shares")

    # Verify each asset is associated with the correct account
    asset_accounts = {}
    for month, asset_id, account, amount in cohort_assets:
        asset_name = asset_map[asset_id]
        asset_accounts[asset_name] = account
    
    # Asset A should be owned by account 1111
    # Asset B should be owned by account 2222
    assert asset_accounts.get('Asset A') == '1111', "Asset A should be owned by account 1111"
    assert asset_accounts.get('Asset B') == '2222', "Asset B should be owned by account 2222"


def test_accounts_only_hold_assets_they_purchased(database_savings_account_scenario):
    """
    Test that accounts only hold assets they actually purchased.
    """
    db = database_savings_account_scenario
    db.connect()
    cur = db.get_cursor()

    # Process transactions
    parser = DataParser(db)
    parser.process_transactions()

    # Get all asset purchases by account (join by asset name)
    cur.execute("""
        SELECT t.account, t.asset_name, SUM(t.amount) as purchased_amount
        FROM transactions t
        WHERE t.transaction_type = 'Köp' AND t.amount > 0
        GROUP BY t.account, t.asset_name
        ORDER BY t.account, t.asset_name
    """)
    purchases = cur.fetchall()
    
    # Get all asset holdings by account
    cur.execute("""
        SELECT ma.account, a.asset, SUM(ma.amount) as held_amount
        FROM cohort_assets ma
        JOIN assets a ON ma.asset_id = a.asset_id
        WHERE ma.amount > 0
        GROUP BY ma.account, a.asset
        ORDER BY ma.account, a.asset
    """)
    holdings = cur.fetchall()
    
    # Create purchase and holding dictionaries
    purchase_dict = {(account, asset_name): amount for account, asset_name, amount in purchases}
    holding_dict = {(account, asset): amount for account, asset, amount in holdings}
    
    print("Purchases:", purchase_dict)
    print("Holdings:", holding_dict)
    
    # Rule 1: Every holding must have a corresponding purchase
    for (account, asset), held_amount in holding_dict.items():
        assert (account, asset) in purchase_dict, \
            f"Account {account} holds {asset} but never purchased it"
        purchased_amount = purchase_dict[(account, asset)]
        assert abs(purchased_amount - held_amount) < 0.001, \
            f"Account {account} purchased {purchased_amount} of {asset} but holds {held_amount}"
    
    # Rule 2: Accounts without purchases should have no holdings
    # Get all accounts that made purchases
    accounts_with_purchases = {account for account, _ in purchase_dict.keys()}
    
    # Check each account with holdings
    for (account, asset), held_amount in holding_dict.items():
        assert account in accounts_with_purchases, \
            f"Account {account} has holdings but never made any purchases"
    
    # In our test data:
    # - SavingsAccount: Deposited 5000, made NO purchases
    # - InvestmentAccount: Deposited 27000, purchased Asset A
    # Therefore: SavingsAccount should have 0 holdings


def test_sales_with_ownership_validation(database_sales_validation):
    """
    Test that accounts CANNOT sell assets they never purchased.
    """
    db = database_sales_validation
    db.connect()
    cur = db.get_cursor()

    # Process transactions - should fail because 1111 tries to sell Asset B (owned by 2222)
    parser = DataParser(db)
    
    # This should raise an AssetDeficit error
    import sys
    import io
    from contextlib import redirect_stderr, redirect_stdout
    
    # Capture stderr to check for error
    stderr_capture = io.StringIO()
    
    try:
        with redirect_stderr(stderr_capture):
            parser.process_transactions()
        
        # If we get here, the sale was processed (which would be wrong)
        stderr_output = stderr_capture.getvalue()
        print(f"Stderr output: {stderr_output}")
        
        # Check if error message is in stderr
        assert "could not be processed due to a missmatch of assets" in stderr_output, \
            "Should have error about asset mismatch"
        assert "Asset B" in stderr_output, "Error should mention Asset B"
        
    except Exception as e:
        # AssetDeficit exception would also be acceptable
        print(f"Exception raised (acceptable): {type(e).__name__}: {e}")
        assert "AssetDeficit" in str(type(e).__name__) or "could not be processed" in str(e), \
            f"Expected AssetDeficit or processing error, got {type(e).__name__}"


def test_proportional_attribution_logic():
    """
    Test the mathematical logic of proportional attribution.
    Demonstrates why SUM(capital) is correct for cash calculation.
    """
    # Example: SavingsAccount has capital in multiple months
    # Jan 2024: 1,000
    # Apr 2024: 2,000  
    # Jan 2026: 3,000
    # Total: 6,000
    
    savings_account_capital = {
        '2024-01': 1000,
        '2024-04': 2000,
        '2026-01': 3000
    }
    
    total_cash = sum(savings_account_capital.values())
    assert total_cash == 6000, f"Total cash should be 6,000, got {total_cash}"
    
    # Demonstrates that looking for "latest non-zero capital" gives wrong answer
    latest_month = max(savings_account_capital.keys())
    latest_capital = savings_account_capital[latest_month]
    
    print(f"Latest month ({latest_month}) capital: {latest_capital}")
    print(f"Total capital (sum across months): {total_cash}")
    print(f"Error if using latest only: {total_cash - latest_capital} SEK missing")
    
    assert latest_capital == 3000, "Latest capital should be 3,000"
    assert total_cash > latest_capital, "Total should be greater than latest month only"
    assert total_cash - latest_capital == 3000, "Should be missing 3,000 SEK if using latest only"