#!/usr/bin/env python3
"""Integrated deterministic Phase 16 qualification using project-owned fixtures."""

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

from PIL import Image  # noqa: E402
from pptx import Presentation  # noqa: E402

from assemble_ppt import create_presentation  # noqa: E402
from helpers.fake_ocr_provider import FakeOCRProvider  # noqa: E402
from helpers.synthetic_pdf import build_text_pdf  # noqa: E402
from image_ocr import ImagePreparationProvenance, ImageSourceIdentity, StandaloneImageOCRResult  # noqa: E402
from ocr_grounding import translate_mixed_pdf, translate_pdf_ocr_page, translate_standalone_image  # noqa: E402
from ocr_providers import OCRRequest  # noqa: E402
from pdf_ocr import PDFPageIdentity, PDFSourceIdentity, MixedPDFExecutionResult, OCRPageExecution, TextPageExecution  # noqa: E402
from phase16_claims import Claim, ContentOrigin, binding_from_grounding_page, binding_from_unit  # noqa: E402
from phase16_editorial import EditorialSession, EditorialSlide, PresentationMode, SlideRole  # noqa: E402
from phase16_outline import GroundedOutlinePlan, GroundedOutlineSlide, GroundedOutlineWorkflow  # noqa: E402
from phase16_slide_evidence import MaterialClaim, SlideEvidencePlan  # noqa: E402
from phase16_traceability import FinalSlideRecord, FinalTraceabilityError, build_traceability_report, dependency_impact, notes_map  # noqa: E402
from presentation_workflow import PresentationApprovalWorkflow, READY_FOR_FULL_GENERATION  # noqa: E402
from project_state import ProjectState  # noqa: E402
from source_grounding import SourceInventory  # noqa: E402
from source_ingestion import ingest_source, phase12_locator  # noqa: E402


class Provenance:
    def __init__(self, label="fixture-raster"):
        self.label = label

    def to_dict(self):
        return {"kind": self.label}


class Phase16IntegratedE2E(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def register_page(self, inv, page, source_type="pdf", label="Fixture source"):
        if page.source_id not in inv.source_ids():
            inv.add_source(page.source_id, source_type, label=label, source_digest=page.source_digest)
        unit = inv.add_unit(page.source_id, "page", dict(page.locator), "HIGH")
        return binding_from_grounding_page(inv, page), unit

    def final_record(self, inv, text, binding, slide_id="slide_01", origin=ContentOrigin.SOURCE_GROUNDED):
        claim = Claim.create(inv, text, origin, [binding] if binding else ())
        plan = SlideEvidencePlan.create(slide_id, [MaterialClaim(claim)])
        return claim, FinalSlideRecord(plan, text, "Explain the core point naturally.")

    def test_a_searchable_pdf_to_final_pptx_notes_and_original_page(self):
        pdf = self.root / "searchable.pdf"
        pdf.write_bytes(build_text_pdf(["Revenue grew in 2025"]))
        extracted = ingest_source(pdf, "src_searchable")
        inv = SourceInventory.initialize(self.root, "scenario-a")
        inv.add_source(extracted.source_id, "pdf", label="Searchable report", source_digest=extracted.source_digest)
        block = extracted.blocks[0]
        unit = inv.add_unit(extracted.source_id, block.block_type, phase12_locator(block), "HIGH")
        binding = binding_from_unit(inv, unit["unit_id"])
        claim, record = self.final_record(inv, "Revenue grew 18% in 2025", binding)

        outline = GroundedOutlinePlan.create([GroundedOutlineSlide.create(1, "Growth was evidence-led", "Explain", [claim])])
        approval = GroundedOutlineWorkflow(PresentationApprovalWorkflow(ProjectState.initialize(self.root, "approval")))
        approval.submit(outline)
        approval.approve()
        approval.workflow.submit_style({"direction": "executive editorial"})
        approval.workflow.approve_style()
        approval.workflow.generate_sample(lambda _slide: "sample.png")
        approval.workflow.approve_sample()
        self.assertEqual(approval.workflow.status, READY_FOR_FULL_GENERATION)

        edited = EditorialSession(PresentationMode.EXECUTIVE, (
            EditorialSlide("slide_01", record.rendered_text, ("Evidence-led growth",), record.speaker_notes, SlideRole.DATA, evidence_plan=record.plan),
        )).repair_once()
        self.assertIs(edited.slides[0].evidence_plan, record.plan)
        report = build_traceability_report(inv, [record])
        report.require_complete()

        image = self.root / "slide_01.png"
        Image.new("RGB", (1600, 900), "white").save(image)
        output = self.root / "scenario-a.pptx"
        self.assertTrue(create_presentation([str(image)], str(output), speaker_notes=notes_map([record], inv)))
        notes = Presentation(output).slides[0].notes_slide.notes_text_frame.text
        self.assertIn("Searchable report — page 1", notes)

    def test_b_ocr_pdf_reuses_deterministic_translation(self):
        raw = b"%PDF OCR fixture"
        source = PDFSourceIdentity("src_ocr_pdf", hashlib.sha256(raw).hexdigest())
        page_id = PDFPageIdentity(2, 2)
        evidence = FakeOCRProvider(text="OCR metric 18%").recognize(OCRRequest(b"raster", source.source_id, source.source_digest, page_id.to_dict()))
        page = translate_pdf_ocr_page(source, page_id, evidence, Provenance())
        inv = SourceInventory.initialize(self.root, "scenario-b")
        binding, _ = self.register_page(inv, page, label="Scanned report")
        _, record = self.final_record(inv, "OCR metric 18%", binding)
        build_traceability_report(inv, [record]).require_complete()

    def test_c_image_ocr_preserves_original_identity(self):
        raw = b"original-image-fixture"
        source = ImageSourceIdentity.from_bytes("src_image", raw)
        evidence = FakeOCRProvider(text="Image metric 12%").recognize(OCRRequest(b"prepared", source.source_id, source.source_digest, {"kind": "image", "ordinal": 1}))
        preparation = ImagePreparationProvenance(
            "Pillow", "10.0", "PNG", 4, 3, "RGBA", 1, False, False,
            "composite_on_white", "rgba_to_rgb", "PNG", "RGB", 4, 3,
            hashlib.sha256(b"prepared").hexdigest(),
        )
        page = translate_standalone_image(StandaloneImageOCRResult(source, preparation, evidence), raw)
        inv = SourceInventory.initialize(self.root, "scenario-c")
        inv.add_source(page.source_id, "image", label="Source image", source_digest=page.source_digest)
        unit = inv.add_unit(page.source_id, "image", dict(page.locator), "HIGH")
        binding = binding_from_unit(inv, unit["unit_id"])
        self.assertEqual(binding.source_digest, hashlib.sha256(raw).hexdigest())
        self.assertNotEqual(binding.source_digest, preparation.prepared_image_digest)

    def test_d_mixed_pdf_preserves_order_and_routing(self):
        raw = b"%PDF mixed fixture"
        source = PDFSourceIdentity("src_mixed", hashlib.sha256(raw).hexdigest())
        one, two = PDFPageIdentity(1, 2), PDFPageIdentity(2, 2)
        evidence = FakeOCRProvider(text="OCR page two").recognize(OCRRequest(b"raster", source.source_id, source.source_digest, two.to_dict()))
        mixed = MixedPDFExecutionResult(source, (TextPageExecution(source, one, "Text page one"), OCRPageExecution(source, two, evidence, Provenance())))
        translated = translate_mixed_pdf(mixed, raw)
        self.assertEqual([page.route for page in translated.pages], ["TEXT", "OCR"])
        self.assertEqual([page.locator["start"] for page in translated.pages], [1, 2])

    def test_e_multiple_sources_preserve_separate_support(self):
        inv = SourceInventory.initialize(self.root, "scenario-e")
        bindings = []
        for index in (1, 2):
            raw = f"source-{index}".encode()
            digest = hashlib.sha256(raw).hexdigest()
            source_id = f"src_{index}"
            inv.add_source(source_id, "pdf", source_digest=digest)
            unit = inv.add_unit(source_id, "page", {"kind": "page", "start": 1, "end": 1}, "HIGH")
            bindings.append(binding_from_unit(inv, unit["unit_id"]))
        claim = Claim.create(inv, "Combined result 18%", ContentOrigin.SOURCE_GROUNDED, bindings)
        record = FinalSlideRecord(SlideEvidencePlan.create("slide_01", [MaterialClaim(claim)]), claim.text)
        self.assertEqual(build_traceability_report(inv, [record]).evidence_bindings, 2)

    def test_f_user_content_stays_user_provided(self):
        inv = SourceInventory.initialize(self.root, "scenario-f")
        claim, record = self.final_record(inv, "Our target is 20%", None, origin=ContentOrigin.USER_PROVIDED)
        report = build_traceability_report(inv, [record])
        self.assertEqual(claim.origin, ContentOrigin.USER_PROVIDED)
        self.assertEqual(report.user_provided_claims, 1)

    def test_g_agy_synthesis_stays_synthesis(self):
        inv = SourceInventory.initialize(self.root, "scenario-g")
        claim, record = self.final_record(inv, "Retention should lead", None, origin=ContentOrigin.AGY_SYNTHESIS)
        self.assertEqual(claim.origin, ContentOrigin.AGY_SYNTHESIS)
        self.assertEqual(build_traceability_report(inv, [record]).agy_synthesis_claims, 1)

    def test_h_unsupported_source_fact_cannot_silently_pass(self):
        inv = SourceInventory.initialize(self.root, "scenario-h")
        claim = Claim.create(inv, "Transition", ContentOrigin.AGY_SYNTHESIS)
        plan = SlideEvidencePlan.create("slide_01", [MaterialClaim(claim, material=False)])
        report = build_traceability_report(inv, [FinalSlideRecord(plan, "Transition", unsupported_source_claims=("Revenue rose 99%",))])
        with self.assertRaises(FinalTraceabilityError):
            report.require_complete()

    def approved_record(self, project, through_sample=False):
        inv = SourceInventory.initialize(self.root, project)
        digest = hashlib.sha256(b"source").hexdigest()
        inv.add_source("src_change", "pdf", source_digest=digest)
        unit = inv.add_unit("src_change", "page", {"kind": "page", "start": 1, "end": 1}, "HIGH")
        binding = binding_from_unit(inv, unit["unit_id"])
        claim, record = self.final_record(inv, "Metric 18%", binding)
        outline = GroundedOutlinePlan.create([GroundedOutlineSlide.create(1, "Metric 18%", "Explain", [claim])])
        workflow = GroundedOutlineWorkflow(PresentationApprovalWorkflow(ProjectState.initialize(self.root, project + "-state")))
        workflow.submit(outline)
        workflow.approve()
        if through_sample:
            workflow.workflow.submit_style({"direction": "technical"})
            workflow.workflow.approve_style()
            workflow.workflow.generate_sample(lambda _slide: "sample.png")
            workflow.workflow.approve_sample()
        return inv, record

    def test_i_source_change_after_outline_approval_marks_dependency_stale(self):
        inv, record = self.approved_record("scenario-i")
        impact = dependency_impact([record], {"src_change": "0" * 64})
        self.assertEqual(impact.slide_ids, ("slide_01",))

    def test_j_source_change_after_sample_approval_blocks_final(self):
        inv, record = self.approved_record("scenario-j", through_sample=True)
        report = build_traceability_report(inv, [record], current_source_digests={"src_change": "0" * 64})
        with self.assertRaises(FinalTraceabilityError):
            report.require_complete()

    def test_k_mechanical_deck_warns_repairs_once_and_preserves_evidence(self):
        inv = SourceInventory.initialize(self.root, "scenario-k")
        digest = hashlib.sha256(b"editorial-source").hexdigest()
        inv.add_source("src_editorial", "pdf", source_digest=digest)
        unit = inv.add_unit("src_editorial", "page", {"kind": "page", "start": 1, "end": 1}, "HIGH")
        claim = Claim.create(
            inv, "成長 18%", ContentOrigin.SOURCE_GROUNDED,
            [binding_from_unit(inv, unit["unit_id"])],
        )
        slides = tuple(
            EditorialSlide(
                f"slide_{i:02d}", "成長 18%｜" + "打造賦能共贏" * 8,
                ("我們將打造價值",) * 3, "接下來我們來看，固定轉場",
                SlideRole.DATA, "cards-3", "right", "DENSE",
                SlideEvidencePlan.create(f"slide_{i:02d}", [MaterialClaim(claim)]),
            )
            for i in range(1, 6)
        )
        session = EditorialSession(PresentationMode.SALES, slides)
        before = session.lint().count()
        repaired = session.repair_once()
        self.assertLess(repaired.lint().count(), before)
        self.assertEqual(repaired.repair_count, 1)
        self.assertTrue(all(after.evidence_plan is before.evidence_plan for before, after in zip(slides, repaired.slides)))
        self.assertNotIn("AI_DETECTED", str(repaired.lint()))

    def test_l_modes_change_editorial_behavior_not_facts(self):
        facts = "Revenue rose 18% in 2025"
        outputs = {}
        for mode in (PresentationMode.EXECUTIVE, PresentationMode.SALES, PresentationMode.TECHNICAL):
            slide = EditorialSlide("slide_01", facts, ("Explain context",), "Natural notes", SlideRole.DATA)
            session = EditorialSession(mode, (slide,))
            outputs[mode] = (session.mode, session.slides[0].copy)
        self.assertEqual({copy for _, copy in outputs.values()}, {facts + "\nExplain context"})
        self.assertEqual(len({mode for mode, _ in outputs.values()}), 3)


if __name__ == "__main__":
    unittest.main()
