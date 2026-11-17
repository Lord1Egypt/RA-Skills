#!/usr/bin/env python3
"""Tests for the AGY-owned deterministic project state (Phase 6).

Run with::

    python3 -m unittest discover -s skills/agy-ppt/tests -t skills/agy-ppt/tests -p "test_*.py"

No real Kiro or Codex process is launched and no subscription quota is used.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import project_state as ps  # noqa: E402
from project_state import (  # noqa: E402
    CONTROLLER,
    PHASE_ASSEMBLY,
    PHASE_BLOCKED,
    PHASE_COMPLETE,
    PHASE_INTAKE,
    PHASE_OUTLINE,
    PHASE_SAMPLE,
    PHASE_SLIDE_GENERATION,
    PHASE_STYLE,
    PHASE_VISUAL_QA,
    SLIDE_ASSEMBLED,
    SLIDE_BLOCKED,
    SLIDE_GENERATED,
    SLIDE_GENERATING,
    SLIDE_GENERATION_FAILED,
    SLIDE_PLANNED,
    SLIDE_QA_FAILED,
    SLIDE_QA_PASSED,
    SLIDE_READY,
    InvalidStateTransition,
    ProjectState,
    ProjectStateInvalid,
    WorkerResultInvalid,
    validate_state,
    validate_worker_result,
)

import validate_project  # noqa: E402


def codex_completed(slide_id="slide_01", output_path="origin_image/slide_01.png", **extra):
    result = {
        "status": "completed",
        "slide_id": slide_id,
        "operation": "generate",
        "backend": "codex_builtin_imagegen",
        "output_path": output_path,
        "warnings": [],
        "diagnostics": {"auth": "chatgpt_cli_session", "api_fallback_used": False,
                        "thread_id": "01a0-thread"},
    }
    result.update(extra)
    return result


def codex_error(slide_id="slide_01", error_code="IMAGE_GENERATION_FAILED", **extra):
    result = {
        "status": "error",
        "slide_id": slide_id,
        "operation": "generate",
        "backend": "codex_builtin_imagegen",
        "error_code": error_code,
        "diagnostics": {"auth": "chatgpt_cli_session", "api_fallback_used": False},
    }
    result.update(extra)
    return result


def kiro_result(status="completed", error_code=None):
    return {
        "schema": "agy-ppt/kiro-acp-bridge-result/1",
        "status": status,
        "control": "returned_to_agy",
        "error_code": error_code,
        "diagnostics": {"engine": "v3"},
    }


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.ws = Path(self._tmp.name) / "deck"
        self.ws.mkdir(parents=True)

    def tearDown(self):
        self._tmp.cleanup()

    def new_state(self, slides=("slide_01", "slide_02")):
        return ProjectState.initialize(self.ws, "ppt_demo", slide_ids=slides)

    def ready_generating(self, state, slide_id="slide_01"):
        state.set_slide_status(slide_id, SLIDE_READY)
        return state.begin_generation(slide_id)


# 1. initialize
class InitializeTests(Base):
    def test_initialize_defaults(self):
        state = self.new_state()
        self.assertEqual(state.phase, PHASE_INTAKE)
        self.assertEqual(state.data["controller"], "agy")
        self.assertTrue(state.data["sequential_only"])
        self.assertEqual(state.slide("slide_01")["status"], SLIDE_PLANNED)
        self.assertEqual(state.slide("slide_01")["generation"], 0)

    def test_initialize_rejects_bad_project_id(self):
        with self.assertRaises(ProjectStateInvalid):
            ProjectState.initialize(self.ws, "bad id!", slide_ids=["slide_01"])

    def test_initialize_rejects_bad_slide_id(self):
        with self.assertRaises(ProjectStateInvalid):
            ProjectState.initialize(self.ws, "ppt_demo", slide_ids=["slide1"])


# 2. schema validation
class SchemaValidationTests(Base):
    def test_valid_state_passes(self):
        state = self.new_state()
        self.assertEqual(validate_state(state.data), [])

    def test_controller_must_be_agy(self):
        state = self.new_state()
        state.data["controller"] = "kiro"
        self.assertTrue(validate_state(state.data))

    def test_sequential_only_must_be_true(self):
        state = self.new_state()
        state.data["sequential_only"] = False
        errors = validate_state(state.data)
        self.assertTrue(any("sequential_only" in e for e in errors))

    def test_bad_phase_flagged(self):
        state = self.new_state()
        state.data["phase"] = "rendering"
        self.assertTrue(validate_state(state.data))

    def test_negative_generation_flagged(self):
        state = self.new_state()
        state.data["slides"]["slide_01"]["generation"] = -1
        self.assertTrue(validate_state(state.data))


# 3. atomic write / 4. corrupt state / save round-trip
class PersistenceTests(Base):
    def test_save_and_load_round_trip(self):
        state = self.new_state()
        path = state.save()
        self.assertTrue(path.exists())
        loaded = ProjectState.load(self.ws)
        self.assertEqual(loaded.project_id, "ppt_demo")
        self.assertEqual(loaded.phase, PHASE_INTAKE)

    def test_atomic_write_leaves_no_temp(self):
        state = self.new_state()
        state.save()
        leftovers = [p for p in self.ws.iterdir() if p.name.endswith(".tmp")]
        self.assertEqual(leftovers, [])

    def test_corrupt_state_not_overwritten(self):
        path = ProjectState.state_path(self.ws)
        path.write_text("{ this is not json", encoding="utf-8")
        with self.assertRaises(ProjectStateInvalid):
            ProjectState.load(self.ws)
        # File must be untouched.
        self.assertEqual(path.read_text(encoding="utf-8"), "{ this is not json")

    def test_save_refuses_invalid_state(self):
        state = self.new_state()
        state.save()  # good baseline on disk
        good = ProjectState.state_path(self.ws).read_text(encoding="utf-8")
        state.data["controller"] = "hacker"
        with self.assertRaises(ProjectStateInvalid):
            state.save()
        # On-disk good state is preserved.
        self.assertEqual(ProjectState.state_path(self.ws).read_text(encoding="utf-8"), good)

    def test_missing_state_reports_invalid(self):
        with self.assertRaises(ProjectStateInvalid):
            ProjectState.load(self.ws)


# 5. workspace path boundary
class PathBoundaryTests(Base):
    def test_image_path_outside_workspace_rejected(self):
        state = self.new_state()
        self.ready_generating(state)
        result = codex_completed(output_path="/etc/evil.png")
        with self.assertRaises(ProjectStateInvalid):
            state.record_worker_result("slide_01", result)

    def test_job_path_traversal_rejected(self):
        state = self.new_state()
        state.set_slide_status("slide_01", SLIDE_READY)
        with self.assertRaises(ProjectStateInvalid):
            state.begin_generation("slide_01", job_path="../../escape.json")


# 6/7. project transitions
class ProjectTransitionTests(Base):
    def test_full_legal_phase_path(self):
        state = self.new_state()
        for target in (
            PHASE_OUTLINE,
            PHASE_STYLE,
            PHASE_SAMPLE,
            PHASE_SLIDE_GENERATION,
            PHASE_VISUAL_QA,
            PHASE_ASSEMBLY,
            PHASE_COMPLETE,
        ):
            state.set_phase(target)
        self.assertEqual(state.phase, PHASE_COMPLETE)

    def test_illegal_phase_skip_rejected(self):
        state = self.new_state()
        with self.assertRaises(InvalidStateTransition):
            state.set_phase(PHASE_SLIDE_GENERATION)  # intake -> slide_generation

    def test_visual_qa_can_return_to_generation(self):
        state = self.new_state()
        for target in (PHASE_OUTLINE, PHASE_STYLE, PHASE_SAMPLE, PHASE_SLIDE_GENERATION, PHASE_VISUAL_QA):
            state.set_phase(target)
        state.set_phase(PHASE_SLIDE_GENERATION)
        self.assertEqual(state.phase, PHASE_SLIDE_GENERATION)


# 24. blocked project + resume
class BlockedProjectTests(Base):
    def test_any_phase_can_block(self):
        state = self.new_state()
        state.set_phase(PHASE_OUTLINE)
        state.set_phase(PHASE_BLOCKED, note="need engineering fix")
        self.assertEqual(state.phase, PHASE_BLOCKED)
        self.assertEqual(state.data["phase_before_block"], PHASE_OUTLINE)

    def test_resume_from_blocked_to_remembered_phase(self):
        state = self.new_state()
        state.set_phase(PHASE_OUTLINE)
        state.set_phase(PHASE_BLOCKED)
        state.set_phase(PHASE_OUTLINE)  # AGY explicitly resumes
        self.assertEqual(state.phase, PHASE_OUTLINE)

    def test_resume_cannot_jump_arbitrarily(self):
        state = self.new_state()
        state.set_phase(PHASE_OUTLINE)
        state.set_phase(PHASE_BLOCKED)
        with self.assertRaises(InvalidStateTransition):
            state.set_phase(PHASE_ASSEMBLY)


# 8/9. slide transitions
class SlideTransitionTests(Base):
    def test_legal_slide_path(self):
        state = self.new_state()
        state.set_slide_status("slide_01", SLIDE_READY)
        state.begin_generation("slide_01")
        state.record_worker_result("slide_01", codex_completed())
        self.assertEqual(state.slide("slide_01")["status"], SLIDE_GENERATED)
        state.set_slide_status("slide_01", SLIDE_QA_PASSED)
        state.set_slide_status("slide_01", SLIDE_ASSEMBLED)
        self.assertEqual(state.slide("slide_01")["status"], SLIDE_ASSEMBLED)

    def test_illegal_slide_transition_rejected(self):
        state = self.new_state()
        with self.assertRaises(InvalidStateTransition):
            state.set_slide_status("slide_01", SLIDE_QA_PASSED)  # planned -> qa_passed

    def test_qa_failed_returns_to_ready(self):
        state = self.new_state()
        self.ready_generating(state)
        state.record_worker_result("slide_01", codex_completed())
        state.set_slide_status("slide_01", SLIDE_QA_FAILED)
        state.set_slide_status("slide_01", SLIDE_READY)
        self.assertEqual(state.slide("slide_01")["status"], SLIDE_READY)


# 10. generated never auto qa_passed / 11. worker cannot set phase
class OwnershipTests(Base):
    def test_generated_is_not_qa_passed(self):
        state = self.new_state()
        self.ready_generating(state)
        state.record_worker_result("slide_01", codex_completed())
        self.assertEqual(state.slide("slide_01")["status"], SLIDE_GENERATED)
        self.assertNotEqual(state.slide("slide_01")["status"], SLIDE_QA_PASSED)

    def test_qa_judgement_is_agy_only(self):
        state = self.new_state()
        self.ready_generating(state)
        state.record_worker_result("slide_01", codex_completed())
        with self.assertRaises(InvalidStateTransition):
            state.set_slide_status("slide_01", SLIDE_QA_PASSED, by="codex")
        # AGY can do it.
        state.set_slide_status("slide_01", SLIDE_QA_PASSED, by="agy")
        self.assertEqual(state.slide("slide_01")["status"], SLIDE_QA_PASSED)

    def test_worker_result_setting_phase_rejected(self):
        state = self.new_state()
        self.ready_generating(state)
        bad = codex_completed()
        bad["phase"] = "complete"
        with self.assertRaises(WorkerResultInvalid):
            state.record_worker_result("slide_01", bad)

    def test_controller_always_agy(self):
        state = self.new_state()
        self.ready_generating(state)
        state.record_worker_result("slide_01", codex_completed())
        state.set_slide_status("slide_01", SLIDE_QA_PASSED)
        state.set_phase(PHASE_OUTLINE)
        self.assertEqual(state.data["controller"], CONTROLLER)


# 12. generation counter / 13. attempt history / 16. retry
class GenerationCounterTests(Base):
    def test_first_generation_is_one(self):
        state = self.new_state()
        gen = self.ready_generating(state)
        self.assertEqual(gen, 1)
        self.assertEqual(state.slide("slide_01")["generation"], 1)

    def test_retry_increments_generation_and_keeps_history(self):
        state = self.new_state()
        # gen 1 -> qa_failed -> ready -> gen 2
        self.ready_generating(state)
        state.record_worker_result("slide_01", codex_completed())
        state.set_slide_status("slide_01", SLIDE_QA_FAILED)
        state.set_slide_status("slide_01", SLIDE_READY)
        gen2 = state.begin_generation("slide_01")
        state.record_worker_result(
            "slide_01",
            codex_completed(output_path="origin_image/slide_01.png", run_id="run-2"),
        )
        self.assertEqual(gen2, 2)
        self.assertEqual(state.slide("slide_01")["generation"], 2)
        self.assertEqual(len(state.slide("slide_01")["attempts"]), 2)
        gens = [a["generation"] for a in state.slide("slide_01")["attempts"]]
        self.assertEqual(gens, [1, 2])


# 14. idempotency
class IdempotencyTests(Base):
    def test_duplicate_completed_result_is_idempotent(self):
        state = self.new_state()
        self.ready_generating(state)
        result = codex_completed(run_id="run-42")
        state.record_worker_result("slide_01", result)
        # Re-record the exact same result (same idempotency key).
        state.record_worker_result("slide_01", result, idempotency_key="slide_01:run-42")
        self.assertEqual(len(state.slide("slide_01")["attempts"]), 1)
        self.assertEqual(state.slide("slide_01")["generation"], 1)
        self.assertEqual(state.slide("slide_01")["status"], SLIDE_GENERATED)

    def test_thread_id_not_used_as_primary_key(self):
        # Two results with the same thread_id but different run ids are distinct
        # attempts only if recorded against distinct generations; here we verify
        # the derived key does not collapse on thread_id alone.
        state = self.new_state()
        self.ready_generating(state)
        r1 = codex_completed()
        key1 = ps._derive_idempotency_key("slide_01", 1, r1)
        self.assertIn("gen1", key1)
        self.assertNotIn("01a0-thread", key1)


# 15. failed generation / 22. engineering error preserved
class FailureTests(Base):
    def test_failed_generation_records_error(self):
        state = self.new_state()
        self.ready_generating(state)
        state.record_worker_result("slide_01", codex_error(error_code="IMAGE_BACKEND_UNAVAILABLE"))
        slide = state.slide("slide_01")
        self.assertEqual(slide["status"], SLIDE_GENERATION_FAILED)
        self.assertEqual(slide["blocker"]["error_code"], "IMAGE_BACKEND_UNAVAILABLE")

    def test_failed_generation_can_retry(self):
        state = self.new_state()
        self.ready_generating(state)
        state.record_worker_result("slide_01", codex_error())
        state.set_slide_status("slide_01", SLIDE_READY)  # generation_failed -> ready
        self.assertEqual(state.slide("slide_01")["status"], SLIDE_READY)

    def test_engineering_error_preserved(self):
        state = self.new_state()
        result = kiro_result(status="agent_unavailable", error_code="ENGINEERING_AGENT_UNAVAILABLE")
        preserved = state.record_engineering_result(result)
        self.assertEqual(preserved["error_code"], "ENGINEERING_AGENT_UNAVAILABLE")

    def test_engineering_result_cannot_set_phase(self):
        state = self.new_state()
        bad = kiro_result()
        bad["phase"] = "complete"
        with self.assertRaises(WorkerResultInvalid):
            state.record_engineering_result(bad)


# 17. resume / 18. interrupted generating recovery
class ResumeTests(Base):
    def test_resume_does_not_regenerate_completed_slides(self):
        state = ProjectState.initialize(
            self.ws, "ppt_demo", slide_ids=[f"slide_{i:02d}" for i in range(1, 11)]
        )
        # 01-05 generated (and image on disk), 06 generating, 07-10 ready.
        for i in range(1, 6):
            sid = f"slide_{i:02d}"
            state.set_slide_status(sid, SLIDE_READY)
            state.begin_generation(sid)
            out = f"origin_image/slide_{i:02d}.png"
            (self.ws / "origin_image").mkdir(parents=True, exist_ok=True)
            (self.ws / out).write_bytes(b"\x89PNG\r\n\x1a\nfake")
            state.record_worker_result(sid, codex_completed(slide_id=sid, output_path=out))
        state.set_slide_status("slide_06", SLIDE_READY)
        state.begin_generation("slide_06")
        for i in range(7, 11):
            state.set_slide_status(f"slide_{i:02d}", SLIDE_READY)
        state.save()

        # Simulate crash + reopen.
        reopened = ProjectState.load(self.ws)
        recovered = reopened.recover_interrupted()
        self.assertEqual(recovered, ["slide_06"])
        # 01-05 stay generated (not regenerated).
        for i in range(1, 6):
            self.assertEqual(reopened.slide(f"slide_{i:02d}")["status"], SLIDE_GENERATED)
            self.assertEqual(reopened.slide(f"slide_{i:02d}")["generation"], 1)
        # 06 had no recorded completed attempt -> generation_failed.
        self.assertEqual(reopened.slide("slide_06")["status"], SLIDE_GENERATION_FAILED)

    def test_interrupted_with_confirmed_artifact_becomes_generated(self):
        state = self.new_state(slides=["slide_01"])
        state.set_slide_status("slide_01", SLIDE_READY)
        state.begin_generation("slide_01")
        # Record a completed attempt but leave status generating (crash before commit).
        # Do it by hand to simulate the race: append attempt, keep generating.
        slide = state.slide("slide_01")
        slide["attempts"].append(
            {
                "generation": 1,
                "worker": "codex",
                "status": "completed",
                "output_path": "origin_image/slide_01.png",
                "idempotency_key": "slide_01:gen1:x",
                "at": ps.now_iso(),
            }
        )
        slide["image_path"] = "origin_image/slide_01.png"
        (self.ws / "origin_image").mkdir(parents=True, exist_ok=True)
        (self.ws / "origin_image" / "slide_01.png").write_bytes(b"\x89PNG\r\n\x1a\nok")
        recovered = state.recover_interrupted()
        self.assertEqual(recovered, ["slide_01"])
        self.assertEqual(state.slide("slide_01")["status"], SLIDE_GENERATED)

    def test_interrupted_unknown_never_marked_success(self):
        state = self.new_state(slides=["slide_01"])
        state.set_slide_status("slide_01", SLIDE_READY)
        state.begin_generation("slide_01")
        # No attempt recorded, artifact missing.
        recovered = state.recover_interrupted(artifact_exists={})
        self.assertEqual(recovered, ["slide_01"])
        self.assertEqual(state.slide("slide_01")["status"], SLIDE_GENERATION_FAILED)


# 19. codex result validation / 20. ambiguous / 21. backend unavailable
class WorkerResultValidationTests(Base):
    def test_valid_codex_completed(self):
        self.assertEqual(validate_worker_result(codex_completed()), "codex")

    def test_valid_codex_error(self):
        self.assertEqual(validate_worker_result(codex_error()), "codex")

    def test_valid_kiro_result(self):
        self.assertEqual(validate_worker_result(kiro_result()), "kiro")

    def test_completed_without_output_path_rejected(self):
        bad = codex_completed()
        bad.pop("output_path")
        with self.assertRaises(WorkerResultInvalid):
            validate_worker_result(bad)

    def test_completed_with_error_code_rejected(self):
        bad = codex_completed()
        bad["error_code"] = "IMAGE_GENERATION_FAILED"
        with self.assertRaises(WorkerResultInvalid):
            validate_worker_result(bad)

    def test_error_without_error_code_rejected(self):
        bad = codex_error()
        bad.pop("error_code")
        with self.assertRaises(WorkerResultInvalid):
            validate_worker_result(bad)

    def test_unknown_error_code_rejected(self):
        with self.assertRaises(WorkerResultInvalid):
            validate_worker_result(codex_error(error_code="NOPE"))

    def test_api_fallback_used_true_rejected(self):
        bad = codex_completed()
        bad["diagnostics"]["api_fallback_used"] = True
        with self.assertRaises(WorkerResultInvalid):
            validate_worker_result(bad)

    def test_wrong_backend_rejected(self):
        bad = codex_completed()
        bad["backend"] = "openai_images_api"
        with self.assertRaises(WorkerResultInvalid):
            validate_worker_result(bad)

    def test_ambiguous_result_recorded_as_failed(self):
        state = self.new_state()
        self.ready_generating(state)
        state.record_worker_result("slide_01", codex_error(error_code="IMAGE_ARTIFACT_AMBIGUOUS"))
        self.assertEqual(state.slide("slide_01")["status"], SLIDE_GENERATION_FAILED)
        self.assertEqual(state.slide("slide_01")["blocker"]["error_code"], "IMAGE_ARTIFACT_AMBIGUOUS")

    def test_backend_unavailable_recorded_as_failed(self):
        state = self.new_state()
        self.ready_generating(state)
        state.record_worker_result("slide_01", codex_error(error_code="IMAGE_BACKEND_UNAVAILABLE"))
        self.assertEqual(state.slide("slide_01")["status"], SLIDE_GENERATION_FAILED)


# 23. project summary
class SummaryTests(Base):
    def test_summary_counts(self):
        state = ProjectState.initialize(
            self.ws, "ppt_demo", slide_ids=[f"slide_{i:02d}" for i in range(1, 6)]
        )
        state.set_slide_status("slide_01", SLIDE_READY)
        state.set_slide_status("slide_02", SLIDE_READY)
        self.ready_generating(state, "slide_03")  # generating
        summary = state.summary()
        self.assertEqual(summary["slides_total"], 5)
        self.assertEqual(summary["ready"], 2)
        self.assertEqual(summary["generating"], 1)
        self.assertEqual(summary["planned"], 2)
        self.assertEqual(summary["controller"], "agy")

    def test_summary_does_not_decide_next_step(self):
        state = self.new_state()
        summary = state.summary()
        self.assertNotIn("next_step", summary)
        self.assertNotIn("recommendation", summary)


# 25. blocked slide
class BlockedSlideTests(Base):
    def test_slide_can_block_and_resume(self):
        state = self.new_state()
        state.set_slide_status("slide_01", SLIDE_READY)
        state.set_slide_status("slide_01", SLIDE_BLOCKED)
        self.assertEqual(state.slide("slide_01")["status"], SLIDE_BLOCKED)
        self.assertEqual(state.slide("slide_01")["phase_before_block"], SLIDE_READY)
        state.set_slide_status("slide_01", SLIDE_READY)  # resume
        self.assertEqual(state.slide("slide_01")["status"], SLIDE_READY)


# 27. no credentials in state
class CredentialTests(Base):
    def test_credential_key_in_state_flagged(self):
        state = self.new_state()
        state.data["slides"]["slide_01"]["api_key"] = "sk-secret"
        errors = validate_state(state.data)
        self.assertTrue(any("credential" in e for e in errors))

    def test_diagnostics_sanitized_on_record(self):
        state = self.new_state()
        self.ready_generating(state)
        result = codex_completed()
        result["diagnostics"]["OPENAI_API_KEY"] = "sk-leak"
        # record must not raise, but the stored attempt must not carry the key.
        state.record_worker_result("slide_01", result)
        attempt = state.slide("slide_01")["attempts"][0]
        wire = json.dumps(attempt, ensure_ascii=False)
        self.assertNotIn("sk-leak", wire)
        self.assertNotIn("OPENAI_API_KEY", wire)


# 28. sequential-only policy
class SequentialPolicyTests(Base):
    def test_sequential_only_is_true_and_validated(self):
        state = self.new_state()
        self.assertTrue(state.data["sequential_only"])
        state.data["sequential_only"] = 1  # not True
        self.assertTrue(validate_state(state.data))


# validate_project.py CLI
class ValidateProjectCliTests(Base):
    def test_cli_valid(self):
        self.new_state().save()
        out = Path(self._tmp.name) / "report.json"
        rc = validate_project.main([str(self.ws), "--summary", "--output", str(out)])
        self.assertEqual(rc, 0)
        report = json.loads(out.read_text(encoding="utf-8"))
        self.assertTrue(report["valid"])
        self.assertIn("summary", report)

    def test_cli_missing(self):
        out = Path(self._tmp.name) / "report.json"
        rc = validate_project.main([str(self.ws), "--output", str(out)])
        self.assertEqual(rc, 1)
        report = json.loads(out.read_text(encoding="utf-8"))
        self.assertFalse(report["valid"])
        self.assertEqual(report["error_code"], "PROJECT_STATE_INVALID")

    def test_cli_corrupt_not_overwritten(self):
        path = ProjectState.state_path(self.ws)
        path.write_text("{bad", encoding="utf-8")
        out = Path(self._tmp.name) / "report.json"
        rc = validate_project.main([str(self.ws), "--output", str(out)])
        self.assertEqual(rc, 1)
        self.assertEqual(path.read_text(encoding="utf-8"), "{bad")


if __name__ == "__main__":
    unittest.main(verbosity=2)
