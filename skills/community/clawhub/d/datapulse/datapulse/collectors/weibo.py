"""Weibo collector with native/Jina fallback."""

from __future__ import annotations

import os
from urllib.parse import urlparse

from datapulse.core.models import SourceType

from .base import BaseCollector, ParseResult
from .jina import JinaCollector
from .native_bridge import BRIDGE_CMD_ENV, NativeBridgeCollector

WEIBO_BRIDGE_PROFILE = "weibo_spider"
WEIBO_FALLBACK_POLICY = "weibo_native_then_jina"
_WEIBO_HOSTS = {
    "weibo.com",
    "www.weibo.com",
    "weibo.cn",
    "www.weibo.cn",
    "m.weibo.cn",
}


def _merge_unique(values: list[str] | None, *required: str) -> list[str]:
    merged: list[str] = []
    for item in [*(values or []), *required]:
        text = str(item).strip()
        if text and text not in merged:
            merged.append(text)
    return merged


def _with_collector_provenance(
    extra: dict | None,
    *,
    transport: str,
    collector_family: str,
) -> dict:
    payload = dict(extra) if isinstance(extra, dict) else {}
    payload["collector_provenance"] = {
        "collector_family": collector_family,
        "bridge_profile": WEIBO_BRIDGE_PROFILE,
        "transport": transport,
        "session_key": "",
        "session_mode": "none",
        "raw_source_type": "weibo",
        "fallback_policy": WEIBO_FALLBACK_POLICY,
    }
    return payload


class _WeiboNativeBridgeCollector(NativeBridgeCollector):
    name = "weibo_native_bridge"
    source_type = SourceType.WEIBO
    bridge_profile = WEIBO_BRIDGE_PROFILE
    host_source_types = {host: "weibo" for host in _WEIBO_HOSTS}
    setup_hint = f"Set {BRIDGE_CMD_ENV} to enable native Weibo extraction"

    def _fallback_chain(self, source_type_hint: str) -> list[str]:
        return ["jina"]

    def _fallback_policy(self, source_type_hint: str) -> str:
        return WEIBO_FALLBACK_POLICY


class WeiboCollector(BaseCollector):
    name = "weibo"
    source_type = SourceType.WEIBO
    reliability = 0.73
    tier = 2
    setup_hint = f"Set {BRIDGE_CMD_ENV} to enable native Weibo extraction"

    def check(self) -> dict[str, str | bool]:
        if os.getenv(BRIDGE_CMD_ENV, "").strip():
            return {
                "status": "ok",
                "message": "Native Weibo sidecar configured; Jina fallback available",
                "available": True,
            }
        return {
            "status": "warn",
            "message": f"{BRIDGE_CMD_ENV} not set; Weibo collector will use Jina fallback only",
            "available": True,
        }

    def can_handle(self, url: str) -> bool:
        hostname = (urlparse(url).hostname or "").lower()
        return hostname in _WEIBO_HOSTS

    def parse(self, url: str) -> ParseResult:
        native_result = self._parse_native(url)
        if native_result is not None and native_result.success:
            return native_result

        result = JinaCollector().parse(url)
        if result.success:
            return ParseResult(
                url=result.url or url,
                title=result.title,
                content=result.content,
                author=result.author,
                excerpt=result.excerpt,
                source_type=self.source_type,
                tags=_merge_unique(result.tags, "weibo", "jina-fallback"),
                confidence_flags=_merge_unique(result.confidence_flags, "weibo", "jina"),
                extra=_with_collector_provenance(
                    result.extra,
                    transport="jina_reader",
                    collector_family="jina_fallback",
                ),
            )

        if "blocked by policy" in (result.error or "").lower() and not os.getenv(BRIDGE_CMD_ENV, "").strip():
            return ParseResult.failure(
                url,
                f"Weibo blocked by Jina policy; set {BRIDGE_CMD_ENV} to enable the native Weibo path.",
            )

        failures: list[str] = []
        if native_result is not None and native_result.error:
            failures.append(f"native={native_result.error}")
        if result.error:
            failures.append(f"jina={result.error}")
        if failures:
            return ParseResult.failure(url, "; ".join(failures))
        return result

    def _parse_native(self, url: str) -> ParseResult | None:
        if not os.getenv(BRIDGE_CMD_ENV, "").strip():
            return None
        return _WeiboNativeBridgeCollector().parse(url)
