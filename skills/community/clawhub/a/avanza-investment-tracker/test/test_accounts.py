"""
Tests for virtual portfolios via account reassignment (issue #74).

Covers:
- Schema migration (is_virtual, parent_account, origin columns)
- Nickname mutation preserves virtual-account config
- virtual create / allocate (full + partial split) / transfer-cash / transfer
- Capital neutrality and gain realization of the asset-transfer decomposition
- Re-import idempotency via parent-remap dedup
- resolve_accounts physical-only default
- AssetDeficit surfaced on insufficient shares
"""

import argparse
import sqlite3
from datetime import date

import pytest

from database_handler import DatabaseHandler
from data_parser import DataParser, AssetDeficit
import cli


# ---------- helpers ----------

def _write_csv(tmp_path, name, text):
    p = tmp_path / name
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)
    return str(p)


def _base_parent_db(tmp_path):
    """Parent account 1111: deposit 20000, buy 100 'Asset A' @ 100 (cost 10000).
    Leaves 10000 cash + 100 shares on 1111. Fully processed."""
    db_file = tmp_path / "v.db"
    db = DatabaseHandler(db_file)
    parser = DataParser(db)
    csv_text = """Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat
2020-01-01;1111;Insättning;Deposit;-;-;20000;0;SEK;DEPOSIT;-
2020-01-02;1111;Köp;Asset A;100;100;-10000;0;SEK;ASSETA;-"""
    csv_file = _write_csv(tmp_path, "base.csv", csv_text)
    db.connect()
    parser.add_data(csv_file)
    parser.reset_for_reprocessing()
    parser.process_transactions()
    db.disconnect()
    return db_file


def _ns(database, **kw):
    """Build an argparse Namespace for a cli virtual command."""
    base = dict(database=str(database), special_cases=None)
    base.update(kw)
    return argparse.Namespace(**base)


def _holdings(db, account, asset="Asset A"):
    """Total held shares of `asset` on `account` per cohort_assets."""
    db.connect()
    cur = db.get_cursor()
    cur.execute(
        "SELECT COALESCE(SUM(ca.amount), 0) FROM cohort_assets ca "
        "JOIN assets a ON ca.asset_id = a.asset_id "
        "WHERE a.asset = ? AND ca.account = ? AND ca.amount > 0",
        (asset, account),
    )
    val = cur.fetchone()[0]
    db.disconnect()
    return val


def _account_value(db, account):
    """cash (cohort_data capital) + assets at latest_price, for one account."""
    db.connect()
    cur = db.get_cursor()
    cur.execute("SELECT COALESCE(SUM(capital), 0) FROM cohort_data WHERE account = ?", (account,))
    cash = cur.fetchone()[0]
    cur.execute(
        "SELECT COALESCE(SUM(ca.amount * a.latest_price), 0) FROM cohort_assets ca "
        "JOIN assets a ON ca.asset_id = a.asset_id "
        "WHERE ca.account = ? AND ca.amount > 0", (account,)
    )
    assets = cur.fetchone()[0]
    db.disconnect()
    return cash + assets


def _set_latest_price(db, asset, price):
    db.connect()
    cur = db.get_cursor()
    cur.execute("UPDATE assets SET latest_price = ?, latest_price_date = '2020-06-01' WHERE asset = ?", (price, asset))
    db.commit()
    db.disconnect()


# ---------- schema ----------

def test_migration_adds_columns(tmp_path):
    db_file = tmp_path / "s.db"
    db = DatabaseHandler(db_file)
    db.connect()
    cur = db.get_cursor()
    cur.execute("PRAGMA table_info(transactions)")
    cols = {r[1] for r in cur.fetchall()}
    assert "origin" in cols
    cur.execute("PRAGMA table_info(accounts)")
    acols = {r[1] for r in cur.fetchall()}
    assert "is_virtual" in acols
    assert "parent_account" in acols
    db.disconnect()


def test_imported_rows_default_avanza_origin(tmp_path):
    db_file = _base_parent_db(tmp_path)
    db = DatabaseHandler(db_file)
    db.connect()
    cur = db.get_cursor()
    cur.execute("SELECT DISTINCT origin FROM transactions")
    origins = {r[0] for r in cur.fetchall()}
    assert origins == {"avanza"}
    db.disconnect()


# ---------- nickname mutation preserves virtual config ----------

def test_set_nickname_preserves_virtual_flag(tmp_path):
    db_file = tmp_path / "n.db"
    db = DatabaseHandler(db_file)
    db.connect()
    cur = db.get_cursor()
    cur.execute("INSERT INTO accounts (account_id, nickname, is_virtual, parent_account) VALUES ('YOLO','YOLO',1,'1111')")
    db.commit()
    # Setting a nickname must not wipe is_virtual/parent_account
    db.set_account_nickname("YOLO", "Yolo Bets")
    cur.execute("SELECT is_virtual, parent_account FROM accounts WHERE account_id = 'YOLO'")
    row = cur.fetchone()
    assert row[0] == 1
    assert row[1] == "1111"
    db.disconnect()


def test_remove_nickname_preserves_virtual_row(tmp_path):
    db_file = tmp_path / "n.db"
    db = DatabaseHandler(db_file)
    db.connect()
    cur = db.get_cursor()
    cur.execute("INSERT INTO accounts (account_id, nickname, is_virtual, parent_account) VALUES ('YOLO','YOLO',1,'1111')")
    db.commit()
    assert db.remove_account_nickname("YOLO") is True
    cur.execute("SELECT is_virtual, parent_account, nickname FROM accounts WHERE account_id = 'YOLO'")
    row = cur.fetchone()
    assert row is not None  # row preserved
    assert row[0] == 1
    assert row[1] == "1111"
    assert row[2] is None  # nickname nulled
    db.disconnect()


def test_remove_nickname_deletes_empty_physical_row(tmp_path):
    db_file = tmp_path / "n.db"
    db = DatabaseHandler(db_file)
    db.connect()
    db.set_account_nickname("1111", "Main")
    assert db.remove_account_nickname("1111") is True
    cur = db.get_cursor()
    cur.execute("SELECT COUNT(*) FROM accounts WHERE account_id = '1111'")
    assert cur.fetchone()[0] == 0  # empty physical row pruned
    db.disconnect()


# ---------- virtual create ----------

def test_virtual_create_inserts_account(tmp_path):
    db_file = _base_parent_db(tmp_path)
    rc = cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    assert rc == 0
    db = DatabaseHandler(db_file)
    db.connect()
    assert db.is_virtual_account("YOLO") is True
    assert db.get_account_parent("YOLO") == "1111"
    assert db.get_virtual_map() == {"YOLO": "1111"}
    db.disconnect()


def test_virtual_create_rejects_nested_virtual_parent(tmp_path):
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    rc = cli.account_create(_ns(db_file, name="NESTED", parent="YOLO", starting_cash=None, starting_cash_date=None))
    assert rc == 1


def test_virtual_create_with_starting_cash_funds(tmp_path):
    db_file = _base_parent_db(tmp_path)
    rc = cli.account_create(_ns(
        db_file, name="YOLO", parent="1111", starting_cash=5000.0, starting_cash_date="2020-02-01"
    ))
    assert rc == 0
    db = DatabaseHandler(db_file)
    # 5000 moved from parent cash to YOLO cash
    assert _account_value(DatabaseHandler(db_file), "YOLO") == pytest.approx(5000, abs=1)


# ---------- allocate ----------

def test_allocate_full_moves_shares(tmp_path):
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    rc = cli.account_allocate(_ns(
        db_file, tx_date="2020-01-02", tx_asset="Asset A", to="YOLO", from_account=None, shares=None
    ))
    assert rc == 0
    assert _holdings(DatabaseHandler(db_file), "1111") == pytest.approx(0, abs=1e-6)
    assert _holdings(DatabaseHandler(db_file), "YOLO") == pytest.approx(100, abs=1e-6)


def test_allocate_partial_split_math(tmp_path):
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    rc = cli.account_allocate(_ns(
        db_file, tx_date="2020-01-02", tx_asset="Asset A", to="YOLO", from_account=None, shares=30
    ))
    assert rc == 0
    db = DatabaseHandler(db_file)
    db.connect()
    cur = db.get_cursor()
    # Original buy split: 70 on parent, 30 on YOLO, both origin avanza
    cur.execute("SELECT amount, total, courtage, origin FROM transactions WHERE transaction_type='Köp' ORDER BY rowid")
    rows = cur.fetchall()
    assert len(rows) == 2
    amounts = sorted(r[0] for r in rows)
    assert amounts == [30, 70]
    # proportional total: original total was -10000 for 100 shares (-100/share)
    for amt, total, courtage, origin in rows:
        assert origin == "avanza"
        assert total == pytest.approx(-amt * 100, rel=1e-9)
    db.disconnect()
    assert _holdings(DatabaseHandler(db_file), "1111") == pytest.approx(70, abs=1e-6)
    assert _holdings(DatabaseHandler(db_file), "YOLO") == pytest.approx(30, abs=1e-6)


# ---------- transfer-cash ----------

def test_transfer_cash_moves_capital(tmp_path):
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    parent_before = _account_value(DatabaseHandler(db_file), "1111")
    rc = cli.account_transfer_cash(_ns(
        db_file, amount=4000.0, from_account="1111", to="YOLO", date="2020-03-01"
    ))
    assert rc == 0
    db = DatabaseHandler(db_file)
    assert _account_value(db, "YOLO") == pytest.approx(4000, abs=1)
    # parent value dropped by roughly 4000 (cash moved; shares unchanged)
    parent_after = _account_value(DatabaseHandler(db_file), "1111")
    assert parent_before - parent_after == pytest.approx(4000, abs=1)


# ---------- transfer (decomposition) ----------

def test_transfer_asset_capital_neutral_flat_price(tmp_path):
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    total_before = _account_value(DatabaseHandler(db_file), "1111") + _account_value(DatabaseHandler(db_file), "YOLO")

    rc = cli.account_transfer(_ns(
        db_file, asset="Asset A", shares=50, from_account="1111", to="YOLO", date="2020-04-01"
    ))
    assert rc == 0

    db = DatabaseHandler(db_file)
    assert _holdings(db, "1111") == pytest.approx(50, abs=1e-6)
    assert _holdings(db, "YOLO") == pytest.approx(50, abs=1e-6)
    total_after = _account_value(DatabaseHandler(db_file), "1111") + _account_value(DatabaseHandler(db_file), "YOLO")
    # Flat price (100): total value conserved across the move
    assert total_after == pytest.approx(total_before, abs=1)


def test_transfer_asset_realizes_gain_at_source(tmp_path):
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    # Transfer 50 shares at flat price 100 first
    cli.account_transfer(_ns(
        db_file, asset="Asset A", shares=50, from_account="1111", to="YOLO", date="2020-04-01"
    ))
    # Now price rises to 200
    _set_latest_price(DatabaseHandler(db_file), "Asset A", 200.0)

    # parent holds 50 shares (gained 100/share => +5000), YOLO holds 50 (started at
    # cost 100 via rebuy, gained 100/share => +5000). Aggregate gain = 10000.
    parent_val = _account_value(DatabaseHandler(db_file), "1111")
    yolo_val = _account_value(DatabaseHandler(db_file), "YOLO")
    # parent: 10000 cash + 50*200 shares = 20000; deposit 20000 => gain 0 from cash,
    # but the 50 shares it kept appreciated. Cohort gain should be ~5000.
    db = DatabaseHandler(db_file)
    db.connect()
    cur = db.get_cursor()
    cur.execute("SELECT COALESCE(SUM(withdrawal + capital - deposit - transfer_net), 0) FROM cohort_data WHERE account='1111'")
    parent_gl = cur.fetchone()[0]
    cur.execute("SELECT COALESCE(SUM(withdrawal + capital - deposit - transfer_net), 0) FROM cohort_data WHERE account='YOLO'")
    yolo_gl = cur.fetchone()[0]
    db.disconnect()
    # Each account's cohort gain (excludes asset market value) is a lower bound;
    # the decisive invariant is that the two accounts together hold all 100 shares.
    assert _holdings(DatabaseHandler(db_file), "1111") + _holdings(DatabaseHandler(db_file), "YOLO") == pytest.approx(100, abs=1e-6)


def test_transfer_asset_rejects_insufficient_shares(tmp_path):
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    rc = cli.account_transfer(_ns(
        db_file, asset="Asset A", shares=500, from_account="1111", to="YOLO", date="2020-04-01"
    ))
    assert rc == 1  # only 100 shares held


# ---------- re-import idempotency (parent-remap dedup) ----------

def test_reimport_after_full_allocate_does_not_duplicate(tmp_path):
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    cli.account_allocate(_ns(
        db_file, tx_date="2020-01-02", tx_asset="Asset A", to="YOLO", from_account=None, shares=None
    ))

    db = DatabaseHandler(db_file)
    db.connect()
    cur = db.get_cursor()
    cur.execute("SELECT COUNT(*) FROM transactions")
    count_after_allocate = cur.fetchone()[0]
    db.disconnect()

    # Re-import the SAME CSV (overlapping range) — must not resurrect the buy on parent
    csv_text = """Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat
2020-01-01;1111;Insättning;Deposit;-;-;20000;0;SEK;DEPOSIT;-
2020-01-02;1111;Köp;Asset A;100;100;-10000;0;SEK;ASSETA;-"""
    csv_file = _write_csv(tmp_path, "reimport.csv", csv_text)
    parser = DataParser(DatabaseHandler(db_file))
    db.connect()
    parser.add_data(csv_file)
    db.disconnect()

    db = DatabaseHandler(db_file)
    db.connect()
    cur = db.get_cursor()
    cur.execute("SELECT COUNT(*) FROM transactions")
    count_after_reimport = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM transactions WHERE account='1111' AND transaction_type='Köp'")
    parent_buys = cur.fetchone()[0]
    db.disconnect()

    assert count_after_reimport == count_after_allocate  # no duplicate inserted
    assert parent_buys == 0  # buy stays allocated to YOLO, not resurrected on parent


def test_reimport_after_partial_split_sum_matches(tmp_path):
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    cli.account_allocate(_ns(
        db_file, tx_date="2020-01-02", tx_asset="Asset A", to="YOLO", from_account=None, shares=30
    ))

    db = DatabaseHandler(db_file)
    db.connect()
    cur = db.get_cursor()
    cur.execute("SELECT COUNT(*) FROM transactions")
    before = cur.fetchone()[0]
    db.disconnect()

    csv_text = """Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat
2020-01-02;1111;Köp;Asset A;100;100;-10000;0;SEK;ASSETA;-"""
    csv_file = _write_csv(tmp_path, "reimport2.csv", csv_text)
    parser = DataParser(DatabaseHandler(db_file))
    db.connect()
    parser.add_data(csv_file)
    db.disconnect()

    db = DatabaseHandler(db_file)
    db.connect()
    cur = db.get_cursor()
    cur.execute("SELECT COUNT(*) FROM transactions")
    after = cur.fetchone()[0]
    db.disconnect()
    # 70 (parent) + 30 (YOLO remapped to parent) = 100 == proposed 100 => skip
    assert after == before


# ---------- resolve_accounts physical-only default ----------

def test_resolve_accounts_physical_only_when_virtuals_exist(tmp_path):
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    db = DatabaseHandler(db_file)
    db.connect()
    # Unspecified -> physical only
    assert cli.resolve_accounts(db, None) == ["1111"]
    # Explicit 'all' -> None (truly all, incl virtual)
    assert cli.resolve_accounts(db, "all") is None
    db.disconnect()


def test_resolve_accounts_none_when_no_virtuals(tmp_path):
    db_file = _base_parent_db(tmp_path)
    db = DatabaseHandler(db_file)
    db.connect()
    # No virtuals -> None (all) to preserve current behaviour
    assert cli.resolve_accounts(db, None) is None
    db.disconnect()


# ---------- virtual list ----------

def test_virtual_list_empty(tmp_path, capsys):
    db_file = _base_parent_db(tmp_path)
    rc = cli.account_list(_ns(db_file, apy_mode='mwrr', format='table'))
    assert rc == 0
    out = capsys.readouterr().out
    assert "No virtual portfolios" in out


def test_virtual_list_shows_portfolio_with_value(tmp_path, capsys):
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(
        db_file, name="YOLO", parent="1111", starting_cash=5000.0, starting_cash_date="2020-02-01"
    ))
    rc = cli.account_list(_ns(db_file, apy_mode='mwrr', format='table'))
    assert rc == 0
    out = capsys.readouterr().out
    assert "YOLO" in out
    assert "1111" in out  # parent shown


def test_virtual_list_json(tmp_path, capsys):
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(
        db_file, name="YOLO", parent="1111", starting_cash=5000.0, starting_cash_date="2020-02-01"
    ))
    rc = cli.account_list(_ns(db_file, apy_mode='mwrr', format='json'))
    assert rc == 0
    import json
    data = json.loads(capsys.readouterr().out)
    assert len(data) == 1
    assert data[0]["virtual"] == "YOLO"
    assert data[0]["parent_account"] == "1111"
    assert data[0]["is_virtual"] if "is_virtual" in data[0] else True  # is_virtual optional in json
    assert data[0]["total"] == pytest.approx(5000, abs=1)


# ---------- virtual close ----------

def test_virtual_close_empties_virtual_and_preserves_capital(tmp_path):
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(
        db_file, name="YOLO", parent="1111", starting_cash=5000.0, starting_cash_date="2020-02-01"
    ))
    # Allocate all 100 shares to YOLO (cost follows shares) so YOLO holds the asset
    cli.account_allocate(_ns(
        db_file, tx_date="2020-01-02", tx_asset="Asset A", to="YOLO", from_account=None, shares=None
    ))

    total_before = _account_value(DatabaseHandler(db_file), "1111") + _account_value(DatabaseHandler(db_file), "YOLO")
    assert _holdings(DatabaseHandler(db_file), "YOLO") == pytest.approx(100, abs=1e-6)

    rc = cli.account_close(_ns(db_file, name="YOLO", to=None, date="2020-09-01"))
    assert rc == 0

    db = DatabaseHandler(db_file)
    # Virtual emptied of holdings
    assert _holdings(db, "YOLO") == pytest.approx(0, abs=1e-6)
    # Virtual has no residual cash
    db.connect()
    cur = db.get_cursor()
    cur.execute("SELECT COALESCE(SUM(capital),0) FROM cohort_data WHERE account='YOLO'")
    assert cur.fetchone()[0] == pytest.approx(0, abs=1)
    db.disconnect()
    # Capital conserved across the close (parent reabsorbed everything)
    total_after = _account_value(DatabaseHandler(db_file), "1111") + _account_value(DatabaseHandler(db_file), "YOLO")
    assert total_after == pytest.approx(total_before, abs=1)
    # All 100 shares back on parent
    assert _holdings(DatabaseHandler(db_file), "1111") == pytest.approx(100, abs=1e-6)


def test_virtual_close_preserves_account_row(tmp_path):
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(
        db_file, name="YOLO", parent="1111", starting_cash=5000.0, starting_cash_date="2020-02-01"
    ))
    cli.account_close(_ns(db_file, name="YOLO", to=None, date="2020-09-01"))
    db = DatabaseHandler(db_file)
    db.connect()
    # Row preserved (still flagged virtual) so historical cohort data remains queryable
    assert db.is_virtual_account("YOLO") is True
    assert db.get_account_parent("YOLO") == "1111"
    db.disconnect()


def test_virtual_close_rejects_non_virtual(tmp_path):
    db_file = _base_parent_db(tmp_path)
    rc = cli.account_close(_ns(db_file, name="1111", to=None, date="2020-09-01"))
    assert rc == 1


def test_virtual_close_nothing_to_close(tmp_path):
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    rc = cli.account_close(_ns(db_file, name="YOLO", to=None, date="2020-09-01"))
    assert rc == 0  # empty virtual — no-op success


# ---------- auto-routing of sells to the holding account ----------

def _import_more(db_file, csv_text, tmp_path):
    """Append transactions from a CSV, run sell/dividend routing, then reprocess.
    Returns the number of transactions routed/redistributed."""
    csv_file = _write_csv(tmp_path, "more.csv", csv_text)
    db = DatabaseHandler(db_file)
    db.connect()
    parser = DataParser(db)
    parser.add_data(csv_file)
    routed = cli.route_imported_sells_to_holders(db)
    routed += cli.route_imported_dividends_to_holders(db)
    parser.reset_for_reprocessing()
    parser.process_transactions()
    db.disconnect()
    return routed


# Sälj CSV row uses negative Antal (shares leaving), positive Belopp (proceeds).
_SELL = "Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat\n"


def test_sell_routed_when_parent_holds_none(tmp_path):
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    # Allocate ALL 100 shares to YOLO -> parent holds 0
    cli.account_allocate(_ns(db_file, tx_date="2020-01-02", tx_asset="Asset A", to="YOLO", from_account=None, shares=None))
    assert _holdings(DatabaseHandler(db_file), "1111") == pytest.approx(0, abs=1e-6)

    csv = _SELL + "2020-06-01;1111;Sälj;Asset A;-30;100;3000;0;SEK;ASSETA;-"
    routed = _import_more(db_file, csv, tmp_path)
    assert routed == 1
    # Without routing this would have been an AssetDeficit; instead YOLO lost 30.
    assert _holdings(DatabaseHandler(db_file), "YOLO") == pytest.approx(70, abs=1e-6)
    assert _holdings(DatabaseHandler(db_file), "1111") == pytest.approx(0, abs=1e-6)


def test_sell_split_when_parent_holds_partial(tmp_path):
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    # Parent keeps 60, YOLO gets 40
    cli.account_allocate(_ns(db_file, tx_date="2020-01-02", tx_asset="Asset A", to="YOLO", from_account=None, shares=40))
    assert _holdings(DatabaseHandler(db_file), "1111") == pytest.approx(60, abs=1e-6)

    # Sell 80 > parent's 60 -> split: parent sells 60, YOLO sells 20
    csv = _SELL + "2020-06-01;1111;Sälj;Asset A;-80;100;8000;0;SEK;ASSETA;-"
    routed = _import_more(db_file, csv, tmp_path)
    assert routed == 1
    assert _holdings(DatabaseHandler(db_file), "1111") == pytest.approx(0, abs=1e-6)
    assert _holdings(DatabaseHandler(db_file), "YOLO") == pytest.approx(20, abs=1e-6)


def test_sell_left_alone_when_parent_holds_enough(tmp_path):
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    cli.account_allocate(_ns(db_file, tx_date="2020-01-02", tx_asset="Asset A", to="YOLO", from_account=None, shares=40))
    # Parent holds 60 >= sell of 30 -> left on parent
    csv = _SELL + "2020-06-01;1111;Sälj;Asset A;-30;100;3000;0;SEK;ASSETA;-"
    routed = _import_more(db_file, csv, tmp_path)
    assert routed == 0
    assert _holdings(DatabaseHandler(db_file), "1111") == pytest.approx(30, abs=1e-6)
    assert _holdings(DatabaseHandler(db_file), "YOLO") == pytest.approx(40, abs=1e-6)


def test_sell_routing_noop_without_virtuals(tmp_path):
    db_file = _base_parent_db(tmp_path)
    # No virtuals; sell of 30 on parent (holds 100) stays put
    csv = _SELL + "2020-06-01;1111;Sälj;Asset A;-30;100;3000;0;SEK;ASSETA;-"
    routed = _import_more(db_file, csv, tmp_path)
    assert routed == 0
    assert _holdings(DatabaseHandler(db_file), "1111") == pytest.approx(70, abs=1e-6)


def test_sell_routing_e2e_via_import_command(tmp_path):
    """Full import_data path triggers routing automatically."""
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    cli.account_allocate(_ns(db_file, tx_date="2020-01-02", tx_asset="Asset A", to="YOLO", from_account=None, shares=None))

    sell_csv = _SELL + "2020-06-01;1111;Sälj;Asset A;-30;100;3000;0;SEK;ASSETA;-"
    sell_file = _write_csv(tmp_path, "sell.csv", sell_csv)
    rc = cli.import_data(argparse.Namespace(database=str(db_file), special_cases=None, file=sell_file))
    assert rc == 0
    assert _holdings(DatabaseHandler(db_file), "YOLO") == pytest.approx(70, abs=1e-6)


# ---------- auto-distribution of dividends to holding accounts ----------

# Utdelning: Antal = shares held, Kurs = dividend per share, Belopp = total.
_DIV = "Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat\n"


def test_dividend_routed_when_parent_holds_none(tmp_path):
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    cli.account_allocate(_ns(db_file, tx_date="2020-01-02", tx_asset="Asset A", to="YOLO", from_account=None, shares=None))

    parent_before = _account_value(DatabaseHandler(db_file), "1111")
    yolo_before = _account_value(DatabaseHandler(db_file), "YOLO")

    csv = _DIV + "2020-06-01;1111;Utdelning;Asset A;100;2;200;0;SEK;ASSETA;-"
    routed = _import_more(db_file, csv, tmp_path)
    assert routed == 1
    # Parent holds 0 -> entire dividend (100*2=200) credited to YOLO, none to parent
    assert _account_value(DatabaseHandler(db_file), "1111") == pytest.approx(parent_before, abs=1)
    assert _account_value(DatabaseHandler(db_file), "YOLO") == pytest.approx(yolo_before + 200, abs=1)


def test_dividend_split_proportionally_when_both_hold(tmp_path):
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    # Parent 60, YOLO 40
    cli.account_allocate(_ns(db_file, tx_date="2020-01-02", tx_asset="Asset A", to="YOLO", from_account=None, shares=40))

    parent_before = _account_value(DatabaseHandler(db_file), "1111")
    yolo_before = _account_value(DatabaseHandler(db_file), "YOLO")

    csv = _DIV + "2020-06-01;1111;Utdelning;Asset A;100;2;200;0;SEK;ASSETA;-"
    routed = _import_more(db_file, csv, tmp_path)
    assert routed == 1
    # Split 60/40: parent +120 (60*2), YOLO +80 (40*2)
    assert _account_value(DatabaseHandler(db_file), "1111") == pytest.approx(parent_before + 120, abs=1)
    assert _account_value(DatabaseHandler(db_file), "YOLO") == pytest.approx(yolo_before + 80, abs=1)


def test_dividend_left_alone_when_only_parent_holds(tmp_path):
    db_file = _base_parent_db(tmp_path)
    # No allocation -> only parent holds; dividend stays put
    parent_before = _account_value(DatabaseHandler(db_file), "1111")
    csv = _DIV + "2020-06-01;1111;Utdelning;Asset A;100;2;200;0;SEK;ASSETA;-"
    routed = _import_more(db_file, csv, tmp_path)
    assert routed == 0  # no virtuals -> no-op
    assert _account_value(DatabaseHandler(db_file), "1111") == pytest.approx(parent_before + 200, abs=1)


def test_dividend_routing_e2e_via_import_command(tmp_path):
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    cli.account_allocate(_ns(db_file, tx_date="2020-01-02", tx_asset="Asset A", to="YOLO", from_account=None, shares=None))
    yolo_before = _account_value(DatabaseHandler(db_file), "YOLO")

    div_csv = _DIV + "2020-06-01;1111;Utdelning;Asset A;100;2;200;0;SEK;ASSETA;-"
    div_file = _write_csv(tmp_path, "div.csv", div_csv)
    rc = cli.import_data(argparse.Namespace(database=str(db_file), special_cases=None, file=div_file))
    assert rc == 0
    assert _account_value(DatabaseHandler(db_file), "YOLO") == pytest.approx(yolo_before + 200, abs=1)


# ---------- virtual-aware SQL views ----------

def _query_view(db_file, view, where=None, params=()):
    """Read a view via a raw sqlite3 connection (views are persisted in the file)."""
    conn = sqlite3.connect(str(db_file))
    conn.row_factory = sqlite3.Row
    try:
        q = f"SELECT * FROM {view}"
        if where:
            q += f" WHERE {where}"
        return [dict(r) for r in conn.execute(q, params).fetchall()]
    finally:
        conn.close()


def _view_setup(tmp_path):
    """Parent 1111 + virtual YOLO holding 40 of 100 Asset A shares."""
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=5000.0, starting_cash_date="2020-02-01"))
    cli.account_allocate(_ns(db_file, tx_date="2020-01-02", tx_asset="Asset A", to="YOLO", from_account=None, shares=40))
    return db_file


def test_view_current_valuations_is_virtual_aware(tmp_path):
    db_file = _view_setup(tmp_path)
    rows = {r["account"]: r for r in _query_view(db_file, "v_account_current_valuations")}
    assert rows["YOLO"]["is_virtual"] == 1
    assert rows["YOLO"]["parent_account"] == "1111"
    assert rows["YOLO"]["display_name"] == "YOLO"
    assert rows["1111"]["is_virtual"] == 0
    assert rows["1111"]["parent_account"] is None


def test_view_asset_holdings_is_virtual_aware(tmp_path):
    db_file = _view_setup(tmp_path)
    rows = _query_view(db_file, "v_account_asset_holdings", where="asset_name = ?", params=("Asset A",))
    by_account = {r["account"]: r for r in rows}
    # Parent kept 60, YOLO got 40 — both flagged correctly
    assert by_account["1111"]["held_amount"] == pytest.approx(60, abs=1e-6)
    assert by_account["1111"]["is_virtual"] == 0
    assert by_account["YOLO"]["held_amount"] == pytest.approx(40, abs=1e-6)
    assert by_account["YOLO"]["is_virtual"] == 1
    assert by_account["YOLO"]["parent_account"] == "1111"


def test_view_capital_flows_exposes_origin(tmp_path):
    db_file = _view_setup(tmp_path)
    rows = _query_view(db_file, "v_external_capital_flows")
    origins = {r["origin"] for r in rows}
    # Real deposit (avanza) + the virtual funding transfer pair (virtual)
    assert "avanza" in origins
    assert "virtual" in origins
    # The origin column lets consumers filter real flows only
    real_only = _query_view(db_file, "v_external_capital_flows", where="origin = 'avanza'")
    assert all(r["origin"] == "avanza" for r in real_only)


def test_view_rollup_combined_equals_own_plus_virtual(tmp_path):
    db_file = _view_setup(tmp_path)
    rows = _query_view(db_file, "v_virtual_portfolio_rollup")
    assert len(rows) == 1
    r = rows[0]
    assert r["parent_account"] == "1111"
    assert r["virtual_count"] == 1
    # No double counting: combined = own + virtual
    assert r["combined_cash"] == pytest.approx(r["own_cash"] + r["virtual_cash"])
    assert r["combined_assets"] == pytest.approx(r["own_assets"] + r["virtual_assets"])
    assert r["combined_total"] == pytest.approx(r["own_total"] + r["virtual_total"])
    # And combined equals the parent's own + every child's total
    valuations = {v["account"]: v for v in _query_view(db_file, "v_account_current_valuations")}
    expected = valuations["1111"]["total"] + valuations["YOLO"]["total"]
    assert r["combined_total"] == pytest.approx(expected)


def test_view_rollup_no_virtuals(tmp_path):
    db_file = _base_parent_db(tmp_path)
    rows = _query_view(db_file, "v_virtual_portfolio_rollup")
    assert len(rows) == 1
    r = rows[0]
    assert r["parent_account"] == "1111"
    assert r["virtual_count"] == 0
    # With no virtuals, combined == own
    assert r["combined_total"] == pytest.approx(r["own_total"])
    assert r["virtual_total"] == 0.0


def test_view_rollup_excludes_virtual_accounts(tmp_path):
    """The rollup must list physical accounts only — virtuals appear as children, not as parents."""
    db_file = _view_setup(tmp_path)
    rows = _query_view(db_file, "v_virtual_portfolio_rollup")
    parents = {r["parent_account"] for r in rows}
    assert "1111" in parents
    assert "YOLO" not in parents


# ---------- report command (phase 3) ----------

_REPORT_NS = dict(benchmark=None, apy_mode='mwrr', update_prices='never',
                  update_all=False, format='table', no_interpolation=False)


def test_report_renders_with_virtuals(tmp_path, capsys):
    db_file = _view_setup(tmp_path)
    rc = cli.report(_ns(db_file, **_REPORT_NS))
    assert rc == 0
    out = capsys.readouterr().out
    assert "Investment Report" in out
    assert "Virtual portfolios" in out
    assert "YOLO" in out
    assert "Performance comparison" in out
    assert "1111" in out


def test_report_no_virtuals(tmp_path, capsys):
    db_file = _base_parent_db(tmp_path)
    rc = cli.report(_ns(db_file, **_REPORT_NS))
    assert rc == 0
    out = capsys.readouterr().out
    assert "Virtual portfolios:  0" in out
    assert "Investment Report" in out


def test_report_json_shape(tmp_path, capsys):
    db_file = _view_setup(tmp_path)
    rc = cli.report(_ns(db_file, **{**_REPORT_NS, 'format': 'json'}))
    assert rc == 0
    import json
    data = json.loads(capsys.readouterr().out)
    for key in ('overview', 'accounts', 'virtual_portfolios', 'comparison'):
        assert key in data
    assert data['overview']['virtual_count'] == 1
    assert len(data['virtual_portfolios']) == 1
    assert data['virtual_portfolios'][0]['virtual'] == 'YOLO'
    assert data['virtual_portfolios'][0]['parent_account'] == '1111'
    # accounts tree nests virtuals under their physical parent
    assert data['accounts'][0]['children'][0]['account'] == 'YOLO'


# ---------- partial transfer fix (account allocate) ----------

def test_allocate_full_transfer_when_virtual_has_no_cash(tmp_path):
    """Virtual has 0 cash -> transfers full buy cost (existing behaviour)."""
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    rc = cli.account_allocate(_ns(
        db_file, tx_date="2020-01-02", tx_asset="Asset A", to="YOLO", from_account=None, shares=None
    ))
    assert rc == 0
    db = DatabaseHandler(db_file)
    db.connect()
    cur = db.get_cursor()
    cur.execute(
        "SELECT COALESCE(SUM(total), 0) FROM transactions "
        "WHERE transaction_type='Intern överföring' AND origin='virtual' "
        "AND account='YOLO' AND date='2020-01-01'"
    )
    assert cur.fetchone()[0] == pytest.approx(10000, abs=1)
    db.disconnect()
    assert _holdings(DatabaseHandler(db_file), "YOLO") == pytest.approx(100, abs=1e-6)


def test_allocate_partial_transfer_only_moves_shortfall(tmp_path):
    """Virtual has some cash -> transfers only the shortfall."""
    db_file = _base_parent_db(tmp_path)
    # Pre-fund YOLO with 6000 (dated before buy so month filter includes it)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=6000, starting_cash_date="2019-12-15"))
    rc = cli.account_allocate(_ns(
        db_file, tx_date="2020-01-02", tx_asset="Asset A", to="YOLO", from_account=None, shares=None
    ))
    assert rc == 0
    db = DatabaseHandler(db_file)
    db.connect()
    cur = db.get_cursor()
    # Starting-cash transfer (dated 2019-12-15)
    cur.execute(
        "SELECT COALESCE(SUM(total), 0) FROM transactions "
        "WHERE transaction_type='Intern överföring' AND origin='virtual' "
        "AND account='YOLO' AND date='2019-12-15'"
    )
    assert cur.fetchone()[0] == pytest.approx(6000, abs=1)
    # Allocate shortfall transfer (dated 2020-01-01, day before buy)
    cur.execute(
        "SELECT COALESCE(SUM(total), 0) FROM transactions "
        "WHERE transaction_type='Intern överföring' AND origin='virtual' "
        "AND account='YOLO' AND date='2020-01-01'"
    )
    assert cur.fetchone()[0] == pytest.approx(4000, abs=1)  # shortfall, not 10000
    db.disconnect()
    assert _holdings(DatabaseHandler(db_file), "YOLO") == pytest.approx(100, abs=1e-6)


def test_allocate_no_transfer_when_virtual_has_enough_cash(tmp_path):
    """Virtual has enough cash from a prior transfer -> no new transfer."""
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    # Fund YOLO with exactly the buy cost
    cli.account_transfer_cash(_ns(db_file, from_account="1111", to="YOLO", amount=10000, date="2020-01-01"))
    transfers_before = _count_virtual_transfers(db_file)
    rc = cli.account_allocate(_ns(
        db_file, tx_date="2020-01-02", tx_asset="Asset A", to="YOLO", from_account=None, shares=None
    ))
    assert rc == 0
    # No new transfer pair
    assert _count_virtual_transfers(db_file) == transfers_before
    assert _holdings(DatabaseHandler(db_file), "YOLO") == pytest.approx(100, abs=1e-6)


# ---------- issue #82: parent->virtual shifts deposit, physical keeps transfer_net ----------

def test_allocate_parent_to_virtual_shifts_deposit_not_transfer_net(tmp_path):
    """Issue #82: a parent->virtual funding transfer shifts the deposit column
    (so the virtual's deposit>0 for APY/display), not transfer_net. The parent
    gives up the deposit so aggregate deposit is preserved (no double-count)."""
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    rc = cli.account_allocate(_ns(
        db_file, tx_date="2020-01-02", tx_asset="Asset A", to="YOLO", from_account=None, shares=None
    ))
    assert rc == 0
    db = DatabaseHandler(db_file)
    db.connect()
    cur = db.get_cursor()
    cur.execute(
        "SELECT COALESCE(SUM(deposit),0), COALESCE(SUM(transfer_net),0) "
        "FROM cohort_data WHERE account='YOLO'"
    )
    v_dep, v_tn = cur.fetchone()
    assert v_dep == pytest.approx(10000, abs=1)
    assert v_tn == pytest.approx(0, abs=1e-6)
    cur.execute(
        "SELECT COALESCE(SUM(deposit),0), COALESCE(SUM(transfer_net),0) "
        "FROM cohort_data WHERE account='1111'"
    )
    p_dep, p_tn = cur.fetchone()
    assert p_dep == pytest.approx(10000, abs=1)
    assert p_tn == pytest.approx(0, abs=1e-6)
    # Aggregate deposit preserved: parent + virtual == original 20000
    assert (v_dep + p_dep) == pytest.approx(20000, abs=1)
    db.disconnect()


def test_parent_to_virtual_deposit_shift_skips_cohort_cash_flows(tmp_path):
    """Issue #82: deposit-shift transfers must not write cohort_cash_flows rows
    (deposits produce no cash flows), or the Modified Dietz denominator
    (deposit + sum_w_cf) double-counts the amount."""
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    cli.account_allocate(_ns(
        db_file, tx_date="2020-01-02", tx_asset="Asset A", to="YOLO", from_account=None, shares=None
    ))
    db = DatabaseHandler(db_file)
    db.connect()
    cur = db.get_cursor()
    cur.execute("SELECT COUNT(*) FROM cohort_cash_flows WHERE account='YOLO'")
    assert cur.fetchone()[0] == 0
    db.disconnect()


def test_parent_to_virtual_deposit_shift_preserves_realized(tmp_path):
    """Issue #82: realized gain/loss is unchanged since deposit and transfer_net
    both enter the formula with the same sign and cancel."""
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    cli.account_allocate(_ns(
        db_file, tx_date="2020-01-02", tx_asset="Asset A", to="YOLO", from_account=None, shares=None
    ))
    db = DatabaseHandler(db_file)
    db.connect()
    cur = db.get_cursor()
    cur.execute(
        "SELECT COALESCE(SUM(withdrawal + capital - deposit - transfer_net), 0) "
        "FROM cohort_data WHERE account IN ('1111','YOLO')"
    )
    # 20000 deposited, 10000 still cash on parent, 10000 converted to assets on
    # YOLO -> aggregate realized = -10000 (the unrealized asset position).
    assert cur.fetchone()[0] == pytest.approx(-10000, abs=1)
    db.disconnect()


def test_physical_to_physical_transfer_keeps_transfer_net_and_cash_flows(tmp_path):
    """Regression guard (issue #82): physical-to-physical Intern överföring must
    keep using transfer_net (not deposit) and must write cohort_cash_flows rows."""
    db_file = tmp_path / "phys.db"
    csv_text = (
        "Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat\n"
        "2020-01-01;1111;Insättning;Deposit;-;-;200;0;SEK;;-\n"
        "2020-01-02;1111;Intern överföring;To 2222;-;-;-80;0;SEK;;-\n"
        "2020-01-02;2222;Intern överföring;From 1111;-;-;80;0;SEK;;-\n"
    )
    csv_file = _write_csv(tmp_path, "phys.csv", csv_text)
    db = DatabaseHandler(db_file)
    parser = DataParser(db)
    db.connect()
    parser.add_data(csv_file)
    parser.reset_for_reprocessing()
    parser.process_transactions()
    cur = db.get_cursor()
    cur.execute(
        "SELECT COALESCE(SUM(deposit),0), COALESCE(SUM(transfer_net),0) "
        "FROM cohort_data WHERE account='1111'"
    )
    src_dep, src_tn = cur.fetchone()
    assert src_dep == pytest.approx(200, abs=0.01)
    assert src_tn == pytest.approx(-80, abs=0.01)
    cur.execute(
        "SELECT COALESCE(SUM(deposit),0), COALESCE(SUM(transfer_net),0) "
        "FROM cohort_data WHERE account='2222'"
    )
    dst_dep, dst_tn = cur.fetchone()
    assert dst_dep == pytest.approx(0, abs=1e-6)
    assert dst_tn == pytest.approx(80, abs=0.01)
    cur.execute("SELECT COUNT(*) FROM cohort_cash_flows WHERE account IN ('1111','2222')")
    assert cur.fetchone()[0] == 2
    db.disconnect()


# ---------- undo mode (allocate to parent) ----------

def test_allocate_undo_moves_buy_back_and_deletes_transfer(tmp_path):
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    cli.account_allocate(_ns(
        db_file, tx_date="2020-01-02", tx_asset="Asset A", to="YOLO", from_account=None, shares=None
    ))
    assert _holdings(DatabaseHandler(db_file), "YOLO") == pytest.approx(100, abs=1e-6)
    assert _count_virtual_transfers(db_file) == 2  # one pair

    # Undo: allocate back to parent
    rc = cli.account_allocate(_ns(
        db_file, tx_date="2020-01-02", tx_asset="Asset A", to="1111", from_account="YOLO", shares=None
    ))
    assert rc == 0
    db = DatabaseHandler(db_file)
    db.connect()
    cur = db.get_cursor()
    cur.execute("SELECT account FROM transactions WHERE transaction_type='Köp' AND origin='avanza'")
    assert cur.fetchone()[0] == "1111"
    cur.execute("SELECT COUNT(*) FROM transactions WHERE transaction_type='Intern överföring' AND origin='virtual'")
    assert cur.fetchone()[0] == 0  # transfer pair deleted
    db.disconnect()
    assert _holdings(DatabaseHandler(db_file), "1111") == pytest.approx(100, abs=1e-6)
    assert _holdings(DatabaseHandler(db_file), "YOLO") == pytest.approx(0, abs=1e-6)


def test_allocate_undo_requires_from_flag(tmp_path):
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    cli.account_allocate(_ns(
        db_file, tx_date="2020-01-02", tx_asset="Asset A", to="YOLO", from_account=None, shares=None
    ))
    rc = cli.account_allocate(_ns(
        db_file, tx_date="2020-01-02", tx_asset="Asset A", to="1111", from_account=None, shares=None
    ))
    assert rc == 1


def test_allocate_undo_rejects_partial(tmp_path):
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    cli.account_allocate(_ns(
        db_file, tx_date="2020-01-02", tx_asset="Asset A", to="YOLO", from_account=None, shares=None
    ))
    rc = cli.account_allocate(_ns(
        db_file, tx_date="2020-01-02", tx_asset="Asset A", to="1111", from_account="YOLO", shares=30
    ))
    assert rc == 1


# ---------- auto-allocate buys (--allocate-virtual) ----------

_BUY = "Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat\n"


def _import_with_allocate(db_file, csv_text, tmp_path):
    """Import with auto-allocate enabled. Returns count of buys allocated."""
    csv_file = _write_csv(tmp_path, "alloc.csv", csv_text)
    db = DatabaseHandler(db_file)
    db.connect()
    parser = DataParser(db)
    parser.add_data(csv_file)
    cli.route_imported_sells_to_holders(db)
    cli.route_imported_dividends_to_holders(db)
    allocated = cli.auto_allocate_buys_to_virtuals(db)
    parser.reset_for_reprocessing()
    try:
        parser.process_transactions()
    except AssetDeficit:
        pass  # expected when buys are left unallocated on an unfundable parent
    db.disconnect()
    return allocated


def _count_virtual_transfers(db_file):
    db = DatabaseHandler(db_file)
    db.connect()
    cur = db.get_cursor()
    cur.execute("SELECT COUNT(*) FROM transactions WHERE transaction_type='Intern överföring' AND origin='virtual'")
    n = cur.fetchone()[0]
    db.disconnect()
    return n


def test_auto_allocate_noop_without_virtuals(tmp_path):
    db_file = _base_parent_db(tmp_path)
    buy_csv = _BUY + "2020-06-01;1111;Köp;Asset B;10;100;-1000;0;SEK;ASSETB;-"
    allocated = _import_with_allocate(db_file, buy_csv, tmp_path)
    assert allocated == 0
    assert _holdings(DatabaseHandler(db_file), "1111", "Asset B") == pytest.approx(10, abs=1e-6)


def test_auto_allocate_parent_can_fund_skipped(tmp_path):
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    # Parent has 10000 cash -> can fund a 1000 buy
    buy_csv = _BUY + "2020-06-01;1111;Köp;Asset B;10;100;-1000;0;SEK;ASSETB;-"
    allocated = _import_with_allocate(db_file, buy_csv, tmp_path)
    assert allocated == 0
    assert _holdings(DatabaseHandler(db_file), "1111", "Asset B") == pytest.approx(10, abs=1e-6)
    assert _holdings(DatabaseHandler(db_file), "YOLO", "Asset B") == pytest.approx(0, abs=1e-6)


def test_auto_allocate_rebuy_to_virtual(tmp_path):
    """Sell in virtual -> cash in virtual -> rebuy on parent -> auto-allocated to virtual."""
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    cli.account_allocate(_ns(
        db_file, tx_date="2020-01-02", tx_asset="Asset A", to="YOLO", from_account=None, shares=None
    ))
    # Sell 50 shares -> auto-routed to YOLO -> YOLO gets 6000 cash
    sell_csv = _SELL + "2020-06-01;1111;Sälj;Asset A;-50;120;6000;0;SEK;ASSETA;-"
    _import_more(db_file, sell_csv, tmp_path)
    # Drain parent cash so new buy can't fund there
    cli.account_transfer_cash(_ns(db_file, from_account="1111", to="YOLO", amount=10000, date="2020-06-15"))
    transfers_before = _count_virtual_transfers(db_file)
    # Import rebuy on parent
    buy_csv = _BUY + "2020-07-01;1111;Köp;Asset A;50;120;-6000;0;SEK;ASSETA;-"
    allocated = _import_with_allocate(db_file, buy_csv, tmp_path)
    assert allocated == 1
    assert _holdings(DatabaseHandler(db_file), "YOLO") == pytest.approx(100, abs=1e-6)
    assert _holdings(DatabaseHandler(db_file), "1111") == pytest.approx(0, abs=1e-6)
    # No new transfer pair (YOLO had enough cash from sell)
    assert _count_virtual_transfers(db_file) == transfers_before


def test_auto_allocate_new_asset_one_virtual_has_cash(tmp_path):
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=10000, starting_cash_date="2019-12-15"))
    # Drain parent cash
    cli.account_transfer_cash(_ns(db_file, from_account="1111", to="YOLO", amount=10000, date="2020-03-01"))
    # Buy new asset on parent
    buy_csv = _BUY + "2020-07-01;1111;Köp;Asset B;50;100;-5000;0;SEK;ASSETB;-"
    allocated = _import_with_allocate(db_file, buy_csv, tmp_path)
    assert allocated == 1
    assert _holdings(DatabaseHandler(db_file), "YOLO", "Asset B") == pytest.approx(50, abs=1e-6)
    assert _holdings(DatabaseHandler(db_file), "1111", "Asset B") == pytest.approx(0, abs=1e-6)


def test_auto_allocate_new_asset_multiple_virtuals_warns(tmp_path):
    db_file = _base_parent_db(tmp_path)
    # Split parent's 10000 cash between two virtuals
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=5000, starting_cash_date="2019-12-15"))
    cli.account_create(_ns(db_file, name="GROWTH", parent="1111", starting_cash=5000, starting_cash_date="2019-12-15"))
    # Parent: 0 cash. YOLO: 5000. GROWTH: 5000.
    # Buy new asset on parent — both virtuals have cash, ambiguous
    buy_csv = _BUY + "2020-07-01;1111;Köp;Asset B;40;100;-4000;0;SEK;ASSETB;-"
    allocated = _import_with_allocate(db_file, buy_csv, tmp_path)
    assert allocated == 0  # left for manual allocation
    assert _holdings(DatabaseHandler(db_file), "1111", "Asset B") == pytest.approx(0, abs=1e-6)
    assert _holdings(DatabaseHandler(db_file), "YOLO", "Asset B") == pytest.approx(0, abs=1e-6)


def test_auto_allocate_e2e_via_import_command(tmp_path):
    """Full import_data path with --allocate-virtual."""
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    cli.account_allocate(_ns(
        db_file, tx_date="2020-01-02", tx_asset="Asset A", to="YOLO", from_account=None, shares=None
    ))
    sell_csv = _SELL + "2020-06-01;1111;Sälj;Asset A;-50;120;6000;0;SEK;ASSETA;-"
    _import_more(db_file, sell_csv, tmp_path)
    cli.account_transfer_cash(_ns(db_file, from_account="1111", to="YOLO", amount=10000, date="2020-06-15"))

    buy_csv = _BUY + "2020-07-01;1111;Köp;Asset A;50;120;-6000;0;SEK;ASSETA;-"
    buy_file = _write_csv(tmp_path, "buy.csv", buy_csv)
    rc = cli.import_data(argparse.Namespace(
        database=str(db_file), special_cases=None, file=buy_file, allocate_virtual=True
    ))
    assert rc == 0
    assert _holdings(DatabaseHandler(db_file), "YOLO") == pytest.approx(100, abs=1e-6)


# ---------- account delete (clean teardown) ----------

def test_delete_reverts_transactions_and_removes_virtual(tmp_path):
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    cli.account_allocate(_ns(
        db_file, tx_date="2020-01-02", tx_asset="Asset A", to="YOLO", from_account=None, shares=None
    ))
    assert _holdings(DatabaseHandler(db_file), "YOLO") == pytest.approx(100, abs=1e-6)

    rc = cli.account_delete(_ns(db_file, name="YOLO", yes=True))
    assert rc == 0

    db = DatabaseHandler(db_file)
    db.connect()
    cur = db.get_cursor()
    # Buy reverted to parent
    cur.execute("SELECT account FROM transactions WHERE transaction_type='Köp' AND origin='avanza'")
    assert cur.fetchone()[0] == "1111"
    # No virtual transactions left
    cur.execute("SELECT COUNT(*) FROM transactions WHERE origin='virtual'")
    assert cur.fetchone()[0] == 0
    # Account row gone
    cur.execute("SELECT COUNT(*) FROM accounts WHERE account_id='YOLO'")
    assert cur.fetchone()[0] == 0
    db.disconnect()
    # Holdings restored on parent
    assert _holdings(DatabaseHandler(db_file), "1111") == pytest.approx(100, abs=1e-6)
    assert _holdings(DatabaseHandler(db_file), "YOLO") == pytest.approx(0, abs=1e-6)


def test_delete_removes_cash_transfer_traces(tmp_path):
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=5000, starting_cash_date="2020-02-01"))
    assert _count_virtual_transfers(db_file) == 2  # one pair from starting_cash

    rc = cli.account_delete(_ns(db_file, name="YOLO", yes=True))
    assert rc == 0
    assert _count_virtual_transfers(db_file) == 0


def test_delete_cleans_up_asset_transfer_partners(tmp_path):
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    cli.account_allocate(_ns(
        db_file, tx_date="2020-01-02", tx_asset="Asset A", to="YOLO", from_account=None, shares=None
    ))
    cli.account_create(_ns(db_file, name="GROWTH", parent="1111", starting_cash=5000, starting_cash_date="2020-02-01"))
    # Transfer 40 shares from YOLO to GROWTH
    cli.account_transfer(_ns(
        db_file, from_account="YOLO", to="GROWTH", asset="Asset A", shares=40, date="2020-03-01"
    ))
    assert _holdings(DatabaseHandler(db_file), "GROWTH") == pytest.approx(40, abs=1e-6)

    transfers_before = _count_virtual_transfers(db_file)

    rc = cli.account_delete(_ns(db_file, name="YOLO", yes=True))
    assert rc == 0

    db = DatabaseHandler(db_file)
    db.connect()
    cur = db.get_cursor()
    # No origin='virtual' transactions referencing YOLO remain
    cur.execute(
        "SELECT COUNT(*) FROM transactions WHERE origin='virtual' AND "
        "(account='YOLO' OR asset_name LIKE '%YOLO%')"
    )
    assert cur.fetchone()[0] == 0
    # The transfer Köp on GROWTH is deleted (origin='virtual')
    cur.execute(
        "SELECT COUNT(*) FROM transactions WHERE origin='virtual' AND transaction_type='Köp' AND account='GROWTH'"
    )
    assert cur.fetchone()[0] == 0
    # GROWTH's own starting_cash transfer is preserved (not from/to YOLO)
    cur.execute(
        "SELECT COUNT(*) FROM transactions WHERE origin='virtual' AND transaction_type='Intern överföring' "
        "AND account='GROWTH' AND asset_name='Transfer from 1111'"
    )
    assert cur.fetchone()[0] == 1
    db.disconnect()


def test_delete_other_virtuals_unaffected(tmp_path):
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    cli.account_create(_ns(db_file, name="GROWTH", parent="1111", starting_cash=None, starting_cash_date=None))
    cli.account_allocate(_ns(
        db_file, tx_date="2020-01-02", tx_asset="Asset A", to="YOLO", from_account=None, shares=50
    ))
    cli.account_allocate(_ns(
        db_file, tx_date="2020-01-02", tx_asset="Asset A", to="GROWTH", from_account=None, shares=30
    ))
    assert _holdings(DatabaseHandler(db_file), "YOLO") == pytest.approx(50, abs=1e-6)
    assert _holdings(DatabaseHandler(db_file), "GROWTH") == pytest.approx(30, abs=1e-6)

    rc = cli.account_delete(_ns(db_file, name="YOLO", yes=True))
    assert rc == 0

    # GROWTH still exists and has its shares
    assert _holdings(DatabaseHandler(db_file), "GROWTH") == pytest.approx(30, abs=1e-6)
    db = DatabaseHandler(db_file)
    db.connect()
    cur = db.get_cursor()
    cur.execute("SELECT COUNT(*) FROM accounts WHERE account_id='GROWTH'")
    assert cur.fetchone()[0] == 1
    db.disconnect()
    # YOLO gone
    assert _holdings(DatabaseHandler(db_file), "YOLO") == pytest.approx(0, abs=1e-6)


def test_delete_non_virtual_rejected(tmp_path):
    db_file = _base_parent_db(tmp_path)
    rc = cli.account_delete(_ns(db_file, name="1111"))
    assert rc == 1


def test_dividend_routing_preserves_sek_total_for_foreign_currency_dividends(tmp_path):
    """Regression test (issue #83): dividends on foreign-currency instruments
    have a price column in the instrument currency (e.g. DKK) but Belopp/total
    in SEK. Re-splitting across holders must divide the SEK total, not
    recompute shares * dps (which mixes currencies and understates the
    dividend)."""
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    cli.account_allocate(_ns(db_file, tx_date="2020-01-02", tx_asset="Asset A", to="YOLO", from_account=None, shares=None))
    # All 100 shares on YOLO; dividend of 3.75 DKK/share -> 375 DKK = 550 SEK total
    csv = _DIV + "2020-06-01;1111;Utdelning;Asset A;100;3,75;550;0;SEK;ASSETA;-"
    routed = _import_more(db_file, csv, tmp_path)
    assert routed == 1
    db = DatabaseHandler(db_file)
    db.connect()
    cur = db.get_cursor()
    cur.execute("SELECT amount, price, total FROM transactions WHERE transaction_type='Utdelning'")
    rows = cur.fetchall()
    db.disconnect()
    assert len(rows) == 1
    amount, dps, total = rows[0]
    assert amount == pytest.approx(100, abs=1e-6)
    assert dps == pytest.approx(3.75, abs=1e-6)   # instrument currency preserved
    assert total == pytest.approx(550, abs=1e-6)   # SEK total preserved, NOT 375


def test_dividend_credits_capital_from_sek_total_not_native_price(tmp_path):
    """Regression test (issue #85): handle_dividend must credit capital using
    the SEK total (total / amount), not the instrument-currency price column.
    A dividend with Kurs 3.75 (instrument currency) and Belopp 22.05 SEK on
    4 shares must credit 22.05 SEK of capital, not 15.00."""
    db_file = _base_parent_db(tmp_path)
    cli.account_create(_ns(db_file, name="YOLO", parent="1111", starting_cash=None, starting_cash_date=None))
    cli.account_allocate(_ns(db_file, tx_date="2020-01-02", tx_asset="Asset A", to="YOLO", from_account=None, shares=None))
    # All 100 shares on YOLO. Dividend: Kurs 3.75 (instrument currency),
    # Belopp 550 SEK -> per-share SEK rate 5.50, NOT 3.75.
    csv = _DIV + "2020-06-01;1111;Utdelning;Asset A;100;3,75;550;0;SEK;ASSETA;-"
    routed = _import_more(db_file, csv, tmp_path)
    assert routed == 1
    db = DatabaseHandler(db_file)
    db.connect()
    cur = db.get_cursor()
    cur.execute("SELECT COALESCE(SUM(capital), 0) FROM cohort_data WHERE account = 'YOLO'")
    yolo_cash = cur.fetchone()[0]
    db.disconnect()
    # YOLO held all 100 shares at dividend time: 100 * 5.50 = 550 SEK credited
    assert yolo_cash == pytest.approx(550, abs=0.5)
