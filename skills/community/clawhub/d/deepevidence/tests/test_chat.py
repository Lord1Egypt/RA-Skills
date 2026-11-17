import importlib.util
import io
import json
import os
import pathlib
import subprocess
import sys
import unittest
from unittest import mock


CHAT_PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "chat.py"


def load_chat_module():
    spec = importlib.util.spec_from_file_location("deepevidence_chat", CHAT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeHTTPResponse:
    def __init__(self, payload, status=200, headers=None):
        self.payload = payload
        self.status = status
        self.headers = headers or {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")

    def getheader(self, name, default=None):
        return self.headers.get(name, default)


class ChatScriptTest(unittest.TestCase):
    def test_build_request_body_uses_official_image_url_object(self):
        chat = load_chat_module()

        body = chat.build_request_body(
            query="please inspect",
            user="external-user-1",
            image_urls=["https://example.com/medical-image.jpg"],
            stream=True,
            include_usage=True,
        )

        self.assertEqual(
            body,
            {
                "model": "DeepEvidence-V1",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "please inspect"},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": "https://example.com/medical-image.jpg",
                                    "detail": "auto",
                                },
                            },
                        ],
                    }
                ],
                "stream": True,
                "user": "skill_external-user-1",
                "stream_options": {"include_usage": True},
            },
        )

    def test_call_api_uses_stdlib_http_and_outputs_content_only_to_stdout(self):
        chat = load_chat_module()
        response = FakeHTTPResponse(
            {
                "choices": [{"message": {"content": "clinical answer"}}],
                "usage": {"prompt_tokens": 3, "completion_tokens": 4, "total_tokens": 7},
            },
            headers={"x-request-id": "req_123"},
        )

        captured_requests = []

        def fake_urlopen(request, timeout):
            captured_requests.append((request, timeout))
            return response

        stdout = io.StringIO()
        stderr = io.StringIO()
        with mock.patch.dict(os.environ, {"DEEPEVIDENCE_API_KEY": "secret-key"}):
            with mock.patch.object(chat.urllib_request, "urlopen", side_effect=fake_urlopen):
                with mock.patch("sys.stdout", stdout), mock.patch("sys.stderr", stderr):
                    chat.chat("question")

        self.assertEqual(stdout.getvalue(), "clinical answer\n")
        self.assertIn("request_id=req_123", stderr.getvalue())
        request, timeout = captured_requests[0]
        self.assertEqual(timeout, 60)
        self.assertEqual(request.full_url, "https://deepevid.medsci.cn/api/v1/chat/completions")
        self.assertEqual(request.get_method(), "POST")
        self.assertEqual(request.headers["Authorization"], "Bearer secret-key")
        self.assertEqual(json.loads(request.data.decode("utf-8"))["stream"], False)

    def test_missing_api_key_returns_stable_config_error(self):
        result = subprocess.run(
            [
                "env",
                "-u",
                "DEEPEVIDENCE_API_KEY",
                sys.executable,
                str(CHAT_PATH),
                "--query",
                "question",
            ],
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("DE_CONFIG_ERROR", result.stderr)
        self.assertIn("DEEPEVIDENCE_API_KEY is not set", result.stderr)


if __name__ == "__main__":
    unittest.main()
