"""Tests for scripts/parser.py — EventParser with real OpenClaw transcript format."""

import json
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from scripts.parser import EventParser


@pytest.fixture
def parser():
    return EventParser(openclaw_state_dir="/nonexistent")


# --- _classify_event: session ---

def test_classify_session_event(parser):
    raw = {
        "type": "session",
        "id": "1e0ea219-cd85-4885-9cca-ec6c48a3f006",
        "timestamp": "2026-03-21T17:02:29.127Z",
        "version": 3,
        "cwd": "/home/fiddy/.openclaw/workspace",
    }
    events = parser._classify_event(raw)
    assert len(events) == 1
    e = events[0]
    assert e["event_type"] == "session_start"
    assert e["session_id"] == "1e0ea219-cd85-4885-9cca-ec6c48a3f006"
    assert e["timestamp"] == "2026-03-21T17:02:29.127Z"


# --- _classify_event: ignored types ---

def test_classify_model_change_ignored(parser):
    raw = {"type": "model_change", "id": "e52d8d45", "provider": "anthropic"}
    assert parser._classify_event(raw) == []


def test_classify_custom_ignored(parser):
    raw = {"type": "custom", "customType": "model-snapshot", "data": {}}
    assert parser._classify_event(raw) == []


def test_classify_thinking_level_change_ignored(parser):
    raw = {"type": "thinking_level_change", "thinkingLevel": "low"}
    assert parser._classify_event(raw) == []


# --- _classify_event: assistant message with tool call ---

def test_classify_assistant_tool_call(parser):
    raw = {
        "type": "message",
        "id": "a1662928",
        "timestamp": "2026-03-21T17:02:36.261Z",
        "message": {
            "role": "assistant",
            "content": [
                {
                    "type": "thinking",
                    "thinking": "I need to read a file.",
                },
                {
                    "type": "toolCall",
                    "id": "toolu_012i86kkVSTwLPAgXQCfBeAB",
                    "name": "read",
                    "arguments": {"path": "BOOTSTRAP.md"},
                },
            ],
            "usage": {},
            "model": "claude-sonnet-4-20250514",
        },
    }
    events = parser._classify_event(raw)
    tool_starts = [e for e in events if e["event_type"] == "tool_call_start"]
    assert len(tool_starts) == 1
    e = tool_starts[0]
    assert e["tool_name"] == "read"
    assert e["tool_id"] == "toolu_012i86kkVSTwLPAgXQCfBeAB"
    assert e["timestamp"] == "2026-03-21T17:02:36.261Z"
    assert "BOOTSTRAP" in e["params_summary"]


def test_classify_assistant_multiple_tool_calls(parser):
    raw = {
        "type": "message",
        "timestamp": "2026-03-21T17:10:00.000Z",
        "message": {
            "role": "assistant",
            "content": [
                {"type": "toolCall", "id": "t1", "name": "read", "arguments": {"path": "a.md"}},
                {"type": "toolCall", "id": "t2", "name": "write", "arguments": {"path": "b.md", "content": "x"}},
            ],
            "usage": {},
        },
    }
    events = parser._classify_event(raw)
    tool_starts = [e for e in events if e["event_type"] == "tool_call_start"]
    assert len(tool_starts) == 2
    names = {e["tool_name"] for e in tool_starts}
    assert names == {"read", "write"}


# --- _classify_event: assistant message with usage ---

def test_classify_assistant_llm_usage(parser):
    raw = {
        "type": "message",
        "timestamp": "2026-03-21T17:02:36.261Z",
        "message": {
            "role": "assistant",
            "content": [],
            "model": "claude-sonnet-4-20250514",
            "usage": {
                "input": 10,
                "output": 221,
                "cacheRead": 0,
                "cacheWrite": 12492,
                "totalTokens": 12723,
                "cost": {
                    "input": 0.00003,
                    "output": 0.003315,
                    "cacheRead": 0,
                    "cacheWrite": 0.046845,
                    "total": 0.05019,
                },
            },
        },
    }
    events = parser._classify_event(raw)
    llm_events = [e for e in events if e["event_type"] == "llm_call"]
    assert len(llm_events) == 1
    e = llm_events[0]
    assert e["model"] == "claude-sonnet-4-20250514"
    assert e["tokens_in"] == 10   # input + cacheRead (0)
    assert e["tokens_out"] == 221
    assert abs(e["total_cost"] - 0.05019) < 1e-6


def test_classify_assistant_usage_with_cache_read(parser):
    raw = {
        "type": "message",
        "timestamp": "2026-03-21T17:05:00.000Z",
        "message": {
            "role": "assistant",
            "content": [],
            "model": "claude-sonnet-4-20250514",
            "usage": {
                "input": 6,
                "output": 215,
                "cacheRead": 12092,
                "cacheWrite": 703,
                "cost": {"total": 0.009506},
            },
        },
    }
    events = parser._classify_event(raw)
    llm_events = [e for e in events if e["event_type"] == "llm_call"]
    assert len(llm_events) == 1
    e = llm_events[0]
    # tokens_in = input + cacheRead
    assert e["tokens_in"] == 6 + 12092


def test_classify_assistant_no_usage_no_llm_event(parser):
    raw = {
        "type": "message",
        "timestamp": "2026-03-21T17:00:00.000Z",
        "message": {
            "role": "assistant",
            "content": [{"type": "text", "text": "Hello"}],
        },
    }
    events = parser._classify_event(raw)
    llm_events = [e for e in events if e["event_type"] == "llm_call"]
    assert len(llm_events) == 0


# --- _classify_event: tool result ---

def test_classify_tool_result_success(parser):
    raw = {
        "type": "message",
        "id": "9dafbb28",
        "timestamp": "2026-03-21T17:02:36.386Z",
        "message": {
            "role": "toolResult",
            "toolCallId": "toolu_012i86kkVSTwLPAgXQCfBeAB",
            "toolName": "read",
            "content": [{"type": "text", "text": "# BOOTSTRAP.md\nContent here..."}],
            "isError": False,
        },
    }
    events = parser._classify_event(raw)
    assert len(events) == 1
    e = events[0]
    assert e["event_type"] == "tool_call_end"
    assert e["tool_name"] == "read"
    assert e["tool_id"] == "toolu_012i86kkVSTwLPAgXQCfBeAB"
    assert e["success"] is True
    assert e["error_message"] is None


def test_classify_tool_result_explicit_error(parser):
    raw = {
        "type": "message",
        "timestamp": "2026-03-21T17:00:00.000Z",
        "message": {
            "role": "toolResult",
            "toolCallId": "t1",
            "toolName": "bash",
            "content": [{"type": "text", "text": "Command failed with exit code 1"}],
            "isError": True,
        },
    }
    events = parser._classify_event(raw)
    e = events[0]
    assert e["success"] is False
    assert e["error_message"] is not None


def test_classify_tool_result_heuristic_error_detection(parser):
    """isError=False but content contains error keywords — should be detected as failure."""
    raw = {
        "type": "message",
        "timestamp": "2026-03-21T17:00:00.000Z",
        "message": {
            "role": "toolResult",
            "toolCallId": "t1",
            "toolName": "bash",
            "content": [{"type": "text", "text": "Traceback (most recent call last):\n  File 'foo.py'..."}],
            "isError": False,
        },
    }
    events = parser._classify_event(raw)
    e = events[0]
    assert e["success"] is False


def test_classify_tool_result_string_content(parser):
    raw = {
        "type": "message",
        "timestamp": "2026-03-21T17:00:00.000Z",
        "message": {
            "role": "toolResult",
            "toolCallId": "t1",
            "toolName": "write",
            "content": "Successfully wrote 542 bytes to USER.md",
            "isError": False,
        },
    }
    events = parser._classify_event(raw)
    e = events[0]
    assert e["success"] is True


def test_classify_tool_result_error_message_truncated(parser):
    long_error = "error: " + "x" * 600
    raw = {
        "type": "message",
        "timestamp": "2026-03-21T17:00:00.000Z",
        "message": {
            "role": "toolResult",
            "toolCallId": "t1",
            "toolName": "bash",
            "content": [{"type": "text", "text": long_error}],
            "isError": True,
        },
    }
    events = parser._classify_event(raw)
    e = events[0]
    assert len(e["error_message"]) == 500


# --- _summarize_params ---

def test_summarize_params_short(parser):
    result = parser._summarize_params({"path": "README.md"})
    assert "README.md" in result
    assert not result.endswith("...")


def test_summarize_params_long_truncated(parser):
    big = {"content": "x" * 300}
    result = parser._summarize_params(big)
    assert result.endswith("...")
    assert len(result) == 203  # 200 + "..."


def test_summarize_params_empty(parser):
    assert parser._summarize_params({}) == ""
    assert parser._summarize_params(None) == ""


# --- parse_transcript_incremental ---

def test_parse_real_format_session_and_tool_call(tmp_path):
    """Parse a minimal real-format .jsonl file matching actual OpenClaw transcript structure."""
    transcript = tmp_path / "session.jsonl"
    lines = [
        # Session start
        json.dumps({
            "type": "session",
            "version": 3,
            "id": "test-session-001",
            "timestamp": "2026-03-21T17:02:29.127Z",
            "cwd": "/workspace",
        }),
        # model_change (should be ignored)
        json.dumps({
            "type": "model_change",
            "id": "abc",
            "provider": "anthropic",
            "modelId": "claude-sonnet-4-20250514",
        }),
        # Assistant message with tool call + usage
        json.dumps({
            "type": "message",
            "id": "msg-001",
            "timestamp": "2026-03-21T17:02:36.261Z",
            "message": {
                "role": "assistant",
                "content": [
                    {
                        "type": "toolCall",
                        "id": "toolu_abc123",
                        "name": "read",
                        "arguments": {"path": "BOOTSTRAP.md"},
                    }
                ],
                "model": "claude-sonnet-4-20250514",
                "usage": {
                    "input": 10,
                    "output": 221,
                    "cacheRead": 0,
                    "cacheWrite": 12492,
                    "cost": {"total": 0.05019},
                },
            },
        }),
        # Tool result
        json.dumps({
            "type": "message",
            "id": "msg-002",
            "timestamp": "2026-03-21T17:02:36.386Z",
            "message": {
                "role": "toolResult",
                "toolCallId": "toolu_abc123",
                "toolName": "read",
                "content": [{"type": "text", "text": "# BOOTSTRAP.md\nHello, World"}],
                "isError": False,
            },
        }),
    ]
    transcript.write_text("\n".join(lines) + "\n")

    p = EventParser(openclaw_state_dir="/nonexistent")
    events = list(p.parse_transcript_incremental(str(transcript)))

    event_types = [e["event_type"] for e in events]
    assert "session_start" in event_types
    assert "tool_call_start" in event_types
    assert "llm_call" in event_types
    assert "tool_call_end" in event_types

    session = next(e for e in events if e["event_type"] == "session_start")
    assert session["session_id"] == "test-session-001"

    tool_start = next(e for e in events if e["event_type"] == "tool_call_start")
    assert tool_start["tool_name"] == "read"

    tool_end = next(e for e in events if e["event_type"] == "tool_call_end")
    assert tool_end["success"] is True

    llm = next(e for e in events if e["event_type"] == "llm_call")
    assert llm["model"] == "claude-sonnet-4-20250514"
    assert llm["tokens_in"] == 10
    assert abs(llm["total_cost"] - 0.05019) < 1e-6


def test_parse_transcript_incremental_seek(tmp_path):
    """Second call should only yield new lines (incremental seek)."""
    transcript = tmp_path / "session.jsonl"
    line1 = json.dumps({"type": "session", "id": "s1", "timestamp": "2026-01-01T00:00:00Z"})
    transcript.write_text(line1 + "\n")

    p = EventParser(openclaw_state_dir="/nonexistent")
    first = list(p.parse_transcript_incremental(str(transcript)))
    assert len(first) == 1

    # Append a new line
    line2 = json.dumps({"type": "session", "id": "s2", "timestamp": "2026-01-01T00:01:00Z"})
    with open(str(transcript), "a") as f:
        f.write(line2 + "\n")

    second = list(p.parse_transcript_incremental(str(transcript)))
    assert len(second) == 1
    assert second[0]["session_id"] == "s2"


# --- state persistence ---

def test_save_and_load_state(tmp_path):
    """Positions saved by one parser instance are restored by the next."""
    transcript = tmp_path / "session.jsonl"
    line1 = json.dumps({"type": "session", "id": "s1", "timestamp": "2026-01-01T00:00:00Z"})
    transcript.write_text(line1 + "\n")

    state_file = tmp_path / "data" / "parser_state.json"
    p1 = EventParser(openclaw_state_dir="/nonexistent", state_path=str(state_file))
    list(p1.parse_transcript_incremental(str(transcript)))
    p1.save_state()

    assert state_file.exists()

    # New instance — should resume from saved position, not re-parse
    line2 = json.dumps({"type": "session", "id": "s2", "timestamp": "2026-01-01T00:01:00Z"})
    with open(str(transcript), "a") as f:
        f.write(line2 + "\n")

    p2 = EventParser(openclaw_state_dir="/nonexistent", state_path=str(state_file))
    events = list(p2.parse_transcript_incremental(str(transcript)))
    assert len(events) == 1
    assert events[0]["session_id"] == "s2"


def test_save_state_creates_parent_dir(tmp_path):
    state_file = tmp_path / "nested" / "deep" / "state.json"
    p = EventParser(openclaw_state_dir="/nonexistent", state_path=str(state_file))
    p._last_positions["/some/file.jsonl"] = 42
    p.save_state()
    assert state_file.exists()
    assert json.loads(state_file.read_text()) == {"/some/file.jsonl": 42}


def test_load_state_corrupt_file(tmp_path):
    state_file = tmp_path / "state.json"
    state_file.write_text("not valid json{{{")
    p = EventParser(openclaw_state_dir="/nonexistent", state_path=str(state_file))
    assert p._last_positions == {}


def test_no_state_path_save_is_noop(tmp_path):
    """Parser without state_path should not crash on save_state."""
    p = EventParser(openclaw_state_dir="/nonexistent")
    p.save_state()  # should not raise


def test_parse_transcript_invalid_json_skipped(tmp_path):
    transcript = tmp_path / "session.jsonl"
    lines = [
        "not valid json!!!",
        json.dumps({"type": "session", "id": "ok", "timestamp": "2026-01-01T00:00:00Z"}),
        "{broken",
    ]
    transcript.write_text("\n".join(lines) + "\n")

    p = EventParser(openclaw_state_dir="/nonexistent")
    events = list(p.parse_transcript_incremental(str(transcript)))
    assert len(events) == 1
    assert events[0]["session_id"] == "ok"


def test_parse_transcript_missing_file(tmp_path):
    p = EventParser(openclaw_state_dir="/nonexistent")
    events = list(p.parse_transcript_incremental(str(tmp_path / "missing.jsonl")))
    assert events == []


def test_parse_transcript_empty_lines_skipped(tmp_path):
    transcript = tmp_path / "session.jsonl"
    transcript.write_text("\n\n\n")
    p = EventParser(openclaw_state_dir="/nonexistent")
    events = list(p.parse_transcript_incremental(str(transcript)))
    assert events == []


# --- discover_agents / discover_sessions ---

def test_discover_agents(tmp_path):
    (tmp_path / "agents" / "main").mkdir(parents=True)
    (tmp_path / "agents" / "worker").mkdir(parents=True)

    p = EventParser(openclaw_state_dir=str(tmp_path))
    agents = p.discover_agents()
    assert set(agents) == {"main", "worker"}


def test_discover_agents_no_dir(tmp_path):
    p = EventParser(openclaw_state_dir=str(tmp_path / "nonexistent"))
    assert p.discover_agents() == []


def test_discover_sessions(tmp_path):
    sessions_dir = tmp_path / "agents" / "main" / "sessions"
    sessions_dir.mkdir(parents=True)
    (sessions_dir / "abc.jsonl").write_text("")
    (sessions_dir / "def.jsonl").write_text("")
    (sessions_dir / "not_a_transcript.txt").write_text("")

    p = EventParser(openclaw_state_dir=str(tmp_path))
    sessions = p.discover_sessions("main")
    basenames = [os.path.basename(s) for s in sessions]
    assert "abc.jsonl" in basenames
    assert "def.jsonl" in basenames
    assert "not_a_transcript.txt" not in basenames


def test_discover_sessions_no_dir(tmp_path):
    p = EventParser(openclaw_state_dir=str(tmp_path))
    assert p.discover_sessions("nonexistent_agent") == []


# --- scan_all integration ---

def test_scan_all(tmp_path):
    sessions_dir = tmp_path / "agents" / "main" / "sessions"
    sessions_dir.mkdir(parents=True)
    line = json.dumps({"type": "session", "id": "scan-s1", "timestamp": "2026-01-01T00:00:00Z"})
    (sessions_dir / "session.jsonl").write_text(line + "\n")

    p = EventParser(openclaw_state_dir=str(tmp_path))
    events = list(p.scan_all())
    assert len(events) == 1
    assert events[0]["session_id"] == "scan-s1"
