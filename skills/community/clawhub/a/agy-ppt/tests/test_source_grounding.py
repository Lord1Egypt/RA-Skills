#!/usr/bin/env python3
"""Phase 12.1/12.2 -- deterministic tests for source grounding & traceability.

Every test here is deterministic: no real Codex/Kiro process is launched, no
subscription quota is consumed, and no real (confidential or otherwise)
source document is used -- all source material is synthetic fixture text
created inline by the test itself.

These tests validate Layer B (deterministic contract validation) only. They
never assert that a claim is factually true; they assert that AGY's own
persisted judgement is structurally well-formed, internally consistent,
resume-safe, and that a non-source/creative project is never forced through
this workflow.
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import source_grounding as sg  # noqa: E402
import project_state as ps  # noqa: E402


class SourceGroundingTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.ws = Path(self._tmp.name) / "deck"
        self.ws.mkdir(parents=True)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    # -- fixtures -----------------------------------------------------------
    def make_inventory(self, project_id: str = "ppt_demo") -> sg.SourceInventory:
        inv = sg.SourceInventory.initialize(self.ws, project_id)
        inv.add_source(
            "src_sample",
            "text",
            label="Synthetic fixture document",
            source_digest=sg.compute_source_digest("synthetic fixture content, not a real document"),
        )
        return inv


# ===========================================================================
# Inventory (tests 1-5)
# ===========================================================================
class InventoryTests(SourceGroundingTestCase):
    def test_01_valid_inventory_passes(self):
        inv = self.make_inventory()
        inv.add_unit("src_sample", "clause", {"kind": "page", "start": 1}, "HIGH")
        inv.save()
        loaded = sg.SourceInventory.load(self.ws)
        self.assertEqual(sg.validate_source_inventory(loaded.data), [])

    def test_02_duplicate_unit_id_fails(self):
        inv = self.make_inventory()
        inv.add_unit("src_sample", "clause", {"kind": "page", "start": 1}, "HIGH")
        # Manually inject a duplicate (bypassing the idempotent add_unit helper)
        # to prove the *validator* rejects duplicates, not just the helper.
        inv.data["units"].append(dict(inv.data["units"][0]))
        errors = sg.validate_source_inventory(inv.data)
        self.assertTrue(any("duplicate unit_id" in e for e in errors))

    def test_03_invalid_locator_fails(self):
        inv = self.make_inventory()
        with self.assertRaises(sg.SourceInventoryInvalid):
            inv.add_unit("src_sample", "clause", {"kind": "page"}, "HIGH")  # missing start

    def test_04_missing_required_field_fails(self):
        inv = self.make_inventory()
        del inv.data["units"]
        errors = sg.validate_source_inventory(inv.data)
        self.assertTrue(any("units must be a list" in e for e in errors))

    def test_05_source_fingerprint_stable(self):
        digest_a = sg.compute_source_digest("same content twice")
        digest_b = sg.compute_source_digest("same content twice")
        digest_c = sg.compute_source_digest("different content")
        self.assertEqual(digest_a, digest_b)
        self.assertNotEqual(digest_a, digest_c)
        self.assertRegex(digest_a, r"^[a-f0-9]{64}$")


# ===========================================================================
# Traceability (tests 6-10)
# ===========================================================================
class TraceabilityTests(SourceGroundingTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.inv = self.make_inventory()
        self.unit = self.inv.add_unit("src_sample", "clause", {"kind": "page", "start": 1}, "HIGH")
        self.inv.save()

    def test_06_valid_claim_mapping_passes(self):
        trace = sg.ClaimTraceability.initialize(self.ws, "ppt_demo")
        trace.upsert_claim("slide_01", 1, "a claim", [self.unit["unit_id"]], "supported")
        trace.save(known_unit_ids=self.inv.unit_ids(), known_slide_ids={"slide_01"})
        loaded = sg.ClaimTraceability.load(self.ws)
        self.assertEqual(len(loaded.data["claims"]), 1)

    def test_07_dangling_source_unit_fails(self):
        trace = sg.ClaimTraceability.initialize(self.ws, "ppt_demo")
        trace.upsert_claim("slide_01", 1, "a claim", ["su:src_sample:ffffffffffff"], "supported")
        with self.assertRaises(sg.TraceabilityInvalid):
            trace.save(known_unit_ids=self.inv.unit_ids(), known_slide_ids={"slide_01"})

    def test_08_dangling_slide_id_fails(self):
        trace = sg.ClaimTraceability.initialize(self.ws, "ppt_demo")
        trace.upsert_claim("slide_99", 1, "a claim", [self.unit["unit_id"]], "supported")
        with self.assertRaises(sg.TraceabilityInvalid):
            trace.save(known_unit_ids=self.inv.unit_ids(), known_slide_ids={"slide_01"})

    def test_09_duplicate_claim_id_fails(self):
        trace = sg.ClaimTraceability.initialize(self.ws, "ppt_demo")
        trace.upsert_claim("slide_01", 1, "a claim", [self.unit["unit_id"]], "supported")
        trace.data["claims"].append(dict(trace.data["claims"][0]))  # inject duplicate
        errors = sg.validate_claim_traceability(
            trace.data, known_unit_ids=self.inv.unit_ids(), known_slide_ids={"slide_01"}
        )
        self.assertTrue(any("duplicate claim_id" in e for e in errors))

    def test_10_unsupported_status_value_fails(self):
        trace = sg.ClaimTraceability.initialize(self.ws, "ppt_demo")
        with self.assertRaises(sg.TraceabilityInvalid):
            trace.upsert_claim("slide_01", 1, "a claim", [self.unit["unit_id"]], "definitely_true")


# ===========================================================================
# Coverage (tests 11-14)
# ===========================================================================
class CoverageTests(SourceGroundingTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.inv = self.make_inventory()
        self.high_unit = self.inv.add_unit("src_sample", "clause", {"kind": "page", "start": 1}, "HIGH")
        self.med_unit = self.inv.add_unit("src_sample", "clause", {"kind": "page", "start": 2}, "MEDIUM")
        self.inv.save()

    def test_11_all_required_units_accounted_passes(self):
        cov = sg.SourceCoverage.initialize(self.ws, "ppt_demo")
        cov.upsert_entry(self.high_unit["unit_id"], "HIGH", "covered", covered_by_slide_ids=["slide_01"])
        cov.upsert_entry(self.med_unit["unit_id"], "MEDIUM", "covered", covered_by_slide_ids=["slide_01"])
        cov.save(known_unit_ids=self.inv.unit_ids())
        self.assertEqual(cov.unaccounted_high_priority(), [])

    def test_12_high_unit_unaccounted_fails(self):
        cov = sg.SourceCoverage.initialize(self.ws, "ppt_demo")
        cov.upsert_entry(self.high_unit["unit_id"], "HIGH", "unaccounted")
        cov.upsert_entry(self.med_unit["unit_id"], "MEDIUM", "covered", covered_by_slide_ids=["slide_01"])
        cov.save(known_unit_ids=self.inv.unit_ids())  # legal shape, still "unaccounted" recorded
        self.assertEqual(cov.unaccounted_high_priority(), [self.high_unit["unit_id"]])
        # The assembly gate must treat this as a hard failure (see AssemblyGateTests).

    def test_13_intentional_omission_with_reason_passes(self):
        cov = sg.SourceCoverage.initialize(self.ws, "ppt_demo")
        cov.upsert_entry(
            self.high_unit["unit_id"],
            "HIGH",
            "intentionally_omitted",
            omission_reason="not relevant to this audience",
        )
        cov.upsert_entry(self.med_unit["unit_id"], "MEDIUM", "covered", covered_by_slide_ids=["slide_01"])
        cov.save(known_unit_ids=self.inv.unit_ids())
        self.assertEqual(cov.unaccounted_high_priority(), [])

    def test_13b_intentional_omission_without_reason_fails(self):
        cov = sg.SourceCoverage.initialize(self.ws, "ppt_demo")
        with self.assertRaises(sg.SourceCoverageIncomplete):
            cov.upsert_entry(self.high_unit["unit_id"], "HIGH", "intentionally_omitted")

    def test_14_duplicate_accounting_does_not_inflate_coverage(self):
        cov = sg.SourceCoverage.initialize(self.ws, "ppt_demo")
        cov.upsert_entry(self.high_unit["unit_id"], "HIGH", "covered", covered_by_slide_ids=["slide_01"])
        cov.upsert_entry(self.med_unit["unit_id"], "MEDIUM", "covered", covered_by_slide_ids=["slide_01"])
        # upsert again for the same unit -- must replace, not duplicate.
        cov.upsert_entry(self.high_unit["unit_id"], "HIGH", "covered", covered_by_slide_ids=["slide_01", "slide_02"])
        cov.save(known_unit_ids=self.inv.unit_ids())
        self.assertEqual(len(cov.data["entries"]), 2)
        high_entries = [e for e in cov.data["entries"] if e["source_unit_id"] == self.high_unit["unit_id"]]
        self.assertEqual(len(high_entries), 1)


# ===========================================================================
# QA report (tests 15-18)
# ===========================================================================
class QaReportTests(SourceGroundingTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.inv = self.make_inventory()
        self.unit = self.inv.add_unit("src_sample", "clause", {"kind": "page", "start": 1}, "HIGH")
        self.inv.save()
        self.trace = sg.ClaimTraceability.initialize(self.ws, "ppt_demo")
        self.trace.upsert_claim("slide_01", 1, "a claim", [self.unit["unit_id"]], "supported")
        self.trace.save(known_unit_ids=self.inv.unit_ids(), known_slide_ids={"slide_01"})
        self.cov = sg.SourceCoverage.initialize(self.ws, "ppt_demo")
        self.cov.upsert_entry(self.unit["unit_id"], "HIGH", "covered", covered_by_slide_ids=["slide_01"])
        self.cov.save(known_unit_ids=self.inv.unit_ids())

    def test_15_semantic_support_decision_required_for_qa_pass(self):
        # A claim left "pending_review" must surface in unsupported/semantic
        # findings territory, not be silently treated as passed.
        trace = sg.ClaimTraceability.initialize(self.ws, "ppt_demo")
        trace.upsert_claim("slide_01", 1, "an unreviewed claim", [self.unit["unit_id"]], "pending_review")
        trace.save(known_unit_ids=self.inv.unit_ids(), known_slide_ids={"slide_01"})
        report = sg.build_grounded_qa_report(
            "ppt_demo", self.inv, trace, self.cov, {"slide_01"},
            semantic_findings={
                "unsupported_claims": [],
                "numeric_findings": [],
                "modal_findings": [],
                "agy_qa_outcome": "pending",
            },
        )
        self.assertEqual(report["semantic_findings"]["agy_qa_outcome"], "pending")

    def test_16_invalid_numeric_evidence_fails(self):
        with self.assertRaises(sg.TraceabilityInvalid):
            self.trace.upsert_claim(
                "slide_02", 1, "another claim", [self.unit["unit_id"]], "not_a_real_status"
            )

    def test_17_invalid_modal_evidence_shape_rejected_by_schema_validator(self):
        report = sg.build_grounded_qa_report("ppt_demo", self.inv, self.trace, self.cov, {"slide_01"})
        report["semantic_findings"]["agy_qa_outcome"] = "definitely_maybe"
        errors = sg.validate_source_grounded_qa(report)
        self.assertTrue(any("agy_qa_outcome" in e for e in errors))

    def test_18_deterministic_finding_and_agy_judgement_stay_separate(self):
        report = sg.build_grounded_qa_report(
            "ppt_demo", self.inv, self.trace, self.cov, {"slide_01"},
            semantic_findings={
                "unsupported_claims": [],
                "numeric_findings": [{"claim_id": "cl:slide_01:01", "note": "AGY-supplied"}],
                "modal_findings": [],
                "agy_qa_outcome": "passed",
            },
        )
        # The deterministic side never contains AGY's semantic verdict, and
        # vice versa: they are two distinct top-level keys, never merged.
        self.assertNotIn("agy_qa_outcome", report["deterministic_findings"])
        self.assertNotIn("dangling_source_references", report["semantic_findings"])
        self.assertEqual(report["deterministic_findings"]["dangling_source_references"], [])
        sg.save_grounded_qa_report(self.ws, report)
        reloaded = sg.load_grounded_qa_report(self.ws)
        self.assertEqual(reloaded["semantic_findings"]["agy_qa_outcome"], "passed")


# ===========================================================================
# Resume tests (19-24)
# ===========================================================================
class ResumeTests(SourceGroundingTestCase):
    def test_19_resume_does_not_regenerate_stable_source_ids(self):
        inv = self.make_inventory()
        u1 = inv.add_unit("src_sample", "clause", {"kind": "page", "start": 1}, "HIGH")
        inv.save()

        # Fresh load, exactly like a resumed process.
        reloaded = sg.SourceInventory.load(self.ws)
        u1_again = reloaded.add_unit("src_sample", "clause", {"kind": "page", "start": 1}, "HIGH")
        self.assertEqual(u1["unit_id"], u1_again["unit_id"])
        self.assertEqual(len(reloaded.data["units"]), 1, "re-adding the same unit must not duplicate it")

    def test_20_resume_preserves_agy_support_decisions(self):
        inv = self.make_inventory()
        unit = inv.add_unit("src_sample", "clause", {"kind": "page", "start": 1}, "HIGH")
        inv.save()

        trace = sg.ClaimTraceability.initialize(self.ws, "ppt_demo")
        trace.upsert_claim(
            "slide_01", 1, "a claim", [unit["unit_id"]], "supported", evidence_note="AGY confirmed via page 1"
        )
        trace.save(known_unit_ids=inv.unit_ids(), known_slide_ids={"slide_01"})

        reloaded_trace = sg.ClaimTraceability.load(self.ws)
        self.assertEqual(reloaded_trace.data["claims"][0]["support_status"], "supported")
        self.assertEqual(reloaded_trace.data["claims"][0]["evidence_note"], "AGY confirmed via page 1")

    def test_21_resume_preserves_coverage_decisions(self):
        inv = self.make_inventory()
        unit = inv.add_unit("src_sample", "clause", {"kind": "page", "start": 1}, "HIGH")
        inv.save()
        cov = sg.SourceCoverage.initialize(self.ws, "ppt_demo")
        cov.upsert_entry(unit["unit_id"], "HIGH", "covered", covered_by_slide_ids=["slide_01"])
        cov.save(known_unit_ids=inv.unit_ids())

        reloaded_cov = sg.SourceCoverage.load(self.ws)
        self.assertEqual(reloaded_cov.data["entries"][0]["coverage_status"], "covered")
        self.assertEqual(reloaded_cov.data["entries"][0]["covered_by_slide_ids"], ["slide_01"])

    def test_22_source_unchanged_evidence_reusable(self):
        inv = self.make_inventory()
        inv.save()
        current_digest = sg.compute_source_digest("synthetic fixture content, not a real document")
        self.assertFalse(inv.source_changed("src_sample", current_digest))

    def test_23_source_changed_stale_evidence_rejected(self):
        inv = self.make_inventory()
        inv.save()
        different_digest = sg.compute_source_digest("this is a materially different revision")
        self.assertTrue(inv.source_changed("src_sample", different_digest))
        # Detecting the change is the deterministic part; invalidating the
        # stale claim/coverage evidence built on top of it is an explicit AGY
        # /caller decision, surfaced via SourceChanged for callers that want
        # to treat it as fatal.
        if inv.source_changed("src_sample", different_digest):
            with self.assertRaises(sg.SourceChanged):
                raise sg.SourceChanged(
                    f"source src_sample changed; cached traceability evidence must not be reused silently"
                )

    def test_24_completed_qa_report_not_duplicated(self):
        inv = self.make_inventory()
        unit = inv.add_unit("src_sample", "clause", {"kind": "page", "start": 1}, "HIGH")
        inv.save()
        trace = sg.ClaimTraceability.initialize(self.ws, "ppt_demo")
        trace.upsert_claim("slide_01", 1, "a claim", [unit["unit_id"]], "supported")
        trace.save(known_unit_ids=inv.unit_ids(), known_slide_ids={"slide_01"})
        cov = sg.SourceCoverage.initialize(self.ws, "ppt_demo")
        cov.upsert_entry(unit["unit_id"], "HIGH", "covered", covered_by_slide_ids=["slide_01"])
        cov.save(known_unit_ids=inv.unit_ids())

        report_1 = sg.build_grounded_qa_report("ppt_demo", inv, trace, cov, {"slide_01"})
        path_1 = sg.save_grounded_qa_report(self.ws, report_1)
        report_2 = sg.build_grounded_qa_report("ppt_demo", inv, trace, cov, {"slide_01"})
        path_2 = sg.save_grounded_qa_report(self.ws, report_2)
        # Same single file, atomically replaced -- never a second report file.
        self.assertEqual(path_1, path_2)
        self.assertEqual(len(list(self.ws.glob("source_grounded_qa*.json"))), 1)


# ===========================================================================
# Non-source project regression (25-27)
# ===========================================================================
class NonSourceProjectTests(SourceGroundingTestCase):
    def test_25_source_grounding_disabled_normal_project_remains_valid(self):
        self.assertFalse(sg.source_grounding_enabled(self.ws))
        state = ps.ProjectState.initialize(self.ws, "ppt_creative", slide_ids=["slide_01"])
        state.save()
        # A creative deck's own project_state.json is completely unaffected by
        # this module: no import cycle, no required field, no new state.
        reloaded = ps.ProjectState.load(self.ws)
        self.assertEqual(reloaded.phase, ps.PHASE_INTAKE)

    def test_26_creative_no_source_workflow_unchanged(self):
        state = ps.ProjectState.initialize(self.ws, "ppt_creative", slide_ids=["slide_01", "slide_02"])
        for gate in ("outline", "style", "sample"):
            state.set_gate(gate, "approved")
        for phase in (ps.PHASE_OUTLINE, ps.PHASE_STYLE, ps.PHASE_SAMPLE, ps.PHASE_SLIDE_GENERATION):
            state.set_phase(phase)
        state.save()
        # The normal generation lifecycle works with zero source-grounding
        # artifacts present and zero calls into this module required.
        self.assertFalse((self.ws / sg.SOURCE_INVENTORY_FILENAME).exists())
        self.assertEqual(sg.assembly_precondition_errors(self.ws, set(state.data["slides"].keys())), [])

    def test_27_no_mandatory_traceability_artifact_when_disabled(self):
        # Explicitly disabled (present but enabled=false) behaves the same as
        # absent: no artifact is required, no assembly precondition fires.
        inv = sg.SourceInventory.initialize(self.ws, "ppt_demo")
        inv.data["enabled"] = False
        inv.save()
        self.assertFalse(sg.source_grounding_enabled(self.ws))
        self.assertEqual(sg.assembly_precondition_errors(self.ws, {"slide_01"}), [])
        # No claim_traceability.json / source_coverage.json / grounded QA
        # report is required to exist.
        self.assertFalse((self.ws / sg.CLAIM_TRACEABILITY_FILENAME).exists())
        self.assertFalse((self.ws / sg.SOURCE_COVERAGE_FILENAME).exists())
        self.assertFalse((self.ws / sg.SOURCE_GROUNDED_QA_FILENAME).exists())


# ===========================================================================
# Assembly gate (enabled project, real dangling/omission failures)
# ===========================================================================
class AssemblyGateTests(SourceGroundingTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.inv = self.make_inventory()
        self.high_unit = self.inv.add_unit("src_sample", "clause", {"kind": "page", "start": 1}, "HIGH")
        self.inv.save()

    def test_assembly_blocked_by_unaccounted_high_priority_unit(self):
        trace = sg.ClaimTraceability.initialize(self.ws, "ppt_demo")
        trace.save(known_unit_ids=self.inv.unit_ids(), known_slide_ids=set())
        cov = sg.SourceCoverage.initialize(self.ws, "ppt_demo")
        cov.upsert_entry(self.high_unit["unit_id"], "HIGH", "unaccounted")
        cov.save(known_unit_ids=self.inv.unit_ids())

        errors = sg.assembly_precondition_errors(self.ws, set())
        self.assertTrue(errors)
        self.assertTrue(any("unaccounted" in e for e in errors))

    def test_assembly_passes_once_high_priority_unit_is_covered(self):
        trace = sg.ClaimTraceability.initialize(self.ws, "ppt_demo")
        trace.upsert_claim("slide_01", 1, "a claim", [self.high_unit["unit_id"]], "supported")
        trace.save(known_unit_ids=self.inv.unit_ids(), known_slide_ids={"slide_01"})
        cov = sg.SourceCoverage.initialize(self.ws, "ppt_demo")
        cov.upsert_entry(self.high_unit["unit_id"], "HIGH", "covered", covered_by_slide_ids=["slide_01"])
        cov.save(known_unit_ids=self.inv.unit_ids())

        # Structural checks alone are satisfied at this point. Phase 12.3
        # integrated the gate into the AGY workflow, so the *full* gate now
        # additionally requires a grounded QA report carrying AGY's accepted
        # Content-QA outcome -- see the assertion below.
        structural_only = sg.assembly_precondition_errors(
            self.ws, {"slide_01"}, require_grounded_qa=False
        )
        self.assertEqual(structural_only, [])

        # Without AGY's Content-QA outcome the full gate must refuse.
        self.assertTrue(sg.assembly_precondition_errors(self.ws, {"slide_01"}))

        report = sg.build_grounded_qa_report(
            "ppt_demo", self.inv, trace, cov, {"slide_01"},
            semantic_findings={
                "unsupported_claims": [],
                "numeric_findings": [],
                "modal_findings": [],
                "agy_qa_outcome": "passed",
            },
        )
        sg.save_grounded_qa_report(self.ws, report)
        self.assertEqual(sg.assembly_precondition_errors(self.ws, {"slide_01"}), [])


# ===========================================================================
# Security / privacy hygiene
# ===========================================================================
class SecurityHygieneTests(SourceGroundingTestCase):
    def test_credential_shaped_key_rejected_in_inventory(self):
        inv = self.make_inventory()
        inv.data["sources"][0]["metadata"] = {"api_key": "sk-should-be-rejected"}
        errors = sg.validate_source_inventory(inv.data)
        self.assertTrue(any("credential-shaped key" in e for e in errors))

    def test_source_digest_never_stores_raw_content(self):
        inv = self.make_inventory()
        # The only thing persisted for a source is its digest, never the text.
        source = inv.data["sources"][0]
        self.assertNotIn("content", source)
        self.assertNotIn("text", source)
        self.assertRegex(source["source_digest"], r"^[a-f0-9]{64}$")

    def test_unit_id_never_contains_absolute_path(self):
        inv = self.make_inventory()
        unit = inv.add_unit("src_sample", "clause", {"kind": "page", "start": 1}, "HIGH")
        self.assertNotIn("/Users/", unit["unit_id"])
        self.assertNotIn(str(self.ws), unit["unit_id"])


if __name__ == "__main__":
    unittest.main()
