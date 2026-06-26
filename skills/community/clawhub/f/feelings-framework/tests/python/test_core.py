"""
Feelings Framework — Python Tests
"""

import json
import tempfile
from pathlib import Path

import pytest

from feelings import FeelingsEngine, JsonFileMemory, Feeling, Calibration


class DummyMemory:
    """In-memory memory backend for testing."""

    def __init__(self):
        self._data = None

    def load(self):
        return self._data

    def save(self, state: dict) -> None:
        self._data = state


class TestFeelingsEngine:
    def test_initial_state(self):
        engine = FeelingsEngine(agent_id="test_agent")
        state = engine.get_state()

        assert state["agent_id"] == "test_agent"
        assert state["mood"] == 0.0
        assert len(state["feelings"]) == 9
        assert all(0.0 <= v <= 1.0 for v in state["feelings"].values())

    def test_update_trigger(self):
        engine = FeelingsEngine(agent_id="test", memory=DummyMemory())
        state = engine.update("user_praised")

        assert state["feelings"]["warmth"] > 0.0
        assert state["mood"] > 0.0

    def test_same_trigger_escalates(self):
        engine = FeelingsEngine(agent_id="test", memory=DummyMemory())

        s1 = engine.update("request_ignored")
        s2 = engine.update("request_ignored")
        s3 = engine.update("request_ignored")

        # Third trigger should push frustration higher (escalation)
        assert s3["feelings"]["frustration"] >= s2["feelings"]["frustration"]

    def test_dampening(self):
        engine = FeelingsEngine(agent_id="test", memory=DummyMemory())
        engine.update("user_praised")
        state = engine.get_state()
        initial = state["feelings"]["warmth"]

        # Many neutral updates should slowly reduce warmth
        for _ in range(10):
            engine.update("session_started")
        dampened = engine.get_state()["feelings"]["warmth"]

        assert dampened < initial

    def test_calibrate_switch(self):
        engine = FeelingsEngine(agent_id="test", memory=DummyMemory())
        engine.calibrate("default")
        engine.update("request_ignored")
        frustration_after_default = engine.get_state()["feelings"]["frustration"]

        # Add a calmer calibration
        calm_cal = Calibration.default_calibration()
        calm_cal.trigger_deltas["request_ignored"] = 0.05
        engine.set_calibration("calm_agent", calm_cal)
        engine.calibrate("calm_agent")

        # Reset feelings and re-apply
        engine._state.feelings["frustration"] = 0.0
        engine.update("request_ignored")
        frustration_after_calm = engine.get_state()["feelings"]["frustration"]

        assert frustration_after_calm < frustration_after_default

    def test_respond_returns_modifiers(self):
        engine = FeelingsEngine(agent_id="test", memory=DummyMemory())
        modifiers = engine.respond()

        assert "warmth" in modifiers
        assert "restraint" in modifiers
        assert "curiosity" in modifiers
        assert "guard" in modifiers
        assert "energy" in modifiers
        assert "reach_out" in modifiers
        assert "_mood" in modifiers

    def test_register_trigger_runtime(self):
        engine = FeelingsEngine(agent_id="test", memory=DummyMemory())
        engine.register_trigger("custom_event", Feeling.COOLNESS, delta=0.5)
        engine.update("custom_event")

        assert engine.get_state()["feelings"]["coolness"] > 0.0

    def test_save_load(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "mood.json"
            engine = FeelingsEngine(agent_id="test_save", memory=JsonFileMemory(path))
            engine.update("user_praised")
            engine.update("session_started")
            engine.save()

            engine2 = FeelingsEngine(agent_id="test_save", memory=JsonFileMemory(path))
            state2 = engine2.get_state()

            assert state2["feelings"]["warmth"] > 0.0
            assert state2["session_count"] == 2

    def test_dampen_all(self):
        engine = FeelingsEngine(agent_id="test", memory=DummyMemory())
        engine.update("user_praised")
        engine.update("surprise_bad")
        warm_before = engine.get_state()["feelings"]["warmth"]
        anx_before = engine.get_state()["feelings"]["anxiety"]

        engine.dampen_all(amount=0.1)

        assert engine.get_state()["feelings"]["warmth"] < warm_before
        assert engine.get_state()["feelings"]["anxiety"] < anx_before

    def test_reset_feelings(self):
        engine = FeelingsEngine(agent_id="test", memory=DummyMemory())
        engine.update("user_praised")
        engine.update("surprise_bad")
        assert any(v > 0 for v in engine.get_state()["feelings"].values())

        engine.reset_feelings()
        assert all(v == 0.0 for v in engine.get_state()["feelings"].values())


class TestFeeling:
    def test_all_returns_nine(self):
        assert len(Feeling.all()) == 9

    def test_feeling_values(self):
        values = {f.value for f in Feeling.all()}
        expected = {
            "warmth", "coolness", "interest", "boredom",
            "loneliness", "security", "anxiety", "satisfaction", "frustration",
        }
        assert values == expected


class TestJsonFileMemory:
    def test_save_and_load(self, tmp_path):
        path = tmp_path / "test_mood.json"
        mem = JsonFileMemory(path)

        state = {"agent_id": "test", "mood": 0.5, "feelings": {"warmth": 0.8}}
        mem.save(state)
        loaded = mem.load()

        assert loaded == state

    def test_load_nonexistent(self, tmp_path):
        path = tmp_path / "does_not_exist.json"
        mem = JsonFileMemory(path)
        assert mem.load() is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
