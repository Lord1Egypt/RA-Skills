from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from easy_xhs.common import ApiError, AppConfig, EasyXHSError, PublishError, load_reference_json
from easy_xhs.content import apply_template, call_gemini_text_api, parse_generated_content_prompts
from easy_xhs.image import load_progress
from easy_xhs.publish import mcp_call, mcp_init, post_json_with_retry
from easy_xhs.style import load_style_presets, match_style_preset
from cli import cmd_images
from generate_image import parse_style_arg


class FakeResponse:
    def __init__(self, payload: dict, status_error: Exception | None = None):
        self._payload = payload
        self._status_error = status_error

    def raise_for_status(self):
        if self._status_error is not None:
            raise self._status_error

    def json(self):
        return self._payload


class CoreBehaviorTests(unittest.TestCase):
    def test_app_config_legacy_and_new_keys(self):
        config = AppConfig(
            raw={
                "api": {"api_key": "k1", "timeout_seconds": "9", "max_retries": "2"},
                "xhs_mcp": {"url": "http://legacy-mcp"},
            }
        )
        self.assertEqual(config.api_key, "k1")
        self.assertEqual(config.timeout_seconds, 9)
        self.assertEqual(config.max_retries, 2)
        self.assertEqual(config.mcp_url, "http://legacy-mcp")

    def test_content_api_uses_header_and_retries(self):
        config = AppConfig(
            raw={
                "api": {"key": "secret", "base_url": "https://example.com", "model": "m", "timeout_seconds": 3, "max_retries": 2}
            }
        )
        calls = []

        def fake_post(url, json=None, headers=None, timeout=None):
            calls.append((url, headers, timeout))
            if len(calls) == 1:
                import requests

                raise requests.RequestException("boom")
            return FakeResponse({"candidates": [{"content": {"parts": [{"text": "ok"}]}}]})

        with patch("easy_xhs.content.requests.post", side_effect=fake_post):
            result = call_gemini_text_api(config, "hello")

        self.assertEqual(result, "ok")
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0][0], "https://example.com/models/m:generateContent")
        self.assertEqual(calls[0][1], {"x-goog-api-key": "secret"})
        self.assertEqual(calls[0][2], 3)

    def test_progress_corrupted_file_fallback(self):
        import easy_xhs.image as image_mod

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_progress = Path(tmpdir) / ".progress.json"
            tmp_progress.write_text("{bad json", encoding="utf-8")
            old = image_mod.PROGRESS_FILE
            image_mod.PROGRESS_FILE = tmp_progress
            try:
                data = load_progress()
            finally:
                image_mod.PROGRESS_FILE = old
        self.assertEqual(data, {"completed": [], "failed": [], "total": 0})

    def test_publish_retry_on_network_error(self):
        config = AppConfig(raw={"api": {"key": "k", "max_retries": 2}, "mcp": {"url": "http://localhost:18060/mcp", "timeout_seconds": 5}})
        calls = []

        def fake_post(url, json=None, headers=None, timeout=None):
            calls.append((url, timeout))
            if len(calls) == 1:
                import requests

                raise requests.RequestException("network")
            return FakeResponse({})

        with patch("easy_xhs.publish.requests.post", side_effect=fake_post):
            resp = post_json_with_retry(config, {"jsonrpc": "2.0"}, timeout=7)

        self.assertIsInstance(resp, FakeResponse)
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0][0], "http://localhost:18060/mcp")
        self.assertEqual(calls[0][1], 7)

    def test_mcp_init_requires_session_id(self):
        config = AppConfig(raw={"api": {"key": "k"}, "mcp": {"url": "http://localhost:18060/mcp"}})

        class NoSessionResponse:
            def __init__(self):
                self.headers = {}

        with patch("easy_xhs.publish.post_json_with_retry", return_value=NoSessionResponse()):
            with self.assertRaisesRegex(PublishError, "Session ID"):
                mcp_init(config)

    def test_mcp_call_raises_on_error_payload(self):
        config = AppConfig(raw={"api": {"key": "k"}, "mcp": {"url": "http://localhost:18060/mcp"}})

        class ErrorPayloadResponse:
            def json(self):
                return {"error": {"code": -32000, "message": "boom"}}

        with patch("easy_xhs.publish.post_json_with_retry", return_value=ErrorPayloadResponse()):
            with self.assertRaisesRegex(PublishError, "MCP 调用失败"):
                mcp_call(config, "sid", "publish_content", {"title": "t"})

    def test_style_presets_list_schema_is_normalized(self):
        presets = load_style_presets()
        matched = match_style_preset("科技博主", presets)
        self.assertIsInstance(matched, dict)
        self.assertTrue(bool(matched.get("style")))
        self.assertTrue(bool(matched.get("tone")))

    def test_apply_template_reports_missing_variable(self):
        with self.assertRaises(ApiError):
            apply_template("hello {topic}", {"account_type": "科技博主"})

    def test_resume_will_regenerate_when_completed_file_missing(self):
        import easy_xhs.image as image_mod

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_dir = Path(tmpdir)
            old_generated_dir = image_mod.GENERATED_DIR
            old_progress_file = image_mod.PROGRESS_FILE
            image_mod.GENERATED_DIR = tmp_dir
            image_mod.PROGRESS_FILE = tmp_dir / ".progress.json"
            image_mod.save_progress({"completed": [1], "failed": [], "total": 1})
            calls = []

            def fake_generate_image(config, prompt, style_preset, image_index=0, negative_prompt=""):
                calls.append((prompt, image_index))
                output_path = tmp_dir / f"image_{image_index + 1}.png"
                output_path.write_bytes(b"img")
                return output_path

            config = AppConfig(raw={"api": {"key": "k"}})
            try:
                with patch("easy_xhs.image.generate_image", side_effect=fake_generate_image):
                    images = image_mod.generate_images(config, ["p1"], {}, "")
            finally:
                image_mod.GENERATED_DIR = old_generated_dir
                image_mod.PROGRESS_FILE = old_progress_file
        self.assertEqual(calls, [("p1", 0)])
        self.assertEqual(images, [str(tmp_dir / "image_1.png")])

    def test_cli_images_style_must_be_json_object(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            content_path = Path(tmpdir) / "generated_content.json"
            content_path.write_text("成品图生成提示词：test", encoding="utf-8")
            args = type("Args", (), {"content_file": str(content_path), "style": "[]", "negative_prompt": ""})()
            with patch("cli.load_config", return_value=AppConfig(raw={"api": {"key": "k"}})):
                with self.assertRaisesRegex(EasyXHSError, "--style 必须是 JSON 对象"):
                    cmd_images(args)

    def test_cli_images_requires_parsed_prompts(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            content_path = Path(tmpdir) / "generated_content.json"
            content_path.write_text("无效内容", encoding="utf-8")
            args = type("Args", (), {"content_file": str(content_path), "style": "{}", "negative_prompt": ""})()
            with patch("cli.load_config", return_value=AppConfig(raw={"api": {"key": "k"}})):
                with self.assertRaisesRegex(EasyXHSError, "未从图文方案中解析到任何"):
                    cmd_images(args)

    def test_generate_image_style_must_be_json_object(self):
        with self.assertRaisesRegex(EasyXHSError, "--style 必须是 JSON 对象"):
            parse_style_arg("[]")

    def test_parse_generated_content_prompts_supports_structured_payload(self):
        payload = {
            "raw_text": "成品图生成提示词：raw prompt",
            "page_prompts": ["prompt1", " prompt2 "],
        }
        prompts = parse_generated_content_prompts(payload)
        self.assertEqual(prompts, ["prompt1", "prompt2"])

    def test_cli_images_supports_structured_generated_content(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            content_path = Path(tmpdir) / "generated_content.json"
            content_path.write_text(
                json.dumps({"page_prompts": ["p1", "p2"]}, ensure_ascii=False),
                encoding="utf-8",
            )
            args = type("Args", (), {"content_file": str(content_path), "style": "{}", "negative_prompt": ""})()
            with patch("cli.load_config", return_value=AppConfig(raw={"api": {"key": "k"}})):
                with patch("cli.generate_images", return_value=["a.png", "b.png"]) as mocked:
                    cmd_images(args)
            self.assertEqual(mocked.call_args.args[1], ["p1", "p2"])

    def test_style_theme_map_points_to_existing_preset_ids(self):
        raw = load_reference_json("style-presets.json", default={}) or {}
        presets = raw.get("presets", [])
        theme_map = raw.get("theme_to_style_map", {})
        self.assertIsInstance(presets, list)
        self.assertIsInstance(theme_map, dict)
        preset_ids = {
            str(item.get("id")).strip()
            for item in presets
            if isinstance(item, dict) and str(item.get("id", "")).strip()
        }
        for mapped_ids in theme_map.values():
            self.assertIsInstance(mapped_ids, list)
            for mapped_id in mapped_ids:
                self.assertIn(mapped_id, preset_ids)


if __name__ == "__main__":
    unittest.main()
