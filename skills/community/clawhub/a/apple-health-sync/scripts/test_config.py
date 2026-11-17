import json
import os
import secrets
import unittest
from pathlib import Path
from urllib import error, request

from config import ALLOWED_RELAY_URLS, APP_CONFIG, RejectRelayRedirects, load_effective_config, validate_relay_url


class ConfigSecurityTests(unittest.TestCase):
    def test_declared_relay_urls_are_allowed(self) -> None:
        for relay_url in ALLOWED_RELAY_URLS:
            self.assertEqual(validate_relay_url(relay_url), relay_url)

    def test_other_hosts_paths_and_queries_are_rejected(self) -> None:
        rejected_urls = (
            "https://example.com/functions/v1/get-data-v2",
            "http://snpiylxajnxpklpwdtdg.supabase.co/functions/v1/get-data-v2",
            "https://snpiylxajnxpklpwdtdg.supabase.co/functions/v1/unexpected",
            "https://snpiylxajnxpklpwdtdg.supabase.co/functions/v1/get-data-v2?redirect=1",
        )

        for relay_url in rejected_urls:
            with self.subTest(relay_url=relay_url):
                with self.assertRaisesRegex(RuntimeError, "undeclared relay URL"):
                    validate_relay_url(relay_url)

    def test_relay_redirects_are_rejected_before_following_target(self) -> None:
        relay_url = next(iter(ALLOWED_RELAY_URLS))
        relay_request = request.Request(relay_url)

        with self.assertRaisesRegex(error.HTTPError, "Relay redirects are not allowed"):
            RejectRelayRedirects().redirect_request(
                relay_request,
                None,
                302,
                "Found",
                {},
                "https://example.com/collect",
            )

    def test_user_config_cannot_override_app_owned_relay_url(self) -> None:
        runtime_dir = Path("/tmp") / f"ahs-config-test-{secrets.token_hex(8)}"
        config_dir = runtime_dir / "config"
        config_dir.mkdir(mode=0o700, parents=True)
        config_path = config_dir / "config.json"
        config_path.write_text(
            json.dumps(
                {
                    "user_id": "ahs_test",
                    "storage": "sqlite",
                    "supabase_get_data_url": "https://example.com/collect",
                }
            ),
            encoding="utf-8",
        )
        os.chmod(config_path, 0o644)
        try:
            _, effective_config = load_effective_config(runtime_dir)
            self.assertEqual(effective_config["supabase_get_data_url"], APP_CONFIG["supabase_get_data_url"])
            self.assertEqual(config_path.stat().st_mode & 0o777, 0o600)
        finally:
            config_path.unlink(missing_ok=True)
            config_dir.rmdir()
            runtime_dir.rmdir()


if __name__ == "__main__":
    unittest.main()
