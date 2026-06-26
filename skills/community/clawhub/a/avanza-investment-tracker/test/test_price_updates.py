import pytest
from database_handler import DatabaseHandler
from data_parser import DataParser


@pytest.fixture
def database_price_updates(tmp_path):
    """
    Creates a custom dataset to specifically test price updates for 
    Köp, Sälj, and Tillgångsinsättning transactions.
    """
    db_file = tmp_path / "test_asset_data.db"
    csv_file = tmp_path / "price_update_data.csv"
    
    # Create a targeted CSV for precise price tracking verification
    csv_content = """Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat
2023-01-01;1111;Insättning;Deposit;-;-;10000;0;SEK;;-
2023-01-02;1111;Köp;Asset A;10;100;-1000;0;SEK;TESTA;-
2023-01-03;1111;Köp;Asset A;5;120;-600;0;SEK;TESTA;-
2023-01-04;1111;Sälj;Asset A;-5;150;750;0;SEK;TESTA;-
2023-01-05;1111;Tillgångsinsättning;Asset B;10;50;0;0;SEK;TESTB;-
"""
    with open(csv_file, "w") as f:
        f.write(csv_content)
        
    parser = DataParser(DatabaseHandler(db_file))
    parser.add_data(str(csv_file))
    return DatabaseHandler(db_file)


def test_data_parser__price_updates(database_price_updates):
    """
    Tests that handle_purchase, handle_sale, and handle_asset_deposit correctly update
    the latest_price and latest_price_date in the assets table during processing.
    """
    parser = DataParser(database_price_updates)
    database_price_updates.connect()
    
    # Process the transactions
    parser.process_transactions()
    
    # Fetch the updated asset data
    cur = database_price_updates.get_cursor()
    assets = cur.execute("SELECT asset, latest_price, latest_price_date FROM assets").fetchall()
    
    # Convert to a dictionary for targeted assertion
    asset_dict = {row[0]: {"price": row[1], "date": row[2]} for row in assets}
    
    # Asset A sequence: Köp (100) -> Köp (120) -> Sälj (150).
    # The database should reflect the chronological final transaction (Sälj at 150 on 2023-01-04).
    assert "Asset A" in asset_dict
    assert asset_dict["Asset A"]["price"] == 150.0
    assert str(asset_dict["Asset A"]["date"]) == "2023-01-04"
    
    # Asset B sequence: Tillgångsinsättning (50).
    # The database should reflect the baseline price for the transferred shares.
    assert "Asset B" in asset_dict
    assert asset_dict["Asset B"]["price"] == 50.0
    assert str(asset_dict["Asset B"]["date"]) == "2023-01-05"
