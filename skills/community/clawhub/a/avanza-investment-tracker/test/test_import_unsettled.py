"""Tests for deferral of unsettled (pending nota) trades at import (issue #78)."""
import logging

from database_handler import DatabaseHandler
from data_parser import DataParser

HEADER = (
    "Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;"
    "Belopp;Transaktionsvaluta;Courtage;Valutakurs;Instrumentvaluta;ISIN;Resultat\n"
)


def _write_csv(path, rows):
    path.write_text(HEADER + "\n".join(rows) + "\n", encoding="utf-8")


def _buy_names(db):
    db.connect()
    rows = db.conn.execute(
        "SELECT asset_name FROM transactions WHERE transaction_type='Köp'").fetchall()
    db.disconnect()
    return sorted(r[0] for r in rows)


def test_import_skips_unsettled_trades(tmp_path, caplog):
    """Non-SEK buy with empty Courtage/Valutakurs is deferred, others imported (#78)."""
    csv_file = tmp_path / "unsettled.csv"
    _write_csv(csv_file, [
        "2020-01-16;1111;Köp;Unsettled EUR;10;100;-100;EUR;;;EUR;SE0000000001;",
        "2020-01-16;1111;Köp;Settled SEK;10;100;-100;SEK;;;;SEK;SE0000000002;",
    ])
    db = DatabaseHandler(tmp_path / "test.db")
    with caplog.at_level(logging.WARNING):
        DataParser(db).add_data(str(csv_file))

    assert _buy_names(db) == ["Settled SEK"]
    assert any("unsettled" in r.message.lower() for r in caplog.records)


def test_settled_nonsek_trade_imported(tmp_path):
    """A non-SEK buy WITH Courtage and Valutakurs is imported normally (#78)."""
    csv_file = tmp_path / "settled.csv"
    _write_csv(csv_file, [
        "2020-01-16;1111;Köp;Settled EUR;10;100;-100;EUR;5;0,1;EUR;SE0000000001;",
    ])
    db = DatabaseHandler(tmp_path / "test.db")
    DataParser(db).add_data(str(csv_file))
    assert _buy_names(db) == ["Settled EUR"]


def test_sek_trade_empty_courtage_imported(tmp_path):
    """SEK buys are never flagged as unsettled even with empty Courtage (#78)."""
    csv_file = tmp_path / "sek.csv"
    _write_csv(csv_file, [
        "2020-01-16;1111;Köp;SEK Zero;10;100;-100;SEK;;;;SEK;SE0000000001;",
    ])
    db = DatabaseHandler(tmp_path / "test.db")
    DataParser(db).add_data(str(csv_file))
    assert _buy_names(db) == ["SEK Zero"]


def test_allow_unsettled_flag_inserts_deferred_rows(tmp_path):
    """--allow-unsettled ingests pending-nota trades instead of deferring (#78)."""
    csv_file = tmp_path / "force.csv"
    _write_csv(csv_file, [
        "2020-01-16;1111;Köp;Unsettled EUR;10;100;-100;EUR;;;EUR;SE0000000001;",
    ])
    db = DatabaseHandler(tmp_path / "test.db")
    DataParser(db).add_data(str(csv_file), allow_unsettled=True)
    assert _buy_names(db) == ["Unsettled EUR"]
