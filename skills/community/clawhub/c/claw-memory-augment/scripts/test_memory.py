#!/usr/bin/env python3
"""Test suite for memory-augment skill."""

import json
import sys
import uuid
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from memory import MemoryStore


def test_store_and_retrieve():
    """Test storing and retrieving memories."""
    store = MemoryStore()
    
    # Clear existing test memories
    store.memories = []
    
    # Store a memory
    mem_id = store.store("Test memory content", "test", tags=["test"])
    assert mem_id is not None, "Store should return an ID"
    
    # Retrieve it
    results = store.search("Test memory content")
    assert len(results) == 1, f"Should find 1 result, got {len(results)}"
    assert results[0]["content"] == "Test memory content"
    
    print("✅ Store and retrieve test passed")
    return True


def test_memory_types():
    """Test different memory types."""
    store = MemoryStore()
    store.memories = []
    
    # Store different types
    pref_id = store.store("User preference", "preference", tags=["test"])
    dec_id = store.store("User decision", "decision", tags=["test"])
    learn_id = store.store("Agent learning", "learning", tags=["test"])
    ctx_id = store.store("Session context", "context", tags=["test"])
    
    assert all([pref_id, dec_id, learn_id, ctx_id])
    
    print("✅ Memory types test passed")
    return True


def test_search_scoring():
    """Test search scoring algorithm."""
    store = MemoryStore()
    store.memories = []
    
    # Store memories with different relevance
    store.store("Very relevant content", "preference", tags=["test"])
    store.store("Somewhat relevant", "context", tags=["other"])
    store.store("Not relevant at all", "context", tags=["xyz"])
    
    # Search for the first one
    results = store.search("Very relevant")
    
    # First result should be the most relevant
    assert results[0]["score"] > results[1]["score"], "Scoring should prioritize relevance"
    
    print("✅ Search scoring test passed")
    return True


def test_tag_filtering():
    """Test tag-based filtering."""
    store = MemoryStore()
    store.memories = []
    
    store.store("Memory with tags", "context", tags=["test", "income"])
    store.store("Memory without income", "context", tags=["other"])
    store.store("Memory with both", "context", tags=["test", "income", "other"])
    
    # Search with tag
    results = store.search("Memory #income")
    
    # Should find income-tagged memories
    found_income = any("income" in r["tags"] for r in results)
    assert found_income, "Should find income-tagged memories"
    
    print("✅ Tag filtering test passed")
    return True


def test_expiry():
    """Test memory expiry logic."""
    store = MemoryStore()
    store.memories = []
    
    # Store permanent memory (no expiry)
    store.store("Permanent memory", "preference", tags=["test"])
    
    # Store temporary memory (has expiry)
    temp_id = store.store("Temporary memory", "context", tags=["test"])
    
    # Verify the stored memories
    assert any(m["expires"] is None for m in store.memories), "Preference should have no expiry"
    
    print("✅ Expiry test passed")
    return True


def test_import_export():
    """Test memory import/export."""
    store = MemoryStore()
    store.memories = []
    
    # Store some test data
    store.store("Export test 1", "test", tags=["export"])
    store.store("Export test 2", "test", tags=["export"])
    
    # Export to JSON
    exported = store.export()
    data = json.loads(exported)
    assert len(data["memories"]) == 2
    
    # Create new store and import
    store2 = MemoryStore()
    store2.memories = []
    store2.import_memories(exported)
    
    assert len(store2.memories) == 2, "Import should restore all memories"
    
    print("✅ Import/export test passed")
    return True


def run_tests():
    """Run all tests."""
    tests = [
        test_store_and_retrieve,
        test_memory_types,
        test_search_scoring,
        test_tag_filtering,
        test_expiry,
        test_import_export,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"Tests passed: {passed}/{len(tests)}")
    if failed > 0:
        print(f"Tests failed: {failed}/{len(tests)}")
        return False
    return True


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
