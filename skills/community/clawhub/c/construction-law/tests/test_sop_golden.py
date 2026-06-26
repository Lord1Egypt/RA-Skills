#!/usr/bin/env python3
"""
Layer 1: Golden-file tests — frozen known-answer assertions.

Loads hand-computed (claim_date → deadline) pairs from tests/data/golden_timelines.csv.
Any change to SOP date logic that shifts these results is a regression.
"""

import csv
import os
import sys
import unittest
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from sop_calculator import add_sop_days, calc_timeline, is_sop_day, SG_PUBLIC_HOLIDAYS

GOLDEN_CSV = os.path.join(os.path.dirname(__file__), 'data', 'golden_timelines.csv')


def load_golden_data():
    """Load golden CSV, skipping comments."""
    rows = []
    with open(GOLDEN_CSV, 'r') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            rows.append(line.strip())
    reader = csv.DictReader(rows)
    return list(reader)


class TestGoldenTimelines(unittest.TestCase):
    """Assert calc_timeline matches hand-verified deadlines."""

    @classmethod
    def setUpClass(cls):
        cls.golden = load_golden_data()
        assert len(cls.golden) >= 9, f"Expected ≥9 golden rows, got {len(cls.golden)}"

    def _run_scenario(self, row):
        claim = row['claim_date']
        rp = int(row['response_period'])
        result = calc_timeline(claim, response_period=rp)
        timeline = result['timeline']

        # Extract milestones by section
        milestones = {t['section']: t['date'] for t in timeline}

        self.assertEqual(
            milestones['s.11'].isoformat(), row['expected_response'],
            f"Response deadline mismatch for claim {claim} (rp={rp})"
        )
        self.assertEqual(
            milestones['s.13'].isoformat(), row['expected_adj_app'],
            f"Adjudication app deadline mismatch for claim {claim}"
        )
        self.assertEqual(
            milestones['s.17(1)(b)'].isoformat(), row['expected_determination'],
            f"Determination deadline mismatch for claim {claim}"
        )
        self.assertEqual(
            result['determination_extended'].isoformat(), row['expected_det_extended'],
            f"Determination+extension mismatch for claim {claim}"
        )
        self.assertEqual(
            milestones['s.22(1)'].isoformat(), row['expected_payment'],
            f"Payment due mismatch for claim {claim}"
        )

    def test_scenario_01_cny_cluster(self):
        """CNY 2026: claim Feb 15, skips Feb 17-18 PH."""
        self._run_scenario(self.golden[0])

    def test_scenario_02_vesak_hrh_cluster(self):
        """Vesak/HRH 2026: claim May 25, skips May 27 + May 31 (Sun) + Jun 1 (in-lieu)."""
        self._run_scenario(self.golden[1])

    def test_scenario_03_christmas_new_year(self):
        """Christmas/NY: claim Dec 20, crosses year boundary with 2 PH skipped."""
        self._run_scenario(self.golden[2])

    def test_scenario_04_national_day_cluster(self):
        """National Day: claim Aug 5, skips Aug 9 (Sun PH) + Aug 10 (in-lieu Mon)."""
        self._run_scenario(self.golden[3])

    def test_scenario_05_baseline(self):
        """Baseline with few holidays (Mar 21 + Apr 3 in range)."""
        self._run_scenario(self.golden[4])

    def test_scenario_06_claim_on_public_holiday(self):
        """Claim served on New Year's Day — PH as start date."""
        self._run_scenario(self.golden[5])

    def test_scenario_07_fourteen_day_response(self):
        """14-day response period variant."""
        self._run_scenario(self.golden[6])

    def test_scenario_08_standard_with_extension(self):
        """Standard 21-day, verifies s.17(2) +7 extension date."""
        self._run_scenario(self.golden[7])

    def test_scenario_09_saturday_deadline(self):
        """Saturday deadline: claim Apr 10, response lands on Sat May 2.
        Proves Saturdays are NOT skipped — s.50(a) Interpretation Act only
        rolls off Sundays and public holidays, not Saturdays."""
        self._run_scenario(self.golden[8])
        # Extra assertion: response deadline is a Saturday
        result = calc_timeline(self.golden[8]['claim_date'],
                               response_period=int(self.golden[8]['response_period']))
        response = None
        for t in result['timeline']:
            if t['section'] == 's.11':
                response = t['date']
                break
        self.assertEqual(response.weekday(), 5,
                         f"Response deadline {response} should be Saturday (weekday=5)")

    def test_no_golden_deadline_falls_on_holiday(self):
        """Cross-check: none of the expected dates in the golden file should be PH."""
        for row in self.golden:
            for col in ['expected_response', 'expected_adj_app',
                        'expected_determination', 'expected_det_extended',
                        'expected_payment']:
                d = date.fromisoformat(row[col])
                self.assertTrue(is_sop_day(d),
                                f"Golden date {d} (col={col}, claim={row['claim_date']}) "
                                f"falls on a public holiday!")

    def test_determination_extended_is_7_sop_days_after_determination(self):
        """s.17(2): extended deadline must be exactly 7 SOP days after base determination."""
        for row in self.golden:
            det = date.fromisoformat(row['expected_determination'])
            det_ext = date.fromisoformat(row['expected_det_extended'])
            computed_ext = add_sop_days(det, 7)
            self.assertEqual(computed_ext, det_ext,
                             f"s.17(2) extension: det={det}, expected ext={det_ext}, "
                             f"got {computed_ext} (claim={row['claim_date']})")


if __name__ == "__main__":
    unittest.main()
