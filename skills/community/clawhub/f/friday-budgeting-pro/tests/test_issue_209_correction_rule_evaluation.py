"""
tests/test_issue_209_correction_rule_evaluation.py — Tests for issue #209.

Covers:
  - correct_transaction returns rule_suggestions in response
  - Conflicting routing_rule (same merchant pattern, wrong line_item) is detected
  - Merchant appearing 2+ times triggers a create_rule suggestion
  - Merchant appearing only once does NOT trigger create_rule suggestion
  - Already-correct routing_rule (matching line_item_id) is NOT flagged as conflicting
  - create_rule=True suppresses the create_rule suggestion (rule already created)
  - Rule suggestions include required fields (action, reason, etc.)
  - Multiple conflicting rules are all returned
  - Suggestion descriptions are tagged [from-correction]
"""

from __future__ import annotations

import uuid
from pathlib import Path

import pytest

import server.paths
from server.db import get_db, init_db
from ui.auth import create_session, create_user

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _uid() -> str:
    return str(uuid.uuid4())


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def db_path(tmp_path: Path, monkeypatch) -> Path:
    """Fresh temp DB; monkeypatch server.paths.DB_PATH."""
    path = tmp_path / "test_209.db"
    init_db(path)
    monkeypatch.setattr(server.paths, "DB_PATH", path)
    return path


@pytest.fixture()
def authed_user(db_path: Path) -> dict:
    user_id = create_user(db_path, "testuser209", "testpass123")
    token = create_session(db_path, user_id=user_id)
    return {"user_id": user_id, "token": token}


def _seed_base(db_path: Path, user_id: str) -> dict:
    """Seed connection, account, ledger, two line items."""
    conn = get_db(db_path)
    try:
        conn_id = _uid()
        account_id = _uid()
        conn.execute(
            "INSERT INTO bank_connections (id, plaid_access_token_encrypted, status, user_id, institution_name) "
            "VALUES (?, ?, 'active', ?, ?)",
            (conn_id, "enc:fake", user_id, "Test Bank"),
        )
        conn.execute(
            "INSERT INTO bank_accounts (id, connection_id, name) VALUES (?, ?, ?)",
            (account_id, conn_id, "Chequing"),
        )
        ledger_id = _uid()
        li_groceries = _uid()
        li_dining = _uid()
        conn.execute(
            "INSERT INTO ledgers (id, name, user_id) VALUES (?, ?, ?)",
            (ledger_id, "Personal", user_id),
        )
        conn.execute(
            "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
            (li_groceries, ledger_id, "Groceries", "expense"),
        )
        conn.execute(
            "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
            (li_dining, ledger_id, "Dining", "expense"),
        )
        conn.commit()
    finally:
        conn.close()

    return {
        "account_id": account_id,
        "ledger_id": ledger_id,
        "li_groceries": li_groceries,
        "li_dining": li_dining,
    }


def _add_transaction(db_path: Path, account_id: str, merchant: str, amount: float = 25.0) -> str:
    """Insert a transaction and return its ID."""
    tx_id = _uid()
    conn = get_db(db_path)
    try:
        conn.execute(
            "INSERT INTO transactions (id, date, merchant, amount, bank_account_id) VALUES (?, ?, ?, ?, ?)",
            (tx_id, "2026-05-20", merchant, amount, account_id),
        )
        conn.commit()
    finally:
        conn.close()
    return tx_id


def _add_entry(db_path: Path, tx_id: str, ledger_id: str, line_item_id: str) -> None:
    """Insert a transaction_entry for an existing transaction."""
    conn = get_db(db_path)
    try:
        conn.execute(
            "INSERT INTO transaction_entries (id, transaction_id, ledger_id, line_item_id, amount, source, reviewed) "
            "VALUES (?, ?, ?, ?, 25.0, 'rule', 0)",
            (_uid(), tx_id, ledger_id, line_item_id),
        )
        conn.commit()
    finally:
        conn.close()


def _add_routing_rule(db_path: Path, merchant_pattern: str, line_item_id: str) -> str:
    """Insert a routing_rule and return its ID."""
    rule_id = _uid()
    conn = get_db(db_path)
    try:
        conn.execute(
            "INSERT INTO routing_rules (id, merchant_pattern, line_item_id) VALUES (?, ?, ?)",
            (rule_id, merchant_pattern, line_item_id),
        )
        conn.commit()
    finally:
        conn.close()
    return rule_id


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestRuleSuggestionsInResponse:
    def test_response_always_has_rule_suggestions_key(self, db_path, authed_user):
        """correct_transaction always returns rule_suggestions (even when empty)."""
        from server.main import correct_transaction

        ids = _seed_base(db_path, authed_user["user_id"])
        tx_id = _add_transaction(db_path, ids["account_id"], "Starbucks")
        _add_entry(db_path, tx_id, ids["ledger_id"], ids["li_groceries"])

        result = correct_transaction(tx_id, ids["li_dining"])
        assert "rule_suggestions" in result
        assert isinstance(result["rule_suggestions"], list)

    def test_no_suggestions_when_no_rules_and_single_occurrence(self, db_path, authed_user):
        """No suggestions when merchant appears once and no routing rules exist."""
        from server.main import correct_transaction

        ids = _seed_base(db_path, authed_user["user_id"])
        tx_id = _add_transaction(db_path, ids["account_id"], "UniqueMerchant123")
        _add_entry(db_path, tx_id, ids["ledger_id"], ids["li_groceries"])

        result = correct_transaction(tx_id, ids["li_dining"])
        assert result["status"] == "ok"
        assert result["rule_suggestions"] == []


class TestConflictingRoutingRuleDetection:
    def test_conflicting_rule_triggers_update_or_disable_suggestion(self, db_path, authed_user):
        """A routing_rule pointing to the wrong line_item triggers update_or_disable_rule."""
        from server.main import correct_transaction

        ids = _seed_base(db_path, authed_user["user_id"])
        # Routing rule: "Loblaws" → li_groceries (wrong — we want dining)
        rule_id = _add_routing_rule(db_path, "Loblaws", ids["li_groceries"])
        tx_id = _add_transaction(db_path, ids["account_id"], "Loblaws Superstore")
        _add_entry(db_path, tx_id, ids["ledger_id"], ids["li_groceries"])

        # Correct it to dining
        result = correct_transaction(tx_id, ids["li_dining"])
        assert result["status"] == "ok"

        suggestions = result["rule_suggestions"]
        assert len(suggestions) == 1
        s = suggestions[0]
        assert s["action"] == "update_or_disable_rule"
        assert s["rule_id"] == rule_id
        assert s["merchant_pattern"] == "Loblaws"
        assert s["current_line_item_id"] == ids["li_groceries"]
        assert s["suggested_line_item_id"] == ids["li_dining"]
        assert "reason" in s

    def test_correct_routing_rule_not_flagged(self, db_path, authed_user):
        """A routing_rule already pointing to the correct line_item is NOT flagged."""
        from server.main import correct_transaction

        ids = _seed_base(db_path, authed_user["user_id"])
        # Routing rule for "Tim Hortons" → li_dining (same as correction target)
        _add_routing_rule(db_path, "Tim Hortons", ids["li_dining"])
        tx_id = _add_transaction(db_path, ids["account_id"], "Tim Hortons Coffee")
        _add_entry(db_path, tx_id, ids["ledger_id"], ids["li_groceries"])

        result = correct_transaction(tx_id, ids["li_dining"])
        # The routing rule is correct — no conflict
        conflict_suggestions = [
            s for s in result["rule_suggestions"] if s["action"] == "update_or_disable_rule"
        ]
        assert conflict_suggestions == []

    def test_multiple_conflicting_rules_all_returned(self, db_path, authed_user):
        """If multiple routing rules conflict, all are returned."""
        from server.main import correct_transaction

        ids = _seed_base(db_path, authed_user["user_id"])
        rule_id1 = _add_routing_rule(db_path, "Amazon", ids["li_groceries"])
        rule_id2 = _add_routing_rule(db_path, "Amazon Prime", ids["li_groceries"])
        tx_id = _add_transaction(db_path, ids["account_id"], "Amazon Prime Video")
        _add_entry(db_path, tx_id, ids["ledger_id"], ids["li_groceries"])

        result = correct_transaction(tx_id, ids["li_dining"])
        conflict_suggestions = [
            s for s in result["rule_suggestions"] if s["action"] == "update_or_disable_rule"
        ]
        returned_ids = {s["rule_id"] for s in conflict_suggestions}
        assert rule_id1 in returned_ids
        assert rule_id2 in returned_ids

    def test_pattern_matching_is_case_insensitive(self, db_path, authed_user):
        """Routing rule pattern matching is case-insensitive (mirrors apply_rules)."""
        from server.main import correct_transaction

        ids = _seed_base(db_path, authed_user["user_id"])
        rule_id = _add_routing_rule(db_path, "NETFLIX", ids["li_groceries"])
        tx_id = _add_transaction(db_path, ids["account_id"], "Netflix Subscription")
        _add_entry(db_path, tx_id, ids["ledger_id"], ids["li_groceries"])

        result = correct_transaction(tx_id, ids["li_dining"])
        conflict_suggestions = [
            s for s in result["rule_suggestions"] if s["action"] == "update_or_disable_rule"
        ]
        assert any(s["rule_id"] == rule_id for s in conflict_suggestions)


class TestCreateRuleSuggestion:
    def test_suggests_create_rule_when_merchant_appears_twice(self, db_path, authed_user):
        """Merchant appearing 2+ times triggers a create_rule suggestion."""
        from server.main import correct_transaction

        ids = _seed_base(db_path, authed_user["user_id"])
        # Two transactions for the same merchant
        tx_id1 = _add_transaction(db_path, ids["account_id"], "Uber Eats", 15.0)
        tx_id2 = _add_transaction(db_path, ids["account_id"], "Uber Eats", 22.0)
        _add_entry(db_path, tx_id1, ids["ledger_id"], ids["li_groceries"])
        _add_entry(db_path, tx_id2, ids["ledger_id"], ids["li_groceries"])

        result = correct_transaction(tx_id1, ids["li_dining"])
        create_suggestions = [s for s in result["rule_suggestions"] if s["action"] == "create_rule"]
        assert len(create_suggestions) == 1
        s = create_suggestions[0]
        assert s["merchant"] == "Uber Eats"
        assert s["suggested_line_item_id"] == ids["li_dining"]
        assert s["occurrence_count"] >= 2
        assert "[from-correction]" in s["suggested_description"]
        assert "reason" in s

    def test_no_create_rule_suggestion_for_single_occurrence(self, db_path, authed_user):
        """Merchant appearing only once does NOT trigger a create_rule suggestion."""
        from server.main import correct_transaction

        ids = _seed_base(db_path, authed_user["user_id"])
        tx_id = _add_transaction(db_path, ids["account_id"], "RareMerchantXYZ")
        _add_entry(db_path, tx_id, ids["ledger_id"], ids["li_groceries"])

        result = correct_transaction(tx_id, ids["li_dining"])
        create_suggestions = [s for s in result["rule_suggestions"] if s["action"] == "create_rule"]
        assert create_suggestions == []

    def test_create_rule_true_suppresses_create_rule_suggestion(self, db_path, authed_user):
        """When create_rule=True is passed, create_rule suggestion is suppressed."""
        from unittest.mock import patch

        from server.main import correct_transaction

        ids = _seed_base(db_path, authed_user["user_id"])
        tx_id1 = _add_transaction(db_path, ids["account_id"], "DoorDash", 18.0)
        tx_id2 = _add_transaction(db_path, ids["account_id"], "DoorDash", 21.0)
        _add_entry(db_path, tx_id1, ids["ledger_id"], ids["li_groceries"])
        _add_entry(db_path, tx_id2, ids["ledger_id"], ids["li_groceries"])

        with patch("server.main.add_rule") as mock_add_rule:
            mock_add_rule.return_value = {"status": "ok", "rule_id": _uid()}
            result = correct_transaction(tx_id1, ids["li_dining"], create_rule=True)

        assert result["rule_created"] is True
        # Since create_rule=True, no additional create_rule suggestion
        create_suggestions = [s for s in result["rule_suggestions"] if s["action"] == "create_rule"]
        assert create_suggestions == []

    def test_conflicting_rule_suppresses_create_rule_suggestion(self, db_path, authed_user):
        """When conflicting routing rules exist, create_rule suggestion is NOT added."""
        from server.main import correct_transaction

        ids = _seed_base(db_path, authed_user["user_id"])
        _add_routing_rule(db_path, "Walmart", ids["li_groceries"])
        tx_id1 = _add_transaction(db_path, ids["account_id"], "Walmart Supercentre", 55.0)
        tx_id2 = _add_transaction(db_path, ids["account_id"], "Walmart Supercentre", 30.0)
        _add_entry(db_path, tx_id1, ids["ledger_id"], ids["li_groceries"])
        _add_entry(db_path, tx_id2, ids["ledger_id"], ids["li_groceries"])

        result = correct_transaction(tx_id1, ids["li_dining"])
        create_suggestions = [s for s in result["rule_suggestions"] if s["action"] == "create_rule"]
        # Conflicting rule was found, so no redundant create suggestion
        assert create_suggestions == []


class TestRuleSuggestionFields:
    def test_update_suggestion_has_required_fields(self, db_path, authed_user):
        """update_or_disable_rule suggestion includes all required fields."""
        from server.main import correct_transaction

        ids = _seed_base(db_path, authed_user["user_id"])
        _add_routing_rule(db_path, "Spotify", ids["li_groceries"])
        tx_id = _add_transaction(db_path, ids["account_id"], "Spotify Premium")
        _add_entry(db_path, tx_id, ids["ledger_id"], ids["li_groceries"])

        result = correct_transaction(tx_id, ids["li_dining"])
        suggestions = [
            s for s in result["rule_suggestions"] if s["action"] == "update_or_disable_rule"
        ]
        assert len(suggestions) == 1
        s = suggestions[0]
        required_fields = {
            "action",
            "rule_id",
            "merchant_pattern",
            "current_line_item_id",
            "suggested_line_item_id",
            "reason",
        }
        assert required_fields.issubset(s.keys())

    def test_create_suggestion_has_required_fields(self, db_path, authed_user):
        """create_rule suggestion includes all required fields."""
        from server.main import correct_transaction

        ids = _seed_base(db_path, authed_user["user_id"])
        tx_id1 = _add_transaction(db_path, ids["account_id"], "HelloFresh", 80.0)
        tx_id2 = _add_transaction(db_path, ids["account_id"], "HelloFresh", 85.0)
        _add_entry(db_path, tx_id1, ids["ledger_id"], ids["li_groceries"])
        _add_entry(db_path, tx_id2, ids["ledger_id"], ids["li_groceries"])

        result = correct_transaction(tx_id1, ids["li_dining"])
        suggestions = [s for s in result["rule_suggestions"] if s["action"] == "create_rule"]
        assert len(suggestions) == 1
        s = suggestions[0]
        required_fields = {
            "action",
            "merchant",
            "suggested_line_item_id",
            "occurrence_count",
            "suggested_description",
            "reason",
        }
        assert required_fields.issubset(s.keys())
