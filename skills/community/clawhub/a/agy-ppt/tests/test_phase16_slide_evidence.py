#!/usr/bin/env python3
"""Phase 16.3 slide evidence boundary tests."""

from __future__ import annotations

import hashlib
import sys
import tempfile
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ocr_grounding import GroundingPage  # noqa: E402
from phase16_claims import Claim, ContentOrigin, binding_from_grounding_page, binding_from_unit  # noqa: E402
from phase16_slide_evidence import (  # noqa: E402
    ERROR_FACTUAL_DRIFT,
    ERROR_UNSUPPORTED_EXPANSION,
    MaterialClaim,
    SlideEvidenceError,
    SlideEvidencePlan,
)
from source_grounding import SourceInventory  # noqa: E402


class SlideEvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.inv = SourceInventory.initialize(self.temp.name, "slide-evidence")
        self.digest = hashlib.sha256(b"original").hexdigest()
        self.inv.add_source("src_report", "pdf", source_digest=self.digest)
        self.unit = self.inv.add_unit("src_report", "page", {"kind": "page", "start": 1, "end": 1}, "HIGH")
        self.binding = binding_from_unit(self.inv, self.unit["unit_id"])

    def tearDown(self) -> None:
        self.temp.cleanup()

    def plan(self, text="Revenue rose 18% in 2025", bindings=None, terms=()):
        claim = Claim.create(self.inv, text, ContentOrigin.SOURCE_GROUNDED, bindings or [self.binding])
        return SlideEvidencePlan.create("slide_02", [MaterialClaim(claim, protected_terms=terms)])

    def error(self, code, function):
        with self.assertRaises(SlideEvidenceError) as caught:
            function()
        self.assertEqual(caught.exception.error_code, code)

    def test_numeric_claim_is_protected(self):
        self.error(ERROR_FACTUAL_DRIFT, lambda: self.plan().validate_rendered_text("Revenue rose 28% in 2025"))

    def test_date_claim_is_protected(self):
        self.error(ERROR_FACTUAL_DRIFT, lambda: self.plan().validate_rendered_text("Revenue rose 18% in 2024"))

    def test_paraphrased_claim_preserving_facts_passes(self):
        self.plan().validate_rendered_text("In 2025, revenue was up by 18%.")

    def test_multi_source_claim_preserves_all_refs(self):
        digest2 = hashlib.sha256(b"second").hexdigest()
        self.inv.add_source("src_second", "pdf", source_digest=digest2)
        unit2 = self.inv.add_unit("src_second", "page", {"kind": "page", "start": 3, "end": 3}, "HIGH")
        plan = self.plan(bindings=[self.binding, binding_from_unit(self.inv, unit2["unit_id"])])
        snapshot = next(iter(plan.evidence_snapshot.values()))
        self.assertEqual(len(snapshot), 2)

    def test_generated_text_drift_fails(self):
        self.error(ERROR_FACTUAL_DRIFT, lambda: self.plan("Margin was 12.5%").validate_rendered_text("Margin was 12%"))

    def test_unsupported_numeric_expansion_fails(self):
        self.error(ERROR_UNSUPPORTED_EXPANSION, lambda: self.plan().validate_rendered_text("Revenue rose 18% in 2025 and profit rose 9%"))

    def test_worker_cannot_alter_evidence_bindings(self):
        plan = self.plan()
        with self.assertRaises((FrozenInstanceError, TypeError)):
            plan.evidence_snapshot[plan.claims[0].claim.claim_id] = ()
        payload = plan.worker_instruction().to_dict()
        self.assertNotIn("evidence", payload)
        self.assertNotIn("source_id", str(payload))

    def test_deterministic_prompt_planning(self):
        first = self.plan()
        second = self.plan()
        self.assertEqual(first.plan_id, second.plan_id)
        self.assertEqual(first.worker_instruction(), second.worker_instruction())

    def test_source_identity_preserved(self):
        plan = self.plan()
        stored = next(iter(plan.evidence_snapshot.values()))[0]
        self.assertEqual(stored.source_id, "src_report")
        self.assertEqual(stored.source_digest, self.digest)

    def test_ocr_backed_evidence_path(self):
        page = GroundingPage("src_report", self.digest, self.unit["locator"], "OCR 18%", "TEXT", {"kind": "fixture"})
        binding = binding_from_grounding_page(self.inv, page)
        plan = self.plan("OCR result 18%", [binding])
        self.assertEqual(next(iter(plan.evidence_snapshot.values()))[0].unit_id, self.unit["unit_id"])


if __name__ == "__main__":
    unittest.main()
