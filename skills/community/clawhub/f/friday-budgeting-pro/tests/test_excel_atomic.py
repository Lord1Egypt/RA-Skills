"""
tests/test_excel_atomic.py — Atomic export reliability tests for issue #44.

Tests
-----
- Crash simulation: mid-write failure leaves original file unchanged
- Concurrent sync + export: sync_lock held → export raises ExportBusy/LockBusy
  and does NOT corrupt anything
- Happy path: export completes and sync_lock is released afterward
- PID suffix: temp file path contains the current PID
"""

from __future__ import annotations

import os
import sqlite3
import uuid
from pathlib import Path
from unittest.mock import patch

import pytest

import server.paths
from server.db import get_db, init_db
from server.excel_export import ExportBusy, export_to_file
from server.sync_lock import acquire_sync_lock

# ---------------------------------------------------------------------------
# Fixtures (same seeded-db setup as test_excel_export.py)
# ---------------------------------------------------------------------------


@pytest.fixture()
def patched_paths(tmp_path: Path, monkeypatch):
    """Redirect all server.paths path constants to tmp_path."""
    app_dir = tmp_path / ".friday-bp"
    exports_dir = app_dir / "exports"
    db_path = app_dir / "data.db"
    sync_lock_path = app_dir / "sync.lock"

    monkeypatch.setattr(server.paths, "APP_DIR", app_dir)
    monkeypatch.setattr(server.paths, "EXPORTS_DIR", exports_dir)
    monkeypatch.setattr(server.paths, "DB_PATH", db_path)
    monkeypatch.setattr(server.paths, "SYNC_LOCK_PATH", sync_lock_path)

    return {
        "app_dir": app_dir,
        "exports_dir": exports_dir,
        "db_path": db_path,
        "sync_lock_path": sync_lock_path,
    }


@pytest.fixture()
def seeded_db(patched_paths) -> sqlite3.Connection:
    """Initialise DB and seed with minimal data for atomic-export tests."""
    db_path = patched_paths["db_path"]
    db_path.parent.mkdir(parents=True, exist_ok=True)
    init_db(db_path)
    conn = get_db(db_path)

    ledger_id = str(uuid.uuid4())
    groceries_id = str(uuid.uuid4())
    salary_id = str(uuid.uuid4())

    conn.execute("INSERT INTO ledgers (id, name) VALUES (?, ?)", (ledger_id, "Personal"))
    conn.execute(
        "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
        (groceries_id, ledger_id, "Groceries", "expense"),
    )
    conn.execute(
        "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
        (salary_id, ledger_id, "Salary", "income"),
    )

    conn_id = str(uuid.uuid4())
    acct_id = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO bank_connections (id, plaid_item_id, plaid_access_token_encrypted) VALUES (?, ?, ?)",
        (conn_id, "plaid-item-1", "enc-token"),
    )
    conn.execute(
        "INSERT INTO bank_accounts (id, connection_id, plaid_account_id, name) VALUES (?, ?, ?, ?)",
        (acct_id, conn_id, "plaid-acct-1", "Chequing"),
    )

    txns = [
        (str(uuid.uuid4()), "2026-01-05", "Superstore", 100.0, groceries_id, ledger_id),
        (str(uuid.uuid4()), "2026-01-25", "Employer", 2000.0, salary_id, ledger_id),
    ]
    for txn_id, date, merchant, amount, li_id, led_id in txns:
        conn.execute(
            "INSERT INTO transactions (id, bank_account_id, plaid_transaction_id, date, merchant, amount) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (txn_id, acct_id, f"plaid-{txn_id}", date, merchant, amount),
        )
        entry_id = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO transaction_entries (id, transaction_id, ledger_id, line_item_id, amount, source) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (entry_id, txn_id, led_id, li_id, amount, "manual"),
        )

    conn.commit()
    yield conn
    conn.close()


# ---------------------------------------------------------------------------
# Test: crash simulation — original file must be unchanged
# ---------------------------------------------------------------------------


def test_crash_leaves_original_unchanged(seeded_db, patched_paths, tmp_path):
    """If Workbook.save raises mid-write, the original target file is untouched."""
    dest = tmp_path / "budget.xlsx"

    # Create a sentinel "original" file at the destination.
    sentinel_content = b"ORIGINAL CONTENT - must survive crash"
    dest.write_bytes(sentinel_content)

    # Monkeypatch Workbook.save to simulate a crash mid-write.
    original_save = __import__("openpyxl").Workbook.save

    def crash_save(self, filename):
        # Write some junk to the temp path then raise, simulating a partial write.
        Path(filename).write_bytes(b"PARTIAL JUNK")
        raise OSError("Simulated crash during save")

    with patch("openpyxl.Workbook.save", crash_save):
        with pytest.raises(OSError, match="Simulated crash during save"):
            export_to_file(seeded_db, dest)

    # Original file must be byte-for-byte unchanged.
    assert (
        dest.read_bytes() == sentinel_content
    ), "Original file was modified despite a crash during export"

    # No temp file should remain with the non-crashing content.
    # (The crash path cleans up the .tmp.<pid> file.)
    tmp_files = list(tmp_path.glob("budget.xlsx.tmp.*"))
    assert tmp_files == [], f"Temp file(s) were not cleaned up: {tmp_files}"


# ---------------------------------------------------------------------------
# Test: concurrent sync + export — ExportBusy raised, nothing corrupted
# ---------------------------------------------------------------------------


def test_export_busy_when_sync_lock_held(seeded_db, patched_paths, tmp_path):
    """export_to_file raises ExportBusy when sync_lock is already held."""
    dest = tmp_path / "budget.xlsx"

    # Hold the sync lock ourselves to simulate a concurrent sync operation.
    held_lock = acquire_sync_lock(timeout=0.0)
    assert held_lock is not None, "Could not acquire sync lock for test setup"

    try:
        with pytest.raises(ExportBusy):
            # timeout=0.5s so the test doesn't hang; it should fail quickly.
            export_to_file(seeded_db, dest, lock_timeout=0.5)
    finally:
        held_lock.close()

    # The destination must not have been created or corrupted.
    assert not dest.exists(), "Export should not have written anything when the lock was held"


# ---------------------------------------------------------------------------
# Test: happy path — lock is released after export completes
# ---------------------------------------------------------------------------


def test_lock_released_after_successful_export(seeded_db, patched_paths, tmp_path):
    """After a successful export the sync lock is released (can be re-acquired)."""
    dest = tmp_path / "budget.xlsx"

    # Run the export.
    result = export_to_file(seeded_db, dest)
    assert result == dest
    assert dest.exists()

    # The lock should now be available again.
    lock = acquire_sync_lock(timeout=0.0)
    assert lock is not None, "sync_lock was NOT released after export completed"
    lock.close()


# ---------------------------------------------------------------------------
# Test: PID suffix on temp file
# ---------------------------------------------------------------------------


def test_pid_suffix_on_temp_file(seeded_db, patched_paths, tmp_path):
    """The temp file created during export has the current PID as its suffix."""
    dest = tmp_path / "budget.xlsx"
    current_pid = os.getpid()

    recorded_src: list[str] = []

    original_replace = os.replace

    def spy_replace(src, dst):
        recorded_src.append(str(src))
        return original_replace(src, dst)

    with patch("os.replace", spy_replace):
        export_to_file(seeded_db, dest)

    assert recorded_src, "os.replace was never called"
    src_path = recorded_src[0]
    assert (
        f".tmp.{current_pid}" in src_path
    ), f"Expected PID {current_pid} in temp path, got: {src_path}"
