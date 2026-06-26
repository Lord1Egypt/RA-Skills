"""Tests for scripts/store.py — MetricsStore CRUD and metrics queries."""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from scripts.store import MetricsStore


@pytest.fixture
def store(tmp_path):
    db = MetricsStore(db_path=str(tmp_path / "test.db"))
    yield db
    db.close()


# --- tool_invocations ---

def test_record_tool_invocation_success(store):
    store.record_tool_invocation("Read", success=True, duration_ms=42.5,
                                  session_id="s1", agent_id="main")
    stats = store.get_tool_stats(hours=24)
    assert len(stats) == 1
    row = stats[0]
    assert row["tool_name"] == "Read"
    assert row["total_calls"] == 1
    assert row["successes"] == 1
    assert row["failures"] == 0
    assert abs(row["avg_duration_ms"] - 42.5) < 0.01


def test_record_tool_invocation_failure(store):
    store.record_tool_invocation("Bash", success=False, error_message="timeout",
                                  session_id="s1")
    stats = store.get_tool_stats(hours=24)
    row = stats[0]
    assert row["tool_name"] == "Bash"
    assert row["failures"] == 1
    assert row["successes"] == 0


def test_tool_history_upsert(store):
    store.record_tool_invocation("Read", success=True)
    store.record_tool_invocation("Read", success=True)
    store.record_tool_invocation("Read", success=False)

    cur = store.conn.execute("SELECT total_calls, total_failures FROM tool_history WHERE tool_name='Read'")
    row = cur.fetchone()
    assert row["total_calls"] == 3
    assert row["total_failures"] == 1


def test_get_recent_tool_failures(store):
    store.record_tool_invocation("Grep", success=True)
    store.record_tool_invocation("Grep", success=False, error_message="err1")
    store.record_tool_invocation("Grep", success=False, error_message="err2")

    failures = store.get_recent_tool_failures("Grep", limit=10)
    assert len(failures) == 2
    assert all(f["success"] == 0 for f in failures)


def test_get_recent_tool_failures_limit(store):
    for i in range(5):
        store.record_tool_invocation("Edit", success=False)
    failures = store.get_recent_tool_failures("Edit", limit=3)
    assert len(failures) == 3


def test_get_consecutive_failures_all_failures(store):
    for _ in range(4):
        store.record_tool_invocation("Write", success=False)
    assert store.get_consecutive_failures("Write") == 4


def test_get_consecutive_failures_resets_on_success(store):
    store.record_tool_invocation("Write", success=False)
    store.record_tool_invocation("Write", success=False)
    store.record_tool_invocation("Write", success=True)   # breaks streak
    store.record_tool_invocation("Write", success=False)
    store.record_tool_invocation("Write", success=False)
    assert store.get_consecutive_failures("Write") == 2


def test_get_consecutive_failures_no_data(store):
    assert store.get_consecutive_failures("UnknownTool") == 0


def test_is_tool_known_true(store):
    store.record_tool_invocation("Read", success=True)
    assert store.is_tool_known("Read") is True


def test_is_tool_known_false(store):
    assert store.is_tool_known("NonExistentTool") is False


# --- llm_calls ---

def test_record_llm_call(store):
    store.record_llm_call(model="claude-sonnet-4-20250514",
                           tokens_in=1000, tokens_out=200,
                           latency_ms=1500.0, estimated_cost_usd=0.05,
                           session_id="s1", agent_id="main")
    summary = store.get_cost_summary(hours=24)
    assert summary["total_cost_usd"] == 0.05
    assert summary["total_tokens"] == 1200
    assert len(summary["by_model"]) == 1
    assert summary["by_model"][0]["model"] == "claude-sonnet-4-20250514"
    assert summary["by_model"][0]["call_count"] == 1


def test_cost_summary_multiple_models(store):
    store.record_llm_call(model="model-a", estimated_cost_usd=0.10,
                           tokens_in=500, tokens_out=100)
    store.record_llm_call(model="model-b", estimated_cost_usd=0.20,
                           tokens_in=800, tokens_out=200)
    summary = store.get_cost_summary(hours=24)
    assert abs(summary["total_cost_usd"] - 0.30) < 0.0001
    assert summary["total_tokens"] == 1600
    assert len(summary["by_model"]) == 2


def test_get_hourly_cost(store):
    store.record_llm_call(model="m", estimated_cost_usd=0.03)
    store.record_llm_call(model="m", estimated_cost_usd=0.07)
    assert abs(store.get_hourly_cost(hours=1) - 0.10) < 0.0001


def test_get_hourly_cost_empty(store):
    assert store.get_hourly_cost(hours=1) == 0.0


def test_cost_summary_null_costs(store):
    store.record_llm_call(model="m", tokens_in=100, tokens_out=50)  # no cost
    summary = store.get_cost_summary(hours=24)
    assert summary["total_cost_usd"] == 0.0


# --- sessions ---

def test_upsert_session_insert(store):
    store.upsert_session("sess-abc", agent_id="main", started_at="2026-01-01T00:00:00")
    cur = store.conn.execute("SELECT * FROM sessions WHERE session_id='sess-abc'")
    row = cur.fetchone()
    assert row is not None
    assert row["agent_id"] == "main"


def test_upsert_session_update_ended_at(store):
    store.upsert_session("sess-abc", started_at="2026-01-01T00:00:00")
    store.upsert_session("sess-abc", ended_at="2026-01-01T01:00:00")
    cur = store.conn.execute("SELECT ended_at FROM sessions WHERE session_id='sess-abc'")
    row = cur.fetchone()
    assert row["ended_at"] == "2026-01-01T01:00:00"


def test_upsert_session_idempotent(store):
    store.upsert_session("sess-abc")
    store.upsert_session("sess-abc")
    cur = store.conn.execute("SELECT COUNT(*) as cnt FROM sessions WHERE session_id='sess-abc'")
    assert cur.fetchone()["cnt"] == 1


def test_get_session_summary(store):
    store.upsert_session("s1", agent_id="main", started_at="2026-01-01T00:00:00")
    store.record_tool_invocation("Read", success=True, session_id="s1")
    store.record_llm_call(model="m", estimated_cost_usd=0.05, session_id="s1")

    rows = store.get_session_summary()
    assert len(rows) == 1
    r = rows[0]
    assert r["session_id"] == "s1"
    assert r["tool_calls"] == 1
    assert r["llm_calls"] == 1
    assert abs(r["total_cost"] - 0.05) < 0.0001


# --- alerts ---

def test_record_and_get_alerts(store):
    store.record_alert("warning", "high_cost", "Cost exceeded $1/hr",
                        details={"cost": 1.5})
    alerts = store.get_recent_alerts()
    assert len(alerts) == 1
    a = alerts[0]
    assert a["severity"] == "warning"
    assert a["alert_type"] == "high_cost"
    assert "Cost exceeded" in a["message"]


def test_get_recent_alerts_limit(store):
    for i in range(10):
        store.record_alert("info", "test", f"msg {i}")
    alerts = store.get_recent_alerts(limit=5)
    assert len(alerts) == 5


def test_get_last_alert_time_exists(store):
    store.record_alert("critical", "tool_failure", "Tool failed")
    t = store.get_last_alert_time("tool_failure")
    assert t is not None


def test_get_last_alert_time_missing(store):
    result = store.get_last_alert_time("nonexistent_type")
    assert result is None


# --- activity timeline ---

def test_get_activity_timeline_empty(store):
    timeline = store.get_activity_timeline(hours=24)
    assert timeline == []


def test_get_activity_timeline_has_data(store):
    store.record_tool_invocation("Read", success=True)
    store.record_tool_invocation("Read", success=False)
    timeline = store.get_activity_timeline(hours=24, bucket_minutes=30)
    assert len(timeline) >= 1
    bucket = timeline[0]
    assert "bucket" in bucket
    assert "event_count" in bucket
    assert bucket["event_count"] == 2


# --- dashboard summary ---

def test_get_dashboard_summary_structure(store):
    summary = store.get_dashboard_summary()
    assert "tool_stats_24h" in summary
    assert "cost_summary_24h" in summary
    assert "recent_alerts" in summary
    assert "activity_timeline" in summary
    assert "sessions" in summary
