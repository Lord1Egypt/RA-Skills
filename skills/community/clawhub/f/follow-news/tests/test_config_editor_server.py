#!/usr/bin/env python3
"""Tests for config editor save behavior."""

from __future__ import annotations

import json
from io import BytesIO
import socket
import tempfile
import threading
import time
import unittest
from pathlib import Path
from typing import Any, Optional
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import importlib.util

def _load_config_editor_server() -> Any:
    server_path = Path(__file__).resolve().parents[1] / "tools" / "config-editor" / "server.py"
    spec = importlib.util.spec_from_file_location("config_editor_server", server_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load config editor server module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


server_module = _load_config_editor_server()


def _get_free_port() -> int:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


class TestConfigEditorServer(unittest.TestCase):
    def _valid_podcast_source(self, **overrides: Any) -> dict[str, Any]:
        source: dict[str, Any] = {
            "id": "test-podcast",
            "type": "podcast",
            "name": "Test Podcast",
            "enabled": True,
            "priority": False,
            "topics": ["podcast"],
            "url": "https://example.com/feed.xml",
            "platform": "rss",
        }
        source.update(overrides)
        return source

    def test_options_rejects_non_exact_file_route(self) -> None:
        port = _get_free_port()
        server = server_module.HTTPServer(("127.0.0.1", port), server_module.ConfigEditorHandler)
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()
        try:
            time.sleep(0.05)
            request = Request(
                f"http://127.0.0.1:{port}/api/filezzz",
                method="OPTIONS",
            )
            request.add_header("Origin", f"http://127.0.0.1:{port}")
            with self.assertRaises(HTTPError) as context:
                urlopen(request, timeout=2.0)
            self.assertEqual(context.exception.code, 404)
        finally:
            server.shutdown()
            server.server_close()
            server_thread.join(timeout=1.0)

    def test_post_normalizes_legacy_x_type_to_twitter_on_save(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sources_path = Path(tmpdir) / "sources.json"
            topics_path = Path(tmpdir) / "topics.json"

            payload_source = {
                "sources": [
                    {
                        "id": "legacy-x-source",
                        "type": "x",
                        "name": "Legacy X",
                        "enabled": True,
                        "priority": False,
                        "topics": [],
                        "handle": "legacy_x_handle",
                    }
                ]
            }
            sources_path.write_text(json.dumps(payload_source, ensure_ascii=False, indent=2), encoding="utf-8")
            topics_path.write_text("[]", encoding="utf-8")

            allowed_files = {
                "sources": {
                    "path": sources_path,
                    "label_zh": "测试源",
                    "label_en": "Test sources",
                },
                "topics": {
                    "path": topics_path,
                    "label_zh": "测试话题",
                    "label_en": "Test topics",
                },
            }

            port = _get_free_port()

            with patch.dict(server_module.ALLOWED_FILES, allowed_files):
                server = server_module.HTTPServer(("127.0.0.1", port), server_module.ConfigEditorHandler)
                server_thread = threading.Thread(target=server.serve_forever, daemon=True)
                server_thread.start()
                try:
                    time.sleep(0.05)
                    request_payload = {
                        "key": "sources",
                        "content": payload_source,
                    }
                    request = Request(
                        f"http://127.0.0.1:{port}/api/file",
                        data=json.dumps(request_payload, ensure_ascii=False).encode("utf-8"),
                        method="POST",
                        headers={
                            "Content-Type": "application/json",
                            "Origin": f"http://127.0.0.1:{port}",
                        },
                    )
                    with urlopen(request, timeout=2.0) as response:
                        body = response.read().decode("utf-8")
                    data = json.loads(body)
                    self.assertEqual(data, {"ok": True, "key": "sources", "message": "saved"})

                    saved = json.loads(sources_path.read_text(encoding="utf-8"))
                    self.assertEqual(saved["sources"][0]["type"], "twitter")
                finally:
                    server.shutdown()
                    server.server_close()
                    server_thread.join(timeout=1.0)

    def test_post_accepts_podcast_source_on_save(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sources_path = Path(tmpdir) / "sources.json"
            topics_path = Path(tmpdir) / "topics.json"

            payload_source = {
                "sources": [
                    {
                        "id": "whynottv-podcast",
                        "type": "podcast",
                        "name": "WhynotTV Podcast",
                        "enabled": True,
                        "priority": True,
                        "topics": ["podcast"],
                        "url": "https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940",
                        "platform": "xiaoyuzhou",
                        "transcript": {
                            "enabled": True,
                            "backend": "opencli",
                            "languages": [],
                        },
                    }
                ]
            }
            sources_path.write_text(json.dumps(payload_source, ensure_ascii=False, indent=2), encoding="utf-8")
            topics_path.write_text("[]", encoding="utf-8")

            allowed_files = {
                "sources": {
                    "path": sources_path,
                    "label_zh": "测试源",
                    "label_en": "Test sources",
                },
                "topics": {
                    "path": topics_path,
                    "label_zh": "测试话题",
                    "label_en": "Test topics",
                },
            }

            port = _get_free_port()

            with patch.dict(server_module.ALLOWED_FILES, allowed_files):
                server = server_module.HTTPServer(("127.0.0.1", port), server_module.ConfigEditorHandler)
                server_thread = threading.Thread(target=server.serve_forever, daemon=True)
                server_thread.start()
                try:
                    time.sleep(0.05)
                    request_payload = {
                        "key": "sources",
                        "content": payload_source,
                    }
                    request = Request(
                        f"http://127.0.0.1:{port}/api/file",
                        data=json.dumps(request_payload, ensure_ascii=False).encode("utf-8"),
                        method="POST",
                        headers={
                            "Content-Type": "application/json",
                            "Origin": f"http://127.0.0.1:{port}",
                        },
                    )
                    with urlopen(request, timeout=2.0) as response:
                        body = response.read().decode("utf-8")
                    data = json.loads(body)
                    self.assertEqual(data, {"ok": True, "key": "sources", "message": "saved"})

                    saved = json.loads(sources_path.read_text(encoding="utf-8"))
                    self.assertEqual(saved["sources"][0]["type"], "podcast")
                    self.assertEqual(saved["sources"][0]["platform"], "xiaoyuzhou")
                    self.assertEqual(saved["sources"][0]["transcript"]["backend"], "opencli")
                finally:
                    server.shutdown()
                    server.server_close()
                    server_thread.join(timeout=1.0)

    def test_post_accepts_podcast_source_without_optional_fields_on_save(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sources_path = Path(tmpdir) / "sources.json"
            topics_path = Path(tmpdir) / "topics.json"

            payload_source = {
                "sources": [
                    {
                        "id": "minimal-podcast",
                        "type": "podcast",
                        "name": "Minimal Podcast",
                        "enabled": True,
                        "priority": False,
                        "topics": ["podcast"],
                        "url": "https://example.com/podcast.xml",
                    }
                ]
            }
            sources_path.write_text(json.dumps(payload_source, ensure_ascii=False, indent=2), encoding="utf-8")
            topics_path.write_text("[]", encoding="utf-8")

            allowed_files = {
                "sources": {
                    "path": sources_path,
                    "label_zh": "测试源",
                    "label_en": "Test sources",
                },
                "topics": {
                    "path": topics_path,
                    "label_zh": "测试话题",
                    "label_en": "Test topics",
                },
            }

            port = _get_free_port()

            with patch.dict(server_module.ALLOWED_FILES, allowed_files):
                server = server_module.HTTPServer(("127.0.0.1", port), server_module.ConfigEditorHandler)
                server_thread = threading.Thread(target=server.serve_forever, daemon=True)
                server_thread.start()
                try:
                    time.sleep(0.05)
                    request_payload = {
                        "key": "sources",
                        "content": payload_source,
                    }
                    request = Request(
                        f"http://127.0.0.1:{port}/api/file",
                        data=json.dumps(request_payload, ensure_ascii=False).encode("utf-8"),
                        method="POST",
                        headers={
                            "Content-Type": "application/json",
                            "Origin": f"http://127.0.0.1:{port}",
                        },
                    )
                    with urlopen(request, timeout=2.0) as response:
                        body = response.read().decode("utf-8")
                    data = json.loads(body)
                    self.assertEqual(data, {"ok": True, "key": "sources", "message": "saved"})

                    saved = json.loads(sources_path.read_text(encoding="utf-8"))
                    self.assertEqual(saved["sources"][0]["type"], "podcast")
                    self.assertIn("id", saved["sources"][0])
                finally:
                    server.shutdown()
                    server.server_close()
                    server_thread.join(timeout=1.0)

    def test_post_rejects_invalid_podcast_source_fields_on_save(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sources_path = Path(tmpdir) / "sources.json"
            topics_path = Path(tmpdir) / "topics.json"

            sources_path.write_text('{"sources": []}', encoding="utf-8")
            topics_path.write_text("[]", encoding="utf-8")

            allowed_files = {
                "sources": {
                    "path": sources_path,
                    "label_zh": "测试源",
                    "label_en": "Test sources",
                },
                "topics": {
                    "path": topics_path,
                    "label_zh": "测试话题",
                    "label_en": "Test topics",
                },
            }

            base_source = {
                "id": "broken-podcast",
                "type": "podcast",
                "name": "Broken Podcast",
                "enabled": True,
                "priority": False,
                "topics": ["llm"],
                "url": "https://example.com/feed.xml",
                "platform": "rss",
                "transcript": {"backend": "auto"},
            }
            cases = [
                ("missing_url", {"url": None}),
                ("invalid_url", {"url": "not a url"}),
                ("invalid_platform", {"platform": "vimeo"}),
                ("invalid_transcript", {"transcript": []}),
                ("invalid_transcript_backend", {"transcript": {"backend": "manual"}}),
                ("invalid_opencli_backend_platform", {"transcript": {"backend": "opencli"}}),
                ("invalid_transcript_enabled", {"transcript": {"enabled": "yes"}}),
                ("invalid_transcript_languages", {"transcript": {"languages": "en"}}),
                ("invalid_transcript_language_item", {"transcript": {"languages": ["en", 123]}}),
            ]

            port = _get_free_port()

            with patch.dict(server_module.ALLOWED_FILES, allowed_files):
                server = server_module.HTTPServer(("127.0.0.1", port), server_module.ConfigEditorHandler)
                server_thread = threading.Thread(target=server.serve_forever, daemon=True)
                server_thread.start()
                try:
                    time.sleep(0.05)
                    for case_name, overrides in cases:
                        with self.subTest(case=case_name):
                            source = dict(base_source)
                            for key, value in overrides.items():
                                if value is None:
                                    source.pop(key, None)
                                else:
                                    source[key] = value
                            request_payload = {
                                "key": "sources",
                                "content": {"sources": [source]},
                            }
                            request = Request(
                                f"http://127.0.0.1:{port}/api/file",
                                data=json.dumps(request_payload, ensure_ascii=False).encode("utf-8"),
                                method="POST",
                                headers={
                                    "Content-Type": "application/json",
                                    "Origin": f"http://127.0.0.1:{port}",
                                },
                            )
                            with self.assertRaises(HTTPError) as context:
                                urlopen(request, timeout=2.0)
                            self.assertEqual(context.exception.code, 400)
                finally:
                    server.shutdown()
                    server.server_close()
                    server_thread.join(timeout=1.0)

    def test_validate_sources_payload_accepts_xiaoyuzhou_url_with_query_and_fragment(self) -> None:
        handler = server_module.ConfigEditorHandler.__new__(server_module.ConfigEditorHandler)

        handler._validate_sources_payload(
            [
                self._valid_podcast_source(
                    url="https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940?foo=bar#section",
                    platform="xiaoyuzhou",
                )
            ]
        )

    def test_validate_sources_payload_rejects_invalid_xiaoyuzhou_url_shape(self) -> None:
        handler = server_module.ConfigEditorHandler.__new__(server_module.ConfigEditorHandler)
        invalid_urls = [
            "https://www.xiaoyuzhoufm.com/episode/69f441cd5390b7cc928acdcc",
            "https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940/extra",
            "https://www.xiaoyuzhoufm.com/podcast/",
            "https://example.com/podcast/686a1832222ae2de21fea940",
            "ftp://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940",
        ]

        for url in invalid_urls:
            with self.subTest(url=url):
                with self.assertRaises(ValueError):
                    handler._validate_sources_payload(
                        [
                            self._valid_podcast_source(
                                url=url,
                                platform="xiaoyuzhou",
                            )
                        ]
                    )

    def test_post_rejects_invalid_content_type(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sources_path = Path(tmpdir) / "sources.json"
            topics_path = Path(tmpdir) / "topics.json"

            sources_path.write_text('{"sources": []}', encoding="utf-8")
            topics_path.write_text("[]", encoding="utf-8")

            allowed_files = {
                "sources": {
                    "path": sources_path,
                    "label_zh": "测试源",
                    "label_en": "Test sources",
                },
                "topics": {
                    "path": topics_path,
                    "label_zh": "测试话题",
                    "label_en": "Test topics",
                },
            }

            port = _get_free_port()

            with patch.dict(server_module.ALLOWED_FILES, allowed_files):
                server = server_module.HTTPServer(("127.0.0.1", port), server_module.ConfigEditorHandler)
                server_thread = threading.Thread(target=server.serve_forever, daemon=True)
                server_thread.start()
                try:
                    time.sleep(0.05)
                    request_payload = {
                        "key": "sources",
                        "content": 1,
                    }
                    request = Request(
                        f"http://127.0.0.1:{port}/api/file",
                        data=json.dumps(request_payload, ensure_ascii=False).encode("utf-8"),
                        method="POST",
                        headers={
                            "Content-Type": "application/json",
                            "Origin": f"http://127.0.0.1:{port}",
                        },
                    )
                    with self.assertRaises(HTTPError) as context:
                        urlopen(request, timeout=2.0)
                    self.assertEqual(context.exception.code, 400)
                finally:
                    server.shutdown()
                    server.server_close()
                    server_thread.join(timeout=1.0)

    def test_get_returns_500_for_invalid_json_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sources_path = Path(tmpdir) / "sources.json"
            topics_path = Path(tmpdir) / "topics.json"

            sources_path.write_text('{"sources": [}', encoding="utf-8")
            topics_path.write_text("[]", encoding="utf-8")

            allowed_files = {
                "sources": {
                    "path": sources_path,
                    "label_zh": "测试源",
                    "label_en": "Test sources",
                },
                "topics": {
                    "path": topics_path,
                    "label_zh": "测试话题",
                    "label_en": "Test topics",
                },
            }

            port = _get_free_port()

            with patch.dict(server_module.ALLOWED_FILES, allowed_files):
                server = server_module.HTTPServer(("127.0.0.1", port), server_module.ConfigEditorHandler)
                server_thread = threading.Thread(target=server.serve_forever, daemon=True)
                server_thread.start()
                try:
                    time.sleep(0.05)
                    request = Request(
                        f"http://127.0.0.1:{port}/api/file?key=sources",
                        method="GET",
                    )
                    request.add_header("Origin", f"http://127.0.0.1:{port}")
                    with self.assertRaises(HTTPError) as context:
                        urlopen(request, timeout=2.0)
                    self.assertEqual(context.exception.code, 500)
                finally:
                    server.shutdown()
                    server.server_close()
                    server_thread.join(timeout=1.0)

    def test_get_request_host_with_invalid_host_header(self) -> None:
        handler = server_module.ConfigEditorHandler.__new__(server_module.ConfigEditorHandler)
        handler.headers = {"Host": "[::1"}
        self.assertIsNone(handler._get_request_host())

    def test_read_request_json_rejects_invalid_content_length(self) -> None:
        handler = server_module.ConfigEditorHandler.__new__(server_module.ConfigEditorHandler)
        handler.headers = {"Content-Length": "abc"}
        handler.rfile = BytesIO(b"{}")
        with self.assertRaises(ValueError):
            handler._read_request_json()

    def test_read_request_json_rejects_negative_content_length(self) -> None:
        handler = server_module.ConfigEditorHandler.__new__(server_module.ConfigEditorHandler)
        handler.headers = {"Content-Length": "-1"}
        handler.rfile = BytesIO(b"")
        with self.assertRaises(ValueError):
            handler._read_request_json()

    def test_read_request_json_rejects_non_utf8_body(self) -> None:
        handler = server_module.ConfigEditorHandler.__new__(server_module.ConfigEditorHandler)
        handler.headers = {"Content-Length": "2"}
        handler.rfile = BytesIO(b"\xff\x00")
        with self.assertRaises(ValueError):
            handler._read_request_json()

    def test_post_accepts_bound_host_same_origin(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sources_path = Path(tmpdir) / "sources.json"
            topics_path = Path(tmpdir) / "topics.json"

            payload_source = {
                "sources": [
                    {
                        "id": "bound-host-test",
                        "type": "twitter",
                        "name": "Bound Host",
                        "enabled": True,
                        "priority": False,
                        "topics": [],
                        "handle": "boundhost",
                    }
                ]
            }
            sources_path.write_text(json.dumps(payload_source, ensure_ascii=False, indent=2), encoding="utf-8")
            topics_path.write_text("[]", encoding="utf-8")

            allowed_files = {
                "sources": {
                    "path": sources_path,
                    "label_zh": "测试源",
                    "label_en": "Test sources",
                },
                "topics": {
                    "path": topics_path,
                    "label_zh": "测试话题",
                    "label_en": "Test topics",
                },
            }

            port = _get_free_port()

            with patch.dict(server_module.ALLOWED_FILES, allowed_files):
                server = server_module.HTTPServer(("0.0.0.0", port), server_module.ConfigEditorHandler)
                server_thread = threading.Thread(target=server.serve_forever, daemon=True)
                server_thread.start()
                try:
                    time.sleep(0.05)

                    request_payload = {
                        "key": "sources",
                        "content": payload_source,
                    }
                    request = Request(
                        f"http://127.0.0.1:{port}/api/file",
                        data=json.dumps(request_payload, ensure_ascii=False).encode("utf-8"),
                        method="POST",
                        headers={
                            "Content-Type": "application/json",
                            "Origin": f"http://127.0.0.1:{port}",
                        },
                    )
                    with urlopen(request, timeout=2.0) as response:
                        body = response.read().decode("utf-8")
                    data = json.loads(body)
                    self.assertEqual(data, {"ok": True, "key": "sources", "message": "saved"})

                finally:
                    server.shutdown()
                    server.server_close()
                    server_thread.join(timeout=1.0)

    def test_post_rejects_malformed_host_header(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sources_path = Path(tmpdir) / "sources.json"
            topics_path = Path(tmpdir) / "topics.json"

            sources_path.write_text('{"sources": []}', encoding="utf-8")
            topics_path.write_text("[]", encoding="utf-8")

            allowed_files = {
                "sources": {
                    "path": sources_path,
                    "label_zh": "测试源",
                    "label_en": "Test sources",
                },
                "topics": {
                    "path": topics_path,
                    "label_zh": "测试话题",
                    "label_en": "Test topics",
                },
            }

            port = _get_free_port()

            with patch.dict(server_module.ALLOWED_FILES, allowed_files):
                server = server_module.HTTPServer(("127.0.0.1", port), server_module.ConfigEditorHandler)
                server_thread = threading.Thread(target=server.serve_forever, daemon=True)
                server_thread.start()
                try:
                    time.sleep(0.05)

                    request = Request(
                        f"http://127.0.0.1:{port}/api/file",
                        data=b'{"key":"sources","content":{"sources":[]}}',
                        method="POST",
                        headers={
                            "Content-Type": "application/json",
                            "Origin": f"http://127.0.0.1:{port}",
                            "Host": "[::1",
                        },
                    )
                    with self.assertRaises(HTTPError) as context:
                        urlopen(request, timeout=2.0)
                    self.assertEqual(context.exception.code, 403)
                finally:
                    server.shutdown()
                    server.server_close()
                    server_thread.join(timeout=1.0)

    def test_post_rejects_non_utf8_request_body(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sources_path = Path(tmpdir) / "sources.json"
            topics_path = Path(tmpdir) / "topics.json"

            payload_source = {"sources": []}
            sources_path.write_text(json.dumps(payload_source, ensure_ascii=False, indent=2), encoding="utf-8")
            topics_path.write_text("[]", encoding="utf-8")

            allowed_files = {
                "sources": {
                    "path": sources_path,
                    "label_zh": "测试源",
                    "label_en": "Test sources",
                },
                "topics": {
                    "path": topics_path,
                    "label_zh": "测试话题",
                    "label_en": "Test topics",
                },
            }

            port = _get_free_port()
            with patch.dict(server_module.ALLOWED_FILES, allowed_files):
                server = server_module.HTTPServer(("127.0.0.1", port), server_module.ConfigEditorHandler)
                server_thread = threading.Thread(target=server.serve_forever, daemon=True)
                server_thread.start()
                try:
                    time.sleep(0.05)

                    request = Request(
                        f"http://127.0.0.1:{port}/api/file",
                        data=b"\xff\xfe",
                        method="POST",
                        headers={
                            "Content-Type": "application/json",
                            "Origin": f"http://127.0.0.1:{port}",
                            "Content-Length": "2",
                        },
                    )
                    with self.assertRaises(HTTPError) as context:
                        urlopen(request, timeout=2.0)
                    self.assertEqual(context.exception.code, 400)
                finally:
                    server.shutdown()
                    server.server_close()
                    server_thread.join(timeout=1.0)

    def test_post_rejects_invalid_content_length(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sources_path = Path(tmpdir) / "sources.json"
            topics_path = Path(tmpdir) / "topics.json"

            sources_path.write_text('{"sources": []}', encoding="utf-8")
            topics_path.write_text("[]", encoding="utf-8")

            allowed_files = {
                "sources": {
                    "path": sources_path,
                    "label_zh": "测试源",
                    "label_en": "Test sources",
                },
                "topics": {
                    "path": topics_path,
                    "label_zh": "测试话题",
                    "label_en": "Test topics",
                },
            }

            port = _get_free_port()

            with patch.dict(server_module.ALLOWED_FILES, allowed_files):
                server = server_module.HTTPServer(("127.0.0.1", port), server_module.ConfigEditorHandler)
                server_thread = threading.Thread(target=server.serve_forever, daemon=True)
                server_thread.start()
                try:
                    time.sleep(0.05)
                    request_payload = {"key": "sources", "content": {"sources": []}}
                    request = Request(
                        f"http://127.0.0.1:{port}/api/file",
                        data=json.dumps(request_payload, ensure_ascii=False).encode("utf-8"),
                        method="POST",
                        headers={
                            "Content-Type": "application/json",
                            "Origin": f"http://127.0.0.1:{port}",
                            "Content-Length": "abc",
                        },
                    )
                    with self.assertRaises(HTTPError) as context:
                        urlopen(request, timeout=2.0)
                    self.assertEqual(context.exception.code, 400)
                finally:
                    server.shutdown()
                    server.server_close()
                    server_thread.join(timeout=1.0)

    def test_post_rejects_negative_content_length(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sources_path = Path(tmpdir) / "sources.json"
            topics_path = Path(tmpdir) / "topics.json"

            sources_path.write_text('{"sources": []}', encoding="utf-8")
            topics_path.write_text("[]", encoding="utf-8")

            allowed_files = {
                "sources": {
                    "path": sources_path,
                    "label_zh": "测试源",
                    "label_en": "Test sources",
                },
                "topics": {
                    "path": topics_path,
                    "label_zh": "测试话题",
                    "label_en": "Test topics",
                },
            }

            port = _get_free_port()

            with patch.dict(server_module.ALLOWED_FILES, allowed_files):
                server = server_module.HTTPServer(("127.0.0.1", port), server_module.ConfigEditorHandler)
                server_thread = threading.Thread(target=server.serve_forever, daemon=True)
                server_thread.start()
                try:
                    time.sleep(0.05)
                    request_payload = {"key": "sources", "content": {"sources": []}}
                    request = Request(
                        f"http://127.0.0.1:{port}/api/file",
                        data=json.dumps(request_payload, ensure_ascii=False).encode("utf-8"),
                        method="POST",
                        headers={
                            "Content-Type": "application/json",
                            "Origin": f"http://127.0.0.1:{port}",
                            "Content-Length": "-1",
                        },
                    )
                    with self.assertRaises(HTTPError) as context:
                        urlopen(request, timeout=2.0)
                    self.assertEqual(context.exception.code, 400)
                finally:
                    server.shutdown()
                    server.server_close()
                    server_thread.join(timeout=1.0)

    def test_server_can_bind_ipv6_host(self) -> None:
        if not socket.has_ipv6:
            self.skipTest("IPv6 is not supported in this environment")

        port = _get_free_port()
        server = server_module.IPv6ConfigEditorHTTPServer(("::1", port), server_module.ConfigEditorHandler)
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()
        try:
            time.sleep(0.05)

            request = Request(f"http://[::1]:{port}/api/file?key=sources", method="GET")
            with urlopen(request, timeout=2.0) as response:
                payload = json.loads(response.read().decode("utf-8"))
            self.assertEqual(payload["key"], "sources")
            self.assertIn("ok", payload)
            self.assertTrue(payload["ok"])
        finally:
            server.shutdown()
            server.server_close()
            server_thread.join(timeout=1.0)

    def test_post_accepts_ipv6_origin_when_ipv6_bound(self) -> None:
        if not socket.has_ipv6:
            self.skipTest("IPv6 is not supported in this environment")

        with tempfile.TemporaryDirectory() as tmpdir:
            sources_path = Path(tmpdir) / "sources.json"
            topics_path = Path(tmpdir) / "topics.json"

            payload_source = {"sources": []}
            sources_path.write_text(json.dumps(payload_source, ensure_ascii=False, indent=2), encoding="utf-8")
            topics_path.write_text("[]", encoding="utf-8")

            allowed_files = {
                "sources": {
                    "path": sources_path,
                    "label_zh": "测试源",
                    "label_en": "Test sources",
                },
                "topics": {
                    "path": topics_path,
                    "label_zh": "测试话题",
                    "label_en": "Test topics",
                },
            }

            port = _get_free_port()
            with patch.dict(server_module.ALLOWED_FILES, allowed_files):
                server = server_module.IPv6ConfigEditorHTTPServer(("::1", port), server_module.ConfigEditorHandler)
                server_thread = threading.Thread(target=server.serve_forever, daemon=True)
                server_thread.start()
                try:
                    time.sleep(0.05)

                    request_payload = {
                        "key": "sources",
                        "content": payload_source,
                    }
                    request = Request(
                        f"http://[::1]:{port}/api/file",
                        data=json.dumps(request_payload, ensure_ascii=False).encode("utf-8"),
                        method="POST",
                        headers={
                            "Content-Type": "application/json",
                            "Origin": f"http://[::1]:{port}",
                        },
                    )
                    with urlopen(request, timeout=2.0) as response:
                        payload = json.loads(response.read().decode("utf-8"))
                    self.assertEqual(payload["key"], "sources")
                    self.assertEqual(payload["message"], "saved")
                finally:
                    server.shutdown()
                    server.server_close()
                    server_thread.join(timeout=1.0)

    def test_post_rejects_bound_host_mismatched_origin(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sources_path = Path(tmpdir) / "sources.json"
            topics_path = Path(tmpdir) / "topics.json"

            payload_source = {
                "sources": [
                    {
                        "id": "bound-host-lan",
                        "type": "twitter",
                        "name": "Bound Host LAN",
                        "enabled": True,
                        "priority": False,
                        "topics": [],
                        "handle": "boundhostlan",
                    }
                ]
            }
            sources_path.write_text(json.dumps(payload_source, ensure_ascii=False, indent=2), encoding="utf-8")
            topics_path.write_text("[]", encoding="utf-8")

            allowed_files = {
                "sources": {
                    "path": sources_path,
                    "label_zh": "测试源",
                    "label_en": "Test sources",
                },
                "topics": {
                    "path": topics_path,
                    "label_zh": "测试话题",
                    "label_en": "Test topics",
                },
            }

            port = _get_free_port()

            with patch.dict(server_module.ALLOWED_FILES, allowed_files):
                server = server_module.HTTPServer(("0.0.0.0", port), server_module.ConfigEditorHandler)
                server_thread = threading.Thread(target=server.serve_forever, daemon=True)
                server_thread.start()
                try:
                    time.sleep(0.05)

                    request_payload = {
                        "key": "sources",
                        "content": payload_source,
                    }
                    request = Request(
                        f"http://127.0.0.1:{port}/api/file",
                        data=json.dumps(request_payload, ensure_ascii=False).encode("utf-8"),
                        method="POST",
                        headers={
                            "Content-Type": "application/json",
                            "Origin": f"http://192.168.1.12:{port}",
                        },
                    )
                    with self.assertRaises(HTTPError) as context:
                        urlopen(request, timeout=2.0)
                    self.assertEqual(context.exception.code, 403)

                finally:
                    server.shutdown()
                    server.server_close()
                    server_thread.join(timeout=1.0)

    def test_post_rejects_forged_wildcard_host_headers(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sources_path = Path(tmpdir) / "sources.json"
            topics_path = Path(tmpdir) / "topics.json"

            payload_source = {
                "sources": [
                    {
                        "id": "bound-host-fake",
                        "type": "twitter",
                        "name": "Bound Host Fake",
                        "enabled": True,
                        "priority": False,
                        "topics": [],
                        "handle": "boundhostfake",
                    }
                ]
            }
            sources_path.write_text(json.dumps(payload_source, ensure_ascii=False, indent=2), encoding="utf-8")
            topics_path.write_text("[]", encoding="utf-8")

            allowed_files = {
                "sources": {
                    "path": sources_path,
                    "label_zh": "测试源",
                    "label_en": "Test sources",
                },
                "topics": {
                    "path": topics_path,
                    "label_zh": "测试话题",
                    "label_en": "Test topics",
                },
            }

            port = _get_free_port()

            with patch.dict(server_module.ALLOWED_FILES, allowed_files):
                server = server_module.HTTPServer(("0.0.0.0", port), server_module.ConfigEditorHandler)
                server_thread = threading.Thread(target=server.serve_forever, daemon=True)
                server_thread.start()
                try:
                    time.sleep(0.05)

                    request_payload = {
                        "key": "sources",
                        "content": payload_source,
                    }
                    request = Request(
                        f"http://127.0.0.1:{port}/api/file",
                        data=json.dumps(request_payload, ensure_ascii=False).encode("utf-8"),
                        method="POST",
                        headers={
                            "Content-Type": "application/json",
                            "Origin": f"http://192.168.1.12:{port}",
                            "Host": f"192.168.1.12:{port}",
                        },
                    )
                    with self.assertRaises(HTTPError) as context:
                        urlopen(request, timeout=2.0)
                    self.assertEqual(context.exception.code, 403)

                finally:
                    server.shutdown()
                    server.server_close()
                    server_thread.join(timeout=1.0)

    def test_wildcard_origin_host_validation_binds_local_aliases_to_client(self) -> None:
        handler = server_module.ConfigEditorHandler.__new__(server_module.ConfigEditorHandler)

        handler.client_address = ("127.0.0.1", 54321)
        self.assertTrue(handler._is_wildcard_request_local("localhost"))
        self.assertTrue(handler._is_wildcard_request_local("127.0.0.1"))

        handler.client_address = ("192.168.1.99", 54321)
        self.assertFalse(handler._is_wildcard_request_local("localhost"))
        self.assertFalse(handler._is_wildcard_request_local("127.0.0.1"))
        self.assertFalse(handler._is_wildcard_request_local("0.0.0.0"))

        handler.client_address = ("192.168.1.99", 54321)
        self.assertFalse(handler._is_wildcard_request_local("192.168.1.99"))
        self.assertFalse(handler._is_wildcard_request_local("192.168.1.100"))

    def test_post_rejects_non_exact_file_route(self) -> None:
        port = _get_free_port()
        server = server_module.HTTPServer(("127.0.0.1", port), server_module.ConfigEditorHandler)
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()
        try:
            time.sleep(0.05)
            request = Request(f"http://127.0.0.1:{port}/api/filezzz", method="POST")
            request.add_header("Origin", f"http://127.0.0.1:{port}")
            with self.assertRaises(HTTPError) as context:
                urlopen(request, timeout=2.0)
            self.assertEqual(context.exception.code, 404)
        finally:
            server.shutdown()
            server.server_close()
            server_thread.join(timeout=1.0)

    def test_get_rejects_non_exact_file_route(self) -> None:
        port = _get_free_port()
        server = server_module.HTTPServer(("127.0.0.1", port), server_module.ConfigEditorHandler)
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()
        try:
            time.sleep(0.05)

            request = Request(
                f"http://127.0.0.1:{port}/api/filezzz?key=sources",
                method="GET",
            )
            request.add_header("Origin", f"http://127.0.0.1:{port}")

            with self.assertRaises(HTTPError) as context:
                urlopen(request, timeout=2.0)
            self.assertEqual(context.exception.code, 404)
        finally:
            server.shutdown()
            server.server_close()
            server_thread.join(timeout=1.0)


if __name__ == "__main__":
    unittest.main()
