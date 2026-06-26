"""Tests for tier_limits.py (version access control)."""
import pytest
import os
import tempfile
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from tier_limits import (
    Tier, check_tier, check_feature, has_feature,
    record_usage, get_usage_summary,
    TierLimitExceeded, FeatureNotAvailable,
    TIER_MONTHLY_ROWS, TIER_MAX_SOURCES, TIER_FEATURES,
    tier_display_name,
)

# Global state file counter for unique-per-class paths
_STATE_COUNTER = 0


def _fresh_state_path():
    global _STATE_COUNTER
    _STATE_COUNTER += 1
    return tempfile.gettempdir() + f"/dc_test_{_STATE_COUNTER}.json"


class TestHasFeature:
    def test_free_has_basic_dedup(self):
        assert has_feature(Tier.FREE, "basic_dedup") is True

    def test_free_no_fuzzy_join(self):
        assert has_feature(Tier.FREE, "fuzzy_join") is False

    def test_basic_has_multi_format(self):
        assert has_feature(Tier.BASIC, "multi_format") is True

    def test_std_has_smart_fill(self):
        assert has_feature(Tier.STD, "smart_fill") is True

    def test_pro_has_all(self):
        for feat in TIER_FEATURES[Tier.PRO]:
            assert has_feature(Tier.PRO, feat) is True


class TestCheckFeature:
    def test_pro_passes(self):
        check_feature(Tier.PRO, "fuzzy_join")  # no error

    def test_free_raises(self):
        with pytest.raises(FeatureNotAvailable) as exc:
            check_feature(Tier.FREE, "fuzzy_join")
        assert "fuzzy_join" in str(exc.value)

    def test_std_raises_for_bitable(self):
        with pytest.raises(FeatureNotAvailable):
            check_feature(Tier.STD, "bitable_output")


class TestCheckTierRows:
    """Row quota enforcement — isolated state per test."""

    def setup_method(self):
        self._old = os.environ.get("DATA_CLEANER_STATE_FILE")
        self._path = _fresh_state_path()
        os.environ["DATA_CLEANER_STATE_FILE"] = self._path
        # Start with empty state
        with open(self._path, "w") as f:
            json.dump({}, f)

    def teardown_method(self):
        Path(self._path).unlink(missing_ok=True)
        if self._old:
            os.environ["DATA_CLEANER_STATE_FILE"] = self._old
        elif "DATA_CLEANER_STATE_FILE" in os.environ:
            del os.environ["DATA_CLEANER_STATE_FILE"]

    def test_free_under_limit(self):
        check_tier(Tier.FREE, rows=30)  # no error

    def test_free_over_limit_raises(self):
        with pytest.raises(TierLimitExceeded) as exc:
            check_tier(Tier.FREE, rows=51)
        assert "每月限额 50 条" in str(exc.value)

    def test_pro_unlimited(self):
        check_tier(Tier.PRO, rows=100000)  # no error

    def test_basic_under_limit(self):
        check_tier(Tier.BASIC, rows=499)  # no error

    def test_basic_over_limit_raises(self):
        with pytest.raises(TierLimitExceeded):
            check_tier(Tier.BASIC, rows=501)


class TestCheckTierSources:
    """Data-source limit enforcement."""

    def setup_method(self):
        self._old = os.environ.get("DATA_CLEANER_STATE_FILE")
        self._path = _fresh_state_path()
        os.environ["DATA_CLEANER_STATE_FILE"] = self._path
        with open(self._path, "w") as f:
            json.dump({}, f)

    def teardown_method(self):
        Path(self._path).unlink(missing_ok=True)
        if self._old:
            os.environ["DATA_CLEANER_STATE_FILE"] = self._old
        elif "DATA_CLEANER_STATE_FILE" in os.environ:
            del os.environ["DATA_CLEANER_STATE_FILE"]

    def test_free_one_source(self):
        check_tier(Tier.FREE, sources=1)  # ok
        with pytest.raises(TierLimitExceeded):
            check_tier(Tier.FREE, sources=2)

    def test_basic_three_sources(self):
        check_tier(Tier.BASIC, sources=3)  # ok
        with pytest.raises(TierLimitExceeded):
            check_tier(Tier.BASIC, sources=4)


class TestCheckTierColumns:
    def setup_method(self):
        self._old = os.environ.get("DATA_CLEANER_STATE_FILE")
        self._path = _fresh_state_path()
        os.environ["DATA_CLEANER_STATE_FILE"] = self._path
        with open(self._path, "w") as f:
            json.dump({}, f)

    def teardown_method(self):
        Path(self._path).unlink(missing_ok=True)
        if self._old:
            os.environ["DATA_CLEANER_STATE_FILE"] = self._old
        elif "DATA_CLEANER_STATE_FILE" in os.environ:
            del os.environ["DATA_CLEANER_STATE_FILE"]

    def test_free_ten_columns(self):
        check_tier(Tier.FREE, columns=10)  # ok
        with pytest.raises(TierLimitExceeded):
            check_tier(Tier.FREE, columns=11)

    def test_pro_unlimited_columns(self):
        check_tier(Tier.PRO, columns=10000)  # ok


class TestRecordUsage:
    """Usage recording and monthly reset — isolated state per test."""

    def setup_method(self):
        self._old = os.environ.get("DATA_CLEANER_STATE_FILE")
        self._path = _fresh_state_path()
        os.environ["DATA_CLEANER_STATE_FILE"] = self._path
        with open(self._path, "w") as f:
            json.dump({}, f)

    def teardown_method(self):
        Path(self._path).unlink(missing_ok=True)
        if self._old:
            os.environ["DATA_CLEANER_STATE_FILE"] = self._old
        elif "DATA_CLEANER_STATE_FILE" in os.environ:
            del os.environ["DATA_CLEANER_STATE_FILE"]

    def test_records_and_accumulates(self):
        usage = record_usage(rows=10)
        assert usage["rows"] == 10

        usage2 = record_usage(rows=5)
        assert usage2["rows"] == 15  # cumulative

    def test_monthly_reset(self):
        # Pre-seed with a different month
        state = {"usage": {"2025-01": {"rows": 100}}}
        with open(self._path, "w") as f:
            json.dump(state, f)

        usage = record_usage(rows=10)
        assert usage["rows"] == 10  # new month key, not accumulated from old month


class TestTierDisplayName:
    def test_all_tiers(self):
        assert tier_display_name(Tier.FREE) == "免费版"
        assert tier_display_name(Tier.BASIC) == "基础版"
        assert tier_display_name(Tier.STD) == "标准版"
        assert tier_display_name(Tier.PRO) == "专业版"


class TestTierConstants:
    def test_free_monthly_limit(self):
        assert TIER_MONTHLY_ROWS[Tier.FREE] == 50

    def test_pro_monthly_limit_unlimited(self):
        assert TIER_MONTHLY_ROWS[Tier.PRO] == -1

    def test_pro_max_sources_unlimited(self):
        assert TIER_MAX_SOURCES[Tier.PRO] == -1
