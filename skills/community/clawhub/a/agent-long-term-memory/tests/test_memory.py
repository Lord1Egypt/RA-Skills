"""
Tests for AgentMemory
"""
import sys, os, shutil
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tempfile
from src.memory import AgentMemory


def _setup():
    data_dir = tempfile.mkdtemp()
    mem = AgentMemory(data_dir)
    return mem, data_dir


def _teardown(mem, data_dir):
    mem.close()
    shutil.rmtree(data_dir, ignore_errors=True)


def test_basic_facts():
    mem, data_dir = _setup()
    try:
        fact_id = mem.remember("Test fact", tags=["test"])
        assert fact_id is not None
        facts = mem.recall("Test fact")
        assert len(facts) >= 1
        assert facts[0].content == "Test fact"
        assert "test" in facts[0].tags
        fact = mem.get_fact(fact_id)
        assert fact is not None
        assert fact.id == fact_id
        mem.forget(fact_id)
        fact = mem.get_fact(fact_id)
        assert fact is None
        print("[PASS] Basic facts test passed")
    finally:
        _teardown(mem, data_dir)


def test_lessons():
    mem, data_dir = _setup()
    try:
        lesson_id = mem.learn(action="Test action", context="testing",
                              outcome="positive", insight="Tests are good")
        assert lesson_id is not None
        lessons = mem.get_lessons(context="testing")
        assert len(lessons) >= 1
        assert lessons[0].action == "Test action"
        assert lessons[0].outcome == "positive"
        positive = mem.get_lessons(outcome="positive")
        assert len(positive) >= 1
        negative = mem.get_lessons(outcome="negative")
        assert len(negative) == 0
        print("[PASS] Lessons test passed")
    finally:
        _teardown(mem, data_dir)


def test_entities():
    mem, data_dir = _setup()
    try:
        entity_id = mem.track_entity("TestPerson", "person", {"role": "tester"})
        assert entity_id is not None
        entity = mem.get_entity("TestPerson", "person")
        assert entity is not None
        assert entity.name == "TestPerson"
        assert entity.attributes["role"] == "tester"
        mem.track_entity("TestPerson", "person", {"role": "senior tester"})
        entity = mem.get_entity("TestPerson", "person")
        assert entity.attributes["role"] == "senior tester"
        print("[PASS] Entities test passed")
    finally:
        _teardown(mem, data_dir)


def test_supersede():
    mem, data_dir = _setup()
    try:
        old_id = mem.remember("Old fact")
        new_id = mem.supersede(old_id, "New fact")
        old_fact = mem.get_fact(old_id)
        assert old_fact.superseded_by == new_id
        facts = mem.recall("fact")
        contents = [f.content for f in facts]
        assert "New fact" in contents
        print("[PASS] Supersede test passed")
    finally:
        _teardown(mem, data_dir)


def test_stats():
    mem, data_dir = _setup()
    try:
        mem.remember("Fact 1")
        mem.remember("Fact 2")
        mem.learn("Action", "context", "positive", "insight")
        mem.track_entity("Entity", "type", {})
        stats = mem.stats()
        assert stats["active_facts"] == 2
        assert stats["lessons"] == 1
        assert stats["entities"] == 1
        print("[PASS] Stats test passed")
    finally:
        _teardown(mem, data_dir)


def test_export():
    mem, data_dir = _setup()
    try:
        mem.remember("Export test fact", tags=["export"])
        mem.learn("Export action", "export", "neutral", "Export insight")
        mem.track_entity("ExportEntity", "test", {"key": "value"})
        data = mem.export_json()
        assert "exported_at" in data
        assert len(data["facts"]) >= 1
        assert len(data["lessons"]) >= 1
        assert len(data["entities"]) >= 1
        print("[PASS] Export test passed")
    finally:
        _teardown(mem, data_dir)


if __name__ == "__main__":
    test_basic_facts()
    test_lessons()
    test_entities()
    test_supersede()
    test_stats()
    test_export()
    print("\n[OK] All tests passed!")
