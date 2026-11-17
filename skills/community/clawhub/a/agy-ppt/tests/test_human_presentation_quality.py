#!/usr/bin/env python3
"""Deterministic authority rules for the non-numeric human quality gate."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from human_presentation_quality import (  # noqa: E402
    HumanPresentationQualityRecord,
    HumanPresentationQualityState,
    ReviewAuthority,
    automated_quality_assistance,
    human_quality_review,
)


SHA = "a" * 64


class HumanPresentationQualityTests(unittest.TestCase):
    def test_human_rejection_is_block(self):
        record = human_quality_review(SHA, accepted=False, detail="The delivered deck is not presentable.")
        self.assertEqual(record.state, HumanPresentationQualityState.BLOCK)
        self.assertEqual(record.authority, ReviewAuthority.HUMAN)

    def test_only_explicit_human_acceptance_can_pass(self):
        record = human_quality_review(SHA, accepted=True, detail="Reviewed the actual PowerPoint render.")
        self.assertEqual(record.state, HumanPresentationQualityState.PASS)
        with self.assertRaisesRegex(ValueError, "automated assistance cannot pass"):
            HumanPresentationQualityRecord(
                SHA, HumanPresentationQualityState.PASS,
                ReviewAuthority.AUTOMATED_ASSISTANCE, "Jev classified it as acceptable.",
            )

    def test_automated_nonblocking_result_still_requires_human_review(self):
        record = automated_quality_assistance(SHA, blocking=False, detail="No deterministic defects found.")
        self.assertEqual(record.state, HumanPresentationQualityState.REVIEW_REQUIRED)

    def test_automated_block_is_allowed_but_not_release_authority(self):
        record = automated_quality_assistance(SHA, blocking=True, detail="Evidence number changed.")
        self.assertEqual(record.state, HumanPresentationQualityState.BLOCK)
        self.assertEqual(record.authority, ReviewAuthority.AUTOMATED_ASSISTANCE)

    def test_record_is_bound_to_exact_artifact_hash(self):
        with self.assertRaises(ValueError):
            human_quality_review("not-a-sha", accepted=True, detail="Invalid artifact identity.")


if __name__ == "__main__":
    unittest.main()
