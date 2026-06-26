#!/usr/bin/env python3
"""
Tiny local editor backend for follow-news config JSON files.

Usage:
  python3 tools/config-editor/server.py
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import os
import re
import socket
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from typing import Dict, Any, Optional
from urllib.parse import parse_qs, unquote, urlparse


BASE_DIR = Path(__file__).resolve().parents[2]
STATIC_DIR = Path(__file__).resolve().parent
ALLOWED_FILES = {
    "sources": {
        "path": BASE_DIR / "config" / "defaults" / "sources.json",
        "label_zh": "默认订阅源配置",
        "label_en": "Default sources config",
    },
    "topics": {
        "path": BASE_DIR / "config" / "defaults" / "topics.json",
        "label_zh": "默认话题配置",
        "label_en": "Default topics config",
    },
}
XIAOYUZHOU_HOSTS = {"xiaoyuzhoufm.com", "www.xiaoyuzhoufm.com"}


class ConfigEditorHandler(SimpleHTTPRequestHandler):
    _json_prefix = re.compile(r"^/api/")
    _LOCAL_ORIGINS = {"127.0.0.1", "localhost", "::1"}
    _ALLOWED_SOURCE_TYPES = {"rss", "twitter", "web", "github", "reddit", "podcast"}
    _ALLOWED_PODCAST_PLATFORMS = {"auto", "rss", "youtube", "xiaoyuzhou"}
    _ALLOWED_TRANSCRIPT_BACKENDS = {"auto", "yt-dlp", "opencli"}
    _WILDCARD_HOSTS = {"0.0.0.0", "::", "::0"}

    def _send_json(self, payload: Dict[str, Any], status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _api_error(self, status: int, message: str) -> None:
        self._send_json({"ok": False, "error": message}, status=status)

    def _read_request_json(self) -> Dict[str, Any]:
        raw_length = self.headers.get("Content-Length", "0").strip()
        try:
            length = int(raw_length)
        except ValueError as exc:
            raise ValueError("invalid content length") from exc
        if length < 0:
            raise ValueError("invalid content length")

        try:
            raw = self.rfile.read(length).decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("invalid request body encoding") from exc
        if not raw:
            return {}
        return json.loads(raw)

    def _validate_key(self) -> str:
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)
        key = (qs.get("key") or [None])[0]
        if not key or key not in ALLOWED_FILES:
            raise ValueError("unknown config key")
        return key

    def _is_allowed_write_origin(self) -> bool:
        origin = self.headers.get("Origin")
        if not origin:
            return False

        parsed = urlparse(origin)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            return False

        request_host = self._get_request_host()
        if not request_host:
            return False

        try:
            parsed_port = parsed.port
        except ValueError:
            return False

        if parsed_port is None:
            normalized_port = {"http": 80, "https": 443}.get(parsed.scheme)
        else:
            normalized_port = parsed_port
        if normalized_port is None:
            return False

        server_address = self.server.server_address
        if not isinstance(server_address, tuple) or len(server_address) < 2:
            return False
        server_host, server_port = server_address[:2]
        if normalized_port != server_port:
            return False

        origin_host = parsed.hostname.lower()
        if server_host in self._WILDCARD_HOSTS:
            return origin_host == request_host and self._is_wildcard_request_local(origin_host)

        if origin_host in self._LOCAL_ORIGINS and request_host in self._LOCAL_ORIGINS:
            return True

        return origin_host == server_host

    def _is_wildcard_request_local(self, host: str) -> bool:
        if host in self._WILDCARD_HOSTS:
            return self._is_client_loopback()
        if host in self._LOCAL_ORIGINS:
            return self._is_client_loopback()

        try:
            host_addr = ipaddress.ip_address(host)
        except ValueError:
            return False

        if host_addr.is_loopback:
            return self._is_client_loopback()
        return self._is_local_interface_host(host)

    def _is_local_interface_host(self, host: str) -> bool:
        try:
            host_addr = ipaddress.ip_address(host)
        except ValueError:
            return False

        try:
            local_info = socket.getaddrinfo(socket.gethostname(), None, socket.AF_UNSPEC, socket.SOCK_STREAM)
        except OSError:
            return False

        for _, _, _, _, sockaddr in local_info:
            if not sockaddr:
                continue
            try:
                if ipaddress.ip_address(sockaddr[0]) == host_addr:
                    return True
            except (ValueError, IndexError):
                continue

        return False

    def _is_client_loopback(self) -> bool:
        client_host = self.client_address[0]
        try:
            return ipaddress.ip_address(client_host).is_loopback
        except ValueError:
            return False

    def _get_request_host(self) -> Optional[str]:
        host_header = self.headers.get("Host")
        if not host_header:
            return None
        try:
            parsed_host = urlparse(f"//{host_header}")
        except ValueError:
            return None
        return parsed_host.hostname.lower() if parsed_host.hostname else None

    @staticmethod
    def _is_ipv6_host(host: str) -> bool:
        try:
            ip = ipaddress.ip_address(host)
        except ValueError:
            return False
        return ip.version == 6

    def _is_safe_static_path(self, path: Path, base: Path) -> bool:
        try:
            base_str = str(base.resolve())
            path_str = str(path.resolve())
            return os.path.commonpath([path_str, base_str]) == base_str
        except ValueError:
            return False

    def translate_path(self, path: str) -> str:
        static_root = Path(self.directory).resolve()

        # Strip query / fragment
        path = urlparse(path).path
        parts = [segment for segment in unquote(path).split("/") if segment]
        target = static_root

        for part in parts:
            if part in (".", ".."): 
                continue
            target = (target / part).resolve()
            if not self._is_safe_static_path(target, static_root):
                return str(static_root / ".follow-news-forbidden")
        return str(target)

    def _normalize_source_type(self, source_type: Any) -> str:
        if source_type == "x":
            return "twitter"
        return source_type

    @staticmethod
    def _is_http_url_with_hostname(value: Any) -> bool:
        if not isinstance(value, str):
            return False
        if any(char.isspace() or ord(char) < 32 for char in value):
            return False

        try:
            parsed = urlparse(value)
            hostname = parsed.hostname
            parsed.port
        except ValueError:
            return False

        if not hostname:
            return False
        if any(char.isspace() or ord(char) < 32 for char in hostname):
            return False
        return parsed.scheme in {"http", "https"}

    @classmethod
    def _is_xiaoyuzhou_podcast_url(cls, value: Any) -> bool:
        if not cls._is_http_url_with_hostname(value):
            return False

        parsed = urlparse(value)
        host = (parsed.hostname or "").lower()
        if host not in XIAOYUZHOU_HOSTS:
            return False

        parts = [part for part in parsed.path.split("/") if part]
        return len(parts) == 2 and parts[0] == "podcast" and bool(parts[1])

    @classmethod
    def _supports_opencli_transcript(cls, platform: str, url: Any) -> bool:
        return platform == "xiaoyuzhou" or (
            platform == "auto" and cls._is_xiaoyuzhou_podcast_url(url)
        )

    def _normalize_sources_payload(self, sources: Any) -> int:
        if not isinstance(sources, list):
            return 0

        normalized_count = 0
        for source in sources:
            if not isinstance(source, dict):
                continue
            original = source.get("type")
            normalized = self._normalize_source_type(original)
            if normalized != original:
                source["type"] = normalized
                normalized_count += 1
        return normalized_count

    def _send_cors_headers(self) -> None:
        origin = self.headers.get("Origin")
        if origin and self._is_allowed_write_origin():
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")

    def _validate_sources_payload(self, sources: Any) -> None:
        if not isinstance(sources, list):
            raise ValueError("'sources' should be a list")

        for index, source in enumerate(sources):
            if not isinstance(source, dict):
                raise ValueError(f"Source at index {index} should be an object")

            source_id = source.get("id", f"index:{index}")
            missing = []
            for field in ("id", "type", "name", "enabled", "priority", "topics"):
                if field not in source:
                    missing.append(field)
            if missing:
                raise ValueError(
                    f"Source '{source_id}' missing required field(s): {', '.join(missing)}"
                )

            source_type = source["type"]
            if not isinstance(source_type, str) or source_type not in self._ALLOWED_SOURCE_TYPES:
                raise ValueError(f"Source '{source_id}' has unsupported type: {source_type}")

            if not isinstance(source["id"], str) or not source["id"].strip():
                raise ValueError(f"Source at index {index} has invalid 'id'")
            if not isinstance(source["name"], str) or not source["name"].strip():
                raise ValueError(f"Source '{source_id}' has invalid 'name'")
            if not isinstance(source["enabled"], bool):
                raise ValueError(f"Source '{source_id}' has invalid 'enabled' value")
            if not isinstance(source["priority"], bool):
                raise ValueError(f"Source '{source_id}' has invalid 'priority' value")

            topics = source["topics"]
            if not isinstance(topics, list) or not all(isinstance(topic, str) for topic in topics):
                raise ValueError(f"Source '{source_id}' has invalid 'topics'; expected string array")

            if source_type == "rss":
                if not isinstance(source.get("url"), str) or not source["url"].strip():
                    raise ValueError(f"Source '{source_id}' missing required field 'url'")
            elif source_type == "twitter":
                if not isinstance(source.get("handle"), str) or not source["handle"].strip():
                    raise ValueError(f"Source '{source_id}' missing required field 'handle'")
            elif source_type == "github":
                if not isinstance(source.get("repo"), str) or not source["repo"].strip():
                    raise ValueError(f"Source '{source_id}' missing required field 'repo'")
            elif source_type == "reddit":
                if not isinstance(source.get("subreddit"), str) or not source["subreddit"].strip():
                    raise ValueError(f"Source '{source_id}' missing required field 'subreddit'")
            elif source_type == "podcast":
                url = source.get("url")
                if not url:
                    raise ValueError(f"Source '{source_id}' missing required field 'url'")
                if not self._is_http_url_with_hostname(url):
                    raise ValueError(f"Source '{source_id}' has invalid field 'url'")

                platform = source.get("platform", "auto")
                if platform not in self._ALLOWED_PODCAST_PLATFORMS:
                    raise ValueError(f"Source '{source_id}' has invalid field 'platform'")
                if platform == "xiaoyuzhou" and not self._is_xiaoyuzhou_podcast_url(url):
                    raise ValueError(f"Source '{source_id}' has invalid Xiaoyuzhou podcast url")

                if "transcript" in source:
                    transcript = source["transcript"]
                    if not isinstance(transcript, dict):
                        raise ValueError(f"Source '{source_id}' has invalid field 'transcript'")

                    enabled = transcript.get("enabled", False)
                    if "enabled" in transcript and not isinstance(enabled, bool):
                        raise ValueError(f"Source '{source_id}' has invalid field 'transcript.enabled'")

                    backend = transcript.get("backend", "auto")
                    if backend not in self._ALLOWED_TRANSCRIPT_BACKENDS:
                        raise ValueError(f"Source '{source_id}' has invalid field 'transcript.backend'")
                    if backend == "opencli" and not self._supports_opencli_transcript(platform, url):
                        raise ValueError(f"Source '{source_id}' has invalid field 'transcript.backend'")

                    languages = transcript.get("languages", [])
                    if "languages" in transcript and (
                        not isinstance(languages, list)
                        or not all(isinstance(language, str) for language in languages)
                    ):
                        raise ValueError(f"Source '{source_id}' has invalid field 'transcript.languages'")

    def _validate_topics_payload(self, topics: Any) -> None:
        if not isinstance(topics, list):
            raise ValueError("'topics' should be a list")

        for index, topic in enumerate(topics):
            if not isinstance(topic, dict):
                raise ValueError(f"Topic at index {index} should be an object")

            topic_id = topic.get("id", f"index:{index}")
            missing = []
            for field in ("id", "search"):
                if field not in topic:
                    missing.append(field)
            if missing:
                raise ValueError(
                    f"Topic '{topic_id}' missing required field(s): {', '.join(missing)}"
                )

            if not isinstance(topic["id"], str) or not topic["id"].strip():
                raise ValueError(f"Topic '{topic_id}' has invalid 'id'")

            search = topic["search"]
            if not isinstance(search, dict):
                raise ValueError(f"Topic '{topic_id}' has invalid 'search' value")

            queries = search.get("queries")
            if "queries" not in search:
                raise ValueError(f"Topic '{topic_id}' missing required field 'search.queries'")
            if not isinstance(queries, list) or not all(isinstance(query, str) for query in queries):
                raise ValueError(f"Topic '{topic_id}' has invalid field 'search.queries'; expected string array")

    def do_OPTIONS(self) -> None:
        parsed = urlparse(self.path)
        if not parsed.path.startswith("/api/"):
            self.send_response(200)
            self.send_header("Allow", "GET, OPTIONS")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            return

        if parsed.path == "/api/file" and not self._is_allowed_write_origin():
            return self._api_error(403, "forbidden: cross-origin writes are not allowed")
        if parsed.path not in {"/api/file", "/api/list", "/api/"}:
            if parsed.path.startswith("/api/"):
                return self._api_error(404, "not found")

        requested_method = (self.headers.get("Access-Control-Request-Method") or "").upper()
        allow_methods = "GET, OPTIONS"
        if requested_method == "POST" or parsed.path == "/api/file":
            allow_methods = "GET, POST, OPTIONS"

        self.send_response(200)
        self._send_cors_headers()
        self.send_header("Access-Control-Allow-Methods", allow_methods)
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Max-Age", "600")
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if not parsed.path.startswith("/api/"):
            return super().do_GET()

        if parsed.path == "/api/list":
            payload = {
                "ok": True,
                "files": [
                    {
                        "key": key,
                        "path": str(info["path"].relative_to(BASE_DIR)),
                        "label_zh": info["label_zh"],
                        "label_en": info["label_en"],
                    }
                    for key, info in ALLOWED_FILES.items()
                ],
            }
            return self._send_json(payload)

        if parsed.path == "/api/file":
            try:
                key = self._validate_key()
            except ValueError:
                return self._api_error(400, "invalid file key")

            info = ALLOWED_FILES[key]
            path = info["path"]

            if not path.exists():
                return self._api_error(404, f"config file not found: {path}")

            try:
                with path.open("r", encoding="utf-8") as fp:
                    content = json.load(fp)
            except json.JSONDecodeError as exc:
                return self._api_error(500, f"invalid config JSON in {path.name}: {exc}")
            except OSError as exc:
                return self._api_error(500, f"failed to read config file {path.name}: {exc}")

            return self._send_json(
                {
                    "ok": True,
                    "key": key,
                    "path": str(path.relative_to(BASE_DIR)),
                    "content": content,
                    "pretty": json.dumps(content, ensure_ascii=False, indent=2),
                }
            )

        self._api_error(404, "not found")

    def do_POST(self) -> None:
        if urlparse(self.path).path != "/api/file":
            return self._api_error(404, "not found")

        if not self._is_allowed_write_origin():
            return self._api_error(403, "forbidden: cross-origin writes are not allowed")

        try:
            payload = self._read_request_json()
            if not isinstance(payload, dict):
                raise TypeError("invalid request body")
            key = payload.get("key")
            content = payload.get("content")
        except (json.JSONDecodeError, TypeError, UnicodeDecodeError, ValueError):
            return self._api_error(400, "invalid request body")

        if key not in ALLOWED_FILES:
            return self._api_error(400, "invalid file key")

        if content is None:
            return self._api_error(400, "missing content")
        if not isinstance(content, dict):
            return self._api_error(400, "invalid content type; expected object")

        try:
            path = ALLOWED_FILES[key]["path"]
            if key not in content:
                raise ValueError(f"missing top-level key '{key}'")
            if key == "sources":
                self._normalize_sources_payload(content.get("sources"))
                self._validate_sources_payload(content.get("sources"))
            if key == "topics":
                self._validate_topics_payload(content.get("topics"))

            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("w", encoding="utf-8") as fp:
                json.dump(content, fp, ensure_ascii=False, indent=2)
                fp.write("\n")
            self._send_json({"ok": True, "key": key, "message": "saved"}, 200)
            return
        except ValueError as exc:
            return self._api_error(400, str(exc))
        except OSError as exc:
            return self._api_error(500, str(exc))


class ConfigEditorHTTPServer(HTTPServer):
    pass


class IPv6ConfigEditorHTTPServer(ConfigEditorHTTPServer):
    address_family = socket.AF_INET6


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Config editor backend for follow-news")
    parser.add_argument("--host", default="127.0.0.1", help="Bind host")
    parser.add_argument("--port", type=int, default=8787, help="Bind port")
    return parser


def main() -> int:
    args = create_parser().parse_args()
    os.chdir(STATIC_DIR)
    server_class = IPv6ConfigEditorHTTPServer if ConfigEditorHandler._is_ipv6_host(args.host) else ConfigEditorHTTPServer
    httpd = server_class((args.host, args.port), ConfigEditorHandler)
    print(f"Config editor started at http://{args.host}:{args.port}")
    print(f"Serving static files from: {STATIC_DIR}")
    print("Editable files:")
    for key, info in ALLOWED_FILES.items():
        print(f"  - {key}: {info['path']}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
