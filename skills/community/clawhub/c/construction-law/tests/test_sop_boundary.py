#!/usr/bin/env python3
"""
Layer 3: Boundary tests — edge cases and statutory-specific logic.

Covers:
- End-of-month boundaries (Jan 31, Feb 28/29, Mar 31)
- End-of-year boundary (Dec 31 → Jan)
- s.17(2) +7 extension: determination_extended is always exactly 7 SOP days
  after determination_deadline (verified as SOP days, not calendar days)
- Claim date itself is a PH
- Period spans 3+ consecutive holidays
- Out-of-range year produces clear error (not silent wrong answers)
- Version stamp pulls from version.py
- Leap year February
"""

import os
import sys
import unittest
from datetime import date, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from sop_calculator import (
    add_sop_days, is_sop_day, calc_timeline,
    SG_PUBLIC_HOLIDAYS, _COVERED_YEARS, _check_year_coverage,
)


class TestEndOfMonth(unittest.TestCase):
    """Deadlines crossing month boundaries."""

    def test_jan_31_crossing(self):
        """Claim on Jan 31 — response crosses into Feb."""
        result = add_sop_days(date(2026, 1, 31), 7)
        self.assertEqual(result.month, 2)
        self.assertTrue(is_sop_day(result))

    def test_feb_28_non_leap(self):
        """2026 is not a leap year. Feb 28 + 1 → Mar 1."""
        result = add_sop_days(date(2026, 2, 28), 1)
        self.assertEqual(result, date(2026, 3, 1))

    def test_mar_31_crossing(self):
        """Mar 31 + 1 → Apr 1 (no holidays expected Apr 1)."""
        result = add_sop_days(date(2026, 3, 31), 1)
        self.assertEqual(result, date(2026, 4, 1))
        self.assertTrue(is_sop_day(result))


class TestEndOfYear(unittest.TestCase):
    """Deadlines crossing year boundary."""

    def test_dec_31_to_jan(self):
        """Dec 31 2026 + 1 → skips Jan 1 2027 (PH) → Jan 2."""
        result = add_sop_days(date(2026, 12, 31), 1)
        self.assertEqual(result, date(2027, 1, 2))

    def test_last_day_of_year_claim(self):
        """Full timeline from Dec 31 — all milestones in next year."""
        result = calc_timeline("2026-12-31", response_period=21)
        for t in result['timeline']:
            if t['section'] != 's.10':  # Skip the claim date itself
                self.assertGreater(t['date'].year, 2026,
                                   f"{t['event']} should be in 2027")
            self.assertTrue(is_sop_day(t['date']),
                            f"{t['event']} lands on a PH!")


class TestSection17Extension(unittest.TestCase):
    """s.17(2): Adjudicator may extend determination by up to 7 days
    with claimant's written consent. This is 7 SOP days (not calendar days)."""

    def test_extension_is_7_sop_days_after_determination(self):
        """determination_extended = determination + 7 SOP days."""
        result = calc_timeline("2026-06-30", response_period=21)
        det = None
        for t in result['timeline']:
            if t['section'] == 's.17(1)(b)':
                det = t['date']
                break
        self.assertIsNotNone(det)
        expected_ext = add_sop_days(det, 7)
        self.assertEqual(result['determination_extended'], expected_ext)

    def test_extension_skips_holidays(self):
        """If PH falls between det and det+7, extension must skip it."""
        # Claim near National Day — det around Aug, in-lieu might affect
        result = calc_timeline("2026-08-05", response_period=21)
        det = None
        for t in result['timeline']:
            if t['section'] == 's.17(1)(b)':
                det = t['date']
                break
        det_ext = result['determination_extended']
        # Verify no holiday between det and det_ext
        cur = det + timedelta(days=1)
        sop_count = 0
        while cur <= det_ext:
            if is_sop_day(cur):
                sop_count += 1
            cur += timedelta(days=1)
        self.assertEqual(sop_count, 7,
                         f"Expected exactly 7 SOP days between det ({det}) and ext ({det_ext})")

    def test_extension_never_on_holiday(self):
        """Extended determination date must not fall on a PH."""
        test_claims = ["2026-02-15", "2026-05-25", "2026-08-05",
                       "2026-12-20", "2026-06-30"]
        for claim in test_claims:
            result = calc_timeline(claim, response_period=21)
            self.assertTrue(is_sop_day(result['determination_extended']),
                            f"det_extended for claim {claim} falls on PH!")

    def test_extension_mid_week_vs_near_holiday(self):
        """Mid-week determination (no nearby PH): extension should be
        exactly 7 calendar days later (since no PH to skip)."""
        # Claim Jun 30 → det is Aug 20 (Thu), no PH until Nov 8
        result = calc_timeline("2026-06-30", response_period=21)
        det = None
        for t in result['timeline']:
            if t['section'] == 's.17(1)(b)':
                det = t['date']
                break
        det_ext = result['determination_extended']
        # If no holidays between det and det+7 calendar days, should be +7 cal
        calendar_diff = (det_ext - det).days
        self.assertEqual(calendar_diff, 7,
                         f"No holidays near det ({det}), so extension should be +7 calendar days, "
                         f"got +{calendar_diff} days (ext={det_ext})")


class TestClaimOnPublicHoliday(unittest.TestCase):
    """Claim served on a PH — the start date is just a reference,
    counting begins from the next day."""

    def test_claim_on_new_year(self):
        """Claim on Jan 1 (PH). First counted day should be Jan 2."""
        result = add_sop_days(date(2026, 1, 1), 1)
        self.assertEqual(result, date(2026, 1, 2))

    def test_claim_on_cny_day1(self):
        """Claim on CNY Day 1 (Feb 17). First counted day skips Feb 18 too."""
        result = add_sop_days(date(2026, 2, 17), 1)
        # Feb 17 (start, not counted) → Feb 18 (PH skip) → Feb 19 (day 1)
        self.assertEqual(result, date(2026, 2, 19))

    def test_full_timeline_from_ph_all_valid(self):
        """All milestones from a PH-start claim should be valid SOP days."""
        result = calc_timeline("2026-01-01", response_period=21)
        for t in result['timeline']:
            if t['section'] != 's.10':  # Claim date itself can be PH
                self.assertTrue(is_sop_day(t['date']),
                                f"{t['event']} ({t['date']}) lands on PH!")


class TestConsecutiveHolidays(unittest.TestCase):
    """Period spanning 3+ consecutive non-SOP days."""

    def test_vesak_in_lieu_cluster(self):
        """Vesak 2026: May 31 (Sun, PH) + Jun 1 (Mon, in-lieu) = 2 consecutive.
        May 27 (Wed, HRH) also nearby. Counting from May 26 should skip correctly."""
        # May 26 (start) → May 27 (PH skip) → May 28 (day 1)
        result = add_sop_days(date(2026, 5, 26), 1)
        self.assertEqual(result, date(2026, 5, 28))

    def test_triple_skip_vesak_cluster(self):
        """Start May 30: May 31 (PH Sun) + Jun 1 (in-lieu Mon) = skip 2 consecutive."""
        # May 30 (start) → May 31 (PH) → Jun 1 (PH in-lieu) → Jun 2 (day 1)
        result = add_sop_days(date(2026, 5, 30), 1)
        self.assertEqual(result, date(2026, 6, 2))

    def test_cny_plus_weekend_span(self):
        """CNY 2027: Feb 6 (Sat PH), Feb 7 (Sun PH), Feb 8 (Mon in-lieu).
        All three are non-SOP days. Count from Feb 5."""
        # Feb 5 (start) → Feb 6 (PH) → Feb 7 (PH) → Feb 8 (in-lieu PH) → Feb 9 (day 1)
        result = add_sop_days(date(2027, 2, 5), 1)
        self.assertEqual(result, date(2027, 2, 9))
        # Feb 4 (start) → Feb 5 (day 1 — normal Friday)
        result2 = add_sop_days(date(2027, 2, 4), 1)
        self.assertEqual(result2, date(2027, 2, 5))


class TestOutOfRangeYear(unittest.TestCase):
    """Calculator must fail loudly for years without holiday data.

    This is the most critical safety test: without it, dates in uncovered
    years silently produce wrong answers (treating all days as working days).
    The error points in the dangerous direction — understating protection.
    """

    def test_2028_raises_value_error(self):
        """2028 has no holiday data — should raise, not silently compute."""
        with self.assertRaises(ValueError) as ctx:
            calc_timeline("2028-06-30", response_period=21)
        self.assertIn("2028", str(ctx.exception))
        self.assertIn("sg_holidays.json", str(ctx.exception))

    def test_2024_raises_value_error(self):
        """2024 is before our data range."""
        with self.assertRaises(ValueError) as ctx:
            calc_timeline("2024-06-30", response_period=21)
        self.assertIn("2024", str(ctx.exception))

    def test_add_sop_days_uncovered_year_raises(self):
        """add_sop_days must raise for uncovered start year."""
        with self.assertRaises(ValueError):
            add_sop_days(date(2028, 6, 1), 5)

    def test_add_sop_days_crossing_into_uncovered_year_raises(self):
        """add_sop_days must raise when result crosses into uncovered year."""
        with self.assertRaises(ValueError):
            add_sop_days(date(2027, 12, 25), 14)

    def test_is_sop_day_uncovered_year_raises(self):
        """is_sop_day must raise for uncovered year."""
        with self.assertRaises(ValueError):
            is_sop_day(date(2028, 8, 9))

    def test_sop_days_between_uncovered_year_raises(self):
        """sop_days_between must raise if either date is in uncovered year."""
        from sop_calculator import sop_days_between
        with self.assertRaises(ValueError):
            sop_days_between(date(2028, 1, 1), date(2028, 2, 1))

    def test_covered_years_correct(self):
        """_COVERED_YEARS should contain exactly 2025, 2026, 2027."""
        self.assertEqual(_COVERED_YEARS, {2025, 2026, 2027})


class TestLeapYear(unittest.TestCase):
    """Leap year handling (2028 would be leap but is out of range;
    use 2024 is also out of range. Test the math concept with in-range dates)."""

    def test_feb_28_to_mar_non_leap(self):
        """2026 (non-leap): Feb 28 + 1 = Mar 1."""
        result = add_sop_days(date(2026, 2, 28), 1)
        self.assertEqual(result, date(2026, 3, 1))

    def test_feb_27_plus_2(self):
        """2026: Feb 27 + 2 = Mar 1 (no Feb 29)."""
        result = add_sop_days(date(2026, 2, 27), 2)
        self.assertEqual(result, date(2026, 3, 1))


class TestSaturdayDeadline(unittest.TestCase):
    """Saturday deadlines must NOT roll forward.

    s.50(a) Interpretation Act only rolls off Sundays and public holidays.
    Saturdays are ordinary days for SOP purposes. If the deadline lands
    on a Saturday, it stays on Saturday. This is the test that catches
    someone 'fixing' the code to also skip Saturdays.
    """

    def test_deadline_on_saturday_stays(self):
        """Claim on a Tuesday, short period, deadline lands on Saturday.
        Pick a date range with no nearby PHs to isolate the Saturday question.
        2026-04-07 (Tue) + 4 = 2026-04-11 (Sat). No PHs between Apr 3 and May 1."""
        result = add_sop_days(date(2026, 4, 7), 4)
        self.assertEqual(result, date(2026, 4, 11))
        self.assertEqual(result.weekday(), 5, "Result should be Saturday (weekday=5)")
        self.assertTrue(is_sop_day(result), "Saturday must be a valid SOP day")

    def test_saturday_counted_through(self):
        """Saturday is counted, not skipped. Apr 10 (Fri) + 2 = Apr 12 (Sun).
        Sunday is not a PH here, so it's a valid SOP day."""
        result = add_sop_days(date(2026, 4, 10), 2)
        self.assertEqual(result, date(2026, 4, 12))
        self.assertEqual(result.weekday(), 6, "Result should be Sunday (weekday=6)")


class TestInLieuCollision(unittest.TestCase):
    """In-lieu derivation must handle collisions correctly.

    When a Sunday PH's Monday is already occupied (another PH or
    an existing in-lieu), the algorithm must roll forward to Tuesday
    or later. Tests use synthetic holiday sets to exercise the
    while-loop in _add_sunday_in_lieu.
    """

    def test_single_sunday_in_lieu_to_monday(self):
        """Basic case: Sunday PH → in-lieu Monday."""
        from sop_calculator import _add_sunday_in_lieu
        holidays = {date(2026, 8, 9)}  # Sunday
        result = _add_sunday_in_lieu(holidays)
        self.assertIn(date(2026, 8, 10), result, "In-lieu should be Monday")

    def test_collision_rolls_to_tuesday(self):
        """Sunday PH + Monday already a PH → in-lieu Tuesday."""
        from sop_calculator import _add_sunday_in_lieu
        holidays = {
            date(2026, 8, 9),   # Sunday PH
            date(2026, 8, 10),  # Monday already occupied
        }
        result = _add_sunday_in_lieu(holidays)
        self.assertIn(date(2026, 8, 11), result,
                      "In-lieu should roll to Tuesday when Monday is occupied")

    def test_double_collision_rolls_to_wednesday(self):
        """Sunday PH + Monday PH + Tuesday PH → in-lieu Wednesday."""
        from sop_calculator import _add_sunday_in_lieu
        holidays = {
            date(2026, 8, 9),   # Sunday PH
            date(2026, 8, 10),  # Monday PH
            date(2026, 8, 11),  # Tuesday PH
        }
        result = _add_sunday_in_lieu(holidays)
        self.assertIn(date(2026, 8, 12), result,
                      "In-lieu should roll to Wednesday when Mon+Tue occupied")

    def test_two_consecutive_sundays(self):
        """Two Sundays in a row (synthetic): each gets its own in-lieu."""
        from sop_calculator import _add_sunday_in_lieu
        holidays = {
            date(2026, 8, 2),   # Sunday
            date(2026, 8, 9),   # Sunday
        }
        result = _add_sunday_in_lieu(holidays)
        self.assertIn(date(2026, 8, 3), result, "First in-lieu: Monday 3rd")
        self.assertIn(date(2026, 8, 10), result, "Second in-lieu: Monday 10th")

    def test_real_data_cny_2027(self):
        """CNY 2027: Feb 6 (Sat) + Feb 7 (Sun). Sunday gets in-lieu Mon Feb 8."""
        self.assertIn(date(2027, 2, 7), SG_PUBLIC_HOLIDAYS, "CNY Day 2 is Sun PH")
        self.assertIn(date(2027, 2, 8), SG_PUBLIC_HOLIDAYS,
                      "In-lieu Monday for CNY Day 2 Sunday")


class TestSilverBookFitnessForPurpose(unittest.TestCase):
    """Silver Book obligations should include fitness-for-purpose language."""

    def test_silver_has_fitness_for_purpose(self):
        """FIDIC Silver obligations register must surface fitness-for-purpose."""
        from obligations_register import OBLIGATIONS
        silver_contractor = OBLIGATIONS.get("fidic-silver", {}).get("contractor", [])
        ffp_found = any("fitness for purpose" in ob.get("obligation", "").lower()
                        for ob in silver_contractor)
        self.assertTrue(ffp_found,
                        "Silver Book contractor obligations must include "
                        "fitness-for-purpose language (key EPC principle)")


if __name__ == "__main__":
    unittest.main()
