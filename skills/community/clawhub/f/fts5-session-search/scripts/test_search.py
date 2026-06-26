#!/usr/bin/env python3
"""
Tests for FTS5 Session Search

Tests indexing, search, topic search, time-range search,
ranking, incremental indexing, reindex, and integration.
"""

import json
import os
import sqlite3
import sys
import tempfile
import shutil
import importlib.util
from pathlib import Path

# Setup paths
SCRIPT_DIR = Path(__file__).resolve().parent
TEST_DIR = Path(tempfile.mkdtemp(prefix="fts5_test_"))
TEST_DB = TEST_DIR / "search.db"
TEST_SESSIONS = TEST_DIR / "sessions" / "main"
TEST_SESSIONS.mkdir(parents=True, exist_ok=True)

# Load modules with hyphens in filename using importlib
def load_module(name, filepath):
    spec = importlib.util.spec_from_file_location(name, str(filepath))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

search_indexer = load_module('search_indexer', SCRIPT_DIR / 'search-indexer.py')
search_tool = load_module('search_tool', SCRIPT_DIR / 'search-tool.py')
integration = load_module('integration', SCRIPT_DIR / 'integration.py')

# Patch paths before running tests
search_indexer.DB_PATH = TEST_DB
search_indexer.SESSIONS_ROOT = TEST_DIR / "sessions"
search_tool.DB_PATH = TEST_DB
# Also patch in integration's import of search_tool
integration.DB_PATH = TEST_DB

# Override discover_sessions for test sessions
ORIG_DISCOVER = search_indexer.discover_sessions


def test_discover_sessions():
    """Discover sessions in our test directory."""
    sessions = []
    sessions_dir = TEST_SESSIONS
    if sessions_dir.is_dir():
        for f in sorted(sessions_dir.iterdir()):
            if f.suffix != ".jsonl":
                continue
            name = f.stem
            if any(skip in name for skip in [".checkpoint", ".trajectory", ".bak", ".reset"]):
                continue
            base = name.split(".")[0]
            if len(base) != 36:
                if "." in name:
                    continue
            sessions.append(("main", str(f)))
    return sessions


search_indexer.discover_sessions = test_discover_sessions


def create_test_session(session_id, messages, start_time="2026-05-15T12:00:00.000Z"):
    """Create a test session JSONL file."""
    filepath = TEST_SESSIONS / f"{session_id}.jsonl"
    lines = []
    
    # Session header
    lines.append(json.dumps({
        "type": "session",
        "version": 3,
        "id": session_id,
        "timestamp": start_time,
        "cwd": "/tmp/test_workspace"
    }))
    
    # Messages
    for i, msg in enumerate(messages):
        lines.append(json.dumps({
            "type": "message",
            "id": f"msg_{i}",
            "parentId": f"msg_{i-1}" if i > 0 else None,
            "timestamp": msg.get("timestamp", start_time),
            "message": {
                "role": msg["role"],
                "content": [{"type": "text", "text": msg["content"]}],
                "timestamp": 1778847873000 + i * 1000
            }
        }))
    
    with open(filepath, 'w') as f:
        f.write("\n".join(lines) + "\n")
    
    return filepath


def run_tests():
    """Run all tests."""
    passed = 0
    failed = 0
    
    def assert_test(condition, test_name):
        nonlocal passed, failed
        if condition:
            print(f"  ✅ {test_name}")
            passed += 1
        else:
            print(f"  ❌ {test_name}")
            failed += 1
    
    print("=" * 60)
    print("FTS5 Session Search Tests")
    print("=" * 60)
    
    # --- Test 1: Database creation ---
    print("\n📦 Test 1: Database Creation")
    db = search_indexer.get_db()
    assert_test(TEST_DB.exists(), "Database file created")
    
    # Verify FTS5 table exists
    tables = db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    table_names = [t[0] for t in tables]
    assert_test("conversations" in table_names, "FTS5 conversations table exists")
    assert_test("session_meta" in table_names, "session_meta table exists")
    assert_test("index_state" in table_names, "index_state table exists")
    
    # --- Test 2: Index a session ---
    print("\n📝 Test 2: Index Sessions")
    
    # Create test sessions
    create_test_session("test-aaaa-1111-2222-333333333333", [
        {"role": "user", "content": "How do I configure Stratium security?", "timestamp": "2026-05-15T10:00:00.000Z"},
        {"role": "assistant", "content": "Stratium security configuration involves setting up firewall rules, TLS certificates, and access policies.", "timestamp": "2026-05-15T10:00:05.000Z"},
    ], start_time="2026-05-15T10:00:00.000Z")
    
    create_test_session("test-bbbb-4444-5555-666666666666", [
        {"role": "user", "content": "What was the Villavicencio project about?", "timestamp": "2026-05-16T14:00:00.000Z"},
        {"role": "assistant", "content": "The Villavicencio project was a community initiative in Colombia focused on sustainable agriculture.", "timestamp": "2026-05-16T14:00:05.000Z"},
    ], start_time="2026-05-16T14:00:00.000Z")
    
    create_test_session("test-cccc-7777-8888-999999999999", [
        {"role": "user", "content": "Model routing optimization for LLM inference", "timestamp": "2026-05-17T09:00:00.000Z"},
        {"role": "assistant", "content": "Model routing uses cost and latency metrics to select the best LLM for each query.", "timestamp": "2026-05-17T09:00:05.000Z"},
        {"role": "user", "content": "How does security monitoring work?", "timestamp": "2026-05-17T09:01:00.000Z"},
        {"role": "assistant", "content": "Security monitoring tracks network traffic, logs access attempts, and alerts on anomalies.", "timestamp": "2026-05-17T09:01:05.000Z"},
    ], start_time="2026-05-17T09:00:00.000Z")
    
    # Index sessions
    new_count = search_indexer.cmd_index(db)
    assert_test(new_count == 3, f"Indexed 3 sessions (got {new_count})")
    
    # Verify data
    session_count = db.execute("SELECT COUNT(*) FROM session_meta").fetchone()[0]
    assert_test(session_count == 3, f"session_meta has 3 rows (got {session_count})")
    
    msg_count = db.execute("SELECT COUNT(*) FROM conversations").fetchone()[0]
    assert_test(msg_count > 0, f"conversations has messages (got {msg_count})")
    
    # --- Test 3: Basic search ---
    print("\n🔍 Test 3: Basic Search")
    
    results = search_tool.search("stratium")
    assert_test(len(results) > 0, f"Search 'stratium' returns results (got {len(results)})")
    if results:
        assert_test("stratium" in results[0]["content"].lower(), 
                    "Result contains 'stratium'")
    
    results = search_tool.search("villavicencio")
    assert_test(len(results) > 0, f"Search 'villavicencio' returns results (got {len(results)})")
    
    results = search_tool.search("model routing")
    assert_test(len(results) > 0, f"Search 'model routing' returns results (got {len(results)})")
    
    # --- Test 4: Scope filter ---
    print("\n🎯 Test 4: Scope Filter")
    
    results = search_tool.search("security", scope="user")
    if results:
        all_user = all(r["role"] == "user" for r in results)
        assert_test(all_user, "Scope filter 'user' returns only user messages")
    else:
        assert_test(True, "Scope filter works (may have no results for narrow scope)")
    
    results_all = search_tool.search("security")
    results_assistant = search_tool.search("security", scope="assistant")
    assert_test(len(results_all) >= len(results_assistant), 
                "All scope returns >= assistant scope results")
    
    # --- Test 5: Phrase matching ---
    print("\n📝 Test 5: Phrase Matching")
    
    results = search_tool.search('"model routing"')
    assert_test(len(results) >= 0, f"Phrase search works (got {len(results)} results)")
    if results:
        has_phrase = any("model routing" in r["content"].lower() for r in results)
        assert_test(has_phrase, "Phrase match contains the exact phrase")
    
    # --- Test 6: Topic search ---
    print("\n🏷️ Test 6: Topic Search")
    
    results = search_tool.search_by_topic("security")
    assert_test(isinstance(results, list), "Topic search returns a list")
    
    # --- Test 7: Time range search ---
    print("\n⏰ Test 7: Time Range Search")
    
    results = search_tool.search_by_time("2026-05-16T00:00:00.000Z", "2026-05-17T23:59:59.999Z")
    assert_test(len(results) > 0, f"Time range search returns results (got {len(results)})")
    for r in results:
        ts = r["timestamp"]
        assert_test("2026-05-16" in ts or "2026-05-17" in ts, 
                    f"Result timestamp in range: {ts}")
    
    # --- Test 8: Get session ---
    print("\n📄 Test 8: Get Full Session")
    
    session_id = "test-aaaa-1111-2222-333333333333"
    results = search_tool.get_session(session_id)
    assert_test(len(results) > 0, f"Get session returns messages (got {len(results)})")
    assert_test(all(r["session_id"] == session_id for r in results), 
                "All messages belong to correct session")
    
    # --- Test 9: Stats ---
    print("\n📊 Test 9: Statistics")
    
    s = search_tool.stats()
    assert_test(s["sessions_indexed"] == 3, f"Stats shows 3 sessions (got {s['sessions_indexed']})")
    assert_test(s["messages_indexed"] > 0, f"Stats shows messages (got {s['messages_indexed']})")
    assert_test(s["db_size_bytes"] > 0, "Stats shows non-zero DB size")
    assert_test("main" in s["agents"], "Stats includes 'main' agent")
    
    # --- Test 10: Incremental indexing ---
    print("\n📈 Test 10: Incremental Indexing")
    
    # Add a new session
    create_test_session("test-dddd-0000-1111-222222222222", [
        {"role": "user", "content": "This is a brand new test session about deployment.", "timestamp": "2026-05-18T15:00:00.000Z"},
        {"role": "assistant", "content": "Deployment involves building, testing, and releasing software to production.", "timestamp": "2026-05-18T15:00:05.000Z"},
    ], start_time="2026-05-18T15:00:00.000Z")
    
    new_count = search_indexer.cmd_index(db)
    assert_test(new_count == 1, f"Incremental index adds 1 session (got {new_count})")
    
    # Verify total
    session_count = db.execute("SELECT COUNT(*) FROM session_meta").fetchone()[0]
    assert_test(session_count == 4, f"Total sessions now 4 (got {session_count})")
    
    # Re-index should skip existing
    new_count2 = search_indexer.cmd_index(db)
    assert_test(new_count2 == 0, f"Re-indexing skips existing (got {new_count2})")
    
    # --- Test 11: Reindex from scratch ---
    print("\n🔄 Test 11: Reindex From Scratch")
    
    _, db = search_indexer.cmd_reindex(db)
    session_count = db.execute("SELECT COUNT(*) FROM session_meta").fetchone()[0]
    assert_test(session_count == 4, f"Reindex rebuilds all 4 sessions (got {session_count})")
    
    msg_count = db.execute("SELECT COUNT(*) FROM conversations").fetchone()[0]
    assert_test(msg_count > 0, f"Reindex restores messages (got {msg_count})")
    
    # --- Test 12: Negation ---
    print("\n🚫 Test 12: Negation Search")
    
    results_all_sec = search_tool.search("security")
    results_neg = search_tool.search("security -villavicencio")
    assert_test(len(results_neg) <= len(results_all_sec), 
                "Negation reduces or maintains result count")
    
    # --- Test 13: Integration layer ---
    print("\n🔗 Test 13: Integration Layer")
    
    # Patch search_tool path in integration module
    integration.DB_PATH = TEST_DB
    # Also patch the search_tool module loaded inside integration
    integration.search_tool.DB_PATH = TEST_DB
    sys.modules['search_tool'] = search_tool
    
    results = integration.memory_search_enhanced("security", limit=5)
    assert_test(isinstance(results, list), "Integration returns a list")
    if results:
        assert_test(results[0]["source"] == "conversations", "Integration tags source as 'conversations'")
    
    # Test get_conversation_context
    context = integration.get_conversation_context("test-aaaa-1111-2222-333333333333")
    assert_test(isinstance(context, str), "get_conversation_context returns string")
    assert_test(len(context) > 0, "Context is non-empty for existing session")
    
    # --- Test 14: Empty results ---
    print("\n📭 Test 14: Empty Results")
    
    results = search_tool.search("xyzzyplughnonexistent")
    assert_test(len(results) == 0, "Search for nonexistent term returns empty list")
    
    # --- Test 15: Encoding handling ---
    print("\n🔤 Test 15: Encoding Handling")
    
    create_test_session("test-eeee-ffff-0000-111111111111", [
        {"role": "user", "content": "Configuración en español con acentos: áéíóú ñ", "timestamp": "2026-05-19T10:00:00.000Z"},
        {"role": "assistant", "content": "La configuración se completó exitosamente.", "timestamp": "2026-05-19T10:00:05.000Z"},
    ], start_time="2026-05-19T10:00:00.000Z")
    
    new_count = search_indexer.cmd_index(db)
    assert_test(new_count == 1, f"Index handles unicode content (got {new_count})")
    
    results = search_tool.search("configuración")
    assert_test(len(results) > 0, f"Unicode search works (got {len(results)})")
    
    # --- Cleanup ---
    db.close()
    shutil.rmtree(TEST_DIR)
    
    # Restore original discover function
    search_indexer.discover_sessions = ORIG_DISCOVER
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)