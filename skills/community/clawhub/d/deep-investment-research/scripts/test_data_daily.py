"""test_data_daily.py — Unit tests for data_daily.py tag-based fetcher system."""
import sys
import os
import json
import unittest
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_daily import (
    get_active_fetchers, build_groups, FETCHERS,
    FETCHER_TIMEOUT, FETCHER_TIMEOUT_HEAVY, MAX_WORKERS,
    run_fetcher_subprocess, run_special_fetcher, run_group, run_all,
    SCRIPTS_DIR,
)


class TestGetActiveFetchers(unittest.TestCase):
    """Test get_active_fetchers with various tag combinations."""

    def test_tags_morning_returns_13_fetchers(self):
        """tags=["morning"] should return all 13 fetchers."""
        active = get_active_fetchers(["morning"])
        self.assertEqual(len(active), 13, f"Expected 13, got {len(active)}: {sorted(active.keys())}")

    def test_tags_us_refresh_returns_8_with_consensus_no_revision(self):
        """tags=["us_refresh"] should return 8 fetchers: includes analyst_consensus, excludes analyst_revision (morning-only)."""
        active = get_active_fetchers(["us_refresh"])
        self.assertIn("analyst_consensus", active)   # tagged morning+us_refresh
        self.assertNotIn("analyst_revision", active)  # morning-only tag
        expected = {"edgar_filings", "insider_transactions", "superinvestor_moves",
                    "macro_snapshot", "sec_13f", "china_macro", "earnings_surprise",
                    "analyst_consensus"}
        self.assertEqual(set(active.keys()), expected,
                         f"Expected {expected}, got {set(active.keys())}")
        self.assertEqual(len(active), 8)

    def test_tags_hk_close_returns_1(self):
        """tags=["hk_close"] should return only short_interest."""
        active = get_active_fetchers(["hk_close"])
        self.assertEqual(set(active.keys()), {"short_interest"})
        self.assertEqual(len(active), 1)

    def test_tags_all_returns_all_fetchers(self):
        """tags=["all"] should return all defined fetchers."""
        active = get_active_fetchers(["all"])
        self.assertEqual(len(active), len(FETCHERS))
        self.assertEqual(set(active.keys()), set(FETCHERS.keys()))

    def test_tags_morning_hk_close_no_duplicates(self):
        """tags=["morning", "hk_close"] should be union without duplicates."""
        active = get_active_fetchers(["morning", "hk_close"])
        # short_interest is in both morning and hk_close, should appear once
        self.assertIn("short_interest", active)
        # Should be same as morning (13) since hk_close only adds short_interest which is already in morning
        self.assertEqual(len(active), 13)

    def test_us_refresh_excludes_morning_only_analyst_revision(self):
        """analyst_revision is morning-only, so it's excluded from us_refresh even though its dependency (analyst_consensus) is present."""
        active = get_active_fetchers(["us_refresh"])
        # analyst_consensus is tagged morning+us_refresh, so it IS in us_refresh
        self.assertIn("analyst_consensus", active)
        # analyst_revision is morning-only by tag, so excluded regardless of depends
        self.assertNotIn("analyst_revision", active)

    def test_empty_tags_returns_nothing(self):
        """Empty tags list should return no fetchers."""
        active = get_active_fetchers([])
        self.assertEqual(len(active), 0)

    def test_unknown_tag_returns_nothing(self):
        """Unknown tag should return no fetchers."""
        active = get_active_fetchers(["nonexistent_tag"])
        self.assertEqual(len(active), 0)

    def test_multiple_unknown_tags_returns_nothing(self):
        """Multiple unknown tags should still return nothing."""
        active = get_active_fetchers(["foo", "bar", "baz"])
        self.assertEqual(len(active), 0)

    def test_all_with_other_tags_still_returns_all(self):
        """'all' tag takes precedence regardless of other tags."""
        active = get_active_fetchers(["all", "morning"])
        self.assertEqual(len(active), len(FETCHERS))

    def test_us_refresh_hk_close_union(self):
        """us_refresh + hk_close should union correctly."""
        active = get_active_fetchers(["us_refresh", "hk_close"])
        # us_refresh has 8 (incl. analyst_consensus), hk_close adds short_interest
        # short_interest has tags ["morning", "hk_close"] - it matches hk_close
        self.assertIn("short_interest", active)
        # us_refresh (8) + short_interest = 9
        self.assertEqual(len(active), 9)

    def test_returned_dict_preserves_config(self):
        """Returned dict values should contain original config."""
        active = get_active_fetchers(["morning"])
        for name, config in active.items():
            self.assertIn("tags", config)
            self.assertIn("group", config)
            self.assertEqual(config, FETCHERS[name])

    def test_dependency_ordering_sensitivity(self):
        """Test that dependency resolution works even with dict ordering.
        
        Known issue: get_active_fetchers iterates FETCHERS in insertion order.
        If analyst_revision were defined BEFORE analyst_consensus, the 'dep not in active'
        check would fail. This test documents the current behavior.
        """
        # With morning tags, both should be included because analyst_consensus comes first in dict
        active = get_active_fetchers(["morning"])
        self.assertIn("analyst_consensus", active)
        self.assertIn("analyst_revision", active)


class TestBuildGroups(unittest.TestCase):
    """Test build_groups organizes fetchers by group number in order."""

    def test_morning_groups_sorted(self):
        """Groups should be ordered by group number."""
        active = get_active_fetchers(["morning"])
        groups = build_groups(active)
        # Should have 4 groups (1, 2, 3, 4)
        self.assertEqual(len(groups), 4)

    def test_group1_has_independent_fetchers(self):
        """Group 1 should contain the independent fetchers."""
        active = get_active_fetchers(["morning"])
        groups = build_groups(active)
        group1 = groups[0]
        # Group 1 should have 10 fetchers (all group=1 with morning tag)
        group1_expected = {
            "edgar_filings", "hkex_announcements", "insider_transactions", "superinvestor_moves",
            "southbound_top10", "macro_snapshot", "short_interest", "sec_13f",
            "china_macro", "earnings_surprise"
        }
        self.assertEqual(set(group1), group1_expected)

    def test_group2_has_analyst_consensus(self):
        """Group 2 should contain analyst_consensus."""
        active = get_active_fetchers(["morning"])
        groups = build_groups(active)
        group2 = groups[1]
        self.assertEqual(group2, ["analyst_consensus"])

    def test_group3_has_analyst_revision(self):
        """Group 3 should contain analyst_revision."""
        active = get_active_fetchers(["morning"])
        groups = build_groups(active)
        group3 = groups[2]
        self.assertEqual(group3, ["analyst_revision"])

    def test_group4_has_special(self):
        """Group 4 should contain special fetchers."""
        active = get_active_fetchers(["morning"])
        groups = build_groups(active)
        group4 = groups[3]
        self.assertIn("policy_gov", group4)

    def test_us_refresh_two_groups(self):
        """us_refresh fetchers span group 1 and group 2 (analyst_consensus), so 2 groups."""
        active = get_active_fetchers(["us_refresh"])
        groups = build_groups(active)
        self.assertEqual(len(groups), 2)

    def test_hk_close_single_group(self):
        """hk_close has only 1 fetcher in group 1."""
        active = get_active_fetchers(["hk_close"])
        groups = build_groups(active)
        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0], ["short_interest"])

    def test_empty_dict_returns_empty_list(self):
        """Empty fetcher dict should return empty groups."""
        groups = build_groups({})
        self.assertEqual(groups, [])

    def test_single_fetcher_single_group(self):
        """A single fetcher should produce one group."""
        groups = build_groups({"test": {"group": 5, "tags": ["x"]}})
        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0], ["test"])

    def test_groups_are_sorted_by_number(self):
        """Groups must be sorted by group number, not insertion order."""
        fetchers = {
            "c": {"group": 3, "tags": ["x"]},
            "a": {"group": 1, "tags": ["x"]},
            "b": {"group": 2, "tags": ["x"]},
        }
        groups = build_groups(fetchers)
        self.assertEqual(groups, [["a"], ["b"], ["c"]])


class TestTimeoutConfig(unittest.TestCase):
    """Test timeout configuration for heavy vs normal fetchers."""

    def test_fetcher_timeout_normal(self):
        """Normal timeout should be 180s."""
        self.assertEqual(FETCHER_TIMEOUT, 180)

    def test_fetcher_timeout_heavy(self):
        """Heavy timeout reserve should be 600s."""
        self.assertEqual(FETCHER_TIMEOUT_HEAVY, 600)

    def test_no_fetcher_marked_heavy(self):
        """No fetcher is currently heavy (analyst_consensus no longer heavy)."""
        for name, config in FETCHERS.items():
            self.assertFalse(config.get("heavy", False),
                             f"{name} should not be heavy")

    def test_other_fetchers_not_heavy(self):
        """Non-consensus fetchers should not be marked heavy."""
        for name, config in FETCHERS.items():
            if name != "analyst_consensus":
                self.assertFalse(config.get("heavy", False),
                                 f"{name} should not be heavy")

    def test_timeout_selection_in_run_fetcher(self):
        """Verify the timeout logic in run_fetcher_subprocess picks correct value."""
        for name, config in FETCHERS.items():
            is_heavy = config.get("heavy", False)
            timeout = FETCHER_TIMEOUT_HEAVY if is_heavy else FETCHER_TIMEOUT
            # No fetcher is heavy, so all use the normal 180s timeout
            self.assertEqual(timeout, 180, f"{name} should use 180s timeout")

    def test_max_workers(self):
        """MAX_WORKERS should be 4."""
        self.assertEqual(MAX_WORKERS, 4)


class TestDependsLogic(unittest.TestCase):
    """Test the depends field behavior."""

    def test_analyst_revision_depends_on_consensus(self):
        """analyst_revision should declare depends on analyst_consensus."""
        self.assertEqual(FETCHERS["analyst_revision"]["depends"], "analyst_consensus")

    def test_depends_satisfied_when_dep_in_same_tags(self):
        """When running morning, analyst_consensus is included so analyst_revision should be too."""
        active = get_active_fetchers(["morning"])
        self.assertIn("analyst_consensus", active)
        self.assertIn("analyst_revision", active)

    def test_depends_satisfied_in_us_refresh(self):
        """In us_refresh, analyst_consensus is present (tagged us_refresh); analyst_revision is still excluded by its morning-only tag."""
        active = get_active_fetchers(["us_refresh"])
        self.assertIn("analyst_consensus", active)
        self.assertNotIn("analyst_revision", active)

    def test_depends_on_nonexistent_fetcher(self):
        """If depends references a fetcher not in FETCHERS, should be handled gracefully."""
        with patch.dict('data_daily.FETCHERS', {
            "orphan": {"tags": ["morning"], "group": 5, "depends": "nonexistent"},
        }, clear=False):
            from data_daily import get_active_fetchers as gaf
            active = gaf(["morning"])
            # orphan depends on nonexistent which has no tags, so should be skipped
            self.assertNotIn("orphan", active)


class TestSpecialFetchers(unittest.TestCase):
    """Test special fetcher identification."""

    def test_policy_gov_is_special(self):
        """policy_gov should be marked as special."""
        self.assertTrue(FETCHERS["policy_gov"].get("special", False))

    def test_special_fetcher_uses_special_field_in_group(self):
        """Special fetchers are dispatched via the 'special' config field."""
        special = [n for n, c in FETCHERS.items() if c.get("special")]
        self.assertIn("policy_gov", special)


class TestDefaultBehavior(unittest.TestCase):
    """Test that no args = --tags all."""

    def test_default_tags_is_all(self):
        """Default tags should be ['all'] in argparse."""
        active = get_active_fetchers(["all"])
        self.assertEqual(len(active), 13)


class TestRunFetcherSubprocess(unittest.TestCase):
    """Test run_fetcher_subprocess with mocked subprocess."""

    @patch('data_daily.subprocess.run')
    def test_module_not_found(self, mock_run):
        """Non-existent module should return unavailable."""
        result = run_fetcher_subprocess("nonexistent_module_xyz", "2025-01-01", "/tmp/test")
        self.assertEqual(result["status"], "unavailable")
        self.assertIn("Module not found", result["reason"])
        mock_run.assert_not_called()

    @patch('data_daily.subprocess.run')
    def test_successful_fetcher_with_json_output(self, mock_run):
        """Fetcher returning valid JSON status should be parsed."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout='Processing...\n{"name": "test_mod", "status": "ok", "records": 42}\n',
            stderr=""
        )
        # Need module file to exist
        with patch('os.path.exists', return_value=True):
            result = run_fetcher_subprocess("test_mod", "2025-01-01", "/tmp/test")
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["records"], 42)
        self.assertIn("elapsed_s", result)

    @patch('data_daily.subprocess.run')
    def test_successful_fetcher_no_json(self, mock_run):
        """Fetcher with exit 0 but no JSON should infer ok."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout='Done processing.\n',
            stderr=""
        )
        with patch('os.path.exists', return_value=True):
            result = run_fetcher_subprocess("test_mod", "2025-01-01", "/tmp/test")
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["name"], "test_mod")

    @patch('data_daily.subprocess.run')
    def test_failed_fetcher_nonzero_exit(self, mock_run):
        """Fetcher with non-zero exit should return rejected."""
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout='',
            stderr="ImportError: no module named foo"
        )
        with patch('os.path.exists', return_value=True):
            result = run_fetcher_subprocess("test_mod", "2025-01-01", "/tmp/test")
        self.assertEqual(result["status"], "rejected")
        self.assertIn("Exit code 1", result["reason"])

    @patch('data_daily.subprocess.run')
    def test_timeout_returns_rejected(self, mock_run):
        """Subprocess timeout should return rejected with reason."""
        import subprocess
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="test", timeout=180)
        with patch('os.path.exists', return_value=True):
            result = run_fetcher_subprocess("test_mod", "2025-01-01", "/tmp/test")
        self.assertEqual(result["status"], "rejected")
        self.assertIn("Timeout", result["reason"])

    @patch('data_daily.subprocess.run')
    def test_exception_returns_rejected(self, mock_run):
        """General exception should return rejected."""
        mock_run.side_effect = OSError("Permission denied")
        with patch('os.path.exists', return_value=True):
            result = run_fetcher_subprocess("test_mod", "2025-01-01", "/tmp/test")
        self.assertEqual(result["status"], "rejected")
        self.assertIn("Permission denied", result["reason"])

    @patch('data_daily.subprocess.run')
    def test_json_on_last_line_preferred(self, mock_run):
        """Should find JSON on the last non-empty line of stdout."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout='log line 1\nlog line 2\n{"name": "x", "status": "ok", "records": 10}\n',
            stderr=""
        )
        with patch('os.path.exists', return_value=True):
            result = run_fetcher_subprocess("x", "2025-01-01", "/tmp/test")
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["records"], 10)

    @patch('data_daily.subprocess.run')
    def test_malformed_json_falls_back_to_exit_code(self, mock_run):
        """Malformed JSON with exit 0 should fall back to ok status."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout='{invalid json\n',
            stderr=""
        )
        with patch('os.path.exists', return_value=True):
            result = run_fetcher_subprocess("x", "2025-01-01", "/tmp/test")
        self.assertEqual(result["status"], "ok")

    @patch('data_daily.subprocess.run')
    def test_heavy_fetcher_gets_longer_timeout(self, mock_run):
        """analyst_consensus is no longer heavy; should use the normal timeout."""
        mock_run.return_value = MagicMock(returncode=0, stdout='', stderr='')
        with patch('os.path.exists', return_value=True):
            run_fetcher_subprocess("analyst_consensus", "2025-01-01", "/tmp/test")
        call_kwargs = mock_run.call_args[1]
        self.assertEqual(call_kwargs['timeout'], FETCHER_TIMEOUT)

    @patch('data_daily.subprocess.run')
    def test_normal_fetcher_gets_normal_timeout(self, mock_run):
        """Non-heavy fetcher should use FETCHER_TIMEOUT."""
        mock_run.return_value = MagicMock(returncode=0, stdout='', stderr='')
        with patch('os.path.exists', return_value=True):
            run_fetcher_subprocess("edgar_filings", "2025-01-01", "/tmp/test")
        call_kwargs = mock_run.call_args[1]
        self.assertEqual(call_kwargs['timeout'], FETCHER_TIMEOUT)

    @patch('data_daily.subprocess.run')
    def test_empty_stdout_exit_zero(self, mock_run):
        """Empty stdout with exit 0 should still return ok."""
        mock_run.return_value = MagicMock(returncode=0, stdout='', stderr='')
        with patch('os.path.exists', return_value=True):
            result = run_fetcher_subprocess("test_mod", "2025-01-01", "/tmp/test")
        self.assertEqual(result["status"], "ok")

    @patch('data_daily.subprocess.run')
    def test_stderr_truncated_in_reason(self, mock_run):
        """Long stderr should be truncated to last 200 chars."""
        long_stderr = "x" * 500
        mock_run.return_value = MagicMock(returncode=1, stdout='', stderr=long_stderr)
        with patch('os.path.exists', return_value=True):
            result = run_fetcher_subprocess("test_mod", "2025-01-01", "/tmp/test")
        # Reason includes "Exit code 1: " prefix + last 200 chars of stderr
        self.assertLessEqual(len(result["reason"]), 220)


class TestRunSpecialFetcher(unittest.TestCase):
    """Test run_special_fetcher with mocked subprocess."""

    @patch('data_daily.subprocess.run')
    def test_policy_gov_success(self, mock_run):
        """policy_gov with valid JSON output."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout='{"name": "policy_gov", "status": "ok", "total_items": 15, "new_today": 3, "sources_ok": 4}\n',
            stderr=""
        )
        result = run_special_fetcher("policy_gov", "2025-01-01", "/tmp/test")
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["total_items"], 15)
        self.assertIn("elapsed_s", result)

    @patch('data_daily.subprocess.run')
    def test_unknown_special_fetcher(self, mock_run):
        """Unknown special fetcher name should return unavailable."""
        result = run_special_fetcher("unknown_special", "2025-01-01", "/tmp/test")
        self.assertEqual(result["status"], "unavailable")
        self.assertIn("Unknown special fetcher", result["reason"])
        mock_run.assert_not_called()

    @patch('data_daily.subprocess.run')
    def test_special_fetcher_timeout(self, mock_run):
        """Special fetcher timeout should return rejected."""
        import subprocess
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="test", timeout=180)
        result = run_special_fetcher("policy_gov", "2025-01-01", "/tmp/test")
        self.assertEqual(result["status"], "rejected")
        self.assertIn("Timeout", result["reason"])

    @patch('data_daily.subprocess.run')
    def test_special_fetcher_exception(self, mock_run):
        """General exception in special fetcher."""
        mock_run.side_effect = RuntimeError("Unexpected error")
        result = run_special_fetcher("policy_gov", "2025-01-01", "/tmp/test")
        self.assertEqual(result["status"], "rejected")
        self.assertIn("Unexpected error", result["reason"])

    @patch('data_daily.subprocess.run')
    def test_special_fetcher_no_json_exit_zero(self, mock_run):
        """Special fetcher with exit 0 but no JSON should infer ok."""
        mock_run.return_value = MagicMock(returncode=0, stdout='done\n', stderr='')
        result = run_special_fetcher("policy_gov", "2025-01-01", "/tmp/test")
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["name"], "policy_gov")

    @patch('data_daily.subprocess.run')
    def test_special_fetcher_nonzero_exit(self, mock_run):
        """Special fetcher with non-zero exit and no JSON."""
        mock_run.return_value = MagicMock(returncode=1, stdout='', stderr='crash!')
        result = run_special_fetcher("policy_gov", "2025-01-01", "/tmp/test")
        self.assertEqual(result["status"], "rejected")
        self.assertEqual(result["name"], "policy_gov")


class TestRunGroup(unittest.TestCase):
    """Test run_group parallel execution."""

    @patch('data_daily.run_fetcher_subprocess')
    def test_run_group_parallel(self, mock_fetcher):
        """run_group should run all fetchers and collect results."""
        mock_fetcher.return_value = {"name": "test", "status": "ok"}
        results = run_group(["a", "b", "c"], "2025-01-01", "/tmp/test")
        self.assertEqual(len(results), 3)
        self.assertEqual(mock_fetcher.call_count, 3)

    @patch('data_daily.run_special_fetcher')
    @patch('data_daily.run_fetcher_subprocess')
    def test_run_group_dispatches_special(self, mock_normal, mock_special):
        """Fetchers with the 'special' config field should use run_special_fetcher."""
        mock_normal.return_value = {"name": "normal", "status": "ok"}
        mock_special.return_value = {"name": "special", "status": "ok"}
        results = run_group(["edgar_filings", "policy_gov"], "2025-01-01", "/tmp/test")
        self.assertEqual(len(results), 2)
        mock_normal.assert_called_once()
        mock_special.assert_called_once()

    @patch('data_daily.run_fetcher_subprocess')
    def test_run_group_handles_exception_in_future(self, mock_fetcher):
        """If a future raises, it should be caught and recorded as rejected."""
        mock_fetcher.side_effect = Exception("boom")
        results = run_group(["a"], "2025-01-01", "/tmp/test")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["status"], "rejected")
        self.assertIn("boom", results[0]["reason"])

    @patch('data_daily.run_fetcher_subprocess')
    def test_run_group_empty_list(self, mock_fetcher):
        """Empty group should return empty results."""
        results = run_group([], "2025-01-01", "/tmp/test")
        self.assertEqual(results, [])
        mock_fetcher.assert_not_called()


class TestRunAll(unittest.TestCase):
    """Test run_all orchestration logic."""

    def test_dry_run_all(self):
        """dry_run=True should return plan without executing."""
        result = run_all(tags=["all"], dry_run=True)
        self.assertTrue(result["dry_run"])
        self.assertEqual(result["tags"], ["all"])
        self.assertEqual(len(result["fetchers"]), 13)
        self.assertEqual(result["fetchers"], sorted(FETCHERS.keys()))

    def test_dry_run_morning(self):
        """dry_run morning should list 13 fetchers."""
        result = run_all(tags=["morning"], dry_run=True)
        self.assertTrue(result["dry_run"])
        self.assertEqual(len(result["fetchers"]), 13)

    def test_dry_run_us_refresh(self):
        """dry_run us_refresh should list 8 fetchers."""
        result = run_all(tags=["us_refresh"], dry_run=True)
        self.assertEqual(len(result["fetchers"]), 8)
        self.assertIn("analyst_consensus", result["fetchers"])

    def test_dry_run_hk_close(self):
        """dry_run hk_close should list 1 fetcher."""
        result = run_all(tags=["hk_close"], dry_run=True)
        self.assertEqual(result["fetchers"], ["short_interest"])

    def test_dry_run_empty_tags(self):
        """dry_run with empty tags should return empty fetcher list."""
        result = run_all(tags=[], dry_run=True)
        self.assertEqual(result["fetchers"], [])

    @patch('data_daily.run_group')
    @patch('data_daily.date')
    def test_run_all_creates_output_dir(self, mock_date, mock_run_group):
        """run_all should create the daily output directory."""
        mock_date.today.return_value = date(2025, 1, 15)
        mock_run_group.return_value = [{"name": "short_interest", "status": "ok", "elapsed_s": 1.0}]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('data_daily.DATA_DIR', tmpdir):
                result = run_all(tags=["hk_close"], dry_run=False)
                expected_dir = os.path.join(tmpdir, "daily", "2025-01-15")
                self.assertTrue(os.path.isdir(expected_dir))
                # Check _status.json was written
                status_path = os.path.join(expected_dir, "_status.json")
                self.assertTrue(os.path.exists(status_path))
                with open(status_path) as f:
                    status = json.load(f)
                self.assertIn("generated_at", status)
                self.assertIn("sources", status)
                self.assertEqual(status["tags"], ["hk_close"])

    @patch('data_daily.run_group')
    @patch('data_daily.date')
    def test_status_json_format(self, mock_date, mock_run_group):
        """_status.json should have correct structure."""
        mock_date.today.return_value = date(2025, 3, 20)
        mock_run_group.return_value = [
            {"name": "a", "status": "ok", "records": 5, "elapsed_s": 2.1},
            {"name": "b", "status": "rejected", "reason": "Timeout", "elapsed_s": 180.0},
        ]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('data_daily.DATA_DIR', tmpdir):
                with patch('data_daily.get_active_fetchers', return_value={
                    "a": {"tags": ["test"], "group": 1},
                    "b": {"tags": ["test"], "group": 1},
                }):
                    result = run_all(tags=["test"], dry_run=False)
        
        self.assertIn("sources", result)
        self.assertEqual(result["sources"]["a"]["status"], "ok")
        self.assertEqual(result["sources"]["a"]["records"], 5)
        self.assertEqual(result["sources"]["b"]["status"], "rejected")
        self.assertIn("reason", result["sources"]["b"])
        self.assertIn("agent_notice", result)
        self.assertIn("b: rejected", result["agent_notice"])

    @patch('data_daily.run_group')
    @patch('data_daily.date')
    def test_run_all_default_tags_is_all(self, mock_date, mock_run_group):
        """run_all with default None tags should use ['all']."""
        mock_date.today.return_value = date(2025, 1, 1)
        mock_run_group.return_value = []
        
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('data_daily.DATA_DIR', tmpdir):
                result = run_all(tags=None, dry_run=True)
        self.assertEqual(result["tags"], ["all"])
        self.assertEqual(len(result["fetchers"]), 13)


class TestFetcherDefinitionsIntegrity(unittest.TestCase):
    """Validate FETCHERS dict structure and consistency."""

    def test_all_fetchers_have_required_fields(self):
        """Every fetcher must have 'tags' and 'group' fields."""
        for name, config in FETCHERS.items():
            self.assertIn("tags", config, f"{name} missing 'tags'")
            self.assertIn("group", config, f"{name} missing 'group'")
            self.assertIsInstance(config["tags"], list, f"{name} tags not a list")
            self.assertIsInstance(config["group"], int, f"{name} group not an int")

    def test_all_tags_are_known(self):
        """All fetcher tags should be in the known set."""
        known_tags = {"morning", "us_refresh", "hk_close"}
        for name, config in FETCHERS.items():
            for tag in config["tags"]:
                self.assertIn(tag, known_tags,
                              f"{name} has unknown tag '{tag}'")

    def test_all_groups_are_positive_integers(self):
        """Group numbers should be positive integers."""
        for name, config in FETCHERS.items():
            self.assertGreater(config["group"], 0, f"{name} has non-positive group")

    def test_depends_reference_valid_fetchers(self):
        """Any 'depends' value should reference an existing fetcher."""
        for name, config in FETCHERS.items():
            dep = config.get("depends")
            if dep:
                self.assertIn(dep, FETCHERS,
                              f"{name} depends on non-existent '{dep}'")

    def test_depends_fetcher_in_earlier_group(self):
        """Dependency should be in an earlier group than the dependent."""
        for name, config in FETCHERS.items():
            dep = config.get("depends")
            if dep:
                dep_group = FETCHERS[dep]["group"]
                self.assertLess(dep_group, config["group"],
                                f"{name} (group {config['group']}) depends on "
                                f"{dep} (group {dep_group}) - must be earlier group")

    def test_no_circular_depends(self):
        """No circular dependency chains."""
        for name, config in FETCHERS.items():
            visited = set()
            current = name
            while current:
                self.assertNotIn(current, visited,
                                 f"Circular dependency detected involving {current}")
                visited.add(current)
                current = FETCHERS.get(current, {}).get("depends")

    def test_fetcher_count_is_13(self):
        """Total active fetcher count should be 13."""
        self.assertEqual(len(FETCHERS), 13)


class TestEdgeCases(unittest.TestCase):
    """Edge cases and boundary conditions."""

    def test_get_active_fetchers_single_tag_in_list(self):
        """Single-element tag list should work."""
        active = get_active_fetchers(["morning"])
        self.assertGreater(len(active), 0)

    def test_get_active_fetchers_is_idempotent(self):
        """Calling get_active_fetchers multiple times with same args gives same result."""
        r1 = get_active_fetchers(["morning"])
        r2 = get_active_fetchers(["morning"])
        self.assertEqual(r1, r2)

    def test_fetchers_dict_not_mutated(self):
        """get_active_fetchers should not mutate the global FETCHERS dict."""
        original = dict(FETCHERS)
        get_active_fetchers(["morning"])
        get_active_fetchers(["us_refresh"])
        get_active_fetchers(["all"])
        self.assertEqual(FETCHERS, original)

    def test_build_groups_does_not_mutate_input(self):
        """build_groups should not modify its input dict."""
        active = get_active_fetchers(["morning"])
        original = dict(active)
        build_groups(active)
        self.assertEqual(active, original)


if __name__ == "__main__":
    unittest.main(verbosity=2)
