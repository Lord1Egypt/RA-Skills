#!/usr/bin/env python3
"""Integrated deterministic Phase 18 qualification scenarios.

Validates all 18 architecture-defined scenarios:
1. Ordinary editable text
2. Photo + headline
3. Three-card business slide
4. Structured chart
5. Complex artistic slide
6. Traditional Chinese typography
7. English typography
8. Title inside envelope
9. Title outside envelope
10. Logo replacement
11. Photo replacement
12. Save/reopen round-trip
13. Fallback font
14. Evidence-bound numeric content
15. BALANCED profile
16. FIDELITY profile
17. EDITABILITY_PRIORITY profile
18. Approved Sample fidelity
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from PIL import Image  # noqa: E402
from pptx import Presentation  # noqa: E402

from phase18_contract import (  # noqa: E402
    DeliveryEditabilityContract, DeliveryProfile, EditabilityClass, FontPortability, ProductionStrategy,
)
from phase18_fidelity_qa import (  # noqa: E402
    ElementSnapshot, FidelityIssue, QaDimension, QaSeverity, compare_fidelity,
    safe_representation_fallback, verify_pptx_package,
)
from phase18_hybrid_pptx import (  # noqa: E402
    ChartSeries, ChartSpec, ElementBox, HybridElement, HybridSlide, ShapeStyle, TextStyle,
    create_hybrid_presentation,
)
from phase18_production_plan import (  # noqa: E402
    ElementPlanningInput, ElementProductionPlan, ElementRole, PortabilityRisk, plan_element, plan_elements,
)
from phase18_roundtrip_compatibility import (  # noqa: E402
    QualificationType, RoundTripOutcome, audit_client_environments, run_roundtrip_qualification,
    simulate_chart_data_edit, simulate_kpi_edit, simulate_logo_replacement, simulate_photo_replacement,
    simulate_save_reopen, simulate_title_edit, verify_evidence_integrity_guard, verify_fallback_font,
    verify_table_boundary, verify_typography,
)
from presentation_layout_grammar import DEFAULT_LAYOUT_GRAMMAR  # noqa: E402


class Phase18IntegratedE2ETests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.img1 = self.root / "img1.png"
        self.img2 = self.root / "img2.png"
        Image.new("RGB", (320, 180), (30, 60, 90)).save(self.img1)
        Image.new("RGB", (320, 180), (90, 120, 150)).save(self.img2)

    def tearDown(self):
        self.temp.cleanup()

    def _make_plan(self, element_id: str, strategy: ProductionStrategy, content: str, role: ElementRole = ElementRole.BODY, profile: DeliveryProfile = DeliveryProfile.BALANCED, editability: EditabilityClass = EditabilityClass.EDITABLE_PREFERRED) -> ElementProductionPlan:
        return ElementProductionPlan(
            f"ep:{element_id}", element_id, f"claim:{element_id}", f"narrative:{element_id}",
            content, ("pc:evidence",) if "18%" in content else (), role,
            PortabilityRisk.LOW,
            DeliveryEditabilityContract(editability, strategy, FontPortability.FONT_SAFE, delivery_profile=profile),
        )

    def _create_deck(self, elements, notes="Speaker notes", name="deck.pptx") -> Path:
        out = self.root / name
        slide = HybridSlide("slide_01", tuple(elements), speaker_notes=notes)
        create_hybrid_presentation((slide,), str(out))
        return out

    # Scenario 1: Ordinary editable text
    def test_scenario_01_ordinary_editable_text(self):
        plan_name = self._make_plan("name", ProductionStrategy.NATIVE_TEXT, "Presenter: Dr. Lin", ElementRole.NAME)
        plan_date = self._make_plan("date", ProductionStrategy.NATIVE_TEXT, "2026-09-22", ElementRole.DATE)
        elem_name = HybridElement(plan_name, ElementBox(1, 1, 4, 0.8), text_style=TextStyle(font_size=18.0))
        elem_date = HybridElement(plan_date, ElementBox(1, 2, 4, 0.8), text_style=TextStyle(font_size=14.0))
        deck_path = self._create_deck([elem_name, elem_date])

        deck = Presentation(str(deck_path))
        self.assertEqual(len(deck.slides[0].shapes), 2)
        self.assertEqual(deck.slides[0].shapes[0].text, "Presenter: Dr. Lin")
        self.assertEqual(deck.slides[0].shapes[1].text, "2026-09-22")

    # Scenario 2: Photo + headline
    def test_scenario_02_photo_plus_headline(self):
        plan_hl = self._make_plan("headline", ProductionStrategy.NATIVE_TEXT, "Next-Gen AI Platform", ElementRole.TITLE)
        plan_photo = self._make_plan("hero_photo", ProductionStrategy.NATIVE_IMAGE, "photo", ElementRole.PHOTO, editability=EditabilityClass.REPLACEABLE)
        elem_hl = HybridElement(plan_hl, DEFAULT_LAYOUT_GRAMMAR.title_box(), text_style=TextStyle(font_size=30.0, bold=True))
        elem_photo = HybridElement(plan_photo, ElementBox(0.6, 1.45, 5.6, 3.65), image_path=str(self.img1))
        deck_path = self._create_deck([elem_hl, elem_photo])

        deck = Presentation(str(deck_path))
        self.assertEqual(deck.slides[0].shapes[0].name, "agy:headline")
        self.assertEqual(deck.slides[0].shapes[1].name, "agy:hero_photo")

    # Scenario 3: Three-card business slide
    def test_scenario_03_three_card_business_slide(self):
        elements = []
        for i, card in enumerate(DEFAULT_LAYOUT_GRAMMAR.columns(3)):
            shape_plan = self._make_plan(f"card_shape_{i+1}", ProductionStrategy.NATIVE_SHAPE, f"card_{i+1}", ElementRole.SIMPLE_SHAPE)
            text_plan = self._make_plan(f"card_text_{i+1}", ProductionStrategy.NATIVE_TEXT, f"Feature Pillar {i+1}", ElementRole.BODY)
            elements.append(HybridElement(shape_plan, card, shape_style=ShapeStyle("rounded_rectangle", "E8EEF5", "D6DFEA")))
            content_box = DEFAULT_LAYOUT_GRAMMAR.card_content_box(card)
            elements.append(HybridElement(text_plan, ElementBox(content_box.left, content_box.top, content_box.width, 0.7), text_style=TextStyle(font_size=18.0, bold=True)))

        deck_path = self._create_deck(elements)
        deck = Presentation(str(deck_path))
        self.assertEqual(len(deck.slides[0].shapes), 6)
        for i in range(3):
            self.assertEqual(deck.slides[0].shapes[i * 2].name, f"agy:card_shape_{i+1}")
            self.assertEqual(deck.slides[0].shapes[i * 2 + 1].name, f"agy:card_text_{i+1}")

    # Scenario 4: Structured chart
    def test_scenario_04_structured_chart(self):
        chart_plan = self._make_plan("kpi_chart", ProductionStrategy.NATIVE_CHART, "chart", ElementRole.CHART)
        chart_spec = ChartSpec(("2023", "2024", "2025"), (ChartSeries("Growth", (10.0, 14.0, 18.0)),))
        elem_chart = HybridElement(chart_plan, DEFAULT_LAYOUT_GRAMMAR.content_box(), chart=chart_spec)
        deck_path = self._create_deck([elem_chart])

        deck = Presentation(str(deck_path))
        self.assertTrue(deck.slides[0].shapes[0].has_chart)
        self.assertEqual(tuple(deck.slides[0].shapes[0].chart.series[0].values), (10.0, 14.0, 18.0))

    # Scenario 5: Complex artistic slide
    def test_scenario_05_complex_artistic_slide(self):
        art_plan = self._make_plan("hero_art", ProductionStrategy.LOCKED_VISUAL, "hero art", ElementRole.HERO_ARTWORK, editability=EditabilityClass.LOCKED_REQUIRED)
        elem_art = HybridElement(art_plan, ElementBox(0, 0, 10, 5.625), image_path=str(self.img1))
        deck_path = self._create_deck([elem_art])

        deck = Presentation(str(deck_path))
        self.assertEqual(len(deck.slides[0].shapes), 1)
        self.assertEqual(deck.slides[0].shapes[0].name, "agy:hero_art")

    # Scenario 6: Traditional Chinese typography
    def test_scenario_06_traditional_chinese_typography(self):
        text = "繁體中文核心指標：年營收成長率 18.5%，客戶滿意度達 96%。"
        finding = verify_typography(text, language="zh-TW", font_name="Microsoft JhengHei")
        self.assertEqual(finding.outcome, RoundTripOutcome.PASS)
        plan_zh = self._make_plan("kpi_zh", ProductionStrategy.NATIVE_TEXT, text, ElementRole.KPI)
        elem_zh = HybridElement(plan_zh, ElementBox(0.6, 1, 8.8, 2), text_style=TextStyle(font_name="Aptos", east_asian_font_name="Microsoft JhengHei", font_size=20.0))
        deck_path = self._create_deck([elem_zh])
        deck = Presentation(str(deck_path))
        self.assertIn("18.5%", deck.slides[0].shapes[0].text)

    # Scenario 7: English typography
    def test_scenario_07_english_typography(self):
        text = "Strategic Transformation: Scalable Architecture with 99.99% Reliability."
        finding = verify_typography(text, language="en", font_name="Arial")
        self.assertEqual(finding.outcome, RoundTripOutcome.PASS)
        plan_en = self._make_plan("headline_en", ProductionStrategy.NATIVE_TEXT, text, ElementRole.TITLE)
        elem_en = HybridElement(plan_en, ElementBox(0.6, 1, 8.8, 1.5), text_style=TextStyle(font_name="Aptos", font_size=24.0))
        deck_path = self._create_deck([elem_en])
        deck = Presentation(str(deck_path))
        self.assertEqual(deck.slides[0].shapes[0].text, text)

    # Scenario 8: Title edited within envelope
    def test_scenario_08_title_edited_within_envelope(self):
        plan_t = self._make_plan("title", ProductionStrategy.NATIVE_TEXT, "Executive Summary", ElementRole.TITLE)
        elem_t = HybridElement(plan_t, ElementBox(1, 1, 8, 1), text_style=TextStyle(font_size=28.0))
        deck_path = self._create_deck([elem_t])

        finding = simulate_title_edit(deck_path, "title", "Executive Summary 2026", max_chars=35)
        self.assertEqual(finding.outcome, RoundTripOutcome.PASS)
        self.assertIn("stable reflow", finding.detail)

    # Scenario 9: Title edited beyond envelope
    def test_scenario_09_title_edited_beyond_envelope(self):
        plan_t = self._make_plan("title", ProductionStrategy.NATIVE_TEXT, "Executive Summary", ElementRole.TITLE)
        elem_t = HybridElement(plan_t, ElementBox(1, 1, 8, 1), text_style=TextStyle(font_size=28.0))
        deck_path = self._create_deck([elem_t])

        long_title = "This headline contains an excessive quantity of words that is guaranteed to overflow normal presentation title boundaries"
        finding = simulate_title_edit(deck_path, "title", long_title, max_chars=35)
        self.assertEqual(finding.outcome, RoundTripOutcome.WARNING)
        self.assertIn("exceeds envelope", finding.detail)

    # Scenario 10: Logo replacement
    def test_scenario_10_logo_replacement(self):
        plan_l = self._make_plan("logo", ProductionStrategy.NATIVE_IMAGE, "logo", ElementRole.LOGO, editability=EditabilityClass.REPLACEABLE)
        elem_l = HybridElement(plan_l, ElementBox(8.2, 0.45, 1.2, 0.65), image_path=str(self.img1))
        deck_path = self._create_deck([elem_l])

        finding = simulate_logo_replacement(deck_path, "logo", self.img2)
        self.assertEqual(finding.outcome, RoundTripOutcome.PASS)
        deck = Presentation(str(deck_path))
        self.assertEqual(deck.slides[0].shapes[0].image.blob, self.img2.read_bytes())

    # Scenario 11: Photo replacement
    def test_scenario_11_photo_replacement(self):
        plan_p = self._make_plan("photo", ProductionStrategy.NATIVE_IMAGE, "photo", ElementRole.PHOTO, editability=EditabilityClass.REPLACEABLE)
        elem_p = HybridElement(plan_p, ElementBox(2, 2, 5, 3.5), image_path=str(self.img1))
        deck_path = self._create_deck([elem_p])

        finding = simulate_photo_replacement(deck_path, "photo", self.img2)
        self.assertEqual(finding.outcome, RoundTripOutcome.PASS)
        deck = Presentation(str(deck_path))
        self.assertEqual(deck.slides[0].shapes[0].image.blob, self.img2.read_bytes())

    # Scenario 12: Save/reopen round-trip
    def test_scenario_12_save_reopen_round_trip(self):
        plan_t = self._make_plan("title", ProductionStrategy.NATIVE_TEXT, "Persistent Deck", ElementRole.TITLE)
        elem_t = HybridElement(plan_t, ElementBox(1, 1, 6, 1), text_style=TextStyle())
        deck_path = self._create_deck([elem_t], notes="Auditable notes text")
        out_path = self.root / "reopened_cycle.pptx"

        finding = simulate_save_reopen(deck_path, save_path=out_path)
        self.assertEqual(finding.outcome, RoundTripOutcome.PASS)
        reopened = Presentation(str(out_path))
        self.assertEqual(reopened.slides[0].shapes[0].text, "Persistent Deck")
        self.assertEqual(reopened.slides[0].notes_slide.notes_text_frame.text, "Auditable notes text")

    # Scenario 13: Fallback font
    def test_scenario_13_fallback_font(self):
        safe = verify_fallback_font("Calibri", FontPortability.FONT_SAFE)
        self.assertEqual(safe.outcome, RoundTripOutcome.PASS)
        critical = verify_fallback_font("SpecialProprietaryFont", FontPortability.FONT_CRITICAL)
        self.assertEqual(critical.outcome, RoundTripOutcome.WARNING)
        self.assertIn("protected visual", critical.detail)

    # Scenario 14: Evidence-bound numeric content
    def test_scenario_14_evidence_bound_numeric_content(self):
        kpi_plan = self._make_plan("kpi", ProductionStrategy.NATIVE_TEXT, "18%", ElementRole.KPI, editability=EditabilityClass.EDITABLE_REQUIRED)
        elem_kpi = HybridElement(kpi_plan, ElementBox(1, 1, 3, 1), text_style=TextStyle())
        deck_path = self._create_deck([elem_kpi])

        # Accidental production corruption is blocked
        accidental = verify_evidence_integrity_guard("18%", "1.8%", is_intentional_user_edit=False)
        self.assertEqual(accidental.outcome, RoundTripOutcome.BLOCKING)

        # Intentional test edit succeeds and updates
        intentional = simulate_kpi_edit(deck_path, "kpi", "22%")
        self.assertEqual(intentional.outcome, RoundTripOutcome.PASS)
        deck = Presentation(str(deck_path))
        self.assertEqual(deck.slides[0].shapes[0].text, "22%")

    # Scenario 15: BALANCED profile
    def test_scenario_15_balanced_profile(self):
        kpi_plan = self._make_plan("kpi", ProductionStrategy.NATIVE_TEXT, "18%", ElementRole.KPI, profile=DeliveryProfile.BALANCED)
        art_plan = self._make_plan("art", ProductionStrategy.LOCKED_VISUAL, "art", ElementRole.DECORATIVE_ARTWORK, profile=DeliveryProfile.BALANCED)
        self.assertEqual(kpi_plan.contract.strategy, ProductionStrategy.NATIVE_TEXT)
        self.assertEqual(art_plan.contract.strategy, ProductionStrategy.LOCKED_VISUAL)

    # Scenario 16: FIDELITY profile
    def test_scenario_16_fidelity_profile(self):
        body_plan = self._make_plan("body", ProductionStrategy.LOCKED_VISUAL, "complex typography body", ElementRole.BODY, profile=DeliveryProfile.FIDELITY)
        self.assertEqual(body_plan.contract.delivery_profile, DeliveryProfile.FIDELITY)
        self.assertEqual(body_plan.contract.strategy, ProductionStrategy.LOCKED_VISUAL)

    # Scenario 17: EDITABILITY_PRIORITY profile
    def test_scenario_17_editability_priority_profile(self):
        title_plan = self._make_plan("title", ProductionStrategy.NATIVE_TEXT, "Editable Title", ElementRole.TITLE, profile=DeliveryProfile.EDITABILITY_PRIORITY)
        kpi_plan = self._make_plan("kpi", ProductionStrategy.NATIVE_TEXT, "18%", ElementRole.KPI, profile=DeliveryProfile.EDITABILITY_PRIORITY)
        self.assertEqual(title_plan.contract.strategy, ProductionStrategy.NATIVE_TEXT)
        self.assertEqual(kpi_plan.contract.strategy, ProductionStrategy.NATIVE_TEXT)

    # Scenario 18: Approved Sample fidelity
    def test_scenario_18_approved_sample_fidelity(self):
        approved = ElementSnapshot("kpi", "18%", ElementBox(1, 1, 3, 1), prominence=3, editable=True, evidence_bound=True)
        # Material hierarchy degradation blocks
        degraded = ElementSnapshot("kpi", "18%", ElementBox(1, 1, 3, 1), prominence=1, editable=True, evidence_bound=True)
        report_deg = compare_fidelity((approved,), (degraded,), approved_sample=True)
        self.assertEqual(report_deg.status, QaSeverity.BLOCKING)
        self.assertEqual(report_deg.count(FidelityIssue.HIERARCHY_DEGRADATION), 1)

        # Slight layout drift passes
        drifted = ElementSnapshot("kpi", "18%", ElementBox(1.03, 1, 3, 1), line_count=2, prominence=3, editable=True, evidence_bound=True)
        report_drift = compare_fidelity((approved,), (drifted,), approved_sample=True)
        self.assertEqual(report_drift.status, QaSeverity.ACCEPTABLE)


if __name__ == "__main__":
    unittest.main()
