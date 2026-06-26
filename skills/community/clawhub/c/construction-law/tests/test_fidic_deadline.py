#!/usr/bin/env python3
"""
Tests for the FIDIC Deadline Calculator.

Golden tests use hand-computed Singapore scenarios (bundled, gazette-verified).
Property tests validate invariants that apply regardless of jurisdiction
when a user supplies their own holiday file.
"""

import csv
import json
import os
import sys
import tempfile
import unittest
from datetime import date, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from fidic_deadline import compute_deadline, load_holidays, list_available_seats

GOLDEN_CSV = os.path.join(os.path.dirname(__file__), 'data', 'golden_deadlines.csv')


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


class TestFidicDeadlineGoldenSG(unittest.TestCase):
    """Assert compute_deadline matches hand-verified Singapore deadlines."""

    @classmethod
    def setUpClass(cls):
        cls.golden = load_golden_data()
        assert len(cls.golden) >= 4, f"Expected >=4 golden rows, got {len(cls.golden)}"

    def _run_scenario(self, row, scenario_num):
        seat = row['seat']
        trigger = date.fromisoformat(row['trigger_date'])
        period = int(row['period'])
        mode = row['mode']
        expected_deadline = date.fromisoformat(row['expected_deadline'])
        expected_ph_count = int(row['holidays_skipped_count'])
        expected_cal_days = int(row['calendar_days_elapsed'])

        result = compute_deadline(trigger, period, seat, mode)

        self.assertEqual(
            result['deadline'], expected_deadline,
            f"Scenario {scenario_num}: {seat} {trigger} +{period} {mode} expected {expected_deadline}, got {result['deadline']}"
        )
        self.assertEqual(
            len(result['holidays_skipped']), expected_ph_count,
            f"Scenario {scenario_num}: expected {expected_ph_count} PHs skipped, got {len(result['holidays_skipped'])}"
        )
        actual_cal_days = (result['deadline'] - trigger).days
        self.assertEqual(
            actual_cal_days, expected_cal_days,
            f"Scenario {scenario_num}: expected {expected_cal_days} calendar days, got {actual_cal_days}"
        )

    def test_scenario_01_sg_calendar_fidic_default(self):
        self._run_scenario(self.golden[0], 1)

    def test_scenario_02_sg_exclude_ph_vesak_hrh(self):
        self._run_scenario(self.golden[1], 2)

    def test_scenario_03_sg_exclude_ph_cny(self):
        self._run_scenario(self.golden[2], 3)

    def test_scenario_04_sg_exclude_ph_national_day(self):
        self._run_scenario(self.golden[3], 4)


class TestFidicDeadlineSeats(unittest.TestCase):
    def test_list_seats_returns_sg(self):
        seats = list_available_seats()
        isos = {s['iso'] for s in seats}
        self.assertIn('SG', isos)
        self.assertEqual(isos, {'SG'})

    def test_non_sg_without_file_raises_valueerror(self):
        with self.assertRaises(ValueError) as ctx:
            load_holidays('AE', 2026)
        msg = str(ctx.exception)
        self.assertIn("No bundled holiday data", msg)
        self.assertIn("--holidays-file", msg)

    def test_missing_year_raises_valueerror(self):
        with self.assertRaises(ValueError) as ctx:
            load_holidays('SG', 2030)
        self.assertIn('2030', str(ctx.exception))

    def test_calendar_mode_ignores_seat(self):
        trigger = date(2026, 3, 18)
        r_sg = compute_deadline(trigger, 28, 'SG', 'calendar')
        r_xx = compute_deadline(trigger, 28, 'XX', 'calendar')
        self.assertEqual(r_sg['deadline'], r_xx['deadline'])
        self.assertEqual(r_sg['deadline'], trigger + timedelta(days=28))

    def test_sg_exclude_ph_matches_sop_calculator(self):
        from sop_calculator import add_sop_days
        test_cases = [
            (date(2026, 5, 25), 28),
            (date(2026, 2, 15), 28),
            (date(2026, 8, 5), 28),
            (date(2026, 1, 1), 21),
            (date(2026, 12, 20), 14),
        ]
        for trigger, period in test_cases:
            sop_result = add_sop_days(trigger, period)
            dl_result = compute_deadline(trigger, period, 'SG', 'exclude_ph')
            self.assertEqual(
                sop_result, dl_result['deadline'],
                f"Logic drift: SOP={sop_result}, Deadline={dl_result['deadline']} for trigger={trigger}, period={period}"
            )


class TestFidicDeadlineUserSupplied(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.holidays_data = {
            "_meta": {
                "country": "Testland",
                "iso": "TL",
                "source": "Test data",
                "last_verified": "2026-05-10",
                "notes": "Test jurisdiction",
                "weekend": ["Sat", "Sun"],
                "in_lieu_rule": "none"
            },
            "2026": {
                "source": "Test",
                "dates": [
                    "2026-01-01",
                    "2026-03-20",
                    "2026-03-21",
                    "2026-03-22",
                    "2026-03-23",
                    "2026-05-01",
                    "2026-06-17",
                    "2026-08-09",
                    "2026-12-25",
                    "2026-12-26"
                ],
                "names": [
                    "New Year", "Holiday A", "Holiday B", "Holiday C", "Holiday D",
                    "Labour Day", "Mid-year", "National Day", "Christmas", "Boxing Day"
                ]
            }
        }
        cls.tmpfile = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(cls.holidays_data, cls.tmpfile)
        cls.tmpfile.close()
        cls.holidays_file = cls.tmpfile.name

    @classmethod
    def tearDownClass(cls):
        os.unlink(cls.holidays_file)

    def test_exclude_ph_deadline_never_on_holiday(self):
        triggers = [date(2026, 3, 15), date(2026, 1, 1), date(2026, 5, 1), date(2026, 12, 20)]
        holidays = {date.fromisoformat(d) for d in self.holidays_data['2026']['dates']}
        for trigger in triggers:
            result = compute_deadline(trigger, 28, 'TL', 'exclude_ph', self.holidays_file)
            self.assertNotIn(result['deadline'], holidays)

    def test_working_deadline_never_on_weekend_or_holiday(self):
        triggers = [date(2026, 3, 15), date(2026, 1, 1), date(2026, 5, 1), date(2026, 12, 20)]
        holidays = {date.fromisoformat(d) for d in self.holidays_data['2026']['dates']}
        for trigger in triggers:
            result = compute_deadline(trigger, 28, 'TL', 'working', self.holidays_file)
            self.assertNotIn(result['deadline'].weekday(), {5, 6})
            self.assertNotIn(result['deadline'], holidays)

    def test_calendar_mode_never_skips_holidays(self):
        trigger = date(2026, 3, 15)
        result = compute_deadline(trigger, 28, 'TL', 'calendar', self.holidays_file)
        self.assertEqual(len(result['holidays_skipped']), 0)
        self.assertEqual(result['deadline'], trigger + timedelta(days=28))

    def test_non_sg_seat_without_file_errors_in_exclude_ph(self):
        with self.assertRaises(ValueError) as ctx:
            compute_deadline(date(2026, 3, 18), 28, 'AE', 'exclude_ph')
        self.assertIn('holidays-file', str(ctx.exception))

    def test_non_sg_seat_calendar_mode_works_without_file(self):
        result = compute_deadline(date(2026, 3, 18), 28, 'AE', 'calendar')
        self.assertEqual(result['deadline'], date(2026, 4, 15))

    def test_user_supplied_file_loads_correctly(self):
        result = compute_deadline(date(2026, 3, 15), 28, 'TL', 'exclude_ph', self.holidays_file)
        self.assertGreater(len(result['holidays_skipped']), 0)
        self.assertEqual(result['seat'], 'TL')


if __name__ == "__main__":
    unittest.main()
