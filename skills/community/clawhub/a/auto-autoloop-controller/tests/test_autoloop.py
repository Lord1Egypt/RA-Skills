import json
from pathlib import Path

import pytest

from autoloop import AutoloopState, should_stop


class TestAutoloopState:
    def test_create_fresh(self, tmp_path):
        state_path = tmp_path / "autoloop_state.json"
        state = AutoloopState.load(state_path)
        assert state.schema_version == "1.0"
        assert state.iterations_completed == 0
        assert state.status == "running"
        assert state.started_at != ""

    def test_save_and_reload(self, tmp_path):
        state_path = tmp_path / "autoloop_state.json"
        state = AutoloopState.load(state_path)
        state.target = "/some/skill"
        state.iterations_completed = 3
        state.total_cost_usd = 12.5
        state.current_scores = {"clarity": 0.85}
        state.save(state_path)

        reloaded = AutoloopState.load(state_path)
        assert reloaded.target == "/some/skill"
        assert reloaded.iterations_completed == 3
        assert reloaded.total_cost_usd == 12.5
        assert reloaded.current_scores == {"clarity": 0.85}

    def test_should_stop_max_iterations(self):
        state = AutoloopState(
            iterations_completed=5,
            max_iterations=5,
        )
        stop, reason = should_stop(state)
        assert stop is True
        assert "max_iterations" in reason

    def test_should_stop_cost_cap(self):
        state = AutoloopState(
            iterations_completed=2,
            max_iterations=10,
            total_cost_usd=55.0,
            max_cost_usd=50.0,
        )
        stop, reason = should_stop(state)
        assert stop is True
        assert "cost_cap" in reason

    def test_should_stop_plateau(self):
        state = AutoloopState(
            iterations_completed=5,
            max_iterations=10,
            plateau_window=3,
            score_history=[
                {"weighted_score": 0.85, "decision": "keep"},
                {"weighted_score": 0.83, "decision": "reject"},
                {"weighted_score": 0.84, "decision": "reject"},
                {"weighted_score": 0.82, "decision": "reject"},
            ],
        )
        stop, reason = should_stop(state)
        assert stop is True
        assert "plateau" in reason

    def test_should_not_stop_early(self):
        state = AutoloopState(
            iterations_completed=1,
            max_iterations=10,
            total_cost_usd=5.0,
            max_cost_usd=50.0,
            plateau_window=3,
            score_history=[
                {"weighted_score": 0.80, "decision": "keep"},
                {"weighted_score": 0.85, "decision": "keep"},
            ],
        )
        stop, reason = should_stop(state)
        assert stop is False
        assert reason == ""

    def test_ignores_unknown_fields_on_load(self, tmp_path):
        """Unknown fields in JSON should not crash deserialization."""
        state_path = tmp_path / "autoloop_state.json"
        data = {
            "schema_version": "1.0",
            "target": "/skill",
            "iterations_completed": 2,
            "unknown_future_field": "some_value",
        }
        state_path.write_text(json.dumps(data))
        state = AutoloopState.load(state_path)
        assert state.iterations_completed == 2
        assert state.target == "/skill"
