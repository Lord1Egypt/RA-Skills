import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from feishu_task_toolkit.config import AppConfig
from feishu_task_toolkit.http import FeishuHttpClient


class HttpClientTests(unittest.TestCase):
    def test_get_tenant_access_token_fetches_and_caches_token(self) -> None:
        client = FeishuHttpClient(AppConfig(app_id="cli_x", app_secret="secret_x"))
        calls = []

        def fake_request(method, path, params=None, body=None, use_auth=True):
            calls.append((method, path, use_auth))
            return {"tenant_access_token": "t-123"}

        client.request = fake_request  # type: ignore[method-assign]

        first = client.get_tenant_access_token()
        second = client.get_tenant_access_token()

        self.assertEqual(first, "t-123")
        self.assertEqual(second, "t-123")
        self.assertEqual(calls, [("POST", "/auth/v3/tenant_access_token/internal", False)])

    def test_task_endpoints_prefer_configured_user_token(self) -> None:
        client = FeishuHttpClient(AppConfig(app_id="cli_x", app_secret="secret_x", user_access_token="u-123456"))

        self.assertEqual(client.get_auth_token_for_path("/task/v2/tasks"), "u-123456")

    def test_contact_endpoints_use_tenant_token_even_when_user_token_exists(self) -> None:
        client = FeishuHttpClient(AppConfig(app_id="cli_x", app_secret="secret_x", user_access_token="u-123456"))

        def fake_request(method, path, params=None, body=None, use_auth=True):
            if path != "/auth/v3/tenant_access_token/internal":
                raise AssertionError(f"unexpected path: {path}")
            return {"tenant_access_token": "t-123"}

        client.request = fake_request  # type: ignore[method-assign]

        self.assertEqual(client.get_auth_token_for_path("/contact/v3/scopes"), "t-123")

    def test_task_endpoints_fall_back_to_tenant_token_without_user_token(self) -> None:
        client = FeishuHttpClient(AppConfig(app_id="cli_x", app_secret="secret_x"))

        def fake_request(method, path, params=None, body=None, use_auth=True):
            if path != "/auth/v3/tenant_access_token/internal":
                raise AssertionError(f"unexpected path: {path}")
            return {"tenant_access_token": "t-123"}

        client.request = fake_request  # type: ignore[method-assign]

        self.assertEqual(client.get_auth_token_for_path("/task/v2/tasks"), "t-123")


if __name__ == "__main__":
    unittest.main()
