#!/usr/bin/env python3
"""Phase 12.3 -- AGY source-grounding workflow integration tests.

These tests exercise the *workflow contract*, not model intelligence. Every
AGY semantic decision (`support_status`, coverage decisions, omission
reasons, `agy_qa_outcome`) is supplied explicitly as a synthetic decision, so
the test is fully deterministic. No real AGY LLM session, no real Codex image
generation, no `image_gen`, no live recovery, and no subscription quota are
involved.

The source material is a short synthetic "Service Agreement" created inline
by this test file. No real contract, customer document, or confidential
source is used anywhere.

Test map (see the Phase 12.3 task specification):

* Test A -- happy path: enabled + valid + accepted QA -> gate ready
* Test B -- unsupported claim -> gate refuses; after AGY resolution -> ready
* Test C -- HIGH-priority coverage gap -> gate refuses; after accounting -> ready
* Test D -- source changed -> SOURCE_CHANGED, stale evidence rejected
* Test E -- resume: stable IDs + preserved semantic decisions
* Test F -- non-source project regression (mandatory gate)
* Test G -- speaker-notes-only coverage backed by a real claim
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import project_state as ps  # noqa: E402
import source_grounding as sg  # noqa: E402

VALIDATE_CLI = SCRIPTS_DIR / "validate_source_grounding.py"

# --- Synthetic source material (NOT a real contract) -----------------------
SYNTHETIC_AGREEMENT = """\
Synthetic Service Agreement (test fixture)

Section A: Supplier must deliver report within 10 days.
Section B: Customer may terminate with 30 days notice.
Section C: Fee is 500 units.
"""

SYNTHETIC_AGREEMENT_REVISED = """\
Synthetic Service Agreement (test fixture, revision 2)

Section A: Supplier must deliver report within 15 days.
Section B: Customer may terminate with 30 days notice.
Section C: Fee is 500 units.
"""

SOURCE_ID = "src_agreement"


class WorkflowTestCase(unittest.TestCase):
    """Shared synthetic source-driven project."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.ws = Path(self._tmp.name) / "deck"
        self.ws.mkdir(parents=True)
        self.project_id = "ppt_synthetic_agreement"
        self.slide_ids = ["slide_01", "slide_02"]

    def tearDown(self) -> None:
        self._tmp.cleanup()

    # -- project state (frozen core, untouched by this module) --------------
    def make_project_state(self, slide_ids: list[str] | None = None) -> ps.ProjectState:
        state = ps.ProjectState.initialize(
            self.ws, self.project_id, slide_ids=slide_ids or self.slide_ids
        )
        for gate in ("outline", "style", "sample"):
            state.set_gate(gate, "approved")
        for phase in (
            ps.PHASE_OUTLINE,
            ps.PHASE_STYLE,
            ps.PHASE_SAMPLE,
            ps.PHASE_SLIDE_GENERATION,
        ):
            state.set_phase(phase)
        state.save()
        return state

    # -- Stage: source intake ----------------------------------------------
    def make_inventory(self, content: str = SYNTHETIC_AGREEMENT) -> sg.SourceInventory:
        """AGY intake: activate grounding, register source + fingerprint, segment units."""
        inv = sg.SourceInventory.initialize(self.ws, self.project_id)
        inv.add_source(
            SOURCE_ID,
            "text",
            label="Synthetic Service Agreement (test fixture)",
            source_digest=sg.compute_source_digest(content),
        )
        # AGY is the segmentation authority; these are AGY's chosen units.
        self.unit_a = inv.add_unit(
            SOURCE_ID, "clause", {"kind": "section", "label": "Section A"}, "HIGH",
            title="Delivery obligation",
        )
        self.unit_b = inv.add_unit(
            SOURCE_ID, "clause", {"kind": "section", "label": "Section B"}, "HIGH",
            title="Termination right",
        )
        self.unit_c = inv.add_unit(
            SOURCE_ID, "clause", {"kind": "section", "label": "Section C"}, "MEDIUM",
            title="Fee",
        )
        inv.save()
        return inv

    # -- Stage: claim planning + AGY semantic decisions --------------------
    def make_traceability(
        self,
        inv: sg.SourceInventory,
        *,
        section_a_status: str = "supported",
    ) -> sg.ClaimTraceability:
        trace = sg.ClaimTraceability.initialize(self.ws, self.project_id)
        trace.upsert_claim(
            "slide_01", 1,
            "Supplier must deliver the report within 10 days",
            [self.unit_a["unit_id"]],
            section_a_status,
            evidence_note="AGY: Section A states the 10-day delivery obligation",
            numeric_evidence={
                "source_value": "10 days",
                "slide_value": "10 days",
                "unit": "days",
                "comparison_status": "match",
            },
            modal_evidence={
                "source_modality": "must",
                "slide_modality": "must",
                "responsible_party": "Supplier",
                "comparison_status": "match",
            },
        )
        trace.upsert_claim(
            "slide_02", 1,
            "Customer may terminate with 30 days notice",
            [self.unit_b["unit_id"]],
            "supported",
            evidence_note="AGY: Section B grants a 30-day notice termination right",
            modal_evidence={
                "source_modality": "may",
                "slide_modality": "may",
                "responsible_party": "Customer",
                "comparison_status": "match",
            },
        )
        trace.save(known_unit_ids=inv.unit_ids(), known_slide_ids=set(self.slide_ids))
        return trace

    # -- Stage: coverage accounting ----------------------------------------
    def make_coverage(
        self,
        inv: sg.SourceInventory,
        trace: sg.ClaimTraceability,
        *,
        section_b_status: str = "covered",
    ) -> sg.SourceCoverage:
        cov = sg.SourceCoverage.initialize(self.ws, self.project_id)
        cov.upsert_entry(
            self.unit_a["unit_id"], "HIGH", "covered",
            covered_by_slide_ids=["slide_01"],
            covered_by_claim_ids=["cl:slide_01:01"],
        )
        if section_b_status == "covered":
            cov.upsert_entry(
                self.unit_b["unit_id"], "HIGH", "covered",
                covered_by_slide_ids=["slide_02"],
                covered_by_claim_ids=["cl:slide_02:01"],
            )
        else:
            cov.upsert_entry(self.unit_b["unit_id"], "HIGH", section_b_status)
        # AGY decided the fee clause is not needed on a slide.
        cov.upsert_entry(
            self.unit_c["unit_id"], "MEDIUM", "intentionally_omitted",
            omission_reason="AGY: fee detail is out of scope for this audience",
        )
        cov.save(known_unit_ids=inv.unit_ids(), known_claim_ids=trace.claim_ids())
        return cov

    # -- Stage: Content QA -> grounded QA report ---------------------------
    def make_qa_report(
        self,
        inv: sg.SourceInventory,
        trace: sg.ClaimTraceability,
        cov: sg.SourceCoverage,
        *,
        outcome: str = "passed",
    ) -> dict:
        report = sg.build_grounded_qa_report(
            self.project_id, inv, trace, cov, set(self.slide_ids),
            semantic_findings={
                "unsupported_claims": trace.unsupported_claim_ids(),
                "numeric_findings": [
                    {"claim_id": "cl:slide_01:01", "note": "AGY: 10 days matches Section A"}
                ],
                "modal_findings": [
                    {"claim_id": "cl:slide_02:01", "note": "AGY: 'may' preserved from Section B"}
                ],
                "agy_qa_outcome": outcome,
            },
        )
        sg.save_grounded_qa_report(self.ws, report)
        return report

    def full_grounded_project(self, **kwargs) -> tuple:
        state = self.make_project_state()
        inv = self.make_inventory()
        trace = self.make_traceability(inv, **{k: v for k, v in kwargs.items() if k == "section_a_status"})
        cov = self.make_coverage(
            inv, trace, **{k: v for k, v in kwargs.items() if k == "section_b_status"}
        )
        outcome = kwargs.get("outcome", "passed")
        self.make_qa_report(inv, trace, cov, outcome=outcome)
        return state, inv, trace, cov

    def gate(self, **kwargs) -> sg.GroundingGateResult:
        return sg.evaluate_assembly_gate(self.ws, set(self.slide_ids), **kwargs)


# ===========================================================================
# Test A -- happy path
# ===========================================================================
class TestAHappyPath(WorkflowTestCase):
    def test_a_full_source_driven_workflow_reaches_assembly_ready(self):
        self.full_grounded_project()

        self.assertTrue(sg.source_grounding_enabled(self.ws))
        result = self.gate()
        self.assertTrue(result.enabled)
        self.assertTrue(result.ready, result.errors)
        self.assertEqual(result.errors, [])
        self.assertEqual(result.error_codes, [])

    def test_a_all_four_artifacts_persisted(self):
        self.full_grounded_project()
        for filename in (
            sg.SOURCE_INVENTORY_FILENAME,
            sg.CLAIM_TRACEABILITY_FILENAME,
            sg.SOURCE_COVERAGE_FILENAME,
            sg.SOURCE_GROUNDED_QA_FILENAME,
        ):
            self.assertTrue((self.ws / filename).is_file(), filename)

    def test_a_cli_adapter_reports_ready(self):
        self.full_grounded_project()
        proc = subprocess.run(  # noqa: S603 - fixed argv, test-only
            [sys.executable, str(VALIDATE_CLI), str(self.ws)],
            capture_output=True, text=True, timeout=60, check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertTrue(payload["ready"])
        self.assertTrue(payload["source_grounding_enabled"])

    def test_a_deterministic_findings_are_clean(self):
        _, inv, trace, cov = self.full_grounded_project()
        report = sg.load_grounded_qa_report(self.ws)
        det = report["deterministic_findings"]
        self.assertEqual(det["dangling_source_references"], [])
        self.assertEqual(det["dangling_slide_references"], [])
        self.assertEqual(det["high_priority_omissions"], [])
        self.assertEqual(det["invalid_references"], [])


# ===========================================================================
# Test B -- unsupported claim
# ===========================================================================
class TestBUnsupportedClaim(WorkflowTestCase):
    def test_b_unsupported_claim_blocks_then_resolution_unblocks(self):
        state = self.make_project_state()
        inv = self.make_inventory()
        trace = self.make_traceability(inv, section_a_status="unsupported")
        cov = self.make_coverage(inv, trace)
        self.make_qa_report(inv, trace, cov, outcome="passed")

        result = self.gate()
        self.assertFalse(result.ready)
        self.assertTrue(any("unsupported/pending_review" in e for e in result.errors))
        self.assertIn(sg.ERROR_TRACEABILITY_INVALID, result.error_codes)

        # AGY resolves it: after review the claim is confirmed supported.
        trace.upsert_claim(
            "slide_01", 1,
            "Supplier must deliver the report within 10 days",
            [self.unit_a["unit_id"]],
            "supported",
            evidence_note="AGY: confirmed against Section A after review",
        )
        trace.save(known_unit_ids=inv.unit_ids(), known_slide_ids=set(self.slide_ids))
        self.make_qa_report(inv, trace, cov, outcome="passed")

        self.assertTrue(self.gate().ready, self.gate().errors)

    def test_b_pending_review_also_blocks(self):
        state = self.make_project_state()
        inv = self.make_inventory()
        trace = self.make_traceability(inv, section_a_status="pending_review")
        cov = self.make_coverage(inv, trace)
        self.make_qa_report(inv, trace, cov, outcome="passed")

        result = self.gate()
        self.assertFalse(result.ready)
        self.assertIn("cl:slide_01:01", str(result.errors))

    def test_b_deterministic_code_never_edits_the_claim(self):
        state = self.make_project_state()
        inv = self.make_inventory()
        trace = self.make_traceability(inv, section_a_status="unsupported")
        cov = self.make_coverage(inv, trace)
        self.make_qa_report(inv, trace, cov)

        self.gate()  # evaluate the gate; it must not mutate anything
        reloaded = sg.ClaimTraceability.load(self.ws)
        claim = next(c for c in reloaded.data["claims"] if c["claim_id"] == "cl:slide_01:01")
        self.assertEqual(claim["support_status"], "unsupported")


# ===========================================================================
# Test C -- HIGH priority coverage gap
# ===========================================================================
class TestCHighCoverageGap(WorkflowTestCase):
    def test_c_high_unaccounted_blocks_then_covered_unblocks(self):
        state = self.make_project_state()
        inv = self.make_inventory()
        trace = self.make_traceability(inv)
        cov = self.make_coverage(inv, trace, section_b_status="unaccounted")
        self.make_qa_report(inv, trace, cov)

        result = self.gate()
        self.assertFalse(result.ready)
        self.assertTrue(any("unaccounted" in e for e in result.errors))
        self.assertIn(sg.ERROR_SOURCE_COVERAGE_INCOMPLETE, result.error_codes)

        # AGY accounts for it properly.
        cov.upsert_entry(
            self.unit_b["unit_id"], "HIGH", "covered",
            covered_by_slide_ids=["slide_02"], covered_by_claim_ids=["cl:slide_02:01"],
        )
        cov.save(known_unit_ids=inv.unit_ids(), known_claim_ids=trace.claim_ids())
        self.make_qa_report(inv, trace, cov)

        self.assertTrue(self.gate().ready, self.gate().errors)

    def test_c_high_intentional_omission_requires_explicit_reason(self):
        state = self.make_project_state()
        inv = self.make_inventory()
        trace = self.make_traceability(inv)
        cov = self.make_coverage(inv, trace, section_b_status="unaccounted")

        # A HIGH unit may be intentionally omitted, but only with an explicit
        # AGY semantic reason -- never silently.
        with self.assertRaises(sg.SourceCoverageIncomplete):
            cov.upsert_entry(self.unit_b["unit_id"], "HIGH", "intentionally_omitted")

        cov.upsert_entry(
            self.unit_b["unit_id"], "HIGH", "intentionally_omitted",
            omission_reason="AGY: termination terms handled in a separate legal annex",
        )
        cov.save(known_unit_ids=inv.unit_ids(), known_claim_ids=trace.claim_ids())
        self.make_qa_report(inv, trace, cov)
        self.assertTrue(self.gate().ready, self.gate().errors)

    def test_c_high_omission_is_visible_in_the_qa_report(self):
        state = self.make_project_state()
        inv = self.make_inventory()
        trace = self.make_traceability(inv)
        cov = self.make_coverage(inv, trace, section_b_status="unaccounted")
        report = self.make_qa_report(inv, trace, cov)
        # An unaccounted HIGH unit must surface in the deterministic findings,
        # never be silently dropped.
        self.assertIn(self.unit_b["unit_id"], report["deterministic_findings"]["high_priority_omissions"])


# ===========================================================================
# Test D -- source changed
# ===========================================================================
class TestDSourceChanged(WorkflowTestCase):
    def test_d_changed_source_rejects_stale_evidence(self):
        self.full_grounded_project()
        self.assertTrue(self.gate().ready)

        # The source document is revised (10 days -> 15 days).
        new_digest = sg.compute_source_digest(SYNTHETIC_AGREEMENT_REVISED)
        result = self.gate(current_source_digests={SOURCE_ID: new_digest})

        self.assertFalse(result.ready)
        self.assertIn(sg.ERROR_SOURCE_CHANGED, result.error_codes)
        self.assertTrue(any(sg.ERROR_SOURCE_CHANGED in e for e in result.errors))

    def test_d_unchanged_source_digest_still_ready(self):
        self.full_grounded_project()
        same_digest = sg.compute_source_digest(SYNTHETIC_AGREEMENT)
        result = self.gate(current_source_digests={SOURCE_ID: same_digest})
        self.assertTrue(result.ready, result.errors)

    def test_d_source_changed_detected_by_inventory_helper(self):
        _, inv, _, _ = self.full_grounded_project()
        self.assertFalse(inv.source_changed(SOURCE_ID, sg.compute_source_digest(SYNTHETIC_AGREEMENT)))
        self.assertTrue(
            inv.source_changed(SOURCE_ID, sg.compute_source_digest(SYNTHETIC_AGREEMENT_REVISED))
        )

    def test_d_stale_evidence_is_not_destroyed(self):
        self.full_grounded_project()
        new_digest = sg.compute_source_digest(SYNTHETIC_AGREEMENT_REVISED)
        self.gate(current_source_digests={SOURCE_ID: new_digest})

        # Detection must not destructively delete the historical evidence; AGY
        # revalidates/rebuilds it explicitly.
        self.assertTrue((self.ws / sg.CLAIM_TRACEABILITY_FILENAME).is_file())
        reloaded = sg.ClaimTraceability.load(self.ws)
        self.assertEqual(len(reloaded.data["claims"]), 2)

    def test_d_cli_reports_source_changed(self):
        self.full_grounded_project()
        new_digest = sg.compute_source_digest(SYNTHETIC_AGREEMENT_REVISED)
        proc = subprocess.run(  # noqa: S603 - fixed argv, test-only
            [sys.executable, str(VALIDATE_CLI), str(self.ws),
             "--source-digest", f"{SOURCE_ID}={new_digest}"],
            capture_output=True, text=True, timeout=60, check=False,
        )
        self.assertEqual(proc.returncode, 1)
        payload = json.loads(proc.stdout)
        self.assertFalse(payload["ready"])
        self.assertIn(sg.ERROR_SOURCE_CHANGED, payload["error_codes"])


# ===========================================================================
# Test E -- resume
# ===========================================================================
class TestEResume(WorkflowTestCase):
    def test_e_resume_preserves_stable_ids_and_semantic_decisions(self):
        state = self.make_project_state()
        inv = self.make_inventory()
        trace = self.make_traceability(inv)
        original_unit_ids = sorted(inv.unit_ids())
        original_claim_ids = sorted(trace.claim_ids())

        # Simulate an interruption: drop every in-memory object, reload from disk.
        del inv, trace

        inv2 = sg.SourceInventory.load(self.ws)
        trace2 = sg.ClaimTraceability.load(self.ws)
        self.assertEqual(sorted(inv2.unit_ids()), original_unit_ids)
        self.assertEqual(sorted(trace2.claim_ids()), original_claim_ids)

        claim = next(c for c in trace2.data["claims"] if c["claim_id"] == "cl:slide_01:01")
        self.assertEqual(claim["support_status"], "supported")
        self.assertIn("Section A", claim["evidence_note"])

        # Re-segmenting the same source is idempotent: no new/duplicated units.
        inv2.add_unit(SOURCE_ID, "clause", {"kind": "section", "label": "Section A"}, "HIGH")
        self.assertEqual(sorted(inv2.unit_ids()), original_unit_ids)

    def test_e_resume_completes_remaining_workflow_steps(self):
        state = self.make_project_state()
        inv = self.make_inventory()
        trace = self.make_traceability(inv)
        # Interrupted before coverage/QA existed.
        self.assertFalse((self.ws / sg.SOURCE_COVERAGE_FILENAME).exists())
        self.assertFalse((self.ws / sg.SOURCE_GROUNDED_QA_FILENAME).exists())
        self.assertFalse(self.gate().ready)

        inv2 = sg.SourceInventory.load(self.ws)
        trace2 = sg.ClaimTraceability.load(self.ws)
        cov = self.make_coverage(inv2, trace2)
        self.make_qa_report(inv2, trace2, cov)
        self.assertTrue(self.gate().ready, self.gate().errors)

    def test_e_resume_does_not_duplicate_entries_or_reports(self):
        self.full_grounded_project()
        inv2 = sg.SourceInventory.load(self.ws)
        trace2 = sg.ClaimTraceability.load(self.ws)
        cov2 = sg.SourceCoverage.load(self.ws)

        # Re-running each upsert with identical input must not grow anything.
        trace2.upsert_claim(
            "slide_01", 1,
            "Supplier must deliver the report within 10 days",
            [self.unit_a["unit_id"]], "supported",
        )
        cov2.upsert_entry(
            self.unit_a["unit_id"], "HIGH", "covered",
            covered_by_slide_ids=["slide_01"], covered_by_claim_ids=["cl:slide_01:01"],
        )
        trace2.save(known_unit_ids=inv2.unit_ids(), known_slide_ids=set(self.slide_ids))
        cov2.save(known_unit_ids=inv2.unit_ids(), known_claim_ids=trace2.claim_ids())
        self.make_qa_report(inv2, trace2, cov2)

        self.assertEqual(len(sg.ClaimTraceability.load(self.ws).data["claims"]), 2)
        self.assertEqual(len(sg.SourceCoverage.load(self.ws).data["entries"]), 3)
        self.assertEqual(len(list(self.ws.glob("source_grounded_qa*.json"))), 1)

    def test_e_resume_with_new_slide_keeps_existing_ids(self):
        state = self.make_project_state()
        inv = self.make_inventory()
        trace = self.make_traceability(inv)
        original_claim_ids = sorted(trace.claim_ids())

        # A new slide is added later in the project (frozen ProjectState API).
        state = ps.ProjectState.load(self.ws)
        state.add_slide("slide_03")
        state.save()
        extended_slides = set(state.data["slides"].keys())
        self.assertEqual(extended_slides, {"slide_01", "slide_02", "slide_03"})

        # Existing claim ids are untouched; only a new one is added.
        trace2 = sg.ClaimTraceability.load(self.ws)
        trace2.upsert_claim(
            "slide_03", 1, "Fee is 500 units", [self.unit_c["unit_id"]], "supported",
        )
        trace2.save(known_unit_ids=inv.unit_ids(), known_slide_ids=extended_slides)

        new_ids = sorted(trace2.claim_ids())
        for claim_id in original_claim_ids:
            self.assertIn(claim_id, new_ids, "existing claim ids must not drift")
        self.assertIn("cl:slide_03:01", new_ids)

    def test_e_deleted_claim_evidence_does_not_leak_to_a_new_claim(self):
        state = self.make_project_state()
        inv = self.make_inventory()
        trace = self.make_traceability(inv)

        # AGY replaces slide_01's claim with different content at the same
        # slide-local sequence. upsert must overwrite wholesale, never merge
        # stale evidence into the new semantic claim.
        trace.upsert_claim(
            "slide_01", 1,
            "Supplier delivers a summary, not the full report",
            [self.unit_a["unit_id"]],
            "partially_supported",
        )
        trace.save(known_unit_ids=inv.unit_ids(), known_slide_ids=set(self.slide_ids))

        claim = next(c for c in sg.ClaimTraceability.load(self.ws).data["claims"]
                     if c["claim_id"] == "cl:slide_01:01")
        self.assertEqual(claim["support_status"], "partially_supported")
        self.assertIsNone(claim["evidence_note"], "stale evidence must not survive the overwrite")
        self.assertIsNone(claim["numeric_evidence"])
        self.assertIsNone(claim["modal_evidence"])


# ===========================================================================
# Test F -- non-source project regression (mandatory gate)
# ===========================================================================
class TestFNonSourceRegression(WorkflowTestCase):
    def test_f_creative_project_needs_no_grounding_artifacts(self):
        state = self.make_project_state()
        self.assertFalse(sg.source_grounding_enabled(self.ws))

        result = self.gate()
        self.assertFalse(result.enabled)
        self.assertTrue(result.ready)
        self.assertEqual(result.errors, [])

        for filename in (
            sg.SOURCE_INVENTORY_FILENAME,
            sg.CLAIM_TRACEABILITY_FILENAME,
            sg.SOURCE_COVERAGE_FILENAME,
            sg.SOURCE_GROUNDED_QA_FILENAME,
        ):
            self.assertFalse((self.ws / filename).exists(), filename)

    def test_f_explicitly_disabled_behaves_like_absent(self):
        self.make_project_state()
        inv = sg.SourceInventory.initialize(self.ws, self.project_id)
        inv.data["enabled"] = False
        inv.save()

        self.assertFalse(sg.source_grounding_enabled(self.ws))
        self.assertTrue(self.gate().ready)

    def test_f_visual_qa_lifecycle_unaffected(self):
        state = self.make_project_state()
        # The frozen Visual QA state machine still works exactly as before,
        # with zero awareness of source grounding.
        state.set_slide_status("slide_01", ps.SLIDE_READY)
        state.begin_generation("slide_01")
        state.record_worker_result("slide_01", {
            "status": "completed",
            "slide_id": "slide_01",
            "operation": "generate",
            "backend": "codex_builtin_imagegen",
            "output_path": "origin_image/slide_01.png",
            "diagnostics": {"auth": "chatgpt_cli_session", "api_fallback_used": False},
        })
        state.set_slide_status("slide_01", ps.SLIDE_QA_PASSED, by=ps.CONTROLLER)
        state.save()
        self.assertEqual(state.slide("slide_01")["status"], ps.SLIDE_QA_PASSED)
        self.assertTrue(self.gate().ready)

    def test_f_cli_exits_zero_for_disabled_project(self):
        self.make_project_state()
        proc = subprocess.run(  # noqa: S603 - fixed argv, test-only
            [sys.executable, str(VALIDATE_CLI), str(self.ws)],
            capture_output=True, text=True, timeout=60, check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertFalse(payload["source_grounding_enabled"])
        self.assertTrue(payload["ready"])


# ===========================================================================
# Test G -- speaker-notes-only coverage
# ===========================================================================
class TestGSpeakerNotesOnly(WorkflowTestCase):
    def test_g_speaker_notes_only_coverage_backed_by_a_claim(self):
        state = self.make_project_state()
        inv = self.make_inventory()
        trace = self.make_traceability(inv)

        # A source-dependent claim that lives in speech.md rather than on the
        # slide image still gets a claim_id, source mapping and support status.
        trace.upsert_claim(
            "slide_02", 2,
            "Fee is 500 units (spoken only, not shown on the slide)",
            [self.unit_c["unit_id"]],
            "supported",
            evidence_note="AGY: delivered verbally from Section C; kept off the slide",
        )
        trace.save(known_unit_ids=inv.unit_ids(), known_slide_ids=set(self.slide_ids))

        cov = sg.SourceCoverage.initialize(self.ws, self.project_id)
        cov.upsert_entry(
            self.unit_a["unit_id"], "HIGH", "covered",
            covered_by_slide_ids=["slide_01"], covered_by_claim_ids=["cl:slide_01:01"],
        )
        cov.upsert_entry(
            self.unit_b["unit_id"], "HIGH", "covered",
            covered_by_slide_ids=["slide_02"], covered_by_claim_ids=["cl:slide_02:01"],
        )
        cov.upsert_entry(
            self.unit_c["unit_id"], "MEDIUM", "speaker_notes_only",
            covered_by_slide_ids=["slide_02"], covered_by_claim_ids=["cl:slide_02:02"],
        )
        cov.save(known_unit_ids=inv.unit_ids(), known_claim_ids=trace.claim_ids())
        self.make_qa_report(inv, trace, cov)

        self.assertTrue(self.gate().ready, self.gate().errors)

    def test_g_speaker_notes_only_without_a_claim_is_rejected(self):
        state = self.make_project_state()
        inv = self.make_inventory()
        trace = self.make_traceability(inv)

        cov = sg.SourceCoverage.initialize(self.ws, self.project_id)
        cov.upsert_entry(
            self.unit_a["unit_id"], "HIGH", "covered",
            covered_by_slide_ids=["slide_01"], covered_by_claim_ids=["cl:slide_01:01"],
        )
        cov.upsert_entry(
            self.unit_b["unit_id"], "HIGH", "covered",
            covered_by_slide_ids=["slide_02"], covered_by_claim_ids=["cl:slide_02:01"],
        )
        # "covered in the notes" with no claim backing it is unverifiable.
        cov.upsert_entry(self.unit_c["unit_id"], "MEDIUM", "speaker_notes_only")
        with self.assertRaises(sg.SourceCoverageIncomplete):
            cov.save(known_unit_ids=inv.unit_ids(), known_claim_ids=trace.claim_ids())

    def test_g_speaker_notes_claim_reference_must_exist(self):
        state = self.make_project_state()
        inv = self.make_inventory()
        trace = self.make_traceability(inv)

        cov = sg.SourceCoverage.initialize(self.ws, self.project_id)
        cov.upsert_entry(
            self.unit_a["unit_id"], "HIGH", "covered",
            covered_by_slide_ids=["slide_01"], covered_by_claim_ids=["cl:slide_01:01"],
        )
        cov.upsert_entry(
            self.unit_b["unit_id"], "HIGH", "covered",
            covered_by_slide_ids=["slide_02"], covered_by_claim_ids=["cl:slide_02:01"],
        )
        cov.upsert_entry(
            self.unit_c["unit_id"], "MEDIUM", "speaker_notes_only",
            covered_by_claim_ids=["cl:slide_02:99"],  # does not exist
        )
        with self.assertRaises(sg.SourceCoverageIncomplete):
            cov.save(known_unit_ids=inv.unit_ids(), known_claim_ids=trace.claim_ids())


# ===========================================================================
# Boundary: grounding precondition failure is NOT an assembly failure
# ===========================================================================
class GroundingPreconditionBoundaryTests(WorkflowTestCase):
    def test_grounding_failure_uses_its_own_error_taxonomy(self):
        state = self.make_project_state()
        inv = self.make_inventory()
        trace = self.make_traceability(inv, section_a_status="unsupported")
        cov = self.make_coverage(inv, trace)
        self.make_qa_report(inv, trace, cov)

        result = self.gate()
        self.assertFalse(result.ready)
        # Never an image/worker error code, never an assembly-failure code.
        for code in result.error_codes:
            self.assertNotIn("IMAGE_", code)
            self.assertNotEqual(code, "ASSEMBLY_FAILED")
            self.assertTrue(
                code.startswith("SOURCE_") or code.startswith("TRACEABILITY_")
                or code.startswith("GROUNDED_QA_") or code.startswith("CODEX_PPT_"),
                f"unexpected error code family: {code}",
            )

    def test_grounding_failure_does_not_touch_project_state(self):
        state = self.make_project_state()
        inv = self.make_inventory()
        trace = self.make_traceability(inv, section_a_status="unsupported")
        cov = self.make_coverage(inv, trace)
        self.make_qa_report(inv, trace, cov)

        phase_before = ps.ProjectState.load(self.ws).phase
        self.gate()
        after = ps.ProjectState.load(self.ws)
        # No blocked path, no phase change, no slide state change.
        self.assertEqual(after.phase, phase_before)
        self.assertNotEqual(after.phase, ps.PHASE_BLOCKED)

    def test_qa_outcome_must_be_accepted_even_when_structurally_clean(self):
        state = self.make_project_state()
        inv = self.make_inventory()
        trace = self.make_traceability(inv)
        cov = self.make_coverage(inv, trace)
        self.make_qa_report(inv, trace, cov, outcome="failed")

        result = self.gate()
        self.assertFalse(result.ready)
        self.assertIn(sg.ERROR_GROUNDED_QA_INCOMPLETE, result.error_codes)

        self.make_qa_report(inv, trace, cov, outcome="passed_with_notes")
        self.assertTrue(self.gate().ready, self.gate().errors)


# ===========================================================================
# Security / privacy hygiene for the workflow fixtures
# ===========================================================================
class WorkflowSecurityTests(WorkflowTestCase):
    def test_artifacts_never_persist_full_source_content(self):
        self.full_grounded_project()
        for filename in (
            sg.SOURCE_INVENTORY_FILENAME,
            sg.CLAIM_TRACEABILITY_FILENAME,
            sg.SOURCE_COVERAGE_FILENAME,
            sg.SOURCE_GROUNDED_QA_FILENAME,
        ):
            text = (self.ws / filename).read_text(encoding="utf-8")
            self.assertNotIn("Synthetic Service Agreement (test fixture)\n\nSection A", text)
            self.assertNotIn(SYNTHETIC_AGREEMENT, text)

    def test_artifacts_contain_no_absolute_local_paths(self):
        self.full_grounded_project()
        for filename in (
            sg.SOURCE_INVENTORY_FILENAME,
            sg.CLAIM_TRACEABILITY_FILENAME,
            sg.SOURCE_COVERAGE_FILENAME,
            sg.SOURCE_GROUNDED_QA_FILENAME,
        ):
            text = (self.ws / filename).read_text(encoding="utf-8")
            self.assertNotIn("/Users/", text)
            self.assertNotIn(str(self.ws), text)


if __name__ == "__main__":
    unittest.main()
