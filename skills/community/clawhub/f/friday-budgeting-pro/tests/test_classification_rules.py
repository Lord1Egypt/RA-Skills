"""
tests/test_classification_rules.py — Tests for classification rules schema,
default seeding, and MCP tools.

Covers:
- Migration: fresh DB seeds exactly 6 default rules with correct priorities
- Migration is idempotent (running init_db again does not duplicate)
- list_rules() returns rules in priority order, all metadata present
- add_rule() creates a new rule, appears in list
- update_rule() updates specified fields, leaves others unchanged
- reorder_rules() assigns priorities 10, 20, 30 ... in supplied order
- disable_rule() / enable_rule() toggle the enabled column
- delete_rule() on default rule → error; on user rule → ok
- Invalid rule_type in add_rule → ValueError
"""

from __future__ import annotations

import pytest

from server.db import init_db
from server.main import (
    add_rule,
    delete_rule,
    disable_rule,
    enable_rule,
    list_rules,
    reorder_rules,
    update_rule,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def tmp_db(tmp_path, monkeypatch):
    """Create a fresh DB at tmp_path and monkeypatch server.paths.DB_PATH."""
    import server.paths

    db_file = tmp_path / "test.db"
    monkeypatch.setattr(server.paths, "DB_PATH", db_file)
    init_db(db_file)
    return db_file


# ---------------------------------------------------------------------------
# Migration / seeding tests
# ---------------------------------------------------------------------------


def test_default_rules_seeded(tmp_db):
    """Fresh DB must have exactly 6 default rules seeded."""
    result = list_rules()
    defaults = [r for r in result["rules"] if r["is_default"]]
    assert len(defaults) == 6


def test_default_rules_priorities(tmp_db):
    """Default rules must have priorities 1, 10, 20, 30, 40, 50."""
    result = list_rules()
    defaults = sorted([r for r in result["rules"] if r["is_default"]], key=lambda r: r["priority"])
    assert [r["priority"] for r in defaults] == [1, 10, 20, 30, 40, 50]


def test_default_rules_is_default_flag(tmp_db):
    """All seeded default rules must have is_default=True."""
    result = list_rules()
    defaults = [r for r in result["rules"] if r["is_default"]]
    assert all(r["is_default"] is True for r in defaults)


def test_migration_idempotent(tmp_db):
    """Calling init_db a second time must not duplicate default rules."""

    init_db(tmp_db)  # second call
    result = list_rules()
    defaults = [r for r in result["rules"] if r["is_default"]]
    assert len(defaults) == 6


# ---------------------------------------------------------------------------
# list_rules tests
# ---------------------------------------------------------------------------


def test_list_rules_sorted_by_priority(tmp_db):
    """list_rules must return rules in ascending priority order."""
    result = list_rules()
    priorities = [r["priority"] for r in result["rules"]]
    assert priorities == sorted(priorities)


def test_list_rules_metadata_fields(tmp_db):
    """Every rule dict must contain all expected metadata fields."""
    result = list_rules()
    required_fields = {
        "id",
        "name",
        "description",
        "rule_type",
        "line_item_id",
        "priority",
        "is_default",
        "enabled",
        "created_at",
    }
    for rule in result["rules"]:
        assert required_fields.issubset(
            rule.keys()
        ), f"Missing fields in rule {rule.get('id')}: {required_fields - set(rule.keys())}"


# ---------------------------------------------------------------------------
# add_rule tests
# ---------------------------------------------------------------------------


def test_add_rule_creates_rule(tmp_db):
    """add_rule must return status ok with a rule_id, and rule must appear in list."""
    result = add_rule(
        name="Test rule",
        description="Purchases at test merchant are spending",
        rule_type="spending",
    )
    assert result["status"] == "ok"
    rule_id = result["rule_id"]
    assert isinstance(rule_id, str) and len(rule_id) > 0

    rules = list_rules()["rules"]
    ids = [r["id"] for r in rules]
    assert rule_id in ids


def test_add_rule_custom_priority(tmp_db):
    """add_rule with explicit priority must honour it."""
    result = add_rule(
        name="High-priority test",
        description="desc",
        rule_type="income",
        priority=5,
    )
    rule_id = result["rule_id"]
    rule = next(r for r in list_rules()["rules"] if r["id"] == rule_id)
    assert rule["priority"] == 5


def test_add_rule_invalid_type_raises(tmp_db):
    """add_rule with an unrecognised rule_type must raise ValueError."""
    with pytest.raises(ValueError, match="rule_type"):
        add_rule(name="Bad", description="bad", rule_type="garbage")


# ---------------------------------------------------------------------------
# update_rule tests
# ---------------------------------------------------------------------------


def test_update_rule_changes_fields(tmp_db):
    """update_rule must update only the supplied fields."""
    r = add_rule(name="Before", description="original desc", rule_type="spending")
    rule_id = r["rule_id"]

    result = update_rule(id=rule_id, name="After", priority=200)
    assert result["status"] == "ok"

    rule = next(r for r in list_rules()["rules"] if r["id"] == rule_id)
    assert rule["name"] == "After"
    assert rule["priority"] == 200
    assert rule["description"] == "original desc"  # unchanged


def test_update_rule_no_fields_is_noop(tmp_db):
    """update_rule with no fields provided must return ok without error."""
    r = add_rule(name="Noop test", description="desc", rule_type="skip")
    result = update_rule(id=r["rule_id"])
    assert result["status"] == "ok"


def test_update_rule_invalid_type_raises(tmp_db):
    """update_rule with an invalid rule_type must raise ValueError."""
    r = add_rule(name="Type test", description="desc", rule_type="spending")
    with pytest.raises(ValueError, match="rule_type"):
        update_rule(id=r["rule_id"], rule_type="nonsense")


# ---------------------------------------------------------------------------
# reorder_rules tests
# ---------------------------------------------------------------------------


def test_reorder_rules(tmp_db):
    """reorder_rules must assign priorities 10, 20, 30 ... in supplied order."""
    r1 = add_rule(name="R1", description="d1", rule_type="spending", priority=300)["rule_id"]
    r2 = add_rule(name="R2", description="d2", rule_type="income", priority=200)["rule_id"]
    r3 = add_rule(name="R3", description="d3", rule_type="skip", priority=100)["rule_id"]

    result = reorder_rules(rule_ids=[r3, r1, r2])
    assert result["status"] == "ok"

    by_id = {r["id"]: r for r in list_rules()["rules"]}
    assert by_id[r3]["priority"] == 10
    assert by_id[r1]["priority"] == 20
    assert by_id[r2]["priority"] == 30


# ---------------------------------------------------------------------------
# disable_rule / enable_rule tests
# ---------------------------------------------------------------------------


def test_disable_enable_rule(tmp_db):
    """disable_rule and enable_rule must toggle the enabled field."""
    r = add_rule(name="Toggle me", description="d", rule_type="transfer")
    rule_id = r["rule_id"]

    # starts enabled
    rule = next(x for x in list_rules()["rules"] if x["id"] == rule_id)
    assert rule["enabled"] is True

    assert disable_rule(id=rule_id)["status"] == "ok"
    rule = next(x for x in list_rules()["rules"] if x["id"] == rule_id)
    assert rule["enabled"] is False

    assert enable_rule(id=rule_id)["status"] == "ok"
    rule = next(x for x in list_rules()["rules"] if x["id"] == rule_id)
    assert rule["enabled"] is True


def test_disable_default_rule(tmp_db):
    """Default rules can be disabled (they just can't be deleted)."""
    default_rule = next(r for r in list_rules()["rules"] if r["is_default"])
    result = disable_rule(id=default_rule["id"])
    assert result["status"] == "ok"

    rule = next(r for r in list_rules()["rules"] if r["id"] == default_rule["id"])
    assert rule["enabled"] is False


# ---------------------------------------------------------------------------
# delete_rule tests
# ---------------------------------------------------------------------------


def test_delete_user_rule(tmp_db):
    """delete_rule on a user-created rule must succeed."""
    r = add_rule(name="Deletable", description="d", rule_type="spending")
    rule_id = r["rule_id"]

    result = delete_rule(id=rule_id)
    assert result["status"] == "ok"

    ids = [r["id"] for r in list_rules()["rules"]]
    assert rule_id not in ids


def test_delete_default_rule_refused(tmp_db):
    """delete_rule on a default rule must return an error."""
    default_rule = next(r for r in list_rules()["rules"] if r["is_default"])
    result = delete_rule(id=default_rule["id"])
    assert result["status"] == "error"
    assert "Cannot delete default rule" in result["message"]

    # Rule must still exist
    ids = [r["id"] for r in list_rules()["rules"]]
    assert default_rule["id"] in ids


def test_delete_nonexistent_rule(tmp_db):
    """delete_rule on an unknown ID must return an error."""
    result = delete_rule(id="nonexistent-id-xyz")
    assert result["status"] == "error"
