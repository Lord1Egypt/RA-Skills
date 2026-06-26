#!/usr/bin/env python3
"""Tests for the OpenCLI Twitter backend."""

import json
import os
import inspect
import tempfile
import subprocess
import sys
import tempfile
import unittest
import importlib.util
from datetime import datetime
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import MagicMock, call, patch
from unittest.mock import mock_open
from urllib.error import HTTPError

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

spec = importlib.util.spec_from_file_location("fetch_twitter", SCRIPTS_DIR / "fetch-twitter.py")
fetch_twitter = importlib.util.module_from_spec(spec)
sys.modules["fetch_twitter"] = fetch_twitter
spec.loader.exec_module(fetch_twitter)

_FETCH_WITH_BACKEND_CHAIN_PARAMS = list(inspect.signature(fetch_twitter.fetch_with_backend_chain).parameters.keys())
_OPENCLI_AUTO_UPDATE_PARAM_INDEX = (
    _FETCH_WITH_BACKEND_CHAIN_PARAMS.index("opencli_auto_update")
    if "opencli_auto_update" in _FETCH_WITH_BACKEND_CHAIN_PARAMS
    else None
)


def _require_attr(module, name: str):
    value = getattr(module, name, None)
    if value is None:
        raise AssertionError(f"{module.__name__}.{name} must exist for OpenCLI update tests.")
    return value


def _read_opencli_auto_update_arg(mock_call):
    args, kwargs = mock_call
    if "opencli_auto_update" in kwargs:
        return kwargs["opencli_auto_update"]
    if _OPENCLI_AUTO_UPDATE_PARAM_INDEX is None:
        raise AssertionError("fetch_with_backend_chain does not accept opencli_auto_update")
    if len(args) <= _OPENCLI_AUTO_UPDATE_PARAM_INDEX:
        raise AssertionError(
            "fetch_with_backend_chain was called without expected opencli_auto_update positional arg"
        )
    return args[_OPENCLI_AUTO_UPDATE_PARAM_INDEX]


def _temp_opencli_state_path(stack: ExitStack) -> Path:
    temp_dir = stack.enter_context(tempfile.TemporaryDirectory())
    return Path(temp_dir) / "opencli-update-state.json"


def utc(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def http_error(code):
    return HTTPError("https://example.com", code, "error", {}, None)


def twitter_source():
    return {
        "id": "sama",
        "name": "Sam Altman",
        "handle": "sama",
        "topics": ["ai"],
        "priority": False,
    }


class TestOpenCliTweetNormalization(unittest.TestCase):
    def setUp(self):
        self.source = {
            "id": "sama-twitter",
            "type": "twitter",
            "name": "Sam Altman",
            "handle": "sama",
            "enabled": True,
            "priority": True,
            "topics": ["llm", "ai-agent"],
        }
        self.cutoff = utc("2026-05-08T00:00:00Z")

    def test_normalizes_opencli_tweet(self):
        record = {
            "id": "12345",
            "author": "sama",
            "text": "OpenCLI now powers this digest.",
            "created_at": "Fri May 08 04:03:02 +0000 2026",
            "likes": 10,
            "retweets": 2,
            "replies": 3,
            "views": 400,
            "url": "https://x.com/sama/status/12345",
            "is_retweet": False,
        }

        article = fetch_twitter.normalize_opencli_tweet(record, self.source, self.cutoff)

        self.assertEqual(article["title"], "OpenCLI now powers this digest.")
        self.assertEqual(article["link"], "https://x.com/sama/status/12345")
        self.assertEqual(article["date"], "2026-05-08T04:03:02+00:00")
        self.assertEqual(article["topics"], ["llm", "ai-agent"])
        self.assertEqual(article["tweet_id"], "12345")
        self.assertEqual(
            article["metrics"],
            {
                "like_count": 10,
                "retweet_count": 2,
                "reply_count": 3,
                "quote_count": 0,
                "impression_count": 400,
            },
        )

    def test_builds_link_and_defaults_metrics(self):
        record = {
            "id": "67890",
            "author": "sama",
            "text": "No metrics here.",
            "created_at": "2026-05-08T05:00:00Z",
            "is_retweet": False,
        }

        article = fetch_twitter.normalize_opencli_tweet(record, self.source, self.cutoff)

        self.assertEqual(article["link"], "https://x.com/sama/status/67890")
        self.assertEqual(
            article["metrics"],
            {
                "like_count": 0,
                "retweet_count": 0,
                "reply_count": 0,
                "quote_count": 0,
                "impression_count": 0,
            },
        )

    def test_skips_old_tweets(self):
        record = {
            "id": "old",
            "author": "sama",
            "text": "Old news.",
            "created_at": "2026-05-07T23:59:59Z",
            "is_retweet": False,
        }

        self.assertIsNone(fetch_twitter.normalize_opencli_tweet(record, self.source, self.cutoff))

    def test_skips_retweets(self):
        records = [
            {
                "id": "rt1",
                "author": "sama",
                "text": "A retweet.",
                "created_at": "2026-05-08T05:00:00Z",
                "is_retweet": True,
            },
            {
                "id": "rt2",
                "author": "sama",
                "text": "RT @openai: A retweet.",
                "created_at": "2026-05-08T05:00:00Z",
                "is_retweet": False,
            },
        ]

        for record in records:
            with self.subTest(record=record["id"]):
                self.assertIsNone(fetch_twitter.normalize_opencli_tweet(record, self.source, self.cutoff))

    def test_skips_malformed_records(self):
        records = [
            {"author": "sama", "text": "Missing ID", "created_at": "2026-05-08T05:00:00Z"},
            {"id": "1", "author": "sama", "created_at": "2026-05-08T05:00:00Z"},
            {"id": "1", "author": "sama", "text": "Missing date"},
            {"id": "1", "author": "sama", "text": "Bad date", "created_at": "not a date"},
        ]

        for record in records:
            with self.subTest(record=record):
                self.assertIsNone(fetch_twitter.normalize_opencli_tweet(record, self.source, self.cutoff))

    def test_extracts_records_from_common_json_shapes(self):
        shapes = [
            [{"id": "1"}],
            {"tweets": [{"id": "1"}]},
            {"data": [{"id": "1"}]},
            {"data": {"tweets": [{"id": "1"}]}},
            {"items": [{"id": "1"}]},
        ]

        for payload in shapes:
            with self.subTest(payload=payload):
                self.assertEqual(fetch_twitter.extract_opencli_tweet_records(payload), [{"id": "1"}])


class TestOpenCliDiscovery(unittest.TestCase):
    def test_resolves_opencli_bin_from_env(self):
        with patch.dict(os.environ, {"OPENCLI_BIN": "/custom/opencli"}):
            self.assertEqual(fetch_twitter.resolve_opencli_bin(), "/custom/opencli")

    def test_resolves_opencli_bin_from_path(self):
        with patch.dict(os.environ, {}, clear=True), patch(
            "fetch_twitter.shutil.which",
            return_value="/usr/local/bin/opencli",
        ):
            self.assertEqual(fetch_twitter.resolve_opencli_bin(), "/usr/local/bin/opencli")

    def test_missing_opencli_bin_raises(self):
        with patch.dict(os.environ, {}, clear=True), patch("fetch_twitter.shutil.which", return_value=None):
            with self.assertRaises(fetch_twitter.OpenCliBackendError) as ctx:
                fetch_twitter.resolve_opencli_bin()
        self.assertEqual(ctx.exception.code, "opencli_missing")

    def test_detects_twitter_tweets_capability_from_list_json(self):
        payloads = [
            [{"site": "twitter", "name": "tweets"}],
            {"commands": [{"site": "twitter", "name": "tweets"}]},
            {"commands": [{"command": "twitter tweets"}]},
            {"twitter": ["tweets", "timeline"]},
        ]
        for payload in payloads:
            with self.subTest(payload=payload):
                self.assertTrue(fetch_twitter.opencli_has_twitter_tweets(payload))

    def test_rejects_missing_twitter_tweets_capability(self):
        payload = {"commands": [{"site": "twitter", "name": "search"}]}
        self.assertFalse(fetch_twitter.opencli_has_twitter_tweets(payload))


class TestBackendSelection(unittest.TestCase):
    def test_auto_backend_order_starts_with_opencli(self):
        self.assertEqual(
            fetch_twitter.get_backend_order("auto"),
            ["opencli", "getxapi", "twitterapiio", "official"],
        )

    def test_explicit_opencli_has_no_api_fallback(self):
        self.assertEqual(fetch_twitter.get_backend_order("opencli"), ["opencli"])

    def test_explicit_api_backend_order_is_single_backend(self):
        self.assertEqual(fetch_twitter.get_backend_order("getxapi"), ["getxapi"])
        self.assertEqual(fetch_twitter.get_backend_order("twitterapiio"), ["twitterapiio"])
        self.assertEqual(fetch_twitter.get_backend_order("official"), ["official"])

    def test_opencli_defaults_to_parallel_fetching(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(fetch_twitter.get_opencli_max_workers(), 10)

    def test_opencli_worker_count_can_be_configured(self):
        with patch.dict(os.environ, {"OPENCLI_MAX_WORKERS": "3"}, clear=True):
            self.assertEqual(fetch_twitter.get_opencli_max_workers(), 3)

    def test_opencli_worker_count_rejects_invalid_values(self):
        invalid_values = ["0", "-1", "abc"]
        for value in invalid_values:
            with self.subTest(value=value), patch.dict(os.environ, {"OPENCLI_MAX_WORKERS": value}, clear=True):
                with self.assertLogs(level="WARNING"):
                    self.assertEqual(fetch_twitter.get_opencli_max_workers(), 10)

    def test_opencli_worker_count_caps_to_max(self):
        with patch.dict(os.environ, {"OPENCLI_MAX_WORKERS": "20"}, clear=True):
            with self.assertLogs(level="WARNING"):
                self.assertEqual(fetch_twitter.get_opencli_max_workers(), 10)

    def test_parses_opencli_update_command_override(self):
        parser = _require_attr(fetch_twitter, "_parse_opencli_update_command_spec")
        with patch.dict(os.environ, {"OPENCLI_UPDATE_COMMAND": "self-update --yes"}, clear=True):
            self.assertEqual(
                parser(),
                [["self-update", "--yes"]],
            )


class TestOpenCliAutoUpdate(unittest.TestCase):
    @patch.dict(os.environ, {"OPENCLI_UPDATE_COMMAND": "self-update"}, clear=True)
    def test_ensure_opencli_latest_retries_short_flag_when_long_flag_fails(self):
        with ExitStack() as stack:
            _require_attr(fetch_twitter, "_run_opencli_update_command")
            _require_attr(fetch_twitter, "_record_opencli_update_state")
            _require_attr(fetch_twitter, "_opencli_update_state_path")

            run_mock = stack.enter_context(
                patch("fetch_twitter._run_opencli_update_command")
            )
            stack.enter_context(patch("fetch_twitter._record_opencli_update_state"))
            state_path = _temp_opencli_state_path(stack)
            stack.enter_context(
                patch(
                    "fetch_twitter._opencli_update_state_path",
                    return_value=state_path,
                )
            )
            run_mock.side_effect = [
                subprocess.CompletedProcess(
                    args=["/bin/opencli", "self-update"],
                    returncode=1,
                    stdout="",
                    stderr="Update requires confirmation.",
                ),
                subprocess.CompletedProcess(
                    args=["/bin/opencli", "self-update", "--yes"],
                    returncode=1,
                    stdout="",
                    stderr="opencli: unrecognized argument '--yes'",
                ),
                subprocess.CompletedProcess(
                    args=["/bin/opencli", "self-update", "-y"],
                    returncode=0,
                    stdout="updated",
                    stderr="",
                ),
            ]

            ensure_opencli_latest = _require_attr(fetch_twitter, "_ensure_opencli_latest")

            result = ensure_opencli_latest("/bin/opencli")

            self.assertEqual(result["status"], "updated")
            self.assertEqual(result["command"], "/bin/opencli self-update -y")
            self.assertEqual(run_mock.call_count, 3)
            run_mock.assert_has_calls(
                [
                    call("/bin/opencli", ["self-update"]),
                    call("/bin/opencli", ["self-update", "--yes"]),
                    call("/bin/opencli", ["self-update", "-y"]),
                ]
            )

    @patch.dict(os.environ, {"OPENCLI_UPDATE_COMMAND": "self-update"}, clear=True)
    def test_ensure_opencli_latest_retries_yes_and_y_flags(self):
        with ExitStack() as stack:
            _require_attr(fetch_twitter, "_run_opencli_update_command")
            _require_attr(fetch_twitter, "_record_opencli_update_state")
            _require_attr(fetch_twitter, "_opencli_update_state_path")

            run_mock = stack.enter_context(
                patch("fetch_twitter._run_opencli_update_command")
            )
            stack.enter_context(patch("fetch_twitter._record_opencli_update_state"))
            state_path = _temp_opencli_state_path(stack)
            stack.enter_context(
                patch(
                    "fetch_twitter._opencli_update_state_path",
                    return_value=state_path,
                )
            )
            run_mock.side_effect = [
                subprocess.CompletedProcess(
                    args=["/bin/opencli", "self-update"],
                    returncode=1,
                    stdout="",
                    stderr="Update requires confirmation. Use --yes to continue.",
                ),
                subprocess.CompletedProcess(
                    args=["/bin/opencli", "self-update", "--yes"],
                    returncode=0,
                    stdout="updated",
                    stderr="",
                ),
            ]

            ensure_opencli_latest = _require_attr(fetch_twitter, "_ensure_opencli_latest")

            result = ensure_opencli_latest("/bin/opencli")

            self.assertEqual(result["status"], "updated")
            self.assertEqual(result["command"], "/bin/opencli self-update --yes")
            self.assertEqual(run_mock.call_count, 2)
            run_mock.assert_has_calls(
                [
                    call("/bin/opencli", ["self-update"]),
                    call("/bin/opencli", ["self-update", "--yes"]),
                ]
            )

    @patch.dict(os.environ, {"OPENCLI_UPDATE_COMMAND": "self-update"}, clear=True)
    def test_ensure_opencli_latest_treats_not_found_as_failed_instead_of_unsupported(self):
        with ExitStack() as stack:
            _require_attr(fetch_twitter, "_run_opencli_update_command")
            _require_attr(fetch_twitter, "_record_opencli_update_state")
            _require_attr(fetch_twitter, "_opencli_update_state_path")

            run_mock = stack.enter_context(
                patch("fetch_twitter._run_opencli_update_command")
            )
            stack.enter_context(patch("fetch_twitter._record_opencli_update_state"))
            state_path = _temp_opencli_state_path(stack)
            stack.enter_context(
                patch(
                    "fetch_twitter._opencli_update_state_path",
                    return_value=state_path,
                )
            )
            run_mock.side_effect = [
                subprocess.CompletedProcess(
                    args=["/bin/opencli", "self-update"],
                    returncode=1,
                    stdout="",
                    stderr="Update command exited with: file not found",
                ),
                subprocess.CompletedProcess(
                    args=["/bin/opencli", "self-update", "--yes"],
                    returncode=1,
                    stdout="",
                    stderr="Update command exited with: file not found",
                ),
                subprocess.CompletedProcess(
                    args=["/bin/opencli", "self-update", "-y"],
                    returncode=1,
                    stdout="",
                    stderr="Update command exited with: file not found",
                ),
            ]

            ensure_opencli_latest = _require_attr(fetch_twitter, "_ensure_opencli_latest")

            result = ensure_opencli_latest("/bin/opencli")

            self.assertEqual(result["status"], "failed")
            self.assertEqual(result["command"], "/bin/opencli self-update -y")
            self.assertEqual(run_mock.call_count, 3)
            run_mock.assert_has_calls(
                [
                    call("/bin/opencli", ["self-update"]),
                    call("/bin/opencli", ["self-update", "--yes"]),
                    call("/bin/opencli", ["self-update", "-y"]),
                ]
            )

    @patch.dict(os.environ, {"OPENCLI_UPDATE_COMMAND": "self-update --yes"}, clear=True)
    def test_ensure_opencli_latest_uses_custom_update_command(
        self,
        ):
        with ExitStack() as stack:
            _require_attr(fetch_twitter, "_run_opencli_update_command")
            _require_attr(fetch_twitter, "_record_opencli_update_state")
            _require_attr(fetch_twitter, "_opencli_update_state_path")

            run_mock = stack.enter_context(
                patch("fetch_twitter._run_opencli_update_command")
            )
            stack.enter_context(patch("fetch_twitter._record_opencli_update_state"))
            state_path = _temp_opencli_state_path(stack)
            stack.enter_context(
                patch(
                    "fetch_twitter._opencli_update_state_path",
                    return_value=state_path,
                )
            )
            run_mock.return_value = subprocess.CompletedProcess(
                args=["/bin/opencli", "self-update", "--yes"],
                returncode=0,
                stdout="updated",
                stderr="",
            )

            ensure_opencli_latest = _require_attr(fetch_twitter, "_ensure_opencli_latest")

            result = ensure_opencli_latest("/bin/opencli")

            self.assertEqual(result["status"], "updated")
            self.assertEqual(result["command"], "/bin/opencli self-update --yes")
            run_mock.assert_called_once_with("/bin/opencli", ["self-update", "--yes"])

    @patch.dict(os.environ, {"OPENCLI_NO_UPDATE": "1"}, clear=True)
    def test_ensure_opencli_latest_skips_when_no_update_enabled(
        self,
    ):
        _require_attr(fetch_twitter, "_run_opencli_update_command")
        _require_attr(fetch_twitter, "_opencli_update_state_path")

        with ExitStack() as stack:
            run_mock = stack.enter_context(
                patch("fetch_twitter._run_opencli_update_command")
            )
            state_path = _temp_opencli_state_path(stack)
            stack.enter_context(
                patch(
                    "fetch_twitter._opencli_update_state_path",
                    return_value=state_path,
                )
            )
            ensure_opencli_latest = _require_attr(fetch_twitter, "_ensure_opencli_latest")

            result = ensure_opencli_latest("/bin/opencli")

            self.assertEqual(result["status"], "skipped")
            self.assertIn("OpenCLI auto-update is disabled", result["message"])
            run_mock.assert_not_called()


class TestOpenCliSelectionDiagnostics(unittest.TestCase):
    def test_empty_reason_prioritizes_opencli_failure(self):
        diagnostics = [
            {
                "backend": "opencli",
                "code": "opencli_browser_unavailable",
                "message": "No tab with id: 123",
            },
            {
                "backend": "twitterapiio",
                "code": "backend_unavailable",
                "message": "twitterapiio backend is not configured",
            },
            {
                "backend": "official",
                "code": "backend_unavailable",
                "message": "official backend is not configured",
            },
        ]

        reason = fetch_twitter.build_twitter_skipped_reason("auto", diagnostics)

        self.assertIn("OpenCLI failed first", reason)
        self.assertIn("opencli_browser_unavailable", reason)
        self.assertIn("No tab with id", reason)
        self.assertIn("twitterapi.io", reason)
        self.assertIn("X_BEARER_TOKEN", reason)

    def test_stale_browser_bridge_errors_are_global_opencli_failures(self):
        stale_errors = [
            "No tab with id: 123",
            "SecurityError: Failed to execute 'pushState' on 'History'",
        ]

        for message in stale_errors:
            with self.subTest(message=message):
                code = fetch_twitter._classify_opencli_failure(1, message)

                self.assertEqual(code, "opencli_browser_unavailable")

    def test_stale_browser_bridge_errors_in_stdout_are_global_opencli_failures(self):
        code = fetch_twitter._classify_opencli_failure(1, stdout="No tab with id: 123")
        self.assertEqual(code, "opencli_browser_unavailable")

class TestOpenCliBackend(unittest.TestCase):
    def setUp(self):
        self._env_patch = patch.dict(os.environ, {"OPENCLI_CLOSE_CHROME_WINDOWS_AFTER_RUN": "0"})
        self._env_patch.start()
        self.addCleanup(self._env_patch.stop)
        self._version_patch = patch(
            "fetch_twitter._get_opencli_version",
            return_value="1.7.22",
        )
        self._version_patch.start()
        self.addCleanup(self._version_patch.stop)
        self.source = {
            "id": "sama-twitter",
            "type": "twitter",
            "name": "Sam Altman",
            "handle": "sama",
            "enabled": True,
            "priority": True,
            "topics": ["llm"],
        }
        self.cutoff = utc("2026-05-08T00:00:00Z")

    def _completed(self, stdout, returncode=0, stderr=""):
        return subprocess.CompletedProcess(
            args=["opencli"],
            returncode=returncode,
            stdout=stdout,
            stderr=stderr,
        )

    @patch("fetch_twitter.resolve_opencli_bin", return_value="/bin/opencli")
    @patch("subprocess.run")
    def test_fetches_tweets_for_source(self, run_mock, _resolve_mock):
        run_mock.side_effect = [
            self._completed("Usage: opencli twitter tweets <username> [options]"),
            self._completed("OpenCLI doctor ok"),
            self._completed(json.dumps({"tabs": []})),
            self._completed(json.dumps([
                {
                    "id": "123",
                    "author": "sama",
                    "text": "A useful post.",
                    "created_at": "2026-05-08T01:00:00Z",
                    "likes": 5,
                    "retweets": 1,
                    "replies": 0,
                    "views": 100,
                    "url": "https://x.com/sama/status/123",
                    "is_retweet": False,
                }
            ])),
            self._completed(json.dumps({"tabs": []})),
            self._completed("lease released"),
        ]

        backend = fetch_twitter.OpenCliBackend(no_cache=True)
        results = backend.fetch_all([self.source], self.cutoff)

        self.assertEqual(results[0]["status"], "ok")
        self.assertEqual(results[0]["handle"], "sama")
        self.assertEqual(results[0]["count"], 1)
        self.assertEqual(results[0]["articles"][0]["tweet_id"], "123")
        self.assertIn(
            [
                "/bin/opencli",
                "twitter",
                "tweets",
                "sama",
                "--limit",
                "20",
                "-f",
                "json",
            ],
            [call.args[0] for call in run_mock.call_args_list],
        )

    @patch("fetch_twitter.resolve_opencli_bin", return_value="/bin/opencli")
    @patch("subprocess.run")
    def test_closes_new_twitter_tabs_after_fetch(self, run_mock, _resolve_mock):
        run_mock.side_effect = [
            self._completed("Usage: opencli twitter tweets <username> [options]"),
            self._completed("OpenCLI doctor ok"),
            self._completed(json.dumps({
                "tabs": [
                    {"targetId": "existing-x-tab", "url": "https://x.com/home"},
                ],
            })),
            self._completed(json.dumps([
                {
                    "id": "123",
                    "author": "sama",
                    "text": "A useful post.",
                    "created_at": "2026-05-08T01:00:00Z",
                    "url": "https://x.com/sama/status/123",
                    "is_retweet": False,
                }
            ])),
            self._completed(json.dumps({
                "tabs": [
                    {"targetId": "existing-x-tab", "url": "https://x.com/home"},
                    {"targetId": "new-x-tab", "url": "https://x.com/sama/status/123"},
                    {"page": "new-doc-tab", "url": "https://example.com/docs"},
                    {"page": "new-twitter-tab", "url": "https://twitter.com/sama/status/456"},
                ],
            })),
            self._completed("closed"),
            self._completed("closed"),
            self._completed("lease released"),
        ]

        backend = fetch_twitter.OpenCliBackend(no_cache=True)
        backend.fetch_all([self.source], self.cutoff)

        commands = [call.args[0] for call in run_mock.call_args_list]
        self.assertIn(["/bin/opencli", "browser", "tab", "close", "new-x-tab"], commands)
        self.assertIn(["/bin/opencli", "browser", "tab", "close", "new-twitter-tab"], commands)
        self.assertIn(["/bin/opencli", "browser", "close"], commands)
        self.assertNotIn(["/bin/opencli", "browser", "tab", "close", "existing-x-tab"], commands)
        self.assertNotIn(["/bin/opencli", "browser", "tab", "close", "new-doc-tab"], commands)

    @patch("fetch_twitter.time.sleep")
    @patch("fetch_twitter.OpenCliBackend._run_command")
    def test_closes_new_opencli_twitter_tabs_with_single_pass(self, run_command_mock, sleep_mock):
        backend = fetch_twitter.OpenCliBackend.__new__(fetch_twitter.OpenCliBackend)
        backend.command = "/bin/opencli"

        run_command_mock.side_effect = [
            self._completed(
                json.dumps({
                    "tabs": [
                        {"targetId": "existing-x-tab", "url": "https://x.com/home"},
                        {"targetId": "new-twitter-tab", "url": "https://twitter.com/sama/status/456"},
                    ]
                })
            ),
            self._completed("closed"),
        ]

        backend._cleanup_new_browser_tabs({"existing-x-tab": "https://x.com/home"})

        calls = [call.args[0] for call in run_command_mock.call_args_list]
        self.assertEqual(calls[0], ["browser", "tab", "list"])
        self.assertEqual(calls[1:], [["browser", "tab", "close", "new-twitter-tab"]])
        self.assertEqual(sleep_mock.call_count, 1)
        self.assertEqual(len(calls), 2)

    @patch("fetch_twitter.resolve_opencli_bin", return_value="/bin/opencli")
    @patch("subprocess.run")
    def test_missing_capability_raises_global_error(self, run_mock, _resolve_mock):
        run_mock.return_value = self._completed("", returncode=1, stderr="Unknown command: tweets")

        with self.assertRaises(fetch_twitter.OpenCliBackendError) as ctx:
            fetch_twitter.OpenCliBackend()

        self.assertEqual(ctx.exception.code, "opencli_capability_missing")

    @patch("fetch_twitter.resolve_opencli_bin", return_value="/bin/opencli")
    @patch("subprocess.run")
    def test_auth_required_raises_global_error_on_probe(self, run_mock, _resolve_mock):
        run_mock.side_effect = [
            self._completed("Usage: opencli twitter tweets <username> [options]"),
            self._completed("OpenCLI doctor ok"),
            self._completed(json.dumps({"tabs": []})),
            self._completed("", returncode=77, stderr="Not logged into x.com"),
            self._completed(json.dumps({"tabs": []})),
            self._completed("lease released"),
        ]

        backend = fetch_twitter.OpenCliBackend(no_cache=True)

        with self.assertRaises(fetch_twitter.OpenCliBackendError) as ctx:
            backend.fetch_all([self.source], self.cutoff)

        self.assertEqual(ctx.exception.code, "opencli_auth_required")

    @patch("fetch_twitter._get_opencli_version", return_value="1.7.21")
    @patch("fetch_twitter.resolve_opencli_bin", return_value="/bin/opencli")
    @patch("subprocess.run")
    def test_too_old_version_raises_global_error(self, run_mock, _resolve_mock, _version_mock):
        with self.assertRaises(fetch_twitter.OpenCliBackendError) as ctx:
            fetch_twitter.OpenCliBackend(no_cache=True)

        self.assertEqual(ctx.exception.code, "opencli_version_too_old")
        run_mock.assert_not_called()

    @patch.dict(
        os.environ,
        {
            "OPENCLI_CLOSE_CHROME_WINDOWS_AFTER_RUN": "0",
            "OPENCLI_UPDATE_COMMAND": "self-update",
        },
        clear=True,
    )
    @patch("fetch_twitter.snapshot_chrome_windows", return_value=None)
    @patch("fetch_twitter.OpenCliBackend._run_doctor")
    @patch("fetch_twitter.OpenCliBackend._verify_capability")
    @patch("fetch_twitter.resolve_opencli_bin", return_value="/bin/opencli")
    def test_auto_update_runs_before_min_version_gate(
        self,
        _resolve_mock,
        verify_mock,
        doctor_mock,
        _snapshot_mock,
    ):
        update_ran = {"value": False}

        def _get_version(_binary):
            return "1.7.22" if update_ran["value"] else "1.7.21"

        def _run_update(binary, args, timeout=120):
            update_ran["value"] = True
            return subprocess.CompletedProcess(
                args=[binary] + args,
                returncode=0,
                stdout="updated",
                stderr="",
            )

        with ExitStack() as stack:
            stack.enter_context(patch("fetch_twitter._get_opencli_version", side_effect=_get_version))
            update_mock = stack.enter_context(patch("fetch_twitter._run_opencli_update_command", side_effect=_run_update))
            stack.enter_context(patch("fetch_twitter._record_opencli_update_state"))
            state_path = _temp_opencli_state_path(stack)
            stack.enter_context(patch("fetch_twitter._opencli_update_state_path", return_value=state_path))

            backend = fetch_twitter.OpenCliBackend(auto_update=True, no_cache=True)

        self.assertEqual(backend.command, "/bin/opencli")
        self.assertTrue(update_ran["value"])
        update_mock.assert_called_once_with("/bin/opencli", ["self-update"])
        verify_mock.assert_called_once()
        doctor_mock.assert_called_once()

    @patch.dict(
        os.environ,
        {
            "OPENCLI_CLOSE_CHROME_WINDOWS_AFTER_RUN": "0",
            "OPENCLI_UPDATE_COMMAND": "self-update",
        },
        clear=True,
    )
    @patch("fetch_twitter.snapshot_chrome_windows", return_value=None)
    @patch("fetch_twitter.OpenCliBackend._run_doctor")
    @patch("fetch_twitter.OpenCliBackend._verify_capability")
    @patch("fetch_twitter.resolve_opencli_bin", return_value="/bin/opencli")
    def test_auto_update_forces_retry_when_throttled_and_version_too_old(
        self,
        _resolve_mock,
        verify_mock,
        doctor_mock,
        _snapshot_mock,
    ):
        update_ran = {"value": False}

        def _get_version(_binary):
            return "1.7.22" if update_ran["value"] else "1.7.21"

        def _run_update(binary, args, timeout=120):
            update_ran["value"] = True
            return subprocess.CompletedProcess(
                args=[binary] + args,
                returncode=0,
                stdout="updated",
                stderr="",
            )

        with ExitStack() as stack:
            stack.enter_context(patch("fetch_twitter._get_opencli_version", side_effect=_get_version))
            update_mock = stack.enter_context(patch("fetch_twitter._run_opencli_update_command", side_effect=_run_update))
            stack.enter_context(patch("fetch_twitter._record_opencli_update_state"))
            state_path = _temp_opencli_state_path(stack)
            state_path.write_text("{}", encoding="utf-8")
            stack.enter_context(patch("fetch_twitter._opencli_update_state_path", return_value=state_path))

            backend = fetch_twitter.OpenCliBackend(auto_update=True, no_cache=True)

        self.assertEqual(backend.command, "/bin/opencli")
        self.assertTrue(update_ran["value"])
        update_mock.assert_called_once_with("/bin/opencli", ["self-update"])
        verify_mock.assert_called_once()
        doctor_mock.assert_called_once()

    @patch("fetch_twitter.resolve_opencli_bin", return_value="/bin/opencli")
    @patch("subprocess.run")
    def test_single_source_error_does_not_raise_global_error(self, run_mock, _resolve_mock):
        second_source = dict(self.source)
        second_source["id"] = "openai-twitter"
        second_source["name"] = "OpenAI"
        second_source["handle"] = "OpenAI"

        run_mock.side_effect = [
            self._completed("Usage: opencli twitter tweets <username> [options]"),
            self._completed("OpenCLI doctor ok"),
            self._completed(json.dumps({"tabs": []})),
            self._completed(json.dumps([
                {
                    "id": "probe",
                    "author": "sama",
                    "text": "Probe works.",
                    "created_at": "2026-05-08T01:00:00Z",
                    "is_retweet": False,
                }
            ])),
            self._completed("", returncode=1, stderr="Could not resolve @OpenAI"),
            self._completed(json.dumps({"tabs": []})),
            self._completed("lease released"),
        ]

        backend = fetch_twitter.OpenCliBackend(no_cache=True)
        with self.assertLogs(level="WARNING") as logs:
            results = backend.fetch_all([self.source, second_source], self.cutoff)

        by_handle = {item["handle"]: item for item in results}
        self.assertEqual(by_handle["sama"]["status"], "ok")
        self.assertEqual(by_handle["OpenAI"]["status"], "error")
        self.assertIn("opencli_source_error", by_handle["OpenAI"]["error"])
        self.assertTrue(any("opencli_source_error" in line for line in logs.output))


class TestFetchWithBackendChain(unittest.TestCase):
    @patch("fetch_twitter._instantiate_backend")
    def test_auto_chain_stops_when_opencli_version_too_old(self, instantiate_mock):
        source = {
            "id": "sama-twitter",
            "type": "twitter",
            "name": "Sam Altman",
            "handle": "sama",
            "enabled": True,
            "priority": True,
            "topics": ["llm"],
        }

        def _instantiate(backend_name, *args, **kwargs):
            if backend_name == "opencli":
                raise fetch_twitter.OpenCliBackendError("opencli_version_too_old", "Please upgrade OpenCLI.")
            raise AssertionError(f"unexpected backend instantiation: {backend_name}")

        instantiate_mock.side_effect = _instantiate

        selected, results, diagnostics = fetch_twitter.fetch_with_backend_chain(
            "auto",
            [source],
            utc("2026-05-08T00:00:00Z"),
        )

        self.assertEqual(selected, "opencli")
        self.assertEqual(results, [])
        self.assertEqual(
            diagnostics,
            [{"backend": "opencli", "code": "opencli_version_too_old", "message": "Please upgrade OpenCLI."}],
        )

    @patch("fetch_twitter.OpenCliBackend")
    def test_fetch_with_backend_chain_passes_opencli_workers(self, backend_cls_mock):
        source = {
            "id": "sama-twitter",
            "type": "twitter",
            "name": "Sam Altman",
            "handle": "sama",
            "enabled": True,
            "priority": True,
            "topics": ["llm"],
        }
        backend = backend_cls_mock.return_value
        backend.fetch_all.return_value = []
        backend_cls_mock.return_value = backend

        fetch_twitter.fetch_with_backend_chain(
            "opencli",
            [source],
            utc("2026-05-08T00:00:00Z"),
            opencli_workers=7,
        )

        backend_cls_mock.assert_called_once_with(max_workers=7, auto_update=False, no_cache=False)

    @patch("fetch_twitter.OpenCliBackend")
    def test_no_cache_is_forwarded_to_opencli_backend(self, backend_cls_mock):
        backend = backend_cls_mock.return_value
        backend.fetch_all.return_value = []

        fetch_twitter.fetch_with_backend_chain(
            "opencli",
            [],
            utc("2026-05-08T00:00:00Z"),
            no_cache=True,
        )

        backend_cls_mock.assert_called_once_with(max_workers=None, auto_update=False, no_cache=True)

    @patch.dict(os.environ, {"GETX_API_KEY": "x" * 20}, clear=True)
    @patch("fetch_twitter.GetXApiBackend")
    def test_no_cache_is_forwarded_to_getxapi_backend(self, backend_cls_mock):
        backend = backend_cls_mock.return_value
        backend.fetch_all.return_value = []

        fetch_twitter.fetch_with_backend_chain(
            "getxapi",
            [],
            utc("2026-05-08T00:00:00Z"),
            no_cache=True,
        )

        backend_cls_mock.assert_called_once_with("x" * 20, no_cache=True)

    @patch.dict(os.environ, {"TWITTERAPI_IO_KEY": "x" * 20}, clear=True)
    @patch("fetch_twitter.TwitterApiIoBackend")
    def test_no_cache_is_forwarded_to_twitterapiio_backend(self, backend_cls_mock):
        backend = backend_cls_mock.return_value
        backend.fetch_all.return_value = []

        fetch_twitter.fetch_with_backend_chain(
            "twitterapiio",
            [],
            utc("2026-05-08T00:00:00Z"),
            no_cache=True,
        )

        backend_cls_mock.assert_called_once_with("x" * 20, no_cache=True)


class TestOfficialBackend(unittest.TestCase):
    @patch.object(fetch_twitter.OfficialBackend, "_save_id_cache")
    @patch.object(fetch_twitter.OfficialBackend, "_load_id_cache", return_value={})
    @patch("fetch_twitter.x_request_json")
    def test_batch_user_lookup_skips_individual_fallback_when_rate_deferred(
        self,
        request_mock,
        _load_cache_mock,
        _save_cache_mock,
    ):
        request_mock.side_effect = fetch_twitter.XRateLimitDeferred(1300)
        backend = fetch_twitter.OfficialBackend("token-a")

        result = backend._batch_resolve_user_ids(["sama", "jack"])

        self.assertEqual(result, {})
        request_mock.assert_called_once()

    @patch("fetch_twitter.time.sleep")
    @patch("fetch_twitter.x_request_json")
    def test_transient_429_is_retried_for_timeline_request(self, request_mock, _sleep_mock):
        request_mock.side_effect = [
            http_error(429),
            {"data": []},
        ]
        backend = fetch_twitter.OfficialBackend("token-a")

        result = backend._fetch_user_tweets(twitter_source(), utc("2024-12-09T00:00:00Z"), user_id="1")

        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["attempts"], 2)
        self.assertEqual(request_mock.call_count, 2)

    @patch("fetch_twitter.time.sleep")
    @patch("fetch_twitter.x_request_json")
    def test_backend_no_cache_is_forwarded_to_timeline_request(self, request_mock, _sleep_mock):
        request_mock.return_value = {"data": []}
        backend = fetch_twitter.OfficialBackend("token-a", no_cache=True)

        result = backend._fetch_user_tweets(twitter_source(), utc("2024-12-09T00:00:00Z"), user_id="1")

        self.assertEqual(result["status"], "ok")
        request_mock.assert_called_once()
        self.assertTrue(request_mock.call_args.kwargs["no_cache"])


class TestGetXApiBackend(unittest.TestCase):
    @patch("fetch_twitter.x_request_json")
    def test_backend_no_cache_is_forwarded_to_timeline_requests(self, request_mock):
        request_mock.side_effect = [
            {
                "tweets": [
                    {
                        "id": "1",
                        "text": "fresh tweet",
                        "createdAt": "Tue Dec 10 07:00:30 +0000 2024",
                        "url": "https://x.com/sama/status/1",
                    }
                ],
                "has_more": True,
                "next_cursor": "cursor-1",
            },
            {"tweets": [], "has_more": False},
        ]
        backend = fetch_twitter.GetXApiBackend("token-a-12345", no_cache=True)
        source = twitter_source()

        result = backend._fetch_user_tweets(source, utc("2024-12-09T00:00:00Z"))

        self.assertEqual(result["status"], "ok")
        self.assertEqual(request_mock.call_count, 2)
        self.assertTrue(request_mock.call_args_list[0].kwargs["no_cache"])
        self.assertTrue(request_mock.call_args_list[1].kwargs["no_cache"])

    @patch("fetch_twitter.time.sleep")
    @patch("fetch_twitter.x_request_json")
    def test_transient_429_is_retried_for_timeline_request(self, request_mock, _sleep_mock):
        request_mock.side_effect = [
            http_error(429),
            {"tweets": [], "has_more": False},
        ]
        backend = fetch_twitter.GetXApiBackend("token-a-12345")

        result = backend._fetch_user_tweets(twitter_source(), utc("2024-12-09T00:00:00Z"))

        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["attempts"], 2)
        self.assertEqual(request_mock.call_count, 2)


class TestTwitterApiIoBackend(unittest.TestCase):
    @patch("fetch_twitter.x_request_json")
    def test_backend_no_cache_is_forwarded_to_timeline_requests(self, request_mock):
        request_mock.side_effect = [
            {
                "data": {
                    "tweets": [
                        {
                            "id": "1",
                            "text": "fresh tweet",
                            "createdAt": "Tue Dec 10 07:00:30 +0000 2024",
                            "url": "https://twitter.com/sama/status/1",
                        }
                    ],
                    "has_next_page": True,
                    "next_cursor": "cursor-1",
                }
            },
            {"data": {"tweets": [], "has_next_page": False}},
        ]
        backend = fetch_twitter.TwitterApiIoBackend("token-a", no_cache=True)
        source = twitter_source()

        result = backend._fetch_user_tweets(source, utc("2024-12-09T00:00:00Z"))

        self.assertEqual(result["status"], "ok")
        self.assertEqual(request_mock.call_count, 2)
        self.assertTrue(request_mock.call_args_list[0].kwargs["no_cache"])
        self.assertTrue(request_mock.call_args_list[1].kwargs["no_cache"])

    @patch("fetch_twitter.time.sleep")
    @patch("fetch_twitter.x_request_json")
    def test_transient_429_is_retried_for_timeline_request(self, request_mock, _sleep_mock):
        request_mock.side_effect = [
            http_error(429),
            {"data": {"tweets": [], "has_next_page": False}},
        ]
        backend = fetch_twitter.TwitterApiIoBackend("token-a")

        result = backend._fetch_user_tweets(twitter_source(), utc("2024-12-09T00:00:00Z"))

        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["attempts"], 2)
        self.assertEqual(request_mock.call_count, 2)


class TestMainOpenCliOptions(unittest.TestCase):
    @patch("fetch_twitter.open", new_callable=mock_open)
    @patch("fetch_twitter.fetch_with_backend_chain")
    @patch("fetch_twitter.load_twitter_sources")
    def test_cli_no_update_flag_disables_opencli_auto_update(
        self,
        load_sources_mock,
        backend_chain_mock,
        _open_mock,
    ):
        load_sources_mock.return_value = []
        backend_chain_mock.return_value = ("opencli", [], [])

        with patch.dict(os.environ, {"OPENCLI_AUTO_UPDATE": "1"}, clear=True):
            with patch.object(sys, "argv", ["fetch-twitter.py", "--backend", "opencli", "--no-update"]):
                self.assertEqual(fetch_twitter.main(), 0)

        self.assertEqual(_read_opencli_auto_update_arg(backend_chain_mock.call_args), False)

    @patch("fetch_twitter.open", new_callable=mock_open)
    @patch("fetch_twitter.fetch_with_backend_chain")
    @patch("fetch_twitter.load_twitter_sources")
    def test_no_update_flag_disables_opencli_auto_update(
        self,
        load_sources_mock,
        backend_chain_mock,
        _open_mock,
    ):
        load_sources_mock.return_value = []
        backend_chain_mock.return_value = ("opencli", [], [])

        with patch.dict(os.environ, {"OPENCLI_AUTO_UPDATE": "1", "OPENCLI_NO_UPDATE": "1"}, clear=True):
            with patch.object(sys, "argv", ["fetch-twitter.py", "--backend", "opencli"]):
                self.assertEqual(fetch_twitter.main(), 0)

        self.assertEqual(_read_opencli_auto_update_arg(backend_chain_mock.call_args), False)

    @patch("fetch_twitter.open", new_callable=mock_open)
    @patch("fetch_twitter.fetch_with_backend_chain")
    @patch("fetch_twitter.load_twitter_sources")
    def test_no_update_flag_controls_update_toggle(
        self,
        load_sources_mock,
        backend_chain_mock,
        _open_mock,
    ):
        load_sources_mock.return_value = []
        backend_chain_mock.return_value = ("opencli", [], [])

        with patch.dict(os.environ, {"OPENCLI_AUTO_UPDATE": "1"}, clear=True):
            with patch.object(sys, "argv", ["fetch-twitter.py", "--backend", "opencli"]):
                self.assertEqual(fetch_twitter.main(), 0)
        self.assertEqual(_read_opencli_auto_update_arg(backend_chain_mock.call_args), True)

        with patch.dict(os.environ, {"OPENCLI_AUTO_UPDATE": "1", "OPENCLI_NO_UPDATE": "1"}, clear=True):
            with patch.object(sys, "argv", ["fetch-twitter.py", "--backend", "opencli"]):
                self.assertEqual(fetch_twitter.main(), 0)
        self.assertEqual(_read_opencli_auto_update_arg(backend_chain_mock.call_args_list[1]), False)

    @patch("fetch_twitter.open", new_callable=mock_open)
    @patch("fetch_twitter.fetch_with_backend_chain")
    @patch("fetch_twitter.load_twitter_sources")
    def test_opencli_no_update_env_prevents_auto_update(
        self,
        load_sources_mock,
        backend_chain_mock,
        _open_mock,
    ):
        load_sources_mock.return_value = []
        backend_chain_mock.return_value = ("opencli", [], [])

        with patch.dict(os.environ, {"OPENCLI_NO_UPDATE": "1", "OPENCLI_AUTO_UPDATE": "1"}, clear=True):
            with patch.object(sys, "argv", ["fetch-twitter.py", "--backend", "opencli"]):
                self.assertEqual(fetch_twitter.main(), 0)
            self.assertEqual(_read_opencli_auto_update_arg(backend_chain_mock.call_args_list[0]), False)




class TestOpenCliChromeCleanup(unittest.TestCase):
    def test_parses_chrome_window_snapshot(self):
        raw = (
            "101\thttps://github.com/tangwz/follow-news ||| https://x.com/home\n"
            "202\tabout:blank ||| chrome://newtab/\n"
            "303tabhttps://x.com/explore\n"
        )

        windows = fetch_twitter.parse_chrome_window_snapshot(raw)

        self.assertEqual(
            windows,
            {
                "101": ["https://github.com/tangwz/follow-news", "https://x.com/home"],
                "202": ["about:blank", "chrome://newtab/"],
                "303": ["https://x.com/explore"],
            },
        )

    def test_identifies_opencli_chrome_windows(self):
        self.assertTrue(fetch_twitter.is_opencli_chrome_window(["about:blank"]))
        self.assertTrue(fetch_twitter.is_opencli_chrome_window(["chrome://newtab/", "https://x.com/explore"]))
        self.assertTrue(fetch_twitter.is_opencli_chrome_window(["https://twitter.com/sama/status/123"]))
        self.assertFalse(fetch_twitter.is_opencli_chrome_window(["https://github.com/tangwz/follow-news"]))
        self.assertFalse(fetch_twitter.is_opencli_chrome_window(["https://x.com/home", "https://github.com/"]))

    @patch("fetch_twitter.time.sleep")
    @patch("fetch_twitter.close_chrome_windows")
    @patch("fetch_twitter.snapshot_chrome_windows")
    def test_closes_only_new_opencli_chrome_windows(self, snapshot_mock, close_mock, _sleep_mock):
        before = {
            "1": ["https://github.com/tangwz/follow-news"],
            "2": ["about:blank"],
        }
        snapshot_mock.side_effect = [
            {
                "1": ["https://github.com/tangwz/follow-news"],
                "2": ["about:blank"],
                "3": ["about:blank", "https://x.com/explore"],
                "4": ["https://github.com/new"],
            },
            {
                "1": ["https://github.com/tangwz/follow-news"],
                "2": ["about:blank"],
                "4": ["https://github.com/new"],
            },
        ]

        fetch_twitter.cleanup_new_opencli_chrome_windows(before)

        close_mock.assert_called_once_with(["3"])

    @patch("fetch_twitter.time.sleep")
    @patch("fetch_twitter.close_chrome_windows")
    @patch("fetch_twitter.snapshot_chrome_windows")
    def test_retries_delayed_opencli_chrome_window_cleanup(self, snapshot_mock, close_mock, sleep_mock):
        before = {
            "1": ["https://github.com/tangwz/follow-news"],
        }
        snapshot_mock.side_effect = [
            before,
            {
                "1": ["https://github.com/tangwz/follow-news"],
                "2": ["about:blank"],
            },
            before,
        ]

        fetch_twitter.cleanup_new_opencli_chrome_windows(before)

        sleep_mock.assert_any_call(0.5)
        close_mock.assert_called_once_with(["2"])


class TestBackendChain(unittest.TestCase):
    def setUp(self):
        self.sources = [
            {
                "id": "sama-twitter",
                "type": "twitter",
                "name": "Sam Altman",
                "handle": "sama",
                "enabled": True,
                "priority": True,
                "topics": ["llm"],
            }
        ]
        self.cutoff = utc("2026-05-08T00:00:00Z")

    @patch.dict(os.environ, {"GETX_API_KEY": "x" * 20}, clear=True)
    @patch("fetch_twitter.OpenCliBackend", side_effect=fetch_twitter.OpenCliBackendError("opencli_missing", "missing"))
    @patch("fetch_twitter.GetXApiBackend")
    def test_auto_falls_back_from_opencli_to_getxapi(self, getx_cls, _opencli_cls):
        getx = getx_cls.return_value
        getx.fetch_all.return_value = [{"status": "ok", "count": 0, "articles": []}]

        with self.assertLogs(level="WARNING") as logs:
            backend_name, results, diagnostics = fetch_twitter.fetch_with_backend_chain(
                "auto", self.sources, self.cutoff, no_cache=False
            )

        self.assertEqual(backend_name, "getxapi")
        self.assertEqual(results, [{"status": "ok", "count": 0, "articles": []}])
        self.assertEqual(diagnostics[0]["backend"], "opencli")
        self.assertEqual(diagnostics[0]["code"], "opencli_missing")
        self.assertTrue(any("opencli_missing" in line for line in logs.output))

    @patch.dict(os.environ, {"GETX_API_KEY": "x" * 20}, clear=True)
    @patch("fetch_twitter.GetXApiBackend")
    @patch("fetch_twitter.OpenCliBackend")
    def test_auto_opencli_stale_bridge_failure_retried_once_before_fallback(self, opencli_cls, getx_cls):
        first_opencli_backend = MagicMock()
        second_opencli_backend = MagicMock()
        opencli_cls.side_effect = [first_opencli_backend, second_opencli_backend]
        first_opencli_backend.fetch_all.side_effect = fetch_twitter.OpenCliBackendError(
            "opencli_browser_unavailable",
            "No tab with id: 123",
        )
        second_opencli_backend.fetch_all.side_effect = fetch_twitter.OpenCliBackendError(
            "opencli_browser_unavailable",
            "SecurityError: Failed to execute 'pushState' on 'History'",
        )

        getx = getx_cls.return_value
        getx.fetch_all.return_value = [{"status": "ok", "count": 0, "articles": []}]

        with self.assertLogs(level="WARNING") as logs:
            backend_name, results, diagnostics = fetch_twitter.fetch_with_backend_chain(
                "auto", self.sources, self.cutoff, no_cache=False
            )

        self.assertEqual(backend_name, "getxapi")
        self.assertEqual(results, [{"status": "ok", "count": 0, "articles": []}])
        self.assertEqual(opencli_cls.call_count, 2)
        self.assertEqual(getx_cls.call_count, 1)
        self.assertEqual(
            [item for item in diagnostics if item["backend"] == "opencli"],
            [
                {
                    "backend": "opencli",
                    "code": "opencli_browser_unavailable",
                    "message": "No tab with id: 123",
                },
                {
                    "backend": "opencli",
                    "code": "opencli_browser_unavailable",
                    "message": "SecurityError: Failed to execute 'pushState' on 'History'",
                },
            ],
        )
        self.assertTrue(any("opencli recovery attempt" in line for line in logs.output))

    @patch("fetch_twitter.OpenCliBackend")
    def test_explicit_opencli_retries_once_and_still_fails(self, opencli_cls):
        first_opencli_backend = MagicMock()
        second_opencli_backend = MagicMock()
        opencli_cls.side_effect = [first_opencli_backend, second_opencli_backend]
        first_opencli_backend.fetch_all.side_effect = fetch_twitter.OpenCliBackendError(
            "opencli_browser_unavailable",
            "No tab with id: 123",
        )
        second_opencli_backend.fetch_all.side_effect = fetch_twitter.OpenCliBackendError(
            "opencli_browser_unavailable",
            "SecurityError: Failed to execute 'pushState' on 'History'",
        )

        backend_name, results, diagnostics = fetch_twitter.fetch_with_backend_chain(
            "opencli", self.sources, self.cutoff, no_cache=False
        )

        self.assertEqual(backend_name, "opencli")
        self.assertEqual(results, [])
        self.assertEqual(opencli_cls.call_count, 2)
        self.assertEqual(len([item for item in diagnostics if item["backend"] == "opencli"]), 2)
        self.assertEqual(diagnostics[0]["code"], "opencli_browser_unavailable")

    @patch.dict(os.environ, {}, clear=True)
    @patch("fetch_twitter.OpenCliBackend", side_effect=fetch_twitter.OpenCliBackendError("opencli_missing", "missing"))
    def test_explicit_opencli_does_not_fallback(self, _opencli_cls):
        with self.assertLogs(level="WARNING") as logs:
            backend_name, results, diagnostics = fetch_twitter.fetch_with_backend_chain(
                "opencli", self.sources, self.cutoff, no_cache=False
            )

        self.assertEqual(backend_name, "opencli")
        self.assertEqual(results, [])
        self.assertEqual(diagnostics[0]["code"], "opencli_missing")
        self.assertTrue(any("opencli_missing" in line for line in logs.output))

    @patch.dict(os.environ, {}, clear=True)
    @patch("fetch_twitter.OpenCliBackend", side_effect=fetch_twitter.OpenCliBackendError("opencli_missing", "missing"))
    def test_auto_returns_no_results_when_no_backend_available(self, _opencli_cls):
        with self.assertLogs(level="WARNING") as logs:
            backend_name, results, diagnostics = fetch_twitter.fetch_with_backend_chain(
                "auto", self.sources, self.cutoff, no_cache=False
            )

        self.assertEqual(backend_name, "auto")
        self.assertEqual(results, [])
        self.assertTrue(any(item["backend"] == "opencli" for item in diagnostics))
        self.assertTrue(any("opencli_missing" in line for line in logs.output))


class TestOpenCliMergeCompatibility(unittest.TestCase):
    def test_opencli_articles_keep_existing_merge_shape(self):
        merge_spec = importlib.util.spec_from_file_location(
            "merge_sources",
            SCRIPTS_DIR / "merge-sources.py",
        )
        merge_mod = importlib.util.module_from_spec(merge_spec)
        merge_spec.loader.exec_module(merge_mod)

        source = {
            "source_id": "sama-twitter",
            "source_type": "twitter",
            "name": "Sam Altman",
            "handle": "sama",
            "priority": True,
            "topics": ["llm"],
            "status": "ok",
            "attempts": 1,
            "count": 1,
            "articles": [],
        }
        config_source = {
            "id": "sama-twitter",
            "type": "twitter",
            "name": "Sam Altman",
            "handle": "sama",
            "enabled": True,
            "priority": True,
            "topics": ["llm"],
        }
        article = fetch_twitter.normalize_opencli_tweet(
            {
                "id": "123",
                "author": "sama",
                "text": "A high-signal tweet.",
                "created_at": "2026-05-08T05:00:00Z",
                "likes": 1000,
                "retweets": 20,
                "replies": 3,
                "views": 5000,
                "is_retweet": False,
            },
            config_source,
            utc("2026-05-08T00:00:00Z"),
        )
        article["source_type"] = "twitter"

        score = merge_mod.calculate_base_score(article, source)

        self.assertIn("title", article)
        self.assertIn("link", article)
        self.assertIn("date", article)
        self.assertIn("metrics", article)
        self.assertGreaterEqual(score, 8)


class TestXFileCacheAndRateLimits(unittest.TestCase):
    def test_default_cache_dir_is_project_local(self):
        expected = Path(__file__).parent.parent / ".cache" / "x"
        self.assertEqual(fetch_twitter.get_x_cache_dir(), expected)

    def test_timeline_cache_ttl_defaults_to_short_window(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(fetch_twitter.get_x_timeline_cache_ttl_seconds(), 300)

    def test_timeline_cache_ttl_can_be_overridden(self):
        with patch.dict(os.environ, {"X_TIMELINE_CACHE_TTL_SECONDS": "120"}):
            self.assertEqual(fetch_twitter.get_x_timeline_cache_ttl_seconds(), 120)

    def test_source_timeline_cache_ttl_uses_source_override(self):
        source = {"id": "sama-twitter", "priority": True, "twitter_cache_ttl_seconds": 900}

        self.assertEqual(fetch_twitter.get_source_timeline_cache_ttl_seconds(source), 900)

    def test_source_timeline_cache_ttl_defaults_by_priority(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(fetch_twitter.get_source_timeline_cache_ttl_seconds({"priority": True}), 300)
            self.assertEqual(fetch_twitter.get_source_timeline_cache_ttl_seconds({"priority": False}), 1800)

    def test_source_timeline_cache_ttl_env_overrides_priority_defaults(self):
        with patch.dict(os.environ, {
            "X_PRIORITY_TIMELINE_CACHE_TTL_SECONDS": "600",
            "X_REGULAR_TIMELINE_CACHE_TTL_SECONDS": "7200",
        }):
            self.assertEqual(fetch_twitter.get_source_timeline_cache_ttl_seconds({"priority": True}), 600)
            self.assertEqual(fetch_twitter.get_source_timeline_cache_ttl_seconds({"priority": False}), 7200)

    def test_timeline_cache_entry_uses_short_ttl_when_requested(self):
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {}, clear=True):
            cache = fetch_twitter.XFileCache("official", cache_dir=Path(tmp), credential="token-a")
            cache.put(
                "GET /2/users/:id/tweets",
                {"user_id": "1", "max_results": 20},
                200,
                {},
                {"data": []},
                ttl_seconds=fetch_twitter.get_x_timeline_cache_ttl_seconds(),
            )
            index = cache.index_store.load()
            entry = next(iter(index.values()))

            self.assertEqual(entry["expires_at"] - entry["fetched_at"], 300)

    def test_gitignore_ignores_project_cache(self):
        content = (Path(__file__).parent.parent / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("/.cache/", content)

    def test_json_state_store_returns_default_for_bad_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            path.write_text("{bad json", encoding="utf-8")
            store = fetch_twitter.JsonStateStore(path, default={"ok": True})

            self.assertEqual(store.load(), {"ok": True})

    def test_json_state_store_saves_with_atomic_replace(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            store = fetch_twitter.JsonStateStore(path)

            with patch("fetch_twitter.os.replace", wraps=os.replace) as replace_mock:
                store.save({"value": 1})

            self.assertTrue(replace_mock.called)
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), {"value": 1})

    def test_file_cache_key_is_stable_for_param_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache = fetch_twitter.XFileCache("official", cache_dir=Path(tmp))

            first = cache.make_key("GET /2/users/by", {"b": 2, "a": 1})
            second = cache.make_key("GET /2/users/by", {"a": 1, "b": 2})

            self.assertEqual(first, second)

    def test_file_cache_key_is_scoped_by_credential(self):
        with tempfile.TemporaryDirectory() as tmp:
            first_cache = fetch_twitter.XFileCache("official", cache_dir=Path(tmp), credential="token-a")
            second_cache = fetch_twitter.XFileCache("official", cache_dir=Path(tmp), credential="token-b")

            first = first_cache.make_key("GET /2/users/by", {"usernames": "sama"})
            second = second_cache.make_key("GET /2/users/by", {"usernames": "sama"})

            self.assertNotEqual(first, second)

    def test_file_cache_does_not_share_bodies_between_credentials(self):
        with tempfile.TemporaryDirectory() as tmp:
            first_cache = fetch_twitter.XFileCache("official", cache_dir=Path(tmp), credential="token-a")
            second_cache = fetch_twitter.XFileCache("official", cache_dir=Path(tmp), credential="token-b")
            first_cache.put("GET /2/users/by", {"usernames": "sama"}, 200, {}, {"data": [{"id": "1"}]})

            self.assertIsNone(second_cache.get("GET /2/users/by", {"usernames": "sama"}))

    def test_file_cache_returns_fresh_response(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache = fetch_twitter.XFileCache("official", cache_dir=Path(tmp))
            cache.put("GET /2/users/by", {"usernames": "sama"}, 200, {}, {"data": [{"id": "1"}]})

            self.assertEqual(cache.get("GET /2/users/by", {"usernames": "sama"}), {"data": [{"id": "1"}]})

    def test_x_request_json_skips_before_network_on_cache_hit(self):
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {"X_CACHE_DIR": tmp}):
            endpoint = "GET /twitter/user/last_tweets"
            params = {"userName": "sama", "includeReplies": "false"}
            cache = fetch_twitter.get_x_file_cache("twitterapiio", credential="token-a")
            cache.put(endpoint, params, 200, {}, {"data": {"tweets": []}})
            before_network = MagicMock()

            result = fetch_twitter.x_request_json(
                "twitterapiio",
                endpoint,
                "https://api.twitterapi.io/twitter/user/last_tweets",
                {},
                params,
                credential="token-a",
                before_network=before_network,
            )

            self.assertEqual(result, {"data": {"tweets": []}})
            before_network.assert_not_called()

    def test_x_request_json_runs_before_network_on_cache_miss(self):
        class FakeResponse:
            status = 200
            headers = {}

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def read(self):
                return b'{"data": {"tweets": []}}'

        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {"X_CACHE_DIR": tmp}):
            before_network = MagicMock()
            with patch("fetch_twitter.urlopen", return_value=FakeResponse()):
                result = fetch_twitter.x_request_json(
                    "twitterapiio",
                    "GET /twitter/user/last_tweets",
                    "https://api.twitterapi.io/twitter/user/last_tweets",
                    {},
                    {"userName": "sama", "includeReplies": "false"},
                    credential="token-a",
                    before_network=before_network,
                )

            self.assertEqual(result, {"data": {"tweets": []}})
            before_network.assert_called_once_with()

    def test_file_cache_does_not_store_200_error_payloads(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache = fetch_twitter.XFileCache("getxapi", cache_dir=Path(tmp))
            cache.put("GET /twitter/user/tweets", {"userName": "sama"}, 200, {}, {"error": "temporary provider failure"})

            self.assertIsNone(cache.get("GET /twitter/user/tweets", {"userName": "sama"}))
            self.assertEqual(cache.index_store.load(), {})

    def test_file_cache_does_not_store_200_errors_list_payloads(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache = fetch_twitter.XFileCache("official", cache_dir=Path(tmp))
            cache.put("GET /2/users/by", {"usernames": "sama"}, 200, {}, {"errors": [{"detail": "denied"}]})

            self.assertIsNone(cache.get("GET /2/users/by", {"usernames": "sama"}))
            self.assertEqual(cache.index_store.load(), {})

    def test_file_cache_hit_survives_access_time_save_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache = fetch_twitter.XFileCache("official", cache_dir=Path(tmp))
            cache.put("GET /2/users/by", {"usernames": "sama"}, 200, {}, {"data": [{"id": "1"}]})

            with patch.object(cache.index_store, "save", side_effect=OSError("read-only filesystem")):
                with self.assertLogs(level="WARNING") as logs:
                    body = cache.get("GET /2/users/by", {"usernames": "sama"})

            self.assertEqual(body, {"data": [{"id": "1"}]})
            self.assertTrue(any("Failed to persist X response cache access time" in line for line in logs.output))

    def test_file_cache_misses_expired_response(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache = fetch_twitter.XFileCache("official", cache_dir=Path(tmp))
            cache.put("GET /2/users/by", {"usernames": "sama"}, 200, {}, {"data": []}, ttl_seconds=-1)

            self.assertIsNone(cache.get("GET /2/users/by", {"usernames": "sama"}))

    def test_file_cache_rejects_index_paths_outside_cache_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache_dir = Path(tmp) / "cache"
            outside_path = Path(tmp) / "outside.json"
            outside_path.write_text(json.dumps({"body": {"data": "leaked"}}), encoding="utf-8")
            cache = fetch_twitter.XFileCache("official", cache_dir=cache_dir, credential="token-a")
            cache_key = cache.make_key("GET /2/users/by", {"usernames": "sama"})
            cache.index_store.save({
                cache_key: {
                    "path": "../outside.json",
                    "expires_at": int(fetch_twitter.time.time()) + 3600,
                }
            })

            self.assertIsNone(cache.get("GET /2/users/by", {"usernames": "sama"}))

    def test_cache_janitor_does_not_delete_index_paths_outside_cache_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache_dir = Path(tmp) / "cache"
            outside_path = Path(tmp) / "outside.json"
            outside_path.write_text("keep", encoding="utf-8")
            store = fetch_twitter.JsonStateStore(cache_dir / "cache_index.json")
            store.save({
                "bad": {
                    "path": "../outside.json",
                    "fetched_at": 1,
                    "expires_at": 1,
                    "size": 4,
                    "last_accessed_at": 1,
                }
            })

            fetch_twitter.XCacheJanitor(cache_dir=cache_dir).cleanup()

            self.assertTrue(outside_path.exists())
            self.assertEqual(store.load(), {})

    def test_no_cache_disables_response_read_and_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache = fetch_twitter.XFileCache("official", cache_dir=Path(tmp), no_cache=True)
            cache.put("GET /2/users/by", {"usernames": "sama"}, 200, {}, {"data": []})

            self.assertIsNone(cache.get("GET /2/users/by", {"usernames": "sama"}))
            self.assertFalse((Path(tmp) / "responses").exists())

    def test_oversized_cache_entry_is_not_written(self):
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {"X_CACHE_MAX_ENTRY_BYTES": "64"}):
            cache = fetch_twitter.XFileCache("official", cache_dir=Path(tmp))
            cache.put("GET /2/users/by", {"usernames": "sama"}, 200, {}, {"data": "x" * 1000})

            self.assertEqual(cache.index_store.load(), {})

    def test_cache_entry_size_cap_uses_written_json_size(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache = fetch_twitter.XFileCache("official", cache_dir=Path(tmp))
            endpoint = "GET /2/users/by"
            params = {"usernames": "sama"}
            body = {"data": "x" * 120}
            current = 1000
            ttl = 3600
            payload = {
                "backend": "official",
                "credential_id": "anonymous",
                "endpoint": endpoint,
                "params": params,
                "status_code": 200,
                "headers": {},
                "body": body,
                "fetched_at": current,
                "expires_at": current + ttl,
            }
            compact_size = len(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8"))
            written_size = len(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8"))
            self.assertGreater(written_size, compact_size)

            with patch.dict(os.environ, {"X_CACHE_MAX_ENTRY_BYTES": str(compact_size)}):
                with patch("fetch_twitter.time.time", return_value=current):
                    cache.put(endpoint, params, 200, {}, body, ttl_seconds=ttl)

            self.assertEqual(cache.index_store.load(), {})

    def test_response_cache_persistence_failure_is_non_fatal(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache = fetch_twitter.XFileCache("official", cache_dir=Path(tmp))
            with patch("fetch_twitter._atomic_json_write", side_effect=OSError("disk full")):
                with self.assertLogs(level="WARNING") as logs:
                    cache.put("GET /2/users/by", {"usernames": "sama"}, 200, {}, {"data": []})

            self.assertTrue(any("Failed to persist X response cache entry" in line for line in logs.output))

    def test_cache_janitor_removes_entries_older_than_retention(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache_dir = Path(tmp)
            cache = fetch_twitter.XFileCache("official", cache_dir=cache_dir)
            cache.put("GET /2/users/by", {"usernames": "old"}, 200, {}, {"data": []})
            key = cache.make_key("GET /2/users/by", {"usernames": "old"})
            index = cache.index_store.load()
            index[key]["fetched_at"] = int(fetch_twitter.time.time()) - (31 * 86400)
            index[key]["expires_at"] = int(fetch_twitter.time.time()) + 86400
            cache.index_store.save(index)

            fetch_twitter.XCacheJanitor(cache_dir=cache_dir).cleanup()

            self.assertEqual(cache.index_store.load(), {})

    def test_cache_janitor_removes_oldest_entries_when_over_budget(self):
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {"X_CACHE_MAX_BYTES": "450"}):
            cache_dir = Path(tmp)
            cache = fetch_twitter.XFileCache("official", cache_dir=cache_dir)
            cache.put("GET /2/users/by", {"usernames": "old"}, 200, {}, {"data": "x" * 80})
            cache.put("GET /2/users/by", {"usernames": "new"}, 200, {}, {"data": "y" * 80})
            old_key = cache.make_key("GET /2/users/by", {"usernames": "old"})
            new_key = cache.make_key("GET /2/users/by", {"usernames": "new"})
            index = cache.index_store.load()
            index[old_key]["last_accessed_at"] = 1
            index[new_key]["last_accessed_at"] = 2
            cache.index_store.save(index)

            fetch_twitter.XCacheJanitor(cache_dir=cache_dir).cleanup()
            remaining = cache.index_store.load()

            self.assertNotIn(old_key, remaining)
            self.assertIn(new_key, remaining)

    def test_cache_janitor_keeps_expired_index_entry_when_unlink_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache_dir = Path(tmp)
            cache = fetch_twitter.XFileCache("official", cache_dir=cache_dir)
            cache.put("GET /2/users/by", {"usernames": "old"}, 200, {}, {"data": []})
            key = cache.make_key("GET /2/users/by", {"usernames": "old"})
            index = cache.index_store.load()
            index[key]["fetched_at"] = int(fetch_twitter.time.time()) - (31 * 86400)
            index[key]["expires_at"] = int(fetch_twitter.time.time()) + 86400
            cache.index_store.save(index)

            with patch("pathlib.Path.unlink", side_effect=OSError("permission denied")):
                fetch_twitter.XCacheJanitor(cache_dir=cache_dir).cleanup()

            remaining = cache.index_store.load()
            self.assertIn(key, remaining)

    def test_cache_janitor_keeps_expired_index_entry_when_unlink_and_stat_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache_dir = Path(tmp)
            cache = fetch_twitter.XFileCache("official", cache_dir=cache_dir)
            cache.put("GET /2/users/by", {"usernames": "old"}, 200, {}, {"data": []})
            key = cache.make_key("GET /2/users/by", {"usernames": "old"})
            index = cache.index_store.load()
            index[key]["fetched_at"] = int(fetch_twitter.time.time()) - (31 * 86400)
            index[key]["expires_at"] = int(fetch_twitter.time.time()) + 86400
            cache.index_store.save(index)
            target_path = (cache_dir / index[key]["path"]).resolve()
            original_exists = Path.exists
            original_stat = Path.stat

            def exists_before_unlink(path_self, *args, **kwargs):
                if path_self == target_path:
                    return True
                return original_exists(path_self, *args, **kwargs)

            def stat_with_race(path_self, *args, **kwargs):
                if path_self == target_path:
                    raise FileNotFoundError("raced")
                return original_stat(path_self, *args, **kwargs)

            with patch("pathlib.Path.unlink", side_effect=OSError("permission denied")):
                with patch("pathlib.Path.exists", autospec=True, side_effect=exists_before_unlink):
                    with patch("pathlib.Path.stat", autospec=True, side_effect=stat_with_race):
                        with patch("fetch_twitter.logging.warning") as warning_mock:
                            fetch_twitter.XCacheJanitor(cache_dir=cache_dir).cleanup()

            remaining = cache.index_store.load()
            self.assertIn(key, remaining)
            self.assertEqual(remaining[key]["size"], index[key]["size"])
            self.assertFalse(
                any(
                    call.args and str(call.args[0]).startswith("X cache cleanup failed")
                    for call in warning_mock.call_args_list
                )
            )

    def test_cache_janitor_keeps_over_budget_index_entry_when_unlink_fails(self):
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {"X_CACHE_MAX_BYTES": "450"}):
            cache_dir = Path(tmp)
            cache = fetch_twitter.XFileCache("official", cache_dir=cache_dir)
            cache.put("GET /2/users/by", {"usernames": "old"}, 200, {}, {"data": "x" * 80})
            cache.put("GET /2/users/by", {"usernames": "new"}, 200, {}, {"data": "y" * 80})
            old_key = cache.make_key("GET /2/users/by", {"usernames": "old"})
            index = cache.index_store.load()
            index[old_key]["last_accessed_at"] = 1
            cache.index_store.save(index)

            with patch("pathlib.Path.unlink", side_effect=OSError("permission denied")):
                fetch_twitter.XCacheJanitor(cache_dir=cache_dir).cleanup()

            remaining = cache.index_store.load()
            self.assertIn(old_key, remaining)

    def test_rate_limit_manager_pauses_429_until_reset(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = fetch_twitter.XRateLimitManager(cache_dir=Path(tmp), now_func=lambda: 1000)
            manager.update_from_headers(
                "official",
                "GET /2/users/:id/tweets",
                "secret-token",
                {
                    "x-rate-limit-limit": "15",
                    "x-rate-limit-remaining": "0",
                    "x-rate-limit-reset": "1300",
                },
                status_code=429,
            )

            allowed, deferred_until = manager.can_request(
                "official",
                "GET /2/users/:id/tweets",
                "secret-token",
                now=1001,
            )

            self.assertFalse(allowed)
            self.assertEqual(deferred_until, 1300)

    def test_rate_limit_manager_uses_retry_after_when_reset_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = fetch_twitter.XRateLimitManager(cache_dir=Path(tmp), now_func=lambda: 1000)
            manager.update_from_headers(
                "getxapi",
                "GET /twitter/user/tweets",
                "secret-token",
                {
                    "retry-after": "30",
                },
                status_code=429,
            )

            allowed, deferred_until = manager.can_request(
                "getxapi",
                "GET /twitter/user/tweets",
                "secret-token",
                now=1001,
            )

            self.assertFalse(allowed)
            self.assertEqual(deferred_until, 1030)

    def test_rate_limit_manager_uses_short_fallback_when_429_has_no_retry_headers(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = fetch_twitter.XRateLimitManager(cache_dir=Path(tmp), now_func=lambda: 1000)
            manager.update_from_headers(
                "getxapi",
                "GET /twitter/user/tweets",
                "secret-token",
                {},
                status_code=429,
            )

            allowed, deferred_until = manager.can_request(
                "getxapi",
                "GET /twitter/user/tweets",
                "secret-token",
                now=1001,
            )

            self.assertFalse(allowed)
            self.assertEqual(deferred_until, 1060)

    def test_rate_limit_persistence_failure_is_non_fatal(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = fetch_twitter.XRateLimitManager(cache_dir=Path(tmp), now_func=lambda: 1000)
            with patch.object(manager.store, "save", side_effect=OSError("read-only filesystem")):
                with self.assertLogs(level="WARNING") as logs:
                    manager.update_from_headers(
                        "official",
                        "GET /2/users/:id/tweets",
                        "secret-token",
                        {
                            "x-rate-limit-limit": "15",
                            "x-rate-limit-remaining": "14",
                            "x-rate-limit-reset": "1300",
                        },
                        status_code=200,
                    )

            self.assertTrue(any("Failed to persist X rate-limit state" in line for line in logs.output))

    def test_file_cache_instances_share_index_lock_for_same_cache_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = fetch_twitter.XFileCache("official", cache_dir=Path(tmp), credential="token-a")
            second = fetch_twitter.XFileCache("official", cache_dir=Path(tmp), credential="token-b")

            self.assertIs(first._lock, second._lock)

    def test_rate_limit_managers_share_lock_for_same_cache_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = fetch_twitter.XRateLimitManager(cache_dir=Path(tmp), now_func=lambda: 1000)
            second = fetch_twitter.XRateLimitManager(cache_dir=Path(tmp), now_func=lambda: 1000)

            self.assertIs(first._lock, second._lock)

    def test_get_x_file_cache_reuses_instances_for_same_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = fetch_twitter.get_x_file_cache("official", cache_dir=Path(tmp), credential="token-a")
            second = fetch_twitter.get_x_file_cache("official", cache_dir=Path(tmp), credential="token-a")
            other = fetch_twitter.get_x_file_cache("official", cache_dir=Path(tmp), credential="token-b")

            self.assertIs(first, second)
            self.assertIsNot(first, other)

    def test_get_x_rate_limit_manager_reuses_instances_for_same_cache_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = fetch_twitter.get_x_rate_limit_manager(cache_dir=Path(tmp))
            second = fetch_twitter.get_x_rate_limit_manager(cache_dir=Path(tmp))

            self.assertIs(first, second)
