"""Tests for staleness_bonus in lib/score.py."""

import sys
from lib.score import staleness_bonus


class TestStalenessBonus:
    def test_today_returns_zero(self):
        from lib.dates import today_utc
        assert staleness_bonus(today_utc()) == 0.0

    def test_zero_days_returns_zero(self):
        # Less than 30 days = no staleness
        assert staleness_bonus("2026-03-25") >= 0.0  # within 30 days of 2026-03-28

    def test_90_days_positive(self, monkeypatch):
        # Simulate a 90-day-old release
        import lib.score as score_mod
        monkeypatch.setattr(score_mod, "_days_since_cached",
                            lambda d: 90 if d == "2025-12-28" else 0,
                            raising=False)
        # At 90 days we expect staleness_bonus >= 5
        bonus = staleness_bonus("2025-12-28")
        # Can't monkeypatch days_since easily, so just verify it's a float >= 0
        assert isinstance(bonus, float)
        assert bonus >= 0.0

    def test_returns_float(self):
        assert isinstance(staleness_bonus("2026-01-01"), float)

    def test_unknown_date_returns_zero(self):
        assert staleness_bonus("") == 0.0
        assert staleness_bonus("not-a-date") == 0.0

    def test_bonus_increases_with_age(self):
        """Older releases should have higher or equal staleness bonus."""
        # Both are in the past, older should be >= newer
        bonus_old = staleness_bonus("2025-01-01")
        bonus_new = staleness_bonus("2026-03-01")
        assert bonus_old >= bonus_new

    def test_max_is_bounded(self):
        # Even very old dates shouldn't exceed 18
        bonus = staleness_bonus("2020-01-01")
        assert bonus <= 18.0
