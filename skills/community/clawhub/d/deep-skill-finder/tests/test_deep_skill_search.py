from __future__ import annotations

import contextlib
import io
import json
import sys
import unittest
from pathlib import Path
from unittest import mock


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import deep_skill_search  # noqa: E402


class DeepSkillSearchTests(unittest.TestCase):
    def test_search_deep_preserves_successful_empty_results(self):
        with mock.patch.object(deep_skill_search, "api_request", return_value={"code": 200, "data": []}):
            skills, request_id, error = deep_skill_search.search_deep("rare task")

        self.assertEqual([], skills)
        self.assertEqual("", request_id)
        self.assertIsNone(error)

    def test_search_deep_classifies_timeout_without_raw_exception_text(self):
        response = {"code": 0, "error": True, "errorType": "timeout", "message": "secret host"}
        with mock.patch.object(deep_skill_search, "api_request", return_value=response):
            skills, request_id, error = deep_skill_search.search_deep("task")

        self.assertEqual([], skills)
        self.assertEqual("", request_id)
        self.assertEqual("search_timeout", error["code"])
        self.assertNotIn("secret host", json.dumps(error))

    def test_main_returns_nonzero_and_emits_structured_service_error(self):
        search_error = {"code": "search_service_error", "message": "搜索服务暂时不可用", "httpStatus": 503}
        with (
            mock.patch.object(deep_skill_search, "search_deep", return_value=([], "", search_error)),
            mock.patch.object(sys, "argv", ["deep_skill_search.py", "task"]),
            mock.patch.object(deep_skill_search, "get_client_id", return_value="client"),
            mock.patch("tempfile.gettempdir", return_value=self._testMethodName),
            mock.patch("builtins.open", mock.mock_open()),
            contextlib.redirect_stdout(io.StringIO()) as stdout,
        ):
            exit_code = deep_skill_search.main()

        payload = json.loads(stdout.getvalue())
        self.assertEqual(1, exit_code)
        self.assertEqual("search_service_error", payload["error"]["code"])
        self.assertEqual(503, payload["error"]["httpStatus"])


if __name__ == "__main__":
    unittest.main()
