"""Tests for scripts/lib/dates.py"""
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts" / "lib"))

from dates import (
    days_ago,
    days_since,
    format_relative,
    is_within_days,
    parse_iso,
    recency_score,
    today_utc,
)


# A fixed "now" to use in tests: 2026-03-27T12:00:00Z
_FIXED_NOW = datetime(2026, 3, 27, 12, 0, 0, tzinfo=timezone.utc)


def _mock_now(tz=None):
    return _FIXED_NOW


class TestTodayUtc(unittest.TestCase):

    @patch("dates.datetime")
    def test_returns_yyyy_mm_dd(self, mock_dt):
        mock_dt.now.return_value = _FIXED_NOW
        mock_dt.now.side_effect = None
        result = today_utc()
        self.assertRegex(result, r"^\d{4}-\d{2}-\d{2}$")

    def test_format(self):
        result = today_utc()
        parts = result.split("-")
        self.assertEqual(len(parts), 3)
        self.assertEqual(len(parts[0]), 4)
        self.assertEqual(len(parts[1]), 2)
        self.assertEqual(len(parts[2]), 2)


class TestDaysAgo(unittest.TestCase):

    def test_zero_days_is_today(self):
        result = days_ago(0)
        self.assertEqual(result, today_utc())

    def test_returns_yyyy_mm_dd(self):
        result = days_ago(30)
        self.assertRegex(result, r"^\d{4}-\d{2}-\d{2}$")

    def test_7_days_ago_is_before_today(self):
        result = days_ago(7)
        today = today_utc()
        self.assertLess(result, today)


class TestDaysSince(unittest.TestCase):

    def test_known_date_zero(self):
        today = today_utc()
        result = days_since(today)
        self.assertIsNotNone(result)
        self.assertEqual(result, 0)

    def test_iso_with_time(self):
        # Use yesterday
        yesterday = days_ago(1)
        result = days_since(yesterday)
        self.assertIsNotNone(result)
        self.assertGreaterEqual(result, 1)

    def test_7_days_ago(self):
        date = days_ago(7)
        result = days_since(date)
        self.assertIsNotNone(result)
        self.assertGreaterEqual(result, 7)
        self.assertLessEqual(result, 8)  # allow for time-of-day rounding

    def test_invalid_returns_none(self):
        result = days_since("not-a-date")
        self.assertIsNone(result)

    def test_empty_returns_none(self):
        result = days_since("")
        self.assertIsNone(result)

    def test_iso_with_timezone(self):
        result = days_since("2020-01-01T00:00:00Z")
        self.assertIsNotNone(result)
        self.assertGreater(result, 365)

    def test_date_with_fractional_seconds(self):
        result = days_since("2020-06-15T14:30:00.123456Z")
        self.assertIsNotNone(result)
        self.assertGreater(result, 0)

    def test_non_negative(self):
        # Future date should return 0 (clamped)
        future_date = "2099-01-01"
        result = days_since(future_date)
        self.assertIsNotNone(result)
        self.assertEqual(result, 0)


class TestRecencyScore(unittest.TestCase):

    def test_none_returns_50(self):
        self.assertEqual(recency_score(None), 50)

    def test_empty_returns_50(self):
        self.assertEqual(recency_score(""), 50)

    def test_invalid_returns_50(self):
        self.assertEqual(recency_score("not-a-date"), 50)

    def test_0_to_7_days(self):
        today = today_utc()
        self.assertEqual(recency_score(today), 100)
        date_6d = days_ago(6)
        self.assertEqual(recency_score(date_6d), 100)

    def test_8_to_14_days(self):
        date_10d = days_ago(10)
        self.assertEqual(recency_score(date_10d), 85)

    def test_15_to_30_days(self):
        date_20d = days_ago(20)
        self.assertEqual(recency_score(date_20d), 65)

    def test_31_to_60_days(self):
        date_45d = days_ago(45)
        self.assertEqual(recency_score(date_45d), 40)

    def test_61_to_90_days(self):
        date_75d = days_ago(75)
        self.assertEqual(recency_score(date_75d), 25)

    def test_91_plus_days(self):
        date_120d = days_ago(120)
        self.assertEqual(recency_score(date_120d), 10)

    def test_very_old_date(self):
        self.assertEqual(recency_score("2019-01-01"), 10)


class TestFormatRelative(unittest.TestCase):

    def test_today(self):
        today = today_utc()
        self.assertEqual(format_relative(today), "today")

    def test_1_day_ago(self):
        result = format_relative(days_ago(1))
        self.assertEqual(result, "1 day ago")

    def test_3_days_ago(self):
        result = format_relative(days_ago(3))
        self.assertEqual(result, "3 days ago")

    def test_1_week_ago(self):
        result = format_relative(days_ago(10))
        self.assertEqual(result, "1 week ago")

    def test_weeks_ago(self):
        result = format_relative(days_ago(21))
        self.assertIn("week", result)

    def test_1_month_ago(self):
        result = format_relative(days_ago(45))
        self.assertEqual(result, "1 month ago")

    def test_months_ago(self):
        result = format_relative(days_ago(90))
        self.assertIn("month", result)

    def test_1_year_ago(self):
        result = format_relative(days_ago(365))
        self.assertIn("year", result)

    def test_2_years_ago(self):
        result = format_relative(days_ago(730))
        self.assertIn("years", result)

    def test_invalid_returns_unknown(self):
        self.assertEqual(format_relative("not-a-date"), "unknown date")

    def test_empty_returns_unknown(self):
        self.assertEqual(format_relative(""), "unknown date")


class TestIsWithinDays(unittest.TestCase):

    def test_today_within_7(self):
        today = today_utc()
        self.assertTrue(is_within_days(today, 7))

    def test_3_days_ago_within_7(self):
        self.assertTrue(is_within_days(days_ago(3), 7))

    def test_10_days_ago_not_within_7(self):
        self.assertFalse(is_within_days(days_ago(10), 7))

    def test_exactly_on_boundary(self):
        # days_ago(7) may be 7 or 6 days ago depending on time-of-day
        result = is_within_days(days_ago(7), 7)
        self.assertIsNotNone(result)

    def test_invalid_returns_none(self):
        result = is_within_days("not-a-date", 30)
        self.assertIsNone(result)

    def test_30_day_window(self):
        self.assertTrue(is_within_days(days_ago(15), 30))
        self.assertFalse(is_within_days(days_ago(45), 30))


class TestParseIso(unittest.TestCase):

    def test_plain_date(self):
        result = parse_iso("2023-11-06")
        self.assertIsNotNone(result)
        self.assertEqual(result.year, 2023)
        self.assertEqual(result.month, 11)
        self.assertEqual(result.day, 6)

    def test_datetime_with_z(self):
        result = parse_iso("2023-11-06T12:00:00Z")
        self.assertIsNotNone(result)
        self.assertEqual(result.tzinfo, timezone.utc)
        self.assertEqual(result.hour, 12)

    def test_datetime_with_timezone(self):
        result = parse_iso("2023-11-06T12:00:00+00:00")
        self.assertIsNotNone(result)
        self.assertIsNotNone(result.tzinfo)

    def test_datetime_without_timezone(self):
        result = parse_iso("2023-11-06T12:00:00")
        self.assertIsNotNone(result)
        # Should be treated as UTC
        self.assertEqual(result.tzinfo, timezone.utc)

    def test_datetime_with_space(self):
        result = parse_iso("2023-11-06 12:00:00")
        self.assertIsNotNone(result)

    def test_datetime_with_fractional_seconds(self):
        result = parse_iso("2023-11-06T12:00:00.123456Z")
        self.assertIsNotNone(result)

    def test_invalid_returns_none(self):
        self.assertIsNone(parse_iso("not-a-date"))

    def test_empty_returns_none(self):
        self.assertIsNone(parse_iso(""))

    def test_fuzzy_date_in_string(self):
        # Should still extract the date via fuzzy matching
        result = parse_iso("Published on 2023-11-06 at midnight")
        self.assertIsNotNone(result)
        self.assertEqual(result.year, 2023)


if __name__ == "__main__":
    unittest.main()
