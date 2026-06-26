"""
tests/test_hints.py — Tests for add_hint, list_hints, remove_hint MCP tools.

Covers:
- add_hint creates a new hint and returns {created: True, id: str, text: str}
- add_hint with duplicate text returns {created: False, id: <same id>}
- add_hint with empty / whitespace raises ValueError
- list_hints returns all hints
- remove_hint deletes a row and returns {ok: True, removed: True}
- remove_hint with missing id returns {ok: True, removed: False}
"""

from __future__ import annotations

import pytest

from server.db import init_db
from server.main import add_hint, list_hints, remove_hint

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
# add_hint tests
# ---------------------------------------------------------------------------


def test_add_hint_creates_new(tmp_db):
    result = add_hint("Amazon is shopping")
    assert result["created"] is True
    assert result["text"] == "Amazon is shopping"
    assert isinstance(result["id"], str)
    assert len(result["id"]) > 0


def test_add_hint_deduplicates(tmp_db):
    first = add_hint("Amazon is shopping")
    assert first["created"] is True

    second = add_hint("Amazon is shopping")
    assert second["created"] is False
    assert second["id"] == first["id"]
    assert second["text"] == "Amazon is shopping"


def test_add_hint_empty_raises(tmp_db):
    with pytest.raises(ValueError):
        add_hint("")


def test_add_hint_whitespace_raises(tmp_db):
    with pytest.raises(ValueError):
        add_hint("   ")


# ---------------------------------------------------------------------------
# list_hints tests
# ---------------------------------------------------------------------------


def test_list_hints_returns_all(tmp_db):
    add_hint("Uber is transportation")
    add_hint("Whole Foods is groceries")

    result = list_hints()
    assert "hints" in result
    texts = [h["text"] for h in result["hints"]]
    assert "Uber is transportation" in texts
    assert "Whole Foods is groceries" in texts
    assert len(result["hints"]) == 2


def test_list_hints_empty(tmp_db):
    result = list_hints()
    assert result == {"hints": []}


# ---------------------------------------------------------------------------
# remove_hint tests
# ---------------------------------------------------------------------------


def test_remove_hint_existing(tmp_db):
    created = add_hint("Netflix is entertainment")
    hint_id = created["id"]

    result = remove_hint(hint_id)
    assert result == {"ok": True, "removed": True}

    # Confirm it's gone
    remaining = list_hints()
    assert all(h["id"] != hint_id for h in remaining["hints"])


def test_remove_hint_missing_id(tmp_db):
    result = remove_hint("nonexistent-id-00000")
    assert result == {"ok": True, "removed": False}
