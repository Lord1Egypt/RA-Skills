import argparse
import email.message
import importlib
import io
import json
import os
import sys
import tempfile
import threading
import time
import unittest
import urllib.error
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


def import_fresh(module_name: str):
    sys.modules.pop(module_name, None)
    return importlib.import_module(module_name)


class ValidateConfigRegressionTests(unittest.TestCase):
    def test_validate_config_flags_schema_violations(self):
        validate_config = import_fresh("validate_config")

        config = {
            "schema_version": "1.0",
            "notification_channels": {
                "telegram": {
                    "bot_token": "token",
                    "chat_id": "chat",
                }
            },
            "characters": [
                {
                    "id": "not-an-int",
                    "token": "token",
                    "refresh_token": "refresh",
                    "client_id": "client",
                    "scopes": ["esi-wallet.read_character_wallet.v1"],
                }
            ],
            "alerts": {
                "channels": ["slack"],
            },
            "unexpected_top_level": True,
        }

        result = validate_config.validate_config(config)

        self.assertTrue(
            any("unexpected_top_level" in error for error in result.errors),
            result.errors,
        )
        self.assertTrue(
            any("alerts.channels[0]" in error for error in result.errors),
            result.errors,
        )
        self.assertTrue(
            any("characters[0].id" in error for error in result.errors),
            result.errors,
        )

    def test_validate_scope_coverage_respects_character_filter(self):
        validate_config = import_fresh("validate_config")

        config = {
            "schema_version": "1.0",
            "notification_channels": {
                "telegram": {
                    "bot_token": "token",
                    "chat_id": "chat",
                }
            },
            "characters": [
                {
                    "id": 1,
                    "name": "A",
                    "token": "token",
                    "refresh_token": "refresh",
                    "client_id": "client",
                    "scopes": ["esi-wallet.read_character_wallet.v1"],
                },
                {
                    "id": 2,
                    "name": "B",
                    "token": "token",
                    "refresh_token": "refresh",
                    "client_id": "client",
                    "scopes": ["esi-skills.read_skills.v1"],
                },
            ],
            "alerts": {
                "rules": [
                    {
                        "type": "wallet_large_deposit",
                        "character_filter": [1],
                    }
                ]
            },
        }

        result = validate_config.validate_config(config)

        self.assertFalse(
            any("Character 'B'" in warning for warning in result.warnings),
            result.warnings,
        )


class TokenStoreRegressionTests(unittest.TestCase):
    def test_save_tokens_waits_for_existing_lock(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["OPENCLAW_STATE_DIR"] = tmpdir
            token_store = import_fresh("token_store")

            finished = threading.Event()

            def writer():
                try:
                    token_store.save_tokens({"characters": {"main": {"refresh_token": "r"}}})
                finally:
                    finished.set()

            with token_store.token_file_lock():
                thread = threading.Thread(target=writer)
                thread.start()
                time.sleep(0.2)
                self.assertFalse(finished.is_set(), "save_tokens should wait for lock release")

            thread.join(timeout=1.0)
            self.assertTrue(finished.is_set(), "save_tokens should finish after lock release")


class AuthFlowRegressionTests(unittest.TestCase):
    def test_main_wraps_server_start_errors(self):
        auth_flow = import_fresh("auth_flow")

        with mock.patch.object(sys, "argv", ["auth_flow.py", "--client-id", "client"]):
            with mock.patch.object(
                auth_flow.http.server,
                "HTTPServer",
                side_effect=OSError("Address already in use"),
            ):
                with self.assertRaises(auth_flow.AuthFlowError):
                    auth_flow.main()


class GetTokenRegressionTests(unittest.TestCase):
    def test_main_raises_token_error_for_incomplete_character_metadata(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ["OPENCLAW_STATE_DIR"] = tmpdir
            get_token = import_fresh("get_token")
            token_file = Path(tmpdir) / "eve-tokens.json"
            token_file.write_text(
                '{"characters":{"main":{"character_id":1,"character_name":"Main"}}}',
                encoding="utf-8",
            )

            with mock.patch.object(sys, "argv", ["get_token.py", "--char", "main"]):
                with self.assertRaises(get_token.TokenError):
                    get_token.main()


class EsiQueryWriteGateTests(unittest.TestCase):
    """State-changing requests must not run without an explicit opt-in."""

    def setUp(self):
        self.esi_query = import_fresh("esi_query")

    def test_get_is_never_state_changing(self):
        self.assertFalse(self.esi_query.is_state_changing("GET", "/characters/1/wallet/"))

    def test_documented_bulk_lookups_are_not_state_changing(self):
        for endpoint in (
            "/universe/names/",
            "/characters/affiliation/",
            "/characters/12345/assets/names/",
            "/characters/12345/assets/locations/",
        ):
            with self.subTest(endpoint=endpoint):
                self.assertFalse(self.esi_query.is_state_changing("POST", endpoint))

    def test_undocumented_post_put_delete_are_state_changing(self):
        for method, endpoint in (
            ("POST", "/characters/12345/contacts/"),
            ("POST", "/ui/openwindow/marketdetails/"),
            ("PUT", "/characters/12345/mail/1/"),
            ("DELETE", "/characters/12345/mail/1/"),
        ):
            with self.subTest(method=method, endpoint=endpoint):
                self.assertTrue(self.esi_query.is_state_changing(method, endpoint))

    def test_main_refuses_write_without_allow_write(self):
        argv = [
            "esi_query.py", "--token", "tok",
            "--endpoint", "/characters/12345/contacts/",
            "--method", "POST", "--body", "[]",
        ]
        with mock.patch.object(sys, "argv", argv):
            with mock.patch.object(self.esi_query, "esi_request") as request:
                with self.assertRaises(SystemExit):
                    self.esi_query.main()
                request.assert_not_called()

    def test_lookalike_endpoint_does_not_bypass_gate(self):
        # A path merely containing a read-only segment must still be gated.
        self.assertTrue(
            self.esi_query.is_state_changing("POST", "/characters/affiliation/evil/")
        )


class EsiQueryTokenSourceTests(unittest.TestCase):
    """The token must be resolvable without ever landing in argv."""

    def setUp(self):
        self.esi_query = import_fresh("esi_query")

    def _args(self, **overrides):
        defaults = {"char": None, "token": None, "token_stdin": False}
        defaults.update(overrides)
        return argparse.Namespace(**defaults)

    def test_token_stdin_is_read_from_stdin(self):
        parser = argparse.ArgumentParser()
        with mock.patch.object(sys, "stdin", io.StringIO("secret-token\n")):
            token = self.esi_query.resolve_token(self._args(token_stdin=True), parser)
        self.assertEqual(token, "secret-token")

    def test_char_resolves_in_process(self):
        parser = argparse.ArgumentParser()
        fake = mock.Mock(return_value={"access_token": "fresh-token"})
        with mock.patch.dict(sys.modules, {"get_token": mock.Mock(resolve_access_token=fake)}):
            token = self.esi_query.resolve_token(self._args(char="main"), parser)
        self.assertEqual(token, "fresh-token")
        fake.assert_called_once_with("main")

    def test_conflicting_token_sources_are_rejected(self):
        parser = argparse.ArgumentParser()
        with mock.patch.object(sys, "stderr", io.StringIO()):
            with self.assertRaises(SystemExit):
                self.esi_query.resolve_token(self._args(char="main", token="tok"), parser)

    def test_argv_token_warns_about_exposure(self):
        parser = argparse.ArgumentParser()
        stderr = io.StringIO()
        with mock.patch.object(sys, "stderr", stderr):
            token = self.esi_query.resolve_token(self._args(token="tok"), parser)
        self.assertEqual(token, "tok")
        self.assertIn("argv", stderr.getvalue())


def _fake_response(body: bytes = b"{}", headers: dict | None = None):
    """Stand-in for the object urlopen() yields as a context manager."""
    resp = mock.MagicMock()
    resp.read.return_value = body
    resp.getheaders.return_value = list((headers or {}).items())
    resp.__enter__.return_value = resp
    resp.__exit__.return_value = False
    return resp


def _http_error(code: int, headers: dict):
    hdrs = email.message.Message()
    for key, value in headers.items():
        hdrs[key] = value
    return urllib.error.HTTPError(
        "https://esi.evetech.net/status/", code, "err", hdrs, io.BytesIO(b"{}")
    )


class EsiVersioningTests(unittest.TestCase):
    """ESI replaced versioned URLs with the X-Compatibility-Date header."""

    def setUp(self):
        self.esi_query = import_fresh("esi_query")

    def test_base_url_carries_no_version_segment(self):
        self.assertEqual(self.esi_query.BASE_URL, "https://esi.evetech.net")

    def test_deprecated_version_prefixes_are_stripped(self):
        for raw, expected in (
            ("/latest/status/", "/status/"),
            ("/legacy/universe/names/", "/universe/names/"),
            ("/dev/status/", "/status/"),
            ("/v5/characters/1/wallet/", "/characters/1/wallet/"),
            ("characters/1/wallet/", "/characters/1/wallet/"),
            ("/status/", "/status/"),
        ):
            with self.subTest(raw=raw):
                self.assertEqual(self.esi_query.normalize_endpoint(raw), expected)

    def test_version_prefix_is_not_confused_with_a_real_path(self):
        # /universe/ and /v.../ both start with a 'v'; only the latter is a version.
        self.assertEqual(
            self.esi_query.normalize_endpoint("/universe/types/34/"), "/universe/types/34/"
        )

    def test_prefixed_bulk_lookup_still_passes_the_write_gate(self):
        # Before the prefix was stripped, the allowlist missed these paths and
        # a documented read-only lookup was rejected as a write.
        self.assertFalse(
            self.esi_query.is_state_changing("POST", "/latest/characters/affiliation/")
        )

    def test_request_sends_compatibility_date_and_user_agent(self):
        with mock.patch("urllib.request.urlopen", return_value=_fake_response()) as urlopen:
            self.esi_query.esi_request("/status/")
        request = urlopen.call_args[0][0]
        self.assertEqual(
            request.get_header("X-compatibility-date"),
            self.esi_query.DEFAULT_COMPATIBILITY_DATE,
        )
        self.assertIn("OpenClaw-ESI-Skill/", request.get_header("User-agent"))
        self.assertEqual(request.full_url, "https://esi.evetech.net/status/")

    def test_compatibility_date_is_a_plain_iso_date(self):
        # ESI rejects anything else with a 400, which costs error-limit budget.
        self.assertRegex(self.esi_query.DEFAULT_COMPATIBILITY_DATE, r"^\d{4}-\d{2}-\d{2}$")


class EsiRateLimitTests(unittest.TestCase):
    """429 (bucket limit) and 420 (error limit) both have to be retried."""

    def setUp(self):
        self.esi_query = import_fresh("esi_query")

    def test_429_retries_after_the_retry_after_delay(self):
        error = _http_error(429, {"Retry-After": "7", "X-Ratelimit-Group": "status"})
        responses = [error, _fake_response(b'{"ok": true}')]

        def fake_urlopen(*args, **kwargs):
            item = responses.pop(0)
            if isinstance(item, Exception):
                raise item
            return item

        with mock.patch.object(sys, "stderr", io.StringIO()):
            with mock.patch("urllib.request.urlopen", side_effect=fake_urlopen):
                with mock.patch.object(self.esi_query.time, "sleep") as sleep:
                    body, _ = self.esi_query.esi_request("/status/")

        sleep.assert_called_once_with(7)
        self.assertEqual(body, {"ok": True})

    def test_429_gives_up_after_the_retry_budget(self):
        error = _http_error(429, {"Retry-After": "1"})
        with mock.patch.object(sys, "stderr", io.StringIO()):
            with mock.patch("urllib.request.urlopen", side_effect=error):
                with mock.patch.object(self.esi_query.time, "sleep"):
                    with self.assertRaises(self.esi_query.ESIRateLimitError):
                        self.esi_query.esi_request("/status/")

    def test_low_remaining_budget_warns(self):
        stderr = io.StringIO()
        headers = {
            "X-Ratelimit-Remaining": "5",
            "X-Ratelimit-Limit": "600/15m",
            "X-Ratelimit-Group": "status",
        }
        with mock.patch.object(sys, "stderr", stderr):
            with mock.patch("urllib.request.urlopen", return_value=_fake_response(headers=headers)):
                self.esi_query.esi_request("/status/")
        self.assertIn("rate limit bucket", stderr.getvalue())

    def test_healthy_budget_stays_quiet(self):
        stderr = io.StringIO()
        headers = {"X-Ratelimit-Remaining": "590", "X-Ratelimit-Limit": "600/15m"}
        with mock.patch.object(sys, "stderr", stderr):
            with mock.patch("urllib.request.urlopen", return_value=_fake_response(headers=headers)):
                self.esi_query.esi_request("/status/")
        self.assertNotIn("rate limit bucket", stderr.getvalue())


class RouteEndpointTests(unittest.TestCase):
    """Route planning became a POST with a request body at compat 2025-09-30."""

    def setUp(self):
        self.esi_query = import_fresh("esi_query")

    def test_route_is_posted_with_a_preference_body(self):
        with mock.patch.object(self.esi_query, "esi_request") as request:
            request.return_value = ({"route": [1, 2, 3]}, {})
            route = self.esi_query.get_route(30000142, 30002187, flag="secure")

        self.assertEqual(route, [1, 2, 3])
        _, kwargs = request.call_args
        self.assertEqual(kwargs["method"], "POST")
        self.assertEqual(json.loads(kwargs["body"]), {"preference": "Safer"})

    def test_cli_flags_map_onto_the_new_preference_names(self):
        for flag, expected in (
            ("shortest", "Shorter"),
            ("secure", "Safer"),
            ("insecure", "LessSecure"),
        ):
            with self.subTest(flag=flag):
                with mock.patch.object(self.esi_query, "esi_request") as request:
                    request.return_value = ({"route": []}, {})
                    self.esi_query.get_route(1, 2, flag=flag)
                self.assertEqual(
                    json.loads(request.call_args[1]["body"])["preference"], expected
                )

    def test_avoided_systems_use_the_new_field_name(self):
        with mock.patch.object(self.esi_query, "esi_request") as request:
            request.return_value = ({"route": []}, {})
            self.esi_query.get_route(1, 2, avoid=[30000138])
        self.assertEqual(
            json.loads(request.call_args[1]["body"])["avoid_systems"], [30000138]
        )

    def test_bare_array_from_an_older_date_still_parses(self):
        with mock.patch.object(self.esi_query, "esi_request") as request:
            request.return_value = ([1, 2], {})
            self.assertEqual(self.esi_query.get_route(1, 2), [1, 2])

    def test_route_post_is_not_gated_as_a_write(self):
        self.assertFalse(
            self.esi_query.is_state_changing("POST", "/route/30000142/30002187/")
        )
        self.assertTrue(self.esi_query.is_state_changing("POST", "/route/1/2/evil/"))


class UserAgentTests(unittest.TestCase):
    """CCP asks every caller to identify itself; urllib would not."""

    def test_source_url_is_marked_and_version_is_present(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            user_agent = import_fresh("user_agent")
        self.assertRegex(
            user_agent.build_user_agent(),
            r"^OpenClaw-ESI-Skill/\d+\.\d+\.\d+ \(\+https://github\.com/\S+\)$",
        )

    def test_contact_is_included_when_configured(self):
        with mock.patch.dict(os.environ, {"EVE_ESI_CONTACT": "pilot@example.com"}):
            user_agent = import_fresh("user_agent")
            self.assertIn("pilot@example.com; +https://", user_agent.build_user_agent())

    def test_sso_scripts_identify_themselves(self):
        for module_name in ("auth_flow", "get_token"):
            with self.subTest(module=module_name):
                module = import_fresh(module_name)
                self.assertTrue(module.USER_AGENT.startswith("OpenClaw-ESI-Skill/"))


if __name__ == "__main__":
    unittest.main()
