"""
tests/test_classify_pipeline.py — Tests for the classify_pending_transactions
pipeline (issue fix: redundant double-LLM-call / no-duplicate-entries).

Verifies:
  - When a classification rule matches (apply_rules), exactly ONE
    transaction_entry is written with source='rule'.
  - When no rule matches, the unified LLM classifier writes exactly ONE
    transaction_entry with source='llm'.
  - No duplicate entries are ever written for a single transaction
    (UNIQUE constraint + INSERT OR IGNORE + single-write path).
  - The redundant classify_with_llm() fallback is NOT called when
    classify_transaction() already returned a line_item_id.
  - classify_pending_transactions() is idempotent: calling it twice for
    the same transaction does not create extra entries.
"""

from __future__ import annotations

import json
import uuid
from unittest.mock import patch

import pytest

from server.db import get_db, init_db

# ---------------------------------------------------------------------------
# Shared IDs / helpers
# ---------------------------------------------------------------------------

LEDGER_ID = "ledger-pipeline-test"
LI_GROCERIES = "li-groceries"
LI_INCOME = "li-income"
CONN_ID = "conn-pipeline"
ACCT_ID = "acct-pipeline"
USER_ID = "user-pipeline"
RULE_ID = "rule-starbucks"


def _seed(conn) -> None:
    """Seed the minimum schema rows required by classify_pending_transactions."""
    import time

    conn.execute(
        "INSERT INTO users (id, username, password_hash, created_at) VALUES (?, ?, ?, ?)",
        (USER_ID, "testuser", "fakehash", int(time.time())),
    )
    conn.execute(
        "INSERT INTO ledgers (id, name, user_id) VALUES (?, ?, ?)",
        (LEDGER_ID, "Personal", USER_ID),
    )
    conn.execute(
        "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
        (LI_GROCERIES, LEDGER_ID, "Groceries", "expense"),
    )
    conn.execute(
        "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
        (LI_INCOME, LEDGER_ID, "Salary", "income"),
    )
    conn.execute(
        "INSERT INTO bank_connections (id, user_id, plaid_access_token_encrypted, status)"
        " VALUES (?, ?, ?, ?)",
        (CONN_ID, USER_ID, "tok-enc", "active"),
    )
    conn.execute(
        "INSERT INTO bank_accounts (id, connection_id, name, default_ledger_id)"
        " VALUES (?, ?, ?, ?)",
        (ACCT_ID, CONN_ID, "Chequing", LEDGER_ID),
    )
    conn.commit()


def _insert_txn(conn, merchant: str, amount: float = 10.0, pending: int = 0) -> str:
    """Insert one transaction and return its id."""
    txn_id = str(uuid.uuid4())
    conn.execute(
        "INSERT INTO transactions"
        " (id, bank_account_id, plaid_transaction_id, date, merchant, amount, pending)"
        " VALUES (?, ?, ?, '2025-01-01', ?, ?, ?)",
        (txn_id, ACCT_ID, f"plaid-{txn_id}", merchant, amount, pending),
    )
    conn.commit()
    return txn_id


def _good_llm_response(line_item_id: str, classification_type: str = "spending") -> str:
    """Return a well-formed LLM JSON string for a transaction."""
    return json.dumps(
        {
            "rule_id": None,
            "line_item_id": line_item_id,
            "classification_type": classification_type,
            "confidence": 0.95,
            "reasoning": "mock classification",
        }
    )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def db_path(tmp_path):
    path = tmp_path / "test_pipeline.db"
    init_db(path)
    conn = get_db(path)
    _seed(conn)
    conn.close()
    return path


# ---------------------------------------------------------------------------
# Test: classify_pending_transactions — rule match writes ONE entry
# ---------------------------------------------------------------------------


def test_rule_match_writes_single_entry(db_path, monkeypatch):
    """When apply_rules() matches during sync, exactly 1 entry with source='rule'."""
    import server.paths as _paths

    monkeypatch.setattr(_paths, "DB_PATH", db_path)

    from server.main import classify_pending_transactions

    conn = get_db(db_path)

    # Insert a routing_rule that matches "Starbucks"
    conn.execute(
        "INSERT INTO routing_rules (id, merchant_pattern, line_item_id)" " VALUES (?, ?, ?)",
        (RULE_ID, "starbucks", LI_GROCERIES),
    )
    # Insert a pre-classified entry (simulating apply_rules during sync)
    txn_id = _insert_txn(conn, "Starbucks Coffee", amount=5.50)
    conn.execute(
        "INSERT INTO transaction_entries"
        " (id, transaction_id, ledger_id, line_item_id, amount, source, confidence, reviewed)"
        " VALUES (?, ?, ?, ?, ?, 'rule', 1.0, 0)",
        (str(uuid.uuid4()), txn_id, LEDGER_ID, LI_GROCERIES, 5.50),
    )
    conn.commit()
    conn.close()

    # classify_pending_transactions must skip already-classified transactions
    result = classify_pending_transactions(USER_ID)

    conn = get_db(db_path)
    entries = conn.execute(
        "SELECT * FROM transaction_entries WHERE transaction_id = ?", (txn_id,)
    ).fetchall()
    conn.close()

    # Must still be exactly 1 entry (the rule-written one) — no new entry added
    assert len(entries) == 1
    assert entries[0]["source"] == "rule"
    assert result["classified"] == 0  # nothing new was classified


# ---------------------------------------------------------------------------
# Test: classify_pending_transactions — no rule → LLM → ONE entry
# ---------------------------------------------------------------------------


def test_no_rule_llm_writes_single_entry(db_path, monkeypatch):
    """No routing rule → classify_transaction() is called once → 1 entry written."""
    import server.paths as _paths

    monkeypatch.setattr(_paths, "DB_PATH", db_path)

    from server.main import classify_pending_transactions

    conn = get_db(db_path)
    txn_id = _insert_txn(conn, "Whole Foods", amount=42.00)
    conn.close()

    llm_call_count = 0

    def _mock_chat(messages, temperature=0.0):
        nonlocal llm_call_count
        llm_call_count += 1
        return _good_llm_response(LI_GROCERIES)

    with patch("server.llm.chat", side_effect=_mock_chat):
        result = classify_pending_transactions(USER_ID)

    conn = get_db(db_path)
    entries = conn.execute(
        "SELECT * FROM transaction_entries WHERE transaction_id = ?", (txn_id,)
    ).fetchall()
    conn.close()

    # Exactly 1 entry, from the unified LLM call
    assert len(entries) == 1, f"Expected 1 entry, got {len(entries)}: {entries}"
    assert entries[0]["source"] == "llm"
    assert entries[0]["line_item_id"] == LI_GROCERIES

    # Only 1 LLM call total (no redundant classify_with_llm fallback)
    assert llm_call_count == 1, (
        f"Expected 1 LLM call, got {llm_call_count} — "
        "redundant fallback may have been re-introduced"
    )

    assert result["classified"] == 1
    assert result["uncertain"] == 0


# ---------------------------------------------------------------------------
# Test: no duplicate entries — UNIQUE constraint + idempotency
# ---------------------------------------------------------------------------


def test_no_duplicate_entries(db_path, monkeypatch):
    """Calling classify_pending_transactions twice never creates > 1 entry."""
    import server.paths as _paths

    monkeypatch.setattr(_paths, "DB_PATH", db_path)

    from server.main import classify_pending_transactions

    conn = get_db(db_path)
    txn_id = _insert_txn(conn, "Netflix", amount=14.00)
    conn.close()

    def _mock_chat(messages, temperature=0.0):
        return _good_llm_response(LI_GROCERIES)

    with patch("server.llm.chat", side_effect=_mock_chat):
        result1 = classify_pending_transactions(USER_ID)
        result2 = classify_pending_transactions(USER_ID)  # second call — should be a no-op

    conn = get_db(db_path)
    entries = conn.execute(
        "SELECT * FROM transaction_entries WHERE transaction_id = ?", (txn_id,)
    ).fetchall()
    conn.close()

    assert len(entries) == 1, f"Expected 1 entry after 2 calls, got {len(entries)}"
    assert result1["classified"] == 1
    assert result2["classified"] == 0  # second pass classified nothing


# ---------------------------------------------------------------------------
# Test: income line item → entry_type derived correctly
# ---------------------------------------------------------------------------


def test_income_line_item_sets_entry_type(db_path, monkeypatch):
    """When LLM picks an income line item, entry_type must be 'income'."""
    import server.paths as _paths

    monkeypatch.setattr(_paths, "DB_PATH", db_path)

    from server.main import classify_pending_transactions

    conn = get_db(db_path)
    txn_id = _insert_txn(conn, "Payroll Deposit", amount=-3000.00)
    conn.close()

    def _mock_chat(messages, temperature=0.0):
        return _good_llm_response(LI_INCOME, classification_type="income")

    with patch("server.llm.chat", side_effect=_mock_chat):
        classify_pending_transactions(USER_ID)

    conn = get_db(db_path)
    entry = conn.execute(
        "SELECT entry_type FROM transaction_entries WHERE transaction_id = ?", (txn_id,)
    ).fetchone()
    conn.close()

    assert entry is not None
    assert entry["entry_type"] == "income"


# ---------------------------------------------------------------------------
# Test: classify_transaction returns None line_item → default ledger fallback
# ---------------------------------------------------------------------------


def test_none_line_item_uses_default_ledger_fallback(db_path, monkeypatch):
    """When LLM returns line_item_id=null, the default ledger fallback is used."""
    import server.paths as _paths

    monkeypatch.setattr(_paths, "DB_PATH", db_path)

    from server.main import classify_pending_transactions

    conn = get_db(db_path)
    txn_id = _insert_txn(conn, "Mystery Merchant", amount=9.99)
    conn.close()

    def _mock_chat(messages, temperature=0.0):
        # LLM returns no match
        return json.dumps(
            {
                "rule_id": None,
                "line_item_id": None,
                "classification_type": "spending",
                "confidence": 0.3,
                "reasoning": "unknown merchant",
            }
        )

    with patch("server.llm.chat", side_effect=_mock_chat):
        result = classify_pending_transactions(USER_ID)

    conn = get_db(db_path)
    entries = conn.execute(
        "SELECT * FROM transaction_entries WHERE transaction_id = ?", (txn_id,)
    ).fetchall()
    conn.close()

    # Should be exactly 1 entry (from default ledger fallback or uncertain)
    assert len(entries) == 1, f"Expected 1 entry, got {len(entries)}"


# ---------------------------------------------------------------------------
# Test: classify_with_rules (pure function) — rule match returns correct shape
# ---------------------------------------------------------------------------


def test_classify_with_rules_rule_match():
    """classify_with_rules returns correct dict shape when a rule matches."""
    from server.classifier import classify_with_rules

    rules = [
        {
            "id": "rule-1",
            "name": "Starbucks Rule",
            "description": "Starbucks transactions go to Dining",
            "rule_type": "spending",
            "line_item_id": LI_GROCERIES,
            "priority": 10,
            "enabled": True,
        }
    ]

    def _mock_chat(messages, temperature=0.0):
        return json.dumps(
            {
                "rule_id": "rule-1",
                "line_item_id": LI_GROCERIES,
                "classification_type": "spending",
                "confidence": 0.98,
                "reasoning": "Starbucks matches Starbucks Rule",
            }
        )

    with patch("server.llm.chat", side_effect=_mock_chat):
        result = classify_with_rules(
            {"merchant": "Starbucks", "amount": 5.50, "date": "2025-01-01"},
            rules,
        )

    assert result["rule_id"] == "rule-1"
    assert result["line_item_id"] == LI_GROCERIES
    assert result["classification_type"] == "spending"
    assert result["confidence"] >= 0.7
    assert result["uncertain"] is False


# ---------------------------------------------------------------------------
# Test: classify_with_rules — no rule match returns null rule_id
# ---------------------------------------------------------------------------


def test_classify_with_rules_no_match():
    """classify_with_rules returns rule_id=None when no rule matches."""
    from server.classifier import classify_with_rules

    rules = [
        {
            "id": "rule-1",
            "name": "Starbucks Rule",
            "description": "Starbucks transactions go to Dining",
            "rule_type": "spending",
            "line_item_id": LI_GROCERIES,
            "priority": 10,
            "enabled": True,
        }
    ]

    def _mock_chat(messages, temperature=0.0):
        return json.dumps(
            {
                "rule_id": None,
                "line_item_id": None,
                "classification_type": "spending",
                "confidence": 0.40,
                "reasoning": "No rule clearly matches Amazon purchase",
            }
        )

    with patch("server.llm.chat", side_effect=_mock_chat):
        result = classify_with_rules(
            {"merchant": "Amazon", "amount": 35.00, "date": "2025-01-01"},
            rules,
        )

    assert result["rule_id"] is None
    assert result["line_item_id"] is None
    assert result["uncertain"] is True  # confidence 0.40 < 0.7
