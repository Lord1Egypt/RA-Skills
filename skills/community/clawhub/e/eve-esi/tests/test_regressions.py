import importlib
import os
import sys
import tempfile
import threading
import time
import unittest
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


if __name__ == "__main__":
    unittest.main()
