import json
import os
import sys
import unittest
from contextlib import redirect_stdout
from importlib.util import module_from_spec, spec_from_file_location
from io import StringIO
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parent.parent / "scripts" / "alapi.py"


class AlapiCliTests(unittest.TestCase):
    def _load_module(self):
        spec = spec_from_file_location("alapi_cli", SCRIPT_PATH)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def _run_main_with_stub(self, args, stub_result):
        module = self._load_module()

        def fake_request(url, method="GET", data=None, headers=None):
            return json.loads(json.dumps(stub_result, ensure_ascii=False))

        module._request = fake_request
        stdout = StringIO()
        old_argv = sys.argv
        try:
            sys.argv = ["alapi.py"] + args
            with redirect_stdout(stdout):
                module.main()
        finally:
            sys.argv = old_argv
        return stdout.getvalue()

    def test_search_json_outputs_machine_readable_payload(self):
        stub = {
            "success": True,
            "data": {
                "list": [
                    {
                        "id": 27,
                        "name": "IP 查询",
                        "description": "查询 IP 地址归属地",
                    }
                ]
            },
        }

        output = self._run_main_with_stub(["--json", "search", "IP"], stub)
        payload = json.loads(output)
        self.assertEqual(payload["command"], "search")
        self.assertEqual(payload["keyword"], "IP")
        self.assertEqual(payload["count"], 1)
        self.assertEqual(payload["items"][0]["id"], 27)
        self.assertIn("/api/27/introduction", payload["items"][0]["doc_url"])

    def test_call_json_wraps_live_response(self):
        stub = {
            "success": True,
            "code": 200,
            "message": "success",
            "data": {"city": "Shanghai"},
        }

        output = self._run_main_with_stub(
            ["--json", "call", "ip", "--token", "secret", "--param", "ip=8.8.8.8"],
            stub,
        )

        payload = json.loads(output)
        self.assertEqual(payload["command"], "call")
        self.assertEqual(payload["path"], "ip")
        self.assertEqual(payload["method"], "GET")
        self.assertTrue(payload["success"])
        self.assertEqual(payload["response"]["data"]["city"], "Shanghai")

    def test_call_uses_environment_token_when_flag_missing(self):
        module = self._load_module()
        captured = {}

        def fake_request(url, method="GET", data=None, headers=None):
            captured["data"] = data
            return {"success": True, "code": 200, "message": "success", "data": {}}

        module._request = fake_request
        old_env = os.environ.get("ALAPI_TOKEN")
        old_argv = sys.argv
        stdout = StringIO()
        try:
            os.environ["ALAPI_TOKEN"] = "env-token"
            sys.argv = ["alapi.py", "--json", "call", "ip", "--param", "ip=8.8.8.8"]
            with redirect_stdout(stdout):
                module.main()
        finally:
            if old_env is None:
                os.environ.pop("ALAPI_TOKEN", None)
            else:
                os.environ["ALAPI_TOKEN"] = old_env
            sys.argv = old_argv

        self.assertEqual(captured["data"]["token"], "env-token")

    def test_explicit_token_overrides_environment_token(self):
        module = self._load_module()
        captured = {}

        def fake_request(url, method="GET", data=None, headers=None):
            captured["data"] = data
            return {"success": True, "code": 200, "message": "success", "data": {}}

        module._request = fake_request
        old_env = os.environ.get("ALAPI_TOKEN")
        old_argv = sys.argv
        stdout = StringIO()
        try:
            os.environ["ALAPI_TOKEN"] = "env-token"
            sys.argv = [
                "alapi.py",
                "--json",
                "call",
                "ip",
                "--token",
                "flag-token",
                "--param",
                "ip=8.8.8.8",
            ]
            with redirect_stdout(stdout):
                module.main()
        finally:
            if old_env is None:
                os.environ.pop("ALAPI_TOKEN", None)
            else:
                os.environ["ALAPI_TOKEN"] = old_env
            sys.argv = old_argv

        self.assertEqual(captured["data"]["token"], "flag-token")


if __name__ == "__main__":
    unittest.main()
