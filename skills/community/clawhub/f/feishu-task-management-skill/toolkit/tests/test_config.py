import pathlib
from urllib.parse import quote
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from feishu_task_toolkit.cli_config import build_authorize_url, parse_oauth_callback_input, run_guide
from feishu_task_toolkit.config import AppConfig, AppConfigError, ToolkitPaths, load_json, write_json


class ConfigTests(unittest.TestCase):
    def test_load_prefers_environment_over_runtime_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = pathlib.Path(temp_dir)
            paths = ToolkitPaths(root=root, config_dir=root / "config", data_dir=root / "data")
            paths.ensure()
            write_json(
                paths.config_dir / "runtime.json",
                {
                    "app_id": "file-app",
                    "app_secret": "file-secret",
                },
            )

            config = AppConfig.load(
                paths,
                environ={
                    "FEISHU_APP_ID": "env-app",
                    "FEISHU_APP_SECRET": "env-secret",
                },
            )

        self.assertEqual(config.app_id, "env-app")
        self.assertEqual(config.app_secret, "env-secret")

    def test_load_reads_local_runtime_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = pathlib.Path(temp_dir)
            paths = ToolkitPaths(root=root, config_dir=root / "config", data_dir=root / "data")
            paths.ensure()
            runtime_path = paths.config_dir / "runtime.json"
            write_json(
                runtime_path,
                {
                    "app_id": "file-app",
                    "app_secret": "file-secret",
                    "timezone": "Asia/Shanghai",
                    "default_member_open_id": "ou_default",
                },
            )

            config = AppConfig.load(paths, environ={})

        self.assertEqual(config.app_id, "file-app")
        self.assertEqual(config.app_secret, "file-secret")
        self.assertEqual(config.timezone, "Asia/Shanghai")
        self.assertEqual(config.default_member_open_id, "ou_default")
        self.assertEqual(config.user_access_token, "")

    def test_load_reads_runtime_file_with_oauth_user_tokens(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = pathlib.Path(temp_dir)
            paths = ToolkitPaths(root=root, config_dir=root / "config", data_dir=root / "data")
            paths.ensure()
            write_json(
                paths.config_dir / "runtime.json",
                {
                    "app_id": "file-app",
                    "app_secret": "file-secret",
                    "user_access_token": "u-test-token",
                    "refresh_token": "r-test-token",
                    "user_token_expires_at": "2026-03-10T18:00:00+08:00",
                    "user_scope": "task:task:write offline_access",
                    "default_member_open_id": "ou_default",
                },
            )

            config = AppConfig.load(paths, environ={})

        self.assertEqual(config.app_id, "file-app")
        self.assertEqual(config.app_secret, "file-secret")
        self.assertEqual(config.user_access_token, "u-test-token")
        self.assertEqual(config.refresh_token, "r-test-token")
        self.assertEqual(config.user_token_expires_at, "2026-03-10T18:00:00+08:00")
        self.assertEqual(config.user_scope, "task:task:write offline_access")
        self.assertEqual(config.default_member_open_id, "ou_default")

    def test_app_credentials_are_required_even_with_user_token(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = pathlib.Path(temp_dir)
            paths = ToolkitPaths(root=root, config_dir=root / "config", data_dir=root / "data")
            paths.ensure()
            write_json(paths.config_dir / "runtime.json", {"user_access_token": "u-test-token"})

            with self.assertRaises(AppConfigError) as ctx:
                AppConfig.load(paths, environ={})

        self.assertIn("FEISHU_APP_ID", str(ctx.exception))

    def test_to_public_dict_redacts_user_tokens(self) -> None:
        config = AppConfig(
            app_id="cli_x",
            app_secret="secret_x",
            user_access_token="u-1234567890",
            refresh_token="r-abcdefghij",
        )

        public = config.to_public_dict()

        self.assertNotEqual(public["user_access_token"], "u-1234567890")
        self.assertNotEqual(public["refresh_token"], "r-abcdefghij")

    def test_missing_config_error_contains_consent_guidance(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = pathlib.Path(temp_dir)
            paths = ToolkitPaths(root=root, config_dir=root / "config", data_dir=root / "data")
            paths.ensure()

            with self.assertRaises(AppConfigError) as ctx:
                AppConfig.load(paths, environ={})

        self.assertIn("FEISHU_APP_ID", str(ctx.exception))
        self.assertIn("runtime.json", str(ctx.exception))

    def test_interactive_guide_writes_runtime_config_and_runs_sync(self) -> None:
        prompts = iter(["cli_test", "n", "ou_default", "y", "y"])
        secret_prompts = iter(["secret_test"])
        outputs: list[str] = []
        sync_calls: list[ToolkitPaths] = []

        with tempfile.TemporaryDirectory() as temp_dir:
            root = pathlib.Path(temp_dir)
            paths = ToolkitPaths(root=root, config_dir=root / "config", data_dir=root / "data")
            paths.ensure()

            exit_code = run_guide(
                paths=paths,
                input_fn=lambda _prompt="": next(prompts),
                secret_input_fn=lambda _prompt="": next(secret_prompts),
                print_fn=outputs.append,
                sync_fn=lambda passed_paths: sync_calls.append(passed_paths) or {"member_count": 2},
            )

            runtime = load_json(paths.runtime_config_file, {})

        self.assertEqual(exit_code, 0)
        self.assertEqual(runtime["app_id"], "cli_test")
        self.assertEqual(runtime["app_secret"], "secret_test")
        self.assertEqual(runtime["base_url"], "https://open.feishu.cn/open-apis")
        self.assertEqual(runtime["timezone"], "Asia/Shanghai")
        self.assertEqual(runtime["default_member_open_id"], "ou_default")
        self.assertEqual(runtime["user_access_token"], "")
        self.assertEqual(len(sync_calls), 1)
        self.assertTrue(any("成员同步完成" in line for line in outputs))

    def test_interactive_guide_builds_authorize_url_and_exchanges_callback_url(self) -> None:
        callback = "https://example.com/feishu/oauth/callback?code=oauth-code&state=fixed-state"
        prompts = iter(
            [
                "cli_test",
                "y",
                "",
                callback,
                "ou_default",
                "y",
                "n",
            ]
        )
        secret_prompts = iter(["secret_test"])
        outputs: list[str] = []

        with tempfile.TemporaryDirectory() as temp_dir:
            root = pathlib.Path(temp_dir)
            paths = ToolkitPaths(root=root, config_dir=root / "config", data_dir=root / "data")
            paths.ensure()

            exit_code = run_guide(
                paths=paths,
                input_fn=lambda _prompt="": next(prompts),
                secret_input_fn=lambda _prompt="": next(secret_prompts),
                print_fn=outputs.append,
                state_fn=lambda: "fixed-state",
                exchange_code_fn=lambda app_id, app_secret, code, redirect_uri, code_verifier: {
                    "access_token": f"{app_id}:{code}",
                    "refresh_token": f"{app_secret}:refresh",
                    "expires_in": 7200,
                    "refresh_token_expires_in": 604800,
                    "scope": "task:task:read task:task:write",
                },
                sync_fn=lambda _passed_paths: {"member_count": 0},
            )

            runtime = load_json(paths.runtime_config_file, {})

        self.assertEqual(exit_code, 0)
        self.assertEqual(runtime["app_id"], "cli_test")
        self.assertEqual(runtime["app_secret"], "secret_test")
        self.assertEqual(runtime["user_access_token"], "cli_test:oauth-code")
        self.assertEqual(runtime["refresh_token"], "secret_test:refresh")
        self.assertEqual(runtime["user_scope"], "task:task:read task:task:write")
        self.assertTrue(runtime["user_token_expires_at"])
        self.assertEqual(runtime["default_member_open_id"], "ou_default")
        self.assertTrue(any("授权链接" in line for line in outputs))
        self.assertTrue(any("https://example.com/feishu/oauth/callback" in line for line in outputs))
        self.assertTrue(any("已跳过成员同步" in line for line in outputs))

    def test_interactive_guide_uses_default_redirect_uri(self) -> None:
        callback = "https://example.com/feishu/oauth/callback?code=oauth-code&state=fixed-state"
        prompts = iter(["cli_test", "y", "", callback, "ou_default", "y", "n"])
        secret_prompts = iter(["secret_test"])
        outputs: list[str] = []

        with tempfile.TemporaryDirectory() as temp_dir:
            root = pathlib.Path(temp_dir)
            paths = ToolkitPaths(root=root, config_dir=root / "config", data_dir=root / "data")
            paths.ensure()

            exit_code = run_guide(
                paths=paths,
                input_fn=lambda _prompt="": next(prompts),
                secret_input_fn=lambda _prompt="": next(secret_prompts),
                print_fn=outputs.append,
                state_fn=lambda: "fixed-state",
                exchange_code_fn=lambda app_id, app_secret, code, redirect_uri, code_verifier: {
                    "access_token": f"{app_id}:{code}",
                    "refresh_token": "",
                    "expires_in": 7200,
                    "scope": "task:task:read task:task:write",
                },
                sync_fn=lambda _passed_paths: {"member_count": 0},
            )

        self.assertEqual(exit_code, 0)
        self.assertTrue(any("https://example.com/feishu/oauth/callback" in line for line in outputs))

    def test_interactive_guide_can_abort_without_writing(self) -> None:
        prompts = iter(["cli_test", "n", "", "n"])
        secret_prompts = iter(["secret_test"])
        outputs: list[str] = []

        with tempfile.TemporaryDirectory() as temp_dir:
            root = pathlib.Path(temp_dir)
            paths = ToolkitPaths(root=root, config_dir=root / "config", data_dir=root / "data")
            paths.ensure()

            exit_code = run_guide(
                paths=paths,
                input_fn=lambda _prompt="": next(prompts),
                secret_input_fn=lambda _prompt="": next(secret_prompts),
                print_fn=outputs.append,
                sync_fn=lambda _paths: {"member_count": 0},
            )

            exists = paths.runtime_config_file.exists()

        self.assertEqual(exit_code, 1)
        self.assertFalse(exists)
        self.assertTrue(any("已取消写入" in line for line in outputs))

    def test_interactive_guide_handles_ctrl_c_cleanly(self) -> None:
        outputs: list[str] = []

        with tempfile.TemporaryDirectory() as temp_dir:
            root = pathlib.Path(temp_dir)
            paths = ToolkitPaths(root=root, config_dir=root / "config", data_dir=root / "data")
            paths.ensure()

            exit_code = run_guide(
                paths=paths,
                input_fn=lambda _prompt="": (_ for _ in ()).throw(KeyboardInterrupt()),
                secret_input_fn=lambda _prompt="": "unused",
                print_fn=outputs.append,
                sync_fn=lambda _paths: {"member_count": 0},
            )

            exists = paths.runtime_config_file.exists()

        self.assertEqual(exit_code, 130)
        self.assertFalse(exists)
        self.assertTrue(any("已取消配置向导" in line for line in outputs))

    def test_build_authorize_url_uses_expected_query_parameters(self) -> None:
        url = build_authorize_url(
            client_id="cli_test",
            redirect_uri="https://example.com/feishu/oauth/callback",
            scope="task:task:read task:task:write",
            state="fixed-state",
        )

        self.assertIn("client_id=cli_test", url)
        self.assertIn("response_type=code", url)
        self.assertIn(f"redirect_uri={quote('https://example.com/feishu/oauth/callback', safe='')}", url)
        self.assertIn("scope=task%3Atask%3Aread+task%3Atask%3Awrite", url)
        self.assertIn("state=fixed-state", url)

    def test_parse_oauth_callback_input_accepts_callback_url(self) -> None:
        code = parse_oauth_callback_input(
            "https://example.com/feishu/oauth/callback?code=oauth-code&state=fixed-state",
            expected_state="fixed-state",
        )

        self.assertEqual(code, "oauth-code")

    def test_parse_oauth_callback_input_rejects_raw_code(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            parse_oauth_callback_input("oauth-code", expected_state="fixed-state")

        self.assertIn("callback", str(ctx.exception))

    def test_parse_oauth_callback_input_rejects_state_mismatch(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            parse_oauth_callback_input(
                "https://example.com/feishu/oauth/callback?code=oauth-code&state=wrong-state",
                expected_state="fixed-state",
            )

        self.assertIn("state", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
