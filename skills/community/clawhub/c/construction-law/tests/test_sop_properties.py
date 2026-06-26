#!/usr/bin/env python3
"""
Layer 2: Property-based tests using Hypothesis.

Properties verified:
- Response deadline >= claim_date + N calendar days (can never be less)
- Deadline never falls on a SG public holiday
- add_sop_days is strictly monotonic (n < m → result(n) < result(m))
- Adding a holiday to the set can only push deadlines later, never earlier
- sop_days_between(a, add_sop_days(a, n)) == n (round-trip)
- Version stamp in output comes from version.py
"""

import os
import sys
import unittest
from datetime import date, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

try:
    from hypothesis import given, settings, assume
    from hypothesis.strategies import dates, integers
    HAS_HYPOTHESIS = True
except ImportError:
    HAS_HYPOTHESIS = False

from sop_calculator import (
    add_sop_days, is_sop_day, sop_days_between,
    SG_PUBLIC_HOLIDAYS, _GAZETTED_HOLIDAYS, _add_sunday_in_lieu,
    _COVERED_YEARS,
)

# Restrict date range to years with holiday data.
# Max days capped so results don't cross into uncovered years.
MIN_DATE = date(2025, 1, 1)
MAX_DATE = date(2027, 12, 31)
# For tests that add days, start early enough that result stays in range
MAX_DATE_FOR_ADD = date(2027, 10, 1)  # +60 days stays in 2027


@unittest.skipUnless(HAS_HYPOTHESIS, "hypothesis not installed")
class TestSopProperties(unittest.TestCase):
    """Property-based tests over the covered date range."""

    @given(d=dates(min_value=MIN_DATE, max_value=MAX_DATE_FOR_ADD),
           n=integers(min_value=1, max_value=60))
    @settings(max_examples=500)
    def test_result_never_on_holiday(self, d, n):
        """add_sop_days result must never land on a public holiday."""
        result = add_sop_days(d, n)
        self.assertTrue(is_sop_day(result),
                        f"add_sop_days({d}, {n}) = {result} lands on a PH!")

    @given(d=dates(min_value=MIN_DATE, max_value=MAX_DATE_FOR_ADD),
           n=integers(min_value=1, max_value=60))
    @settings(max_examples=500)
    def test_result_always_advances(self, d, n):
        """Result must always be strictly after start date."""
        result = add_sop_days(d, n)
        self.assertGreater(result, d)

    @given(d=dates(min_value=MIN_DATE, max_value=MAX_DATE_FOR_ADD),
           n=integers(min_value=1, max_value=30),
           m=integers(min_value=1, max_value=30))
    @settings(max_examples=300)
    def test_strict_monotonicity(self, d, n, m):
        """If n < m, then add_sop_days(d, n) < add_sop_days(d, m)."""
        assume(n < m)
        r1 = add_sop_days(d, n)
        r2 = add_sop_days(d, m)
        self.assertLess(r1, r2)

    @given(d=dates(min_value=MIN_DATE, max_value=MAX_DATE_FOR_ADD),
           n=integers(min_value=1, max_value=60))
    @settings(max_examples=500)
    def test_round_trip_sop_days_between(self, d, n):
        """sop_days_between(d, add_sop_days(d, n)) must equal n."""
        result = add_sop_days(d, n)
        computed_n = sop_days_between(d, result)
        self.assertEqual(computed_n, n,
                         f"Round-trip failed: d={d}, n={n}, result={result}, "
                         f"sop_days_between={computed_n}")

    @given(d=dates(min_value=MIN_DATE, max_value=MAX_DATE_FOR_ADD),
           n=integers(min_value=1, max_value=30))
    @settings(max_examples=200)
    def test_result_gte_calendar_days(self, d, n):
        """Result must be at least n calendar days from start
        (since holidays can only add days, never subtract)."""
        result = add_sop_days(d, n)
        self.assertGreaterEqual((result - d).days, n)

    @given(d=dates(min_value=MIN_DATE, max_value=MAX_DATE_FOR_ADD),
           n=integers(min_value=1, max_value=21))
    @settings(max_examples=200)
    def test_adding_holiday_pushes_later(self, d, n):
        """Adding a holiday to the calendar can only push deadlines later."""
        result_normal = add_sop_days(d, n)

        # Add an artificial holiday 5 days after d (if it's not already one)
        artificial = d + timedelta(days=5)
        if artificial in SG_PUBLIC_HOLIDAYS:
            return  # Skip — already a holiday

        # Compute with expanded holiday set
        expanded = SG_PUBLIC_HOLIDAYS | {artificial}
        # Manual computation with expanded set
        cur = d
        remaining = n
        while remaining > 0:
            cur += timedelta(days=1)
            if cur not in expanded:
                remaining -= 1
        result_expanded = cur

        self.assertGreaterEqual(result_expanded, result_normal,
                                f"Adding holiday {artificial} moved deadline earlier! "
                                f"d={d}, n={n}, normal={result_normal}, expanded={result_expanded}")


class TestVersionStamp(unittest.TestCase):
    """Verify version comes from version.py (single source of truth)."""

    def test_version_from_version_py(self):
        """sop_calculator.VERSION should match version.py."""
        from sop_calculator import VERSION
        from version import VERSION as VFILE
        self.assertEqual(VERSION, VFILE,
                         "sop_calculator.VERSION must come from version.py")


class TestSundayInLieuProperties(unittest.TestCase):
    """Property tests on the in-lieu derivation logic."""

    def test_in_lieu_only_from_sundays(self):
        """Every in-lieu day should originate from a Sunday holiday."""
        derived = SG_PUBLIC_HOLIDAYS - _GAZETTED_HOLIDAYS
        for d in derived:
            # The source Sunday should be in the gazetted set
            # Check backwards: d-1 should be Sun, or d-2 if consecutive
            found_source = False
            for offset in range(1, 5):
                candidate = d - timedelta(days=offset)
                if candidate in _GAZETTED_HOLIDAYS and candidate.weekday() == 6:
                    found_source = True
                    break
            self.assertTrue(found_source,
                            f"In-lieu day {d} ({d.strftime('%A')}) has no Sunday source in gazetted")

    def test_in_lieu_count(self):
        """Number of in-lieu days should equal number of Sunday holidays."""
        sunday_holidays = [d for d in _GAZETTED_HOLIDAYS if d.weekday() == 6]
        derived = SG_PUBLIC_HOLIDAYS - _GAZETTED_HOLIDAYS
        self.assertEqual(len(derived), len(sunday_holidays),
                         f"In-lieu count ({len(derived)}) != Sunday holiday count ({len(sunday_holidays)})")


if __name__ == "__main__":
    unittest.main()
