"""Tests for the top-level delete-tx command (issue #80).

Uses fabricated data only (workspace PII rule).
"""
import argparse

import cli
from database_handler import DatabaseHandler
from data_parser import DataParser

BASE_CSV = (
    "Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;"
    "Belopp;Courtage;Valuta;ISIN;Resultat\n"
    "2020-01-01;1111;Insättning;Deposit;-;-;20000;0;SEK;DEPOSIT;-\n"
    "2020-01-02;1111;Köp;Asset A;100;100;-10000;0;SEK;ASSETA;-\n"
)

TWO_BUY_CSV = (
    "Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;"
    "Belopp;Courtage;Valuta;ISIN;Resultat\n"
    "2020-01-01;1111;Insättning;Deposit;-;-;20000;0;SEK;DEPOSIT;-\n"
    "2020-01-02;1111;Köp;Asset A;100;100;-10000;0;SEK;ASSETA;-\n"
    "2020-02-02;1111;Köp;Asset B;10;100;-1000;0;SEK;ASSETB;-\n"
)


def _write_csv(tmp_path, name, text):
    p = tmp_path / name
    p.write_text(text, encoding="utf-8")
    return str(p)


def _build_db(tmp_path, csv_text, filename="v.db"):
    db_file = tmp_path / filename
    db = DatabaseHandler(db_file)
    parser = DataParser(db)
    csv_file = _write_csv(tmp_path, "base.csv", csv_text)
    db.connect()
    parser.add_data(csv_file)
    parser.reset_for_reprocessing()
    parser.process_transactions()
    db.disconnect()
    return db_file


def _ns(database, **kw):
    base = dict(database=str(database), special_cases=None)
    base.update(kw)
    return argparse.Namespace(**base)


def _count(db_file, where, params=()):
    db = DatabaseHandler(db_file)
    db.connect()
    n = db.conn.execute(
        f"SELECT COUNT(*) FROM transactions WHERE {where}", params).fetchone()[0]
    db.disconnect()
    return n


def _asset_amount(db_file, asset="Asset A"):
    db = DatabaseHandler(db_file)
    db.connect()
    val = db.conn.execute("SELECT amount FROM assets WHERE asset=?", (asset,)).fetchone()
    db.disconnect()
    return val[0] if val else None


def test_delete_tx_by_date_asset(tmp_path):
    db_file = _build_db(tmp_path, BASE_CSV)
    assert _asset_amount(db_file) == 100  # held before
    rc = cli.delete_tx(_ns(db_file, tx_id=None, date="2020-01-02", since=None,
                           asset="Asset A", account=None, cascade=False, dry_run=False, yes=True))
    assert rc == 0
    assert _count(db_file, "transaction_type='Köp'") == 0
    assert _count(db_file, "transaction_type='Insättning'") == 1  # deposit untouched
    assert _asset_amount(db_file) in (None, 0)  # reprocessed -> no longer held


def test_delete_tx_tx_id(tmp_path):
    db_file = _build_db(tmp_path, BASE_CSV)
    db = DatabaseHandler(db_file)
    db.connect()
    rid = db.conn.execute(
        "SELECT rowid FROM transactions WHERE transaction_type='Köp'").fetchone()[0]
    db.disconnect()
    rc = cli.delete_tx(_ns(db_file, tx_id=rid, date=None, since=None,
                           asset=None, account=None, cascade=False, dry_run=False, yes=True))
    assert rc == 0
    assert _count(db_file, "transaction_type='Köp'") == 0


def test_delete_tx_since(tmp_path):
    db_file = _build_db(tmp_path, TWO_BUY_CSV)
    assert _count(db_file, "transaction_type='Köp'") == 2
    rc = cli.delete_tx(_ns(db_file, tx_id=None, date=None, since="2020-02-02",
                           asset=None, account=None, cascade=False, dry_run=False, yes=True))
    assert rc == 0
    assert _count(db_file, "transaction_type='Köp' AND asset_name='Asset B'") == 0
    assert _count(db_file, "transaction_type='Köp' AND asset_name='Asset A'") == 1


def test_delete_tx_dry_run(tmp_path):
    db_file = _build_db(tmp_path, BASE_CSV)
    rc = cli.delete_tx(_ns(db_file, tx_id=None, date="2020-01-02", since=None,
                           asset="Asset A", account=None, cascade=False, dry_run=True))
    assert rc == 0
    assert _count(db_file, "transaction_type='Köp'") == 1  # nothing deleted
    assert _asset_amount(db_file) == 100  # unchanged


def test_delete_tx_no_match(tmp_path):
    db_file = _build_db(tmp_path, BASE_CSV)
    rc = cli.delete_tx(_ns(db_file, tx_id=None, date="2020-01-02", since=None,
                           asset="Nonexistent", account=None, cascade=False, dry_run=False, yes=True))
    assert rc == 1


def test_delete_tx_funding_pair_cleanup(tmp_path):
    """Deleting an allocated buy also removes its orphaned funding transfer (#80)."""
    db_file = _build_db(tmp_path, BASE_CSV)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111",
                           starting_cash=None, starting_cash_date=None))
    assert cli.account_allocate(_ns(db_file, tx_date="2020-01-02", tx_asset="Asset A",
                                    to="YOLO", from_account=None, shares=None)) == 0
    assert _count(db_file, "transaction_type='Intern överföring' AND origin='virtual'") >= 2
    rc = cli.delete_tx(_ns(db_file, tx_id=None, date="2020-01-02", since=None,
                           asset="Asset A", account="YOLO", cascade=False, dry_run=False, yes=True))
    assert rc == 0
    assert _count(db_file, "transaction_type='Köp' AND account='YOLO'") == 0
    assert _count(db_file, "transaction_type='Intern överföring' AND origin='virtual'") == 0


def test_delete_tx_cascade(tmp_path):
    """--cascade removes the same date+asset trade across the account family (#80)."""
    db_file = _build_db(tmp_path, BASE_CSV)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111",
                           starting_cash=None, starting_cash_date=None))
    # partial split: 40 shares to YOLO, 60 remain on 1111
    assert cli.account_allocate(_ns(db_file, tx_date="2020-01-02", tx_asset="Asset A",
                                    to="YOLO", from_account=None, shares=40)) == 0
    assert _count(db_file, "transaction_type='Köp'") == 2
    rc = cli.delete_tx(_ns(db_file, tx_id=None, date="2020-01-02", since=None,
                           asset="Asset A", account="1111", cascade=True, dry_run=False, yes=True))
    assert rc == 0
    assert _count(db_file, "transaction_type='Köp'") == 0


def test_delete_tx_refuses_without_yes(tmp_path, monkeypatch):
    """Non-interactive delete-tx without --yes must refuse and delete nothing."""
    import io, sys as _sys
    monkeypatch.setattr(_sys, "stdin", io.StringIO(""))  # not a tty
    db_file = _build_db(tmp_path, BASE_CSV)
    before = _count(db_file, "1=1")
    rc = cli.delete_tx(_ns(db_file, tx_id=None, date="2020-01-02", since=None,
                           asset="Asset A", account=None, cascade=False, dry_run=False))
    assert rc == 1
    assert _count(db_file, "1=1") == before


def test_delete_tx_creates_backup(tmp_path, monkeypatch):
    """delete-tx with --yes writes an automatic pre-delete backup next to the DB."""
    import io, sys as _sys, glob
    monkeypatch.setattr(_sys, "stdin", io.StringIO(""))
    db_file = _build_db(tmp_path, BASE_CSV)
    rc = cli.delete_tx(_ns(db_file, tx_id=None, date="2020-01-02", since=None,
                           asset="Asset A", account=None, cascade=False, dry_run=False, yes=True))
    assert rc == 0
    backups = glob.glob(str(db_file) + ".pre-delete-tx.*.bak")
    assert len(backups) == 1
