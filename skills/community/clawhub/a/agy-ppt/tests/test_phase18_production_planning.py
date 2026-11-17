#!/usr/bin/env python3
"""Phase 18.2 element production-planning tests."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from phase18_contract import DeliveryProfile, EditabilityClass, FontPortability, ProductionStrategy  # noqa: E402
from phase18_production_plan import ElementPlanningInput, ElementRole, plan_element, plan_elements  # noqa: E402


def item(role: ElementRole, **overrides) -> ElementPlanningInput:
    values = {
        "element_id": f"slide-1-{role.value.lower()}",
        "semantic_ref": "claim:stable",
        "narrative_ref": "narrative:stable",
        "role": role,
        "approved_content": "Approved content 18%",
        "evidence_claim_ids": ("pc:source",),
    }
    values.update(overrides)
    return ElementPlanningInput(**values)


class Phase18ProductionPlanningTests(unittest.TestCase):
    def test_name_and_contact_are_editable_required_native_text(self):
        for role in (ElementRole.NAME, ElementRole.CONTACT):
            result = plan_element(item(role))
            self.assertEqual((result.contract.editability, result.contract.strategy), (EditabilityClass.EDITABLE_REQUIRED, ProductionStrategy.NATIVE_TEXT))

    def test_price_and_kpi_are_editable_required(self):
        for role in (ElementRole.PRICE, ElementRole.KPI):
            self.assertEqual(plan_element(item(role)).contract.editability, EditabilityClass.EDITABLE_REQUIRED)

    def test_kpi_native_strategy_has_one_line_envelope(self):
        result = plan_element(item(ElementRole.KPI))
        self.assertEqual(result.contract.strategy, ProductionStrategy.NATIVE_TEXT)
        self.assertEqual(result.contract.envelope.expected_max_lines, 1)
        self.assertEqual(result.contract.envelope.expected_max_characters, 16)
        self.assertGreaterEqual(result.contract.envelope.minimum_font_size, 24)

    def test_ordinary_title_is_native_and_editable_preferred(self):
        result = plan_element(item(ElementRole.TITLE))
        self.assertEqual((result.contract.editability, result.contract.strategy), (EditabilityClass.EDITABLE_PREFERRED, ProductionStrategy.NATIVE_TEXT))
        self.assertEqual(result.contract.envelope.expected_max_lines, 2)
        self.assertEqual(result.contract.envelope.expected_max_characters, 48)

    def test_body_copy_is_native_when_font_is_safe(self):
        self.assertEqual(plan_element(item(ElementRole.BODY)).contract.strategy, ProductionStrategy.NATIVE_TEXT)

    def test_logo_is_replaceable_native_image_by_default(self):
        result = plan_element(item(ElementRole.LOGO))
        self.assertEqual((result.contract.editability, result.contract.strategy), (EditabilityClass.REPLACEABLE, ProductionStrategy.NATIVE_IMAGE))

    def test_vector_safe_logo_can_remain_vector(self):
        self.assertEqual(plan_element(item(ElementRole.LOGO, vector_safe=True)).contract.strategy, ProductionStrategy.VECTOR_GRAPHIC)

    def test_photo_is_replaceable_and_preserves_crop(self):
        result = plan_element(item(ElementRole.PHOTO))
        self.assertEqual(result.contract.strategy, ProductionStrategy.NATIVE_IMAGE)
        self.assertEqual(result.contract.envelope.crop_behavior.value, "PRESERVE_CROP")

    def test_simple_card_background_is_native_shape(self):
        self.assertEqual(plan_element(item(ElementRole.SIMPLE_SHAPE)).contract.strategy, ProductionStrategy.NATIVE_SHAPE)

    def test_artistic_headline_is_locked(self):
        result = plan_element(item(ElementRole.ARTISTIC_HEADLINE, font_portability=FontPortability.FONT_CRITICAL))
        self.assertEqual((result.contract.editability, result.contract.strategy), (EditabilityClass.LOCKED_REQUIRED, ProductionStrategy.LOCKED_VISUAL))

    def test_complex_hero_is_not_decomposed(self):
        result = plan_element(item(ElementRole.HERO_ARTWORK, vector_safe=True))
        self.assertEqual(result.contract.strategy, ProductionStrategy.RASTER_REGION)
        self.assertEqual(result.contract.editability, EditabilityClass.LOCKED_REQUIRED)

    def test_font_critical_ordinary_text_downgrades_to_locked(self):
        result = plan_element(item(ElementRole.TITLE, font_portability=FontPortability.FONT_CRITICAL))
        self.assertEqual(result.contract.strategy, ProductionStrategy.LOCKED_VISUAL)

    def test_balanced_profile_is_applied(self):
        self.assertEqual(plan_element(item(ElementRole.BODY)).contract.delivery_profile, DeliveryProfile.BALANCED)

    def test_fidelity_profile_prefers_locked_artwork(self):
        result = plan_element(item(ElementRole.DECORATIVE_ARTWORK), DeliveryProfile.FIDELITY)
        self.assertEqual(result.contract.strategy, ProductionStrategy.LOCKED_VISUAL)

    def test_editability_priority_uses_vector_only_when_explicitly_safe(self):
        safe = plan_element(item(ElementRole.DECORATIVE_ARTWORK, vector_safe=True), DeliveryProfile.EDITABILITY_PRIORITY)
        unsafe = plan_element(item(ElementRole.DECORATIVE_ARTWORK, vector_safe=False), DeliveryProfile.EDITABILITY_PRIORITY)
        self.assertEqual(safe.contract.strategy, ProductionStrategy.VECTOR_GRAPHIC)
        self.assertEqual(unsafe.contract.strategy, ProductionStrategy.RASTER_REGION)

    def test_evidence_identity_is_unchanged(self):
        source = item(ElementRole.KPI, evidence_claim_ids=("pc:b", "pc:a"))
        result = plan_element(source)
        self.assertEqual(result.evidence_claim_ids, ("pc:a", "pc:b"))

    def test_narrative_identity_is_unchanged(self):
        result = plan_element(item(ElementRole.TITLE, narrative_ref="np:abc"))
        self.assertEqual(result.narrative_ref, "np:abc")

    def test_plan_is_deterministic_and_persistable(self):
        first = plan_element(item(ElementRole.KPI))
        second = plan_element(item(ElementRole.KPI))
        self.assertEqual(first, second)
        self.assertEqual(first.canonical_json(), second.canonical_json())

    def test_planning_does_not_use_unnecessary_full_slide_raster_or_arbitrary_vectorization(self):
        results = plan_elements((item(ElementRole.BODY), item(ElementRole.HERO_ARTWORK, element_id="hero", semantic_ref="s2")))
        self.assertNotIn(ProductionStrategy.FULL_RASTER_SLIDE, {result.contract.strategy for result in results})
        self.assertNotEqual(results[1].contract.strategy, ProductionStrategy.VECTOR_GRAPHIC)


if __name__ == "__main__":
    unittest.main()
