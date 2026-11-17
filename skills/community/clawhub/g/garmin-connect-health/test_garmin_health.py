import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import garmin_health


class GarminAuthenticationTests(unittest.TestCase):
    def test_existing_native_tokenstore_is_reused_without_credentials(self):
        with tempfile.TemporaryDirectory() as tmp:
            tokenstore = Path(tmp)
            (tokenstore / "garmin_tokens.json").write_text("{}", encoding="utf-8")
            client = Mock()
            client.display_name = "demo-user"

            with (
                patch.object(garmin_health, "TOKENSTORE", str(tokenstore)),
                patch.object(garmin_health, "Garmin", return_value=client) as garmin,
                patch.object(garmin_health, "_load_credentials") as load_credentials,
            ):
                result = garmin_health.get_client()

            self.assertIs(result, client)
            garmin.assert_called_once_with(is_cn=False)
            client.login.assert_called_once_with(str(tokenstore))
            load_credentials.assert_not_called()

    def test_invalid_tokenstore_falls_back_to_native_mfa_login(self):
        with tempfile.TemporaryDirectory() as tmp:
            tokenstore = Path(tmp)
            (tokenstore / "garmin_tokens.json").write_text("{}", encoding="utf-8")
            cached_client = Mock()
            cached_client.login.side_effect = RuntimeError("stale token")
            credential_client = Mock()

            with (
                patch.object(garmin_health, "TOKENSTORE", str(tokenstore)),
                patch.object(
                    garmin_health,
                    "Garmin",
                    side_effect=[cached_client, credential_client],
                ) as garmin,
                patch.object(garmin_health, "_load_credentials", return_value=("user@example.com", "secret")),
                patch.object(garmin_health.time, "sleep"),
            ):
                result = garmin_health.get_client()

            self.assertIs(result, credential_client)
            self.assertEqual(cached_client.login.call_count, 3)
            _, kwargs = garmin.call_args
            self.assertEqual(kwargs["email"], "user@example.com")
            self.assertEqual(kwargs["password"], "secret")
            self.assertTrue(callable(kwargs["prompt_mfa"]))
            credential_client.login.assert_called_once_with(str(tokenstore))


if __name__ == "__main__":
    unittest.main()
