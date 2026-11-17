#!/usr/bin/env python3
"""Q1 live-worker contract, qualification evidence, and Jev routing tests."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from codex_image_adapter import (  # noqa: E402
    AdapterResult,
    InvalidRequestError,
    build_worker_prompt,
)
from dev_jev_decisions import (  # noqa: E402
    ConfidenceDisposition,
    JevChoiceResult,
    JevDecisionRecord,
    confidence_disposition,
)
from phase18_worker_contract import (  # noqa: E402
    QualificationEvidence,
    ReservedZonePromptCompliance,
    SampleProvenance,
    WorkerContractCompleteness,
    audit_worker_contract,
    classify_qualification_evidence,
    classify_reserved_zone_prompt,
    classify_sample_provenance,
    render_reserved_zone_contract,
)
from phase18_codex_worker import Phase18CodexWorker, Phase18WorkerRequest  # noqa: E402
from prepare_slide_prompts import _build_prompt  # noqa: E402
from presentation_workflow import (  # noqa: E402
    PresentationApprovalWorkflow,
    SampleArtifact,
)
from project_state import ProjectState  # noqa: E402


def manifest(*, mode: str = "CLEAN_PLATE") -> dict:
    return {
        "slide_id": "slide_02",
        "plate_mode": mode,
        "reserved_zones": [
            {
                "zone_id": "zone:slide_02:kpi",
                "slide_id": "slide_02",
                "element_id": "kpi",
                "role": "KPI",
                "box": {"left": 7.2, "top": 1.5, "width": 3.0, "height": 1.4},
                "editability": "EDITABLE_REQUIRED",
                "strategy": "NATIVE_TEXT",
                "expected_content_type": "text",
                "plate_requirement": "CONTENT_FREE",
                "replacement": {"mode": "NOT_REPLACEABLE", "preserve_position": True, "preserve_size": True},
                "envelope": None,
                "background_treatment": "continue dark-blue field",
            }
        ],
        "locked_content_to_render": ["abstract background texture"],
        "editable_content_to_omit": ["18%"],
        "replaceable_assets_to_omit": [],
        "background_instructions": "Keep the KPI zone visually quiet.",
    }


class WorkerContractTests(unittest.TestCase):
    def test_complete_manifest(self):
        audit = audit_worker_contract(manifest())
        self.assertEqual(audit.status, WorkerContractCompleteness.COMPLETE)
        self.assertEqual(len(audit.manifest_hash or ""), 64)

    def test_missing_manifest_is_unsafe(self):
        self.assertEqual(audit_worker_contract(None).status, WorkerContractCompleteness.UNSAFE)

    def test_content_free_violation_is_unsafe(self):
        value = manifest()
        value["reserved_zones"][0]["plate_requirement"] = "LOCKED_IN_PLATE"
        self.assertEqual(audit_worker_contract(value).status, WorkerContractCompleteness.UNSAFE)

    def test_full_composite_overlay_is_unsafe(self):
        self.assertEqual(audit_worker_contract(manifest(mode="FULL_COMPOSITE")).status, WorkerContractCompleteness.UNSAFE)

    def test_contract_prompt_names_zone_and_exclusion(self):
        text = render_reserved_zone_contract(manifest())
        self.assertIn("zone:slide_02:kpi", text)
        self.assertIn("18%", text)
        self.assertIn("COMPOSITE_CONFLICT", text)

    def test_prompt_compliance_is_deterministic(self):
        value = manifest()
        prompt = render_reserved_zone_contract(value)
        self.assertEqual(
            classify_reserved_zone_prompt(prompt, value),
            ReservedZonePromptCompliance.CLEARLY_PROPAGATED,
        )
        self.assertEqual(
            classify_reserved_zone_prompt("draw a slide", value),
            ReservedZonePromptCompliance.MISSING,
        )

    def test_prepared_prompt_omits_universal_burn_in_instruction(self):
        value = manifest()
        prompt = _build_prompt(
            deck={"language": "Chinese", "style": {}},
            slide={"number": 2, "title": "核心指標", "key_points": ["18%"], "visual_plate_job": value},
            number=2,
            global_style_reference=None,
            base_dir=Path("."),
        )
        self.assertIn("Reserved Editable Zone Contract", prompt)
        self.assertNotIn("final image itself must contain the title and key points", prompt)
        self.assertEqual(
            classify_reserved_zone_prompt(prompt, value),
            ReservedZonePromptCompliance.CLEARLY_PROPAGATED,
        )

    def test_prepared_prompt_forbids_semantic_headline_upgrades(self):
        prompt = _build_prompt(
            deck={"language": "Chinese", "style": {}},
            slide={"number": 2, "title": "核心績效指標", "key_points": ["續約率"]},
            number=2,
            global_style_reference=None,
            base_dir=Path("."),
        )
        self.assertIn("Preserve the approved title and key-point meaning exactly", prompt)
        self.assertIn("Do not turn a topic label into a new factual assertion", prompt)

    def test_phase18_wrapper_appends_contract_when_caller_prompt_lacks_it(self):
        request = Phase18WorkerRequest.from_dict({
            "operation": "generate",
            "slide_id": "slide_02",
            "prompt": "Render the approved plate.",
            "output_path": "origin_image/slide_02.png",
            "visual_plate_job": manifest(),
        })
        prompt = build_worker_prompt(request.image_request)
        self.assertEqual(
            classify_reserved_zone_prompt(prompt, manifest()),
            ReservedZonePromptCompliance.CLEARLY_PROPAGATED,
        )

    def test_phase18_wrapper_rejects_unsafe_manifest_before_dispatch(self):
        value = manifest()
        value["reserved_zones"][0]["plate_requirement"] = "LOCKED_IN_PLATE"
        with self.assertRaises(InvalidRequestError):
            Phase18WorkerRequest.from_dict({
                "operation": "generate", "slide_id": "slide_02", "prompt": "render",
                "output_path": "slide.png", "visual_plate_job": value,
            })

    def test_prepared_job_conversion_preserves_visual_plate_contract(self):
        value = manifest()
        prepared = {
            "slide": 2,
            "prompt": render_reserved_zone_contract(value),
            "out": "slide_02.png",
            "visual_plate_job": value,
        }
        request = Phase18WorkerRequest.from_prepared_job(
            prepared, workspace_root="/tmp/workspace", dispatch_id="dispatch-42"
        )
        self.assertEqual(request.visual_plate_job, value)
        self.assertEqual(request.dispatch_id, "dispatch-42")
        self.assertTrue(request.job_id.startswith("slide-job:"))
        self.assertEqual(request.image_request.output_path, "origin_image/slide_02.png")

    def test_completed_wrapper_result_carries_live_evidence(self):
        with tempfile.TemporaryDirectory() as root:
            output = Path(root) / "origin_image" / "slide_02.png"
            output.parent.mkdir()
            output.write_bytes(b"synthetic-plate")
            request = Phase18WorkerRequest.from_dict({
                "operation": "generate", "slide_id": "slide_02", "prompt": "render",
                "output_path": "origin_image/slide_02.png", "workspace_root": root,
                "dispatch_id": "dispatch-42", "job_id": "job-42",
                "visual_plate_job": manifest(),
            })
            base_result = AdapterResult(
                status="completed", slide_id="slide_02", operation="generate",
                backend="codex_builtin_imagegen", output_path="origin_image/slide_02.png",
                diagnostics={"thread_id": "thread-42"},
            )
            with mock.patch("phase18_codex_worker.CodexImageAdapter.run", return_value=base_result):
                result = Phase18CodexWorker(request).run()
            self.assertEqual(result.diagnostics["qualification_evidence"], "LIVE_VERIFIED")
            self.assertEqual(result.diagnostics["worker_contract"]["prompt_compliance"], "CLEARLY_PROPAGATED")
            self.assertIn("worker_result_id", result.diagnostics)


class QualificationEvidenceTests(unittest.TestCase):
    def test_live_evidence_requires_concrete_identifiers_and_hashes(self):
        record = {
            "backend": "codex_builtin_imagegen", "status": "completed",
            "dispatch_id": "dispatch-1", "job_id": "job-1", "thread_id": "thread-1",
            "worker_result_id": "result-1", "plate_artifact_sha256": "a" * 64,
            "reserved_zone_manifest_sha256": "b" * 64, "output_artifact_sha256": "c" * 64,
        }
        self.assertEqual(classify_qualification_evidence(record), QualificationEvidence.LIVE_VERIFIED)

    def test_proxy_is_never_live_verified(self):
        self.assertEqual(
            classify_qualification_evidence({"proxy": True, "backend": "codex_builtin_imagegen"}),
            QualificationEvidence.PROXY_ONLY,
        )

    def test_incomplete_evidence_is_insufficient(self):
        self.assertEqual(
            classify_qualification_evidence({"backend": "codex_builtin_imagegen", "status": "completed"}),
            QualificationEvidence.INSUFFICIENT_EVIDENCE,
        )

    def test_sample_provenance_is_explicit(self):
        self.assertEqual(
            classify_sample_provenance({"artifact_kind": "RAW_PLATE", "plate_artifact_sha256": "a" * 64}),
            SampleProvenance.RAW_PLATE,
        )
        self.assertEqual(
            classify_sample_provenance({
                "artifact_kind": "HYBRID_PREVIEW", "artifact_ref": "sample.pptx",
                "hybrid_manifest_sha256": "b" * 64, "rendered_preview_sha256": "c" * 64,
            }),
            SampleProvenance.HYBRID_PREVIEW,
        )

    def test_plain_sample_reference_is_not_claimed_as_hybrid(self):
        with tempfile.TemporaryDirectory() as root:
            workflow = PresentationApprovalWorkflow(ProjectState.initialize(root, "provenance"))
            workflow.submit_outline(({"number": 1, "title": "Cover", "role": "cover"},))
            workflow.approve_outline()
            workflow.submit_style({"direction": "editorial"})
            workflow.approve_style()
            result = workflow.generate_sample(lambda _: "raw.png")
            self.assertFalse(result.is_hybrid_preview)
            self.assertEqual(result.provenance, SampleProvenance.AMBIGUOUS)

    def test_explicit_hybrid_sample_is_proven(self):
        with tempfile.TemporaryDirectory() as root:
            workflow = PresentationApprovalWorkflow(ProjectState.initialize(root, "provenance"))
            workflow.submit_outline(({"number": 1, "title": "Cover", "role": "cover"},))
            workflow.approve_outline()
            workflow.submit_style({"direction": "editorial"})
            workflow.approve_style()
            artifact = SampleArtifact("sample.pptx", {
                "artifact_kind": "HYBRID_PREVIEW", "artifact_ref": "sample.pptx",
                "hybrid_manifest_sha256": "b" * 64, "rendered_preview_sha256": "c" * 64,
            })
            result = workflow.generate_sample(lambda _: artifact)
            self.assertTrue(result.is_hybrid_preview)
            self.assertEqual(result.provenance, SampleProvenance.HYBRID_PREVIEW)


class JevDevelopmentLayerTests(unittest.TestCase):
    def test_confidence_routing(self):
        self.assertEqual(confidence_disposition(0.90), ConfidenceDisposition.HIGH_CONFIDENCE)
        self.assertEqual(confidence_disposition(0.75), ConfidenceDisposition.REVIEW_REQUIRED)
        self.assertEqual(confidence_disposition(0.50), ConfidenceDisposition.ESCALATE)

    def test_split_outcome_escalates(self):
        self.assertEqual(
            confidence_disposition(0.96, probabilities={"A": 0.54, "B": 0.46}),
            ConfidenceDisposition.ESCALATE,
        )

    def test_choice_parser_rejects_unbounded_answer(self):
        with self.assertRaises(ValueError):
            JevChoiceResult.parse(
                {"choice": "MAYBE", "probabilities": {"COMPLETE": 0.5, "UNSAFE": 0.5}, "confidence": 0.5},
                ("COMPLETE", "UNSAFE"),
            )

    def test_decision_record_sanitizes_secret_and_requires_capture(self):
        record = JevDecisionRecord(
            decision_id="Q1-JEV-001",
            task="Classify authorization: Bearer development-placeholder",
            answer_schema=("COMPLETE", "PARTIAL", "UNSAFE"),
            evidence_references=("fixture:complete-manifest",),
            result="COMPLETE",
            confidence=0.91,
            codex_action="Adopt only after deterministic agreement",
            escalated=False,
            final_engineering_disposition="Require manifest and prompt hash",
            repository_capture=("phase18_worker_contract.py", "test_phase18_worker_contract.py"),
        )
        encoded = record.canonical_json()
        self.assertNotIn("development-placeholder", encoded)
        self.assertIn("[REDACTED]", encoded)


if __name__ == "__main__":
    unittest.main()
