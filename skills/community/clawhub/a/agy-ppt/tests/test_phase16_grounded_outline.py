#!/usr/bin/env python3
"""Phase 16.2 deterministic grounded-outline tests."""

from __future__ import annotations

import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
TESTS = Path(__file__).resolve().parent
for path in (SCRIPTS, TESTS):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from helpers.fake_ocr_provider import FakeOCRProvider  # noqa: E402
from ocr_grounding import translate_pdf_ocr_page, translate_pdf_text_page  # noqa: E402
from ocr_providers import OCRRequest  # noqa: E402
from pdf_ocr import PDFPageIdentity, PDFSourceIdentity  # noqa: E402
from phase16_claims import Claim, ClaimContractError, ContentOrigin, binding_from_grounding_page, binding_from_unit  # noqa: E402
from phase16_outline import GroundedOutlinePlan, GroundedOutlineSlide, GroundedOutlineWorkflow  # noqa: E402
from presentation_workflow import OUTLINE_PENDING_APPROVAL, STYLE_PENDING_APPROVAL, PresentationApprovalWorkflow  # noqa: E402
from project_state import ProjectState  # noqa: E402
from source_grounding import SourceInventory  # noqa: E402


class Provenance:
    def to_dict(self):
        return {"kind": "deterministic-test-raster"}


class GroundedOutlineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.inventory = SourceInventory.initialize(self.temp.name, "outline")
        self.raw = b"%PDF deterministic phase16.2"
        self.digest = hashlib.sha256(self.raw).hexdigest()
        self.source = PDFSourceIdentity("src_report", self.digest)
        self.inventory.add_source("src_report", "pdf", source_digest=self.digest)
        self.units = [
            self.inventory.add_unit("src_report", "page", {"kind": "page", "start": page, "end": page}, "HIGH")
            for page in (1, 2)
        ]
        state = ProjectState.initialize(self.temp.name, "outline-workflow")
        self.workflow = GroundedOutlineWorkflow(PresentationApprovalWorkflow(state))

    def tearDown(self) -> None:
        self.temp.cleanup()

    def claim(self, text="Revenue increased 18%", origin=ContentOrigin.SOURCE_GROUNDED, evidence=True):
        refs = [binding_from_unit(self.inventory, self.units[0]["unit_id"])] if evidence else []
        return Claim.create(self.inventory, text, origin, refs)

    def plan(self, claims=None, title="Evidence-led growth"):
        return GroundedOutlinePlan.create([
            GroundedOutlineSlide.create(1, "Cover", "Open", (), "cover"),
            GroundedOutlineSlide.create(2, title, "Explain", claims if claims is not None else [self.claim()]),
        ])

    def test_searchable_pdf_grounded_outline(self):
        page = translate_pdf_text_page(self.source, PDFPageIdentity(1, 2), "Revenue increased 18%")
        binding = binding_from_grounding_page(self.inventory, page)
        plan = self.plan([Claim.create(self.inventory, page.text, ContentOrigin.SOURCE_GROUNDED, [binding])])
        self.assertEqual(self.workflow.submit(plan), OUTLINE_PENDING_APPROVAL)

    def test_ocr_grounded_outline_uses_deterministic_fixture(self):
        page_id = PDFPageIdentity(2, 2)
        provider = FakeOCRProvider(text="OCR says 2025")
        evidence = provider.recognize(OCRRequest(b"raster", "src_report", self.digest, page_id.to_dict()))
        page = translate_pdf_ocr_page(self.source, page_id, evidence, Provenance())
        binding = binding_from_grounding_page(self.inventory, page)
        claim = Claim.create(self.inventory, page.text, ContentOrigin.SOURCE_GROUNDED, [binding])
        self.assertEqual(claim.evidence[0].source_digest, self.digest)

    def test_multi_source_outline(self):
        digest2 = hashlib.sha256(b"second").hexdigest()
        self.inventory.add_source("src_second", "pdf", source_digest=digest2)
        unit2 = self.inventory.add_unit("src_second", "page", {"kind": "page", "start": 1, "end": 1}, "HIGH")
        claims = [self.claim(), Claim.create(self.inventory, "Second source", ContentOrigin.SOURCE_GROUNDED, [binding_from_unit(self.inventory, unit2["unit_id"])])]
        self.assertEqual(len(self.plan(claims).claims), 2)

    def test_user_provided_fact(self):
        claim = Claim.create(self.inventory, "Our goal is 20%", ContentOrigin.USER_PROVIDED)
        self.assertIn(ContentOrigin.USER_PROVIDED, self.plan([claim]).origins)

    def test_agy_synthesis(self):
        claim = Claim.create(self.inventory, "Retention should lead", ContentOrigin.AGY_SYNTHESIS)
        self.assertEqual(self.plan([claim]).claims[0].origin, ContentOrigin.AGY_SYNTHESIS)

    def test_mixed_origins_on_one_slide_are_not_flattened(self):
        claims = [
            self.claim(),
            Claim.create(self.inventory, "User target", ContentOrigin.USER_PROVIDED),
            Claim.create(self.inventory, "AGY recommendation", ContentOrigin.AGY_SYNTHESIS),
        ]
        self.assertEqual(len(self.plan(claims).origins), 3)

    def test_unsupported_grounded_fact_cannot_enter_plan(self):
        with self.assertRaises(ClaimContractError):
            self.claim(evidence=False)

    def test_content_revision_recalculates_plan_and_requires_reapproval(self):
        first = self.plan()
        self.workflow.submit(first)
        self.workflow.approve()
        revised = self.plan([self.claim("Revenue increased 19%")], "Revised content")
        self.assertEqual(self.workflow.revise_content(revised), OUTLINE_PENDING_APPROVAL)
        self.assertNotEqual(first.plan_id, revised.plan_id)

    def test_style_revision_preserves_outline_and_evidence_identity(self):
        plan = self.plan()
        self.workflow.submit(plan)
        self.workflow.approve()
        claim_ids = tuple(claim.claim_id for claim in plan.claims)
        self.assertEqual(self.workflow.revise_style({"direction": "editorial"}), STYLE_PENDING_APPROVAL)
        self.assertEqual(self.workflow.plan.plan_id, plan.plan_id)
        self.assertEqual(tuple(claim.claim_id for claim in self.workflow.plan.claims), claim_ids)

    def test_deterministic_planning(self):
        claim = self.claim()
        self.assertEqual(self.plan([claim]).plan_id, self.plan([claim]).plan_id)

    def test_normal_user_prompt_remains_clean(self):
        self.workflow.submit(self.plan())
        text = self.workflow.user_prompt().text
        self.assertIn("2 頁大綱", text)
        for token in ("source_id", "unit_id", "locator", "SOURCE_GROUNDED", "pc:", "su:"):
            self.assertNotIn(token, text)


if __name__ == "__main__":
    unittest.main()
