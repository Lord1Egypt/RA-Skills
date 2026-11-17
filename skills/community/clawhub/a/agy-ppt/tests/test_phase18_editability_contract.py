#!/usr/bin/env python3
"""Phase 18.1 delivery and editability contract tests."""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from phase16_claims import ContentOrigin  # noqa: E402
from phase17_narrative import NarrativeRole  # noqa: E402
from phase18_contract import (  # noqa: E402
    DEFAULT_DELIVERY_PROFILE,
    CropBehavior,
    DeliveryEditabilityContract,
    DeliveryProfile,
    EditabilityClass,
    EditabilityContractError,
    EditabilityEnvelope,
    FontPortability,
    OverflowBehavior,
    ProductionStrategy,
    ReplacementMode,
    ReplacementSemantics,
    ShrinkPolicy,
    user_facing_delivery_message,
)


def contract(**overrides):
    values = {
        "editability": EditabilityClass.EDITABLE_REQUIRED,
        "strategy": ProductionStrategy.NATIVE_TEXT,
        "font_portability": FontPortability.FONT_SAFE,
    }
    values.update(overrides)
    return DeliveryEditabilityContract(**values)


class Phase18EditabilityContractTests(unittest.TestCase):
    def test_all_editability_classes_are_supported(self):
        self.assertEqual(len(EditabilityClass), 5)

    def test_all_production_strategies_are_supported(self):
        self.assertEqual(len(ProductionStrategy), 8)

    def test_editability_and_strategy_are_orthogonal(self):
        for editability in EditabilityClass:
            for strategy in ProductionStrategy:
                replacement = ReplacementSemantics()
                self.assertEqual(contract(editability=editability, strategy=strategy, replacement=replacement).strategy, strategy)

    def test_all_font_portability_classes_are_supported(self):
        self.assertEqual(tuple(item.value for item in FontPortability), ("FONT_SAFE", "FONT_FALLBACK_TOLERANT", "FONT_CRITICAL"))

    def test_editability_envelope_construction(self):
        envelope = EditabilityEnvelope(
            expected_min_characters=3, expected_max_characters=24,
            expected_min_lines=1, expected_max_lines=2,
            minimum_font_size=18, maximum_font_size=28,
            shrink_policy=ShrinkPolicy.TO_MINIMUM,
            overflow_behavior=OverflowBehavior.FLAG_FOR_REVIEW,
            layout_tolerance_points=2.0,
        )
        self.assertEqual(envelope.expected_max_lines, 2)

    def test_deterministic_equality_and_serialization(self):
        first = contract(envelope=EditabilityEnvelope(expected_max_characters=20))
        second = contract(envelope=EditabilityEnvelope(expected_max_characters=20))
        self.assertEqual(first, second)
        self.assertEqual(first.canonical_json(), second.canonical_json())

    def test_invalid_envelopes_fail_deterministically(self):
        cases = (
            {"expected_min_characters": 9, "expected_max_characters": 3},
            {"minimum_font_size": 20, "maximum_font_size": 10},
            {"shrink_policy": ShrinkPolicy.TO_MINIMUM},
            {"crop_behavior": CropBehavior.PRESERVE_CROP},
        )
        for values in cases:
            with self.subTest(values=values), self.assertRaises(EditabilityContractError) as raised:
                EditabilityEnvelope(**values)
            self.assertEqual(raised.exception.error_code, "PHASE18_EDITABILITY_CONTRACT_INVALID")

    def test_replacement_semantics_are_explicit(self):
        replacement = ReplacementSemantics(ReplacementMode.PRESERVE_CROP)
        result = contract(
            editability=EditabilityClass.REPLACEABLE,
            strategy=ProductionStrategy.NATIVE_IMAGE,
            replacement=replacement,
            envelope=EditabilityEnvelope(
                replacement_min_aspect_ratio=0.8,
                replacement_max_aspect_ratio=1.8,
                crop_behavior=CropBehavior.PRESERVE_CROP,
            ),
        )
        self.assertEqual(result.replacement.mode, ReplacementMode.PRESERVE_CROP)

    def test_replacement_behavior_on_non_replaceable_contract_is_rejected(self):
        with self.assertRaises(EditabilityContractError):
            contract(replacement=ReplacementSemantics(ReplacementMode.PRESERVE_FRAME))

    def test_all_delivery_profiles_are_supported(self):
        self.assertEqual(len(DeliveryProfile), 3)

    def test_balanced_is_the_default(self):
        self.assertIs(DEFAULT_DELIVERY_PROFILE, DeliveryProfile.BALANCED)
        self.assertIs(contract().delivery_profile, DeliveryProfile.BALANCED)

    def test_serialization_has_no_environment_or_path_leakage(self):
        with tempfile.TemporaryDirectory() as temp:
            os.environ["PHASE18_TEST_SENTINEL"] = temp
            payload = contract().canonical_json()
            self.assertNotIn(temp, payload)
            self.assertNotIn("PHASE18_TEST_SENTINEL", payload)
            self.assertNotIn(str(Path.cwd()), payload)

    def test_user_message_hides_internal_enum_names(self):
        text = user_facing_delivery_message()
        for internal in ("EDITABLE_REQUIRED", "NATIVE_TEXT", "FONT_SAFE", "BALANCED"):
            self.assertNotIn(internal, text)

    def test_phase16_and_phase17_objects_remain_independent_and_compatible(self):
        result = contract()
        self.assertEqual(ContentOrigin.SOURCE_GROUNDED.value, "SOURCE_GROUNDED")
        self.assertEqual(NarrativeRole.EVIDENCE.value, "EVIDENCE")
        self.assertEqual(result.strategy, ProductionStrategy.NATIVE_TEXT)


if __name__ == "__main__":
    unittest.main()
