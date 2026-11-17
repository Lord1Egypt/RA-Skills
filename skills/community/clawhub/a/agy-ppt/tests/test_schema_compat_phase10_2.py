#!/usr/bin/env python3
"""Schema Compatibility Audit -- Phase 10.2 repeated-generic-failure policy.

Audits that the new production state written by
``project_state.consecutive_failure_streak`` / ``may_retry_immediately`` /
``block_after_repeated_failure`` / ``block_for_operator_confirmed_quota`` is:

* accepted by the actual enforced validator (``validate_project.py`` /
  ``project_state.validate_state``) via real ``save()`` -> reload -> validate
  round trips, not just in-memory Python object construction;
* explicitly documented (not merely tolerated) in
  ``schemas/project_state.schema.json``, at both the new top-level
  ``operator_blocker`` property and the new ``slide.blocker.retry_immediately``
  property;
* provenance-clean: an operator-confirmed quota decision never rewrites a
  worker-reported ``error_code``.

This module also documents, and asserts, a fact discovered during the audit:
nothing in this codebase actually loads ``project_state.schema.json`` with a
JSON Schema library. ``validate_project.py`` calls
``project_state.validate_state()``, a hand-written Python validator. The JSON
Schema file is a *documentation* artifact only. Both are audited here because
both describe the on-disk contract.

Read-only / minimal-verification in spirit: no new production behaviour is
introduced by this file, and no dependency (e.g. ``jsonschema``) is installed
or imported -- the JSON Schema file's structure is inspected directly as data.

No real Codex/Kiro process is launched and no subscription quota is used.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
SCHEMA_PATH = SKILL_DIR / "schemas" / "project_state.schema.json"
VALIDATOR_SCRIPT = SCRIPTS_DIR / "validate_project.py"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import project_state as ps  # noqa: E402
from project_state import ProjectState  # noqa: E402


def _worker_error(slide_id: str, error_code: str = "IMAGE_GENERATION_FAILED") -> dict:
    return {
        "status": "error",
        "slide_id": slide_id,
        "operation": "generate",
        "backend": "codex_builtin_imagegen",
        "error_code": error_code,
        "diagnostics": {"auth": "chatgpt_cli_session", "api_fallback_used": False},
    }


def _fail(state: ProjectState, slide_id: str) -> dict:
    """One real (deterministic, no subprocess) worker-recorded failure."""
    if state.slide(slide_id)["status"] != ps.SLIDE_READY:
        state.set_slide_status(slide_id, ps.SLIDE_READY)
    state.begin_generation(slide_id)
    return state.record_worker_result(slide_id, _worker_error(slide_id))


def _advance_to_slide_generation(state: ProjectState) -> None:
    for gate in ("outline", "style", "sample"):
        state.set_gate(gate, "approved")
    for phase in (
        ps.PHASE_OUTLINE,
        ps.PHASE_STYLE,
        ps.PHASE_SAMPLE,
        ps.PHASE_SLIDE_GENERATION,
    ):
        state.set_phase(phase)


def run_validator_cli(workspace: Path) -> dict:
    """Invoke the real, enforced validator as a subprocess (not the function)."""
    result = subprocess.run(  # noqa: S603 - fixed argv, no user input
        [sys.executable, str(VALIDATOR_SCRIPT), str(workspace), "--summary"],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    return json.loads(result.stdout)


class SchemaFileStructureTests(unittest.TestCase):
    """Audit 1 / 2 static checks: what does the schema file actually declare?"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    def test_top_level_additional_properties_is_true(self):
        self.assertIs(self.schema["additionalProperties"], True)

    def test_operator_blocker_is_now_an_explicit_top_level_property(self):
        self.assertIn("operator_blocker", self.schema["properties"])
        prop = self.schema["properties"]["operator_blocker"]
        self.assertEqual(prop["type"], ["object", "null"])
        self.assertIn("reason", prop["properties"])

    def test_slide_blocker_retry_immediately_is_now_an_explicit_property(self):
        blocker = self.schema["definitions"]["slide"]["properties"]["blocker"]
        self.assertIn("retry_immediately", blocker["properties"])
        self.assertEqual(blocker["properties"]["retry_immediately"]["type"], "boolean")

    def test_slide_blocker_additional_properties_still_true_no_regression(self):
        blocker = self.schema["definitions"]["slide"]["properties"]["blocker"]
        self.assertIs(blocker.get("additionalProperties"), True)

    def test_slide_definition_additional_properties_still_true(self):
        self.assertIs(self.schema["definitions"]["slide"].get("additionalProperties"), True)


class Phase10_2SchemaAuditBase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.ws = Path(self._tmp.name) / "deck"
        self.ws.mkdir(parents=True)

    def tearDown(self) -> None:
        self._tmp.cleanup()


# -- Audit 1: top-level operator_blocker --------------------------------------
class Audit1OperatorBlockerTests(Phase10_2SchemaAuditBase):
    """3. operator_blocker: real save -> reload -> validate_project.py -> schema."""

    def test_operator_blocker_state_is_valid_via_real_validator_cli(self):
        state = ProjectState.initialize(self.ws, "ppt_audit1", slide_ids=["slide_01"])
        _advance_to_slide_generation(state)
        _fail(state, "slide_01")
        state.block_for_operator_confirmed_quota(note="operator confirmed quota exhaustion")
        state.save()

        report = run_validator_cli(self.ws)
        self.assertTrue(report["valid"], report)
        self.assertIsNone(report["error_code"])
        self.assertEqual(
            report["summary"]["operator_blocker"]["reason"], "subscription_quota_exhausted"
        )

    def test_operator_blocker_minimal_shape_is_schema_compatible(self):
        """The exact minimal shape called out by the audit request."""
        minimal_state = {
            "schema_version": "1",
            "project_id": "ppt_audit1_minimal",
            "controller": "agy",
            "phase": "blocked",
            "phase_before_block": "slide_generation",
            "sequential_only": True,
            "slides": {},
            "operator_blocker": {
                "reason": "subscription_quota_exhausted",
                "source": "operator_confirmed",
            },
        }
        errors = ps.validate_state(minimal_state)
        self.assertEqual(errors, [], errors)

        path = ProjectState.state_path(self.ws)
        path.write_text(json.dumps(minimal_state, ensure_ascii=False, indent=2), encoding="utf-8")
        report = run_validator_cli(self.ws)
        self.assertTrue(report["valid"], report)


# -- Audit 2: slide.blocker with retry_immediately ----------------------------
class Audit2SlideBlockerRetryImmediatelyTests(Phase10_2SchemaAuditBase):
    """Second-consecutive-failure blocked state: save -> reload -> validate."""

    def test_repeated_failure_blocker_shape_is_schema_compatible(self):
        blocker = {
            "reason": "repeated_image_backend_failure",
            "error_code": "IMAGE_GENERATION_FAILED",
            "retry_immediately": False,
            "at": "2025-01-01T00:00:00Z",
        }
        state_dict = {
            "schema_version": "1",
            "project_id": "ppt_audit2_minimal",
            "controller": "agy",
            "phase": "blocked",
            "phase_before_block": "slide_generation",
            "sequential_only": True,
            "slides": {
                "slide_01": {
                    "status": "blocked",
                    "generation": 2,
                    "attempts": [
                        {
                            "generation": 1,
                            "worker": "codex",
                            "status": "error",
                            "idempotency_key": "k1",
                            "at": "2025-01-01T00:00:00Z",
                            "error_code": "IMAGE_GENERATION_FAILED",
                        },
                        {
                            "generation": 2,
                            "worker": "codex",
                            "status": "error",
                            "idempotency_key": "k2",
                            "at": "2025-01-01T00:00:01Z",
                            "error_code": "IMAGE_GENERATION_FAILED",
                        },
                    ],
                    "blocker": blocker,
                }
            },
        }
        errors = ps.validate_state(state_dict)
        self.assertEqual(errors, [], errors)

    def test_second_consecutive_failure_end_to_end_is_valid_via_real_validator_cli(self):
        state = ProjectState.initialize(self.ws, "ppt_audit2", slide_ids=["slide_01"])
        _advance_to_slide_generation(state)
        _fail(state, "slide_01")
        state.set_slide_status("slide_01", ps.SLIDE_READY)
        _fail(state, "slide_01")
        self.assertFalse(state.may_retry_immediately("slide_01"))
        state.block_after_repeated_failure("slide_01")
        state.save()

        report = run_validator_cli(self.ws)
        self.assertTrue(report["valid"], report)
        self.assertIsNone(report["error_code"])


# -- Audit 3: full round trip of the repeated-failure block -------------------
class Audit3RoundTripTests(Phase10_2SchemaAuditBase):
    """generation 1 fail, generation 2 fail, block, save, drop, reload, validate."""

    def setUp(self) -> None:
        super().setUp()
        state = ProjectState.initialize(self.ws, "ppt_audit3", slide_ids=["slide_01"])
        _advance_to_slide_generation(state)
        _fail(state, "slide_01")  # generation 1
        state.set_slide_status("slide_01", ps.SLIDE_READY)
        _fail(state, "slide_01")  # generation 2 (consecutive)
        state.block_after_repeated_failure("slide_01")
        state.save()
        del state  # fully release the in-memory object

    def test_disk_json_passes_validate_state(self):
        raw = json.loads((self.ws / "project_state.json").read_text(encoding="utf-8"))
        self.assertEqual(ps.validate_state(raw), [])

    def test_reload_reports_valid_via_cli(self):
        report = run_validator_cli(self.ws)
        self.assertTrue(report["valid"], report)

    def test_reloaded_state_matches_every_required_field(self):
        state = ProjectState.load(self.ws)  # brand-new object, read from disk only
        slide = state.slide("slide_01")

        self.assertEqual(state.phase, ps.PHASE_BLOCKED)
        self.assertEqual(state.data["phase_before_block"], ps.PHASE_SLIDE_GENERATION)
        self.assertEqual(slide["status"], ps.SLIDE_BLOCKED)
        self.assertEqual(len(slide["attempts"]), 2)
        self.assertEqual(slide["generation"], 2)
        self.assertEqual(
            slide["blocker"],
            {
                "reason": "repeated_image_backend_failure",
                "error_code": "IMAGE_GENERATION_FAILED",
                "retry_immediately": False,
                "at": slide["blocker"]["at"],
            },
        )
        self.assertEqual(state.consecutive_failure_streak("slide_01"), 2)
        self.assertFalse(state.may_retry_immediately("slide_01"))


# -- Audit 4: operator blocker round trip + provenance ------------------------
class Audit4OperatorBlockerRoundTripTests(Phase10_2SchemaAuditBase):
    def setUp(self) -> None:
        super().setUp()
        state = ProjectState.initialize(self.ws, "ppt_audit4", slide_ids=["slide_01"])
        _advance_to_slide_generation(state)
        _fail(state, "slide_01")
        state.block_for_operator_confirmed_quota(
            note="operator confirmed subscription quota exhaustion via ChatGPT billing UI"
        )
        state.save()
        del state

    def test_disk_json_passes_validate_state(self):
        raw = json.loads((self.ws / "project_state.json").read_text(encoding="utf-8"))
        self.assertEqual(ps.validate_state(raw), [])

    def test_reload_reports_valid_via_cli(self):
        report = run_validator_cli(self.ws)
        self.assertTrue(report["valid"], report)

    def test_worker_error_provenance_is_preserved_after_reload(self):
        state = ProjectState.load(self.ws)
        slide = state.slide("slide_01")

        # The worker's own evidence is untouched by the operator decision.
        self.assertEqual(slide["attempts"][0]["error_code"], "IMAGE_GENERATION_FAILED")
        self.assertEqual(slide["blocker"]["error_code"], "IMAGE_GENERATION_FAILED")
        self.assertNotEqual(slide["blocker"]["reason"], "subscription_quota_exhausted")

        # The operator's decision lives only in its own, separate field.
        self.assertEqual(
            state.data["operator_blocker"]["reason"], "subscription_quota_exhausted"
        )
        self.assertEqual(state.data["operator_blocker"]["confirmed_by"], "operator")


# -- Negative control: validator still rejects real invalid/unsupported data --
class ValidatorStillRejectsInvalidStateTests(Phase10_2SchemaAuditBase):
    """The audit must not have weakened validation anywhere."""

    def test_bad_enum_values_are_still_rejected(self):
        bad = {
            "schema_version": "1",
            "project_id": "ppt_bad",
            "controller": "not_agy",
            "phase": "not_a_real_phase",
            "sequential_only": True,
            "slides": {
                "slide_01": {"status": "not_a_real_status", "generation": -1, "attempts": []}
            },
        }
        errors = ps.validate_state(bad)
        self.assertTrue(errors)
        joined = " ".join(errors)
        self.assertIn("controller", joined)
        self.assertIn("phase", joined)
        self.assertIn("generation", joined)

    def test_credential_shaped_key_under_operator_blocker_is_still_rejected(self):
        state_dict = {
            "schema_version": "1",
            "project_id": "ppt_bad2",
            "controller": "agy",
            "phase": "intake",
            "sequential_only": True,
            "slides": {},
            "operator_blocker": {
                "reason": "subscription_quota_exhausted",
                "api_key": "sk-should-be-rejected",
            },
        }
        errors = ps.validate_state(state_dict)
        self.assertTrue(any("operator_blocker.api_key" in e for e in errors), errors)

    def test_missing_state_file_is_rejected_by_the_real_cli(self):
        report = run_validator_cli(self.ws)  # workspace has no project_state.json
        self.assertFalse(report["valid"])
        self.assertEqual(report["error_code"], ps.ERROR_PROJECT_STATE_INVALID)

    def test_corrupt_json_is_rejected_and_not_overwritten(self):
        path = ProjectState.state_path(self.ws)
        path.write_text("{ not json", encoding="utf-8")
        report = run_validator_cli(self.ws)
        self.assertFalse(report["valid"])
        self.assertEqual(path.read_text(encoding="utf-8"), "{ not json")


if __name__ == "__main__":
    unittest.main()
