#!/usr/bin/env python3
"""Phase 16.1 deterministic claim/evidence contract tests."""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ocr_grounding import GroundingPage  # noqa: E402
from phase16_claims import (  # noqa: E402
    ERROR_EVIDENCE_REFERENCE_INVALID,
    ERROR_EVIDENCE_REQUIRED,
    ERROR_LOCATOR_MISMATCH,
    ERROR_SOURCE_MISMATCH,
    Claim,
    ClaimContractError,
    ContentOrigin,
    EvidenceBinding,
    binding_from_grounding_page,
    binding_from_unit,
)
from source_grounding import SourceInventory, compute_source_digest  # noqa: E402


class ClaimContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.inventory = SourceInventory.initialize(self.temp.name, "phase16")
        self.digest = compute_source_digest(b"original source")
        self.inventory.add_source("src_pdf", "pdf", label="Report", source_digest=self.digest)
        self.unit = self.inventory.add_unit(
            "src_pdf", "page", {"kind": "page", "start": 2, "end": 2}, "HIGH", title="Metric"
        )
        self.binding = binding_from_unit(self.inventory, self.unit["unit_id"])

    def tearDown(self) -> None:
        self.temp.cleanup()

    def error(self, code: str, function) -> None:
        with self.assertRaises(ClaimContractError) as caught:
            function()
        self.assertEqual(caught.exception.error_code, code)

    def test_valid_source_grounded_claim(self):
        claim = Claim.create(self.inventory, "Revenue increased 18%.", ContentOrigin.SOURCE_GROUNDED, [self.binding])
        self.assertEqual(claim.origin, ContentOrigin.SOURCE_GROUNDED)
        self.assertEqual(claim.evidence, (self.binding,))

    def test_source_grounded_claim_missing_evidence_fails_closed(self):
        self.error(ERROR_EVIDENCE_REQUIRED, lambda: Claim.create(
            self.inventory, "Revenue increased.", ContentOrigin.SOURCE_GROUNDED
        ))

    def test_invalid_evidence_reference_has_no_fuzzy_correction(self):
        bad = EvidenceBinding("src_pdf", self.digest, "su:src_pdf:000000000000", self.unit["locator"])
        self.error(ERROR_EVIDENCE_REFERENCE_INVALID, lambda: Claim.create(
            self.inventory, "Claim", ContentOrigin.SOURCE_GROUNDED, [bad]
        ))

    def test_source_mismatch(self):
        bad = EvidenceBinding("src_other", self.digest, self.unit["unit_id"], self.unit["locator"])
        self.error(ERROR_SOURCE_MISMATCH, lambda: Claim.create(
            self.inventory, "Claim", ContentOrigin.SOURCE_GROUNDED, [bad]
        ))

    def test_locator_mismatch(self):
        bad = EvidenceBinding("src_pdf", self.digest, self.unit["unit_id"], {"kind": "page", "start": 3, "end": 3})
        self.error(ERROR_LOCATOR_MISMATCH, lambda: Claim.create(
            self.inventory, "Claim", ContentOrigin.SOURCE_GROUNDED, [bad]
        ))

    def test_user_provided_without_evidence(self):
        claim = Claim.create(self.inventory, "Our target is 20%.", ContentOrigin.USER_PROVIDED)
        self.assertEqual(claim.origin, ContentOrigin.USER_PROVIDED)
        self.assertEqual(claim.evidence, ())

    def test_agy_synthesis_without_evidence(self):
        claim = Claim.create(self.inventory, "Focus investment on retention.", ContentOrigin.AGY_SYNTHESIS)
        self.assertEqual(claim.origin, ContentOrigin.AGY_SYNTHESIS)

    def test_agy_synthesis_with_support_remains_synthesis(self):
        claim = Claim.create(self.inventory, "Retention is the priority.", ContentOrigin.AGY_SYNTHESIS, [self.binding])
        self.assertEqual(claim.origin, ContentOrigin.AGY_SYNTHESIS)

    def test_multiple_evidence_refs_are_preserved_deterministically(self):
        second = self.inventory.add_unit("src_pdf", "page", {"kind": "page", "start": 4, "end": 4}, "MEDIUM")
        binding2 = binding_from_unit(self.inventory, second["unit_id"])
        a = Claim.create(self.inventory, "Combined result", ContentOrigin.SOURCE_GROUNDED, [binding2, self.binding])
        b = Claim.create(self.inventory, "Combined result", ContentOrigin.SOURCE_GROUNDED, [self.binding, binding2])
        self.assertEqual(a, b)
        self.assertEqual(len(a.evidence), 2)

    def test_phase15_5_grounding_reused_without_live_ocr(self):
        page = GroundingPage(
            "src_pdf", self.digest, self.unit["locator"], "recognized", "TEXT", {"kind": "pdf_page", "page": 2}
        )
        binding = binding_from_grounding_page(self.inventory, page)
        self.assertEqual(binding.unit_id, self.unit["unit_id"])

    def test_no_fabricated_binding_for_unregistered_translated_page(self):
        page = GroundingPage(
            "src_pdf", self.digest, {"kind": "page", "start": 9, "end": 9}, "recognized", "TEXT",
            {"kind": "pdf_page", "page": 9},
        )
        self.error(ERROR_EVIDENCE_REFERENCE_INVALID, lambda: binding_from_grounding_page(self.inventory, page))

    def test_atomic_failure_does_not_mutate_inventory_or_inputs(self):
        before = json.dumps(self.inventory.data, ensure_ascii=False, sort_keys=True)
        bindings = [self.binding, EvidenceBinding("src_pdf", self.digest, "su:src_pdf:000000000000", self.unit["locator"])]
        self.error(ERROR_EVIDENCE_REFERENCE_INVALID, lambda: Claim.create(
            self.inventory, "Atomic", ContentOrigin.SOURCE_GROUNDED, bindings
        ))
        self.assertEqual(json.dumps(self.inventory.data, ensure_ascii=False, sort_keys=True), before)
        self.assertEqual(len(bindings), 2)

    def test_deterministic_equivalence(self):
        first = Claim.create(self.inventory, "Same", ContentOrigin.SOURCE_GROUNDED, [self.binding])
        second = Claim.create(self.inventory, "Same", ContentOrigin.SOURCE_GROUNDED, [self.binding])
        self.assertEqual(first.to_json(), second.to_json())
        self.assertEqual(first.claim_id, second.claim_id)

    def test_no_path_timestamp_or_random_leakage(self):
        claim = Claim.create(self.inventory, "Stable", ContentOrigin.SOURCE_GROUNDED, [self.binding])
        serialized = claim.to_json()
        self.assertNotIn(self.temp.name, serialized)
        self.assertNotIn("/Users/", serialized)
        self.assertNotIn("created_at", serialized)
        self.assertRegex(claim.claim_id, r"^pc:[0-9a-f]{16}$")


if __name__ == "__main__":
    unittest.main()
