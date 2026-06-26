from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from context_guardian import (
    CheckpointStore,
    ContextGuardianConfig,
    ContextMonitor,
    LastAction,
    MemoryAssembler,
    SafetyGate,
    Summarizer,
    TaskArtifact,
    TaskState,
    TaskStep,
    create_default_task_state,
    load_task_state,
    should_trim_context,
)



def make_state() -> TaskState:
    return TaskState(
        task_id="task-1",
        session_id="session-1",
        goal="Preserve task continuity",
        status="running",
        current_phase="implementation",
        plan=[TaskStep(id="step-1", title="Inspect loop", status="done")],
        completed_steps=["Inspect loop"],
        open_issues=["Need final host integration point"],
        decisions=[{"timestamp": "2026-04-07T10:00:00Z", "decision": "Use files", "reason": "Restart safe"}],
        constraints=["Never continue blindly after context loss"],
        important_facts=["Planner exists"],
        artifacts=[TaskArtifact(path=".context_guardian/task_state.json", kind="file", description="state")],
        last_action=LastAction(timestamp="2026-04-07T10:05:00Z", type="tool", summary="Checkpoint written", outcome="success"),
        next_action="Resume from the latest checkpoint",
        state_confidence=0.9,
    )


class ContextGuardianTests(unittest.TestCase):
    def make_temp_path(self) -> Path:
        return Path(tempfile.mkdtemp(prefix="cg-test-"))

    def test_checkpoint_creation(self) -> None:
        tmp_path = self.make_temp_path()
        config = ContextGuardianConfig(root_path=tmp_path, context_path=tmp_path)
        store = CheckpointStore(config)
        state = make_state()
        summary = Summarizer().summarize(state, [], config)
        checkpoint = store.write_checkpoint(state, summary, ["a.py"], ["assumption"], ["risk"], state.next_action)
        self.assertTrue(checkpoint.exists())
        self.assertTrue(store.task_state_json.exists())
        self.assertTrue(store.task_state_md.exists())
        self.assertTrue(store.events_path.exists())

    def test_summary_generation(self) -> None:
        config = ContextGuardianConfig(root_path=Path("."), context_path=Path("."))
        summary = Summarizer().summarize(make_state(), [], config)
        self.assertIn("# Context Guardian Summary", summary)
        self.assertIn("## Goal", summary)
        self.assertIn("## Next Action", summary)

    def test_restart_recovery(self) -> None:
        tmp_path = self.make_temp_path()
        config = ContextGuardianConfig(root_path=tmp_path, context_path=tmp_path)
        store = CheckpointStore(config)
        state = make_state()
        store.write_checkpoint(state, "summary", [], [], [], state.next_action)
        recovered = load_task_state(store)
        self.assertIsNotNone(recovered)
        self.assertEqual(recovered.task_id, state.task_id)
        self.assertEqual(recovered.next_action, state.next_action)

    def test_critical_threshold_stop_behavior(self) -> None:
        tmp_path = self.make_temp_path()
        config = ContextGuardianConfig(root_path=tmp_path, context_path=tmp_path, max_history_chars=100)
        store = CheckpointStore(config)
        gate = SafetyGate(ContextMonitor(0.55, 0.70, 0.85, max_history_chars=100), store, Summarizer())
        state = make_state()
        state.state_confidence = 0.95
        previous_updated_at = state.updated_at
        result = gate.evaluate(["x" * 500], state, [], [])
        self.assertFalse(result["allow"])
        self.assertEqual(result["pressure"]["risk_level"], "critical")
        self.assertEqual(result["reason"], "critical context pressure")
        self.assertIn("checkpoint_path", result)
        self.assertTrue(Path(result["checkpoint_path"]).exists())
        self.assertTrue(store.task_state_json.exists())
        self.assertNotEqual(state.updated_at, previous_updated_at)

    def test_host_pressure_override_wins(self) -> None:
        tmp_path = self.make_temp_path()
        config = ContextGuardianConfig(root_path=tmp_path, context_path=tmp_path, max_history_chars=10000)
        store = CheckpointStore(config)
        gate = SafetyGate(ContextMonitor(0.55, 0.70, 0.85, max_history_chars=10000), store, Summarizer())
        state = make_state()
        result = gate.evaluate(["tiny"], state, [], [], pressure_override=0.9)
        self.assertFalse(result["allow"])
        self.assertEqual(result["pressure"]["risk_level"], "critical")
        self.assertEqual(result["pressure"]["source"], "host")

    def test_warning_threshold_writes_summary(self) -> None:
        tmp_path = self.make_temp_path()
        config = ContextGuardianConfig(root_path=tmp_path, context_path=tmp_path, max_history_chars=10000)
        store = CheckpointStore(config)
        gate = SafetyGate(ContextMonitor(0.55, 0.70, 0.85, max_history_chars=10000), store, Summarizer())
        state = make_state()
        result = gate.evaluate(["tiny"], state, [], [], pressure_override=0.55)
        self.assertTrue(result["allow"])
        self.assertEqual(result["pressure"]["risk_level"], "warning")
        self.assertIsNotNone(result["summary"])
        self.assertTrue(store.summaries_dir.exists())
        summaries = sorted(path for path in store.summaries_dir.glob("*.md") if path.name != "latest-summary.md")
        self.assertTrue(summaries)
        self.assertIn("# Context Guardian Summary", summaries[-1].read_text(encoding="utf-8"))
        self.assertTrue(store.latest_summary_alias.exists())
        self.assertEqual(store.latest_summary_alias.read_text(encoding="utf-8"), summaries[-1].read_text(encoding="utf-8"))
        self.assertIsNone(result["checkpoint_path"])
        self.assertFalse(store.task_state_json.exists())

    def test_noncritical_without_state_change_skips_checkpoint(self) -> None:
        tmp_path = self.make_temp_path()
        config = ContextGuardianConfig(root_path=tmp_path, context_path=tmp_path, max_history_chars=10000)
        store = CheckpointStore(config)
        gate = SafetyGate(ContextMonitor(0.55, 0.70, 0.85, max_history_chars=10000), store, Summarizer())
        state = make_state()
        result = gate.evaluate(["tiny"], state, [], [], pressure_override=0.1, action_changed_state=False)
        self.assertTrue(result["allow"])
        self.assertEqual(result["pressure"]["risk_level"], "normal")
        self.assertIsNone(result["summary"])
        self.assertIsNone(result["checkpoint_path"])
        self.assertFalse(store.task_state_json.exists())

    def test_warning_threshold_with_state_change_writes_checkpoint(self) -> None:
        tmp_path = self.make_temp_path()
        config = ContextGuardianConfig(root_path=tmp_path, context_path=tmp_path, max_history_chars=10000)
        store = CheckpointStore(config)
        gate = SafetyGate(ContextMonitor(0.55, 0.70, 0.85, max_history_chars=10000), store, Summarizer())
        state = make_state()
        result = gate.evaluate(["tiny"], state, [], [], pressure_override=0.55, action_changed_state=True)
        self.assertTrue(result["allow"])
        self.assertEqual(result["pressure"]["risk_level"], "warning")
        self.assertIsNotNone(result["summary"])
        self.assertIsNotNone(result["checkpoint_path"])
        self.assertTrue(Path(result["checkpoint_path"]).exists())
        self.assertTrue(store.task_state_json.exists())

    def test_phase_change_forces_summary_without_checkpoint(self) -> None:
        tmp_path = self.make_temp_path()
        config = ContextGuardianConfig(root_path=tmp_path, context_path=tmp_path, max_history_chars=10000)
        store = CheckpointStore(config)
        gate = SafetyGate(ContextMonitor(0.55, 0.70, 0.85, max_history_chars=10000), store, Summarizer())
        state = make_state()
        result = gate.evaluate(["tiny"], state, [], [], pressure_override=0.1, phase_or_goal_changed=True)
        self.assertTrue(result["allow"])
        self.assertEqual(result["pressure"]["risk_level"], "normal")
        self.assertIsNotNone(result["summary"])
        self.assertTrue(store.latest_summary_alias.exists())
        self.assertIsNone(result["checkpoint_path"])
        self.assertFalse(store.task_state_json.exists())

    def test_atomic_checkpoint_writes_leave_no_tmp_files(self) -> None:
        tmp_path = self.make_temp_path()
        config = ContextGuardianConfig(root_path=tmp_path, context_path=tmp_path)
        store = CheckpointStore(config)
        state = make_state()
        summary = Summarizer().summarize(state, [], config)
        checkpoint_path = store.write_checkpoint(state, summary, ["a.py"], ["assumption"], ["risk"], state.next_action)
        self.assertTrue(checkpoint_path.exists())
        checkpoint_payload = checkpoint_path.read_text(encoding="utf-8")
        task_state_payload = store.task_state_json.read_text(encoding="utf-8")
        self.assertIn('"task_id": "task-1"', checkpoint_payload)
        self.assertIn('"task_id": "task-1"', task_state_payload)
        tmp_files = list(store.guardian_dir.rglob("*.tmp"))
        self.assertEqual(tmp_files, [])

    def test_trimming_policy(self) -> None:
        self.assertTrue(should_trim_context("warning"))
        self.assertTrue(should_trim_context("compress"))
        self.assertTrue(should_trim_context("critical"))
        self.assertFalse(should_trim_context("normal"))

    def test_memory_assembler(self) -> None:
        state = make_state()
        bundle = MemoryAssembler().build_bundle("sys", state, "summary", ["file.py"], "last action")
        self.assertIn("# Working Context Bundle", bundle)
        self.assertNotIn("## Latest Durable State", bundle)
        self.assertIn("## Current Phase", bundle)
        self.assertIn("file.py", bundle)

    def test_create_default_task_state(self) -> None:
        state = create_default_task_state("t", "s", "g")
        self.assertEqual(state.task_id, "t")
        self.assertEqual(state.session_id, "s")
        self.assertEqual(state.goal, "g")

    def test_task_state_round_trip(self) -> None:
        state = make_state()
        payload = state.to_dict()
        round_tripped = TaskState.from_dict(json.loads(json.dumps(payload)))
        self.assertEqual(round_tripped.task_id, state.task_id)
        self.assertEqual(round_tripped.goal, state.goal)


if __name__ == "__main__":
    unittest.main()
