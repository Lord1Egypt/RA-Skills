"""Sidecar-backed native collector bridge."""

from __future__ import annotations

import json
import os
import shlex
import subprocess
from pathlib import Path
from urllib.parse import urlparse

from datapulse.core.models import SourceType
from datapulse.core.utils import clean_text, session_dir, session_path

from .base import BaseCollector, ParseResult

REQUEST_SCHEMA_VERSION = "native_collector_bridge_request.v1"
RESULT_SCHEMA_VERSION = "native_collector_bridge_result.v1"
BRIDGE_PROFILE = "mediacrawler"

BRIDGE_CMD_ENV = "DATAPULSE_NATIVE_COLLECTOR_BRIDGE_CMD"
BRIDGE_WORKDIR_ENV = "DATAPULSE_NATIVE_COLLECTOR_BRIDGE_WORKDIR"
BRIDGE_TIMEOUT_ENV = "DATAPULSE_NATIVE_COLLECTOR_BRIDGE_TIMEOUT_SECONDS"
BRIDGE_STATE_DIR_ENV = "DATAPULSE_NATIVE_COLLECTOR_STATE_DIR"

DEFAULT_TIMEOUT_SECONDS = 45
DEFAULT_STATE_DIR = Path.home() / ".datapulse" / "native_collectors"
_NEAR_EMPTY_CONTENT_THRESHOLD = 12

_HOST_SOURCE_TYPES: dict[str, str] = {
    "xiaohongshu.com": "xhs",
    "www.xiaohongshu.com": "xhs",
    "xhslink.com": "xhs",
    "xhslink.cn": "xhs",
    "www.zhihu.com": "zhihu",
    "zhihu.com": "zhihu",
    "zhuanlan.zhihu.com": "zhihu",
    "tieba.baidu.com": "tieba",
    "www.douyin.com": "douyin",
    "douyin.com": "douyin",
    "v.douyin.com": "douyin",
    "www.iesdouyin.com": "douyin",
    "iesdouyin.com": "douyin",
    "www.kuaishou.com": "kuaishou",
    "kuaishou.com": "kuaishou",
    "v.kuaishou.com": "kuaishou",
}


def _normalize_string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    normalized: list[str] = []
    for item in value:
        text = str(item).strip()
        if text and text not in normalized:
            normalized.append(text)
    return normalized


def _meaningful_length(text: str) -> int:
    return len("".join(text.split()))


class NativeBridgeCollector(BaseCollector):
    name = "native_bridge"
    source_type = SourceType.GENERIC
    reliability = 0.76
    tier = 2
    timeout = DEFAULT_TIMEOUT_SECONDS
    bridge_profile = BRIDGE_PROFILE
    host_source_types = _HOST_SOURCE_TYPES
    setup_hint = (
        f"Set {BRIDGE_CMD_ENV} to enable the MediaCrawler-class sidecar bridge "
        "(optional: DATAPULSE_NATIVE_COLLECTOR_BRIDGE_WORKDIR / "
        "DATAPULSE_NATIVE_COLLECTOR_BRIDGE_TIMEOUT_SECONDS / "
        "DATAPULSE_NATIVE_COLLECTOR_STATE_DIR)"
    )

    def check(self) -> dict[str, str | bool]:
        command = os.getenv(BRIDGE_CMD_ENV, "").strip()
        if not command:
            return {
                "status": "warn",
                "message": f"{BRIDGE_CMD_ENV} not set; native sidecar bridge disabled",
                "available": False,
            }
        return {
            "status": "ok",
            "message": f"native sidecar bridge configured for profile {self.bridge_profile}",
            "available": True,
        }

    def can_handle(self, url: str) -> bool:
        return bool(self._source_type_hint(url))

    def parse(self, url: str) -> ParseResult:
        command = self._command()
        if not command:
            return ParseResult.failure(url, f"bridge_unavailable: {BRIDGE_CMD_ENV} not set")

        source_type_hint = self._source_type_hint(url)
        if not source_type_hint:
            return ParseResult.failure(url, "unsupported_url: native bridge profile does not cover this URL")

        timeout_seconds = self._timeout_seconds()
        request_payload = self._build_request(url, source_type_hint, timeout_seconds)

        try:
            completed = subprocess.run(
                command,
                input=json.dumps(request_payload, ensure_ascii=True),
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                check=False,
                cwd=self._workdir(),
                env=self._bridge_env(),
            )
        except subprocess.TimeoutExpired:
            return ParseResult.failure(
                url,
                f"bridge_unavailable: native bridge timed out after {timeout_seconds}s",
            )
        except OSError as exc:
            return ParseResult.failure(url, f"bridge_unavailable: {exc}")

        stderr = (completed.stderr or "").strip()
        if completed.returncode != 0:
            tail = stderr.splitlines()[-1] if stderr else ""
            detail = f" ({tail})" if tail else ""
            return ParseResult.failure(
                url,
                f"bridge_unavailable: native bridge exited with code {completed.returncode}{detail}",
            )

        stdout = (completed.stdout or "").strip()
        if not stdout:
            return ParseResult.failure(url, "bridge_unavailable: native bridge returned empty stdout")

        try:
            payload = json.loads(stdout)
        except json.JSONDecodeError:
            return ParseResult.failure(url, "bridge_unavailable: native bridge returned invalid JSON")

        return self._normalize_response(url, source_type_hint, payload)

    def _command(self) -> list[str]:
        raw = os.getenv(BRIDGE_CMD_ENV, "").strip()
        if not raw:
            return []
        return shlex.split(raw)

    def _workdir(self) -> str | None:
        raw = os.getenv(BRIDGE_WORKDIR_ENV, "").strip()
        if not raw:
            return None
        return str(Path(raw).expanduser())

    def _timeout_seconds(self) -> int:
        raw = os.getenv(BRIDGE_TIMEOUT_ENV, "").strip()
        if not raw:
            return self.timeout
        try:
            return max(1, int(float(raw)))
        except ValueError:
            return self.timeout

    def _state_dir(self) -> str:
        raw = os.getenv(BRIDGE_STATE_DIR_ENV, "").strip()
        directory = Path(raw).expanduser() if raw else DEFAULT_STATE_DIR
        directory.mkdir(parents=True, exist_ok=True)
        return str(directory)

    def _bridge_env(self) -> dict[str, str]:
        env = dict(os.environ)
        if not env.get(BRIDGE_STATE_DIR_ENV, "").strip():
            env[BRIDGE_STATE_DIR_ENV] = self._state_dir()
        if not env.get("DATAPULSE_SESSION_DIR", "").strip():
            env["DATAPULSE_SESSION_DIR"] = str(session_dir())
        return env

    def _source_type_hint(self, url: str) -> str:
        hostname = (urlparse(url).hostname or "").lower()
        return self.host_source_types.get(hostname, "")

    def _session_payload(self, source_type_hint: str) -> dict[str, object] | None:
        if source_type_hint != "xhs":
            return None
        return {
            "key": "xhs",
            "path": session_path("xhs"),
            "required": False,
        }

    def _fallback_chain(self, source_type_hint: str) -> list[str]:
        if source_type_hint == "xhs":
            return ["jina", "browser"]
        return ["generic", "jina"]

    def _fallback_policy(self, source_type_hint: str) -> str:
        if source_type_hint == "xhs":
            return "xhs_native_then_jina_then_browser"
        raw = source_type_hint or "generic"
        return f"{raw}_native_then_generic_then_jina"

    def _build_request(self, url: str, source_type_hint: str, timeout_seconds: int) -> dict[str, object]:
        payload: dict[str, object] = {
            "schema_version": REQUEST_SCHEMA_VERSION,
            "profile": self.bridge_profile,
            "url": url,
            "source_type_hint": source_type_hint,
            "timeout_seconds": timeout_seconds,
            "metadata": {
                "allow_fallback": True,
                "fallback_chain": self._fallback_chain(source_type_hint),
            },
        }
        session_payload = self._session_payload(source_type_hint)
        if session_payload is not None:
            payload["session"] = session_payload
        return payload

    def _normalize_response(
        self,
        url: str,
        source_type_hint: str,
        payload: object,
    ) -> ParseResult:
        if not isinstance(payload, dict):
            return ParseResult.failure(url, "bridge_unavailable: native bridge result must be a JSON object")

        schema_version = str(payload.get("schema_version", "")).strip()
        if schema_version != RESULT_SCHEMA_VERSION:
            return ParseResult.failure(
                url,
                f"bridge_unavailable: unexpected native bridge schema {schema_version or 'missing'}",
            )

        if not bool(payload.get("ok", False)):
            error_code = str(payload.get("error_code", "bridge_unavailable")).strip() or "bridge_unavailable"
            error = str(payload.get("error", "native bridge failed")).strip() or "native bridge failed"
            return ParseResult.failure(url, f"{error_code}: {error}")

        content = clean_text(str(payload.get("content", "")))
        if _meaningful_length(content) < _NEAR_EMPTY_CONTENT_THRESHOLD:
            return ParseResult.failure(url, "bridge_unavailable: native bridge returned empty or near-empty content")

        raw_source_type = str(payload.get("source_type", "")).strip().lower() or source_type_hint
        tags = _normalize_string_list(payload.get("tags"))
        for tag in [raw_source_type, "native-bridge", self.bridge_profile]:
            if tag and tag not in tags:
                tags.append(tag)

        confidence_flags = _normalize_string_list(payload.get("confidence_flags"))
        if "native-bridge" not in confidence_flags:
            confidence_flags.append("native-bridge")

        provenance_input = payload.get("provenance")
        provenance_payload = dict(provenance_input) if isinstance(provenance_input, dict) else {}
        session_key = str(provenance_payload.get("session_key", "")).strip()
        if session_key and "session-authenticated" not in confidence_flags:
            confidence_flags.append("session-authenticated")

        provenance: dict[str, object] = {
            "collector_family": str(provenance_payload.get("collector_family", "native_sidecar")),
            "bridge_profile": str(provenance_payload.get("bridge_profile", self.bridge_profile)),
            "transport": str(provenance_payload.get("transport", "subprocess_json")),
            "session_key": session_key,
            "session_mode": str(
                provenance_payload.get(
                    "session_mode",
                    "playwright_storage_state" if session_key else "none",
                )
            ),
            "raw_source_type": str(
                provenance_payload.get("raw_source_type", raw_source_type or source_type_hint or "generic")
            ),
            "fallback_policy": str(
                provenance_payload.get("fallback_policy", self._fallback_policy(raw_source_type or source_type_hint))
            ),
        }
        for key in ("sidecar_name", "sidecar_version", "warnings", "rate_limit_window"):
            if key in provenance_payload:
                provenance[key] = provenance_payload[key]

        extra_input = payload.get("extra")
        extra = dict(extra_input) if isinstance(extra_input, dict) else {}
        extra["collector_provenance"] = provenance

        excerpt = clean_text(str(payload.get("excerpt", ""))) or self._safe_excerpt(content)

        return ParseResult(
            url=str(payload.get("canonical_url", "")).strip() or url,
            title=clean_text(str(payload.get("title", ""))),
            content=content,
            author=clean_text(str(payload.get("author", ""))),
            excerpt=excerpt,
            source_type=self._source_type(raw_source_type),
            tags=tags,
            confidence_flags=confidence_flags,
            extra=extra,
        )

    def _source_type(self, raw_source_type: str) -> SourceType:
        mapping = {
            "xhs": SourceType.XHS,
            "wechat": SourceType.WECHAT,
            "weibo": SourceType.WEIBO,
            "bilibili": SourceType.BILIBILI,
            "rss": SourceType.RSS,
        }
        return mapping.get(raw_source_type, SourceType.GENERIC)
