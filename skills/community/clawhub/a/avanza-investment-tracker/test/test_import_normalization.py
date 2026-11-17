"""Tests for asset-name normalization at import (issue #79)."""
import sqlite3

from database_handler import DatabaseHandler
from data_parser import DataParser

NEW_FORMAT_HEADER = (
    "Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;"
    "Belopp;Transaktionsvaluta;Courtage;Valutakurs;Instrumentvaluta;ISIN;Resultat\n"
)


def _write_csv(path, rows):
    path.write_text(NEW_FORMAT_HEADER + "\n".join(rows) + "\n", encoding="utf-8")


def test_import_trims_asset_name_whitespace(tmp_path):
    """Leading/trailing spaces in instrument names are stripped on import (#79)."""
    csv_file = tmp_path / "trim.csv"
    _write_csv(csv_file, [
        "2020-01-15;1111;Insättning;Deposit;-;-;1000;SEK;;;;;",
        "2020-01-16;1111;Köp;Foo ;10;100;-1000;SEK;0;;;SEK;SE0000000001;",
        "2020-01-17;1111;Köp; Bar;5;100;-500;SEK;0;;;SEK;SE0000000002;",
    ])
    db = DatabaseHandler(tmp_path / "test.db")
    DataParser(db).add_data(str(csv_file))

    db.connect()
    names = sorted(r[0] for r in db.conn.execute(
        "SELECT asset_name FROM transactions WHERE transaction_type='Köp'"))
    db.disconnect()
    assert names == ["Bar", "Foo"]


def test_import_dedup_uses_trimmed_names(tmp_path):
    """Re-importing the same CSV does not double-insert once names are trimmed (#79)."""
    csv_file = tmp_path / "trim.csv"
    _write_csv(csv_file, [
        "2020-01-15;1111;Insättning;Deposit;-;-;1000;SEK;;;;;",
        "2020-01-16;1111;Köp;Foo ;10;100;-1000;SEK;0;;;SEK;SE0000000001;",
    ])
    db = DatabaseHandler(tmp_path / "test.db")
    parser = DataParser(db)
    parser.add_data(str(csv_file))
    parser.add_data(str(csv_file))  # re-import should dedup, not duplicate

    db.connect()
    n = db.conn.execute(
        "SELECT COUNT(*) FROM transactions WHERE transaction_type='Köp'").fetchone()[0]
    db.disconnect()
    assert n == 1


def test_migration_trims_existing_dirty_names(tmp_path):
    """Dirty names already in the DB are trimmed when it is reopened (#79 migration)."""
    db_path = tmp_path / "test.db"
    db = DatabaseHandler(db_path)  # creates schema (migration is a no-op here)
    db.disconnect()

    # Seed dirty rows directly, bypassing the import-time trim.
    conn = sqlite3.connect(str(db_path))
    conn.execute(
        "INSERT INTO transactions (date, account, transaction_type, asset_name, "
        "amount, price, total, courtage, currency, isin, processed, origin) "
        "VALUES ('2020-01-16','1111','Köp','Foo ',10,100,-1000,0,'SEK','',0,'avanza')")
    conn.execute("INSERT INTO assets (asset_id, asset, amount) VALUES (1, 'Foo ', 10)")
    conn.commit()
    conn.close()

    # Reopen -> create_tables runs the trim migration before the asset_prices backfill.
    db2 = DatabaseHandler(db_path)
    db2.connect()
    tx_name = db2.conn.execute("SELECT asset_name FROM transactions").fetchone()[0]
    asset_name = db2.conn.execute("SELECT asset FROM assets").fetchone()[0]
    db2.disconnect()

    assert tx_name == "Foo"
    assert asset_name == "Foo"
