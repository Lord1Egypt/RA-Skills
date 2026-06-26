"""WeChat collector with native/Jina/browser fallback chain."""

from __future__ import annotations

import os

from datapulse.core.models import SourceType
from datapulse.core.utils import session_path, session_valid

from .base import BaseCollector, ParseResult
from .jina import JinaCollector
from .native_bridge import BRIDGE_CMD_ENV, NativeBridgeCollector

WECHAT_BRIDGE_PROFILE = "wechat_spider"
WECHAT_FALLBACK_POLICY = "wechat_native_then_jina_then_browser"


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
    session_key: str = "",
) -> dict:
    payload = dict(extra) if isinstance(extra, dict) else {}
    payload["collector_provenance"] = {
        "collector_family": collector_family,
        "bridge_profile": WECHAT_BRIDGE_PROFILE,
        "transport": transport,
        "session_key": session_key,
        "session_mode": "playwright_storage_state" if session_key else "none",
        "raw_source_type": "wechat",
        "fallback_policy": WECHAT_FALLBACK_POLICY,
    }
    return payload


class _WeChatNativeBridgeCollector(NativeBridgeCollector):
    name = "wechat_native_bridge"
    source_type = SourceType.WECHAT
    bridge_profile = WECHAT_BRIDGE_PROFILE
    host_source_types = {"mp.weixin.qq.com": "wechat"}
    setup_hint = (
        f"Run: datapulse --login wechat and set {BRIDGE_CMD_ENV} "
        "to enable native article extraction"
    )

    def _session_payload(self, source_type_hint: str) -> dict[str, object] | None:
        if source_type_hint != "wechat":
            return None
        return {
            "key": "wechat",
            "path": session_path("wechat"),
            "required": True,
        }

    def _fallback_chain(self, source_type_hint: str) -> list[str]:
        return ["jina", "browser"]

    def _fallback_policy(self, source_type_hint: str) -> str:
        return WECHAT_FALLBACK_POLICY


class WeChatCollector(BaseCollector):
    name = "wechat"
    source_type = SourceType.WECHAT
    reliability = 0.8
    tier = 2
    setup_hint = (
        f"Run: datapulse --login wechat; set {BRIDGE_CMD_ENV} "
        "to enable native article extraction"
    )

    def check(self) -> dict[str, str | bool]:
        bridge_configured = bool(os.getenv(BRIDGE_CMD_ENV, "").strip())
        if session_valid("wechat"):
            if bridge_configured:
                return {
                    "status": "ok",
                    "message": "WeChat session valid; native sidecar, Jina, and browser fallback available",
                    "available": True,
                }
            return {
                "status": "warn",
                "message": f"WeChat session valid; set {BRIDGE_CMD_ENV} to enable native article extraction",
                "available": True,
            }
        if bridge_configured:
            return {
                "status": "warn",
                "message": "No WeChat session; native and browser fallback require datapulse --login wechat",
                "available": True,
            }
        return {
            "status": "warn",
            "message": f"No WeChat session and {BRIDGE_CMD_ENV} not set; Jina-only mode",
            "available": True,
        }

    def can_handle(self, url: str) -> bool:
        return "mp.weixin.qq.com" in url.lower()

    def parse(self, url: str) -> ParseResult:
        native_result = self._parse_native(url)
        if native_result is not None and native_result.success:
            return native_result

        jina = JinaCollector()
        result = jina.parse(url)
        if result.success:
            return ParseResult(
                url=url,
                title=result.title,
                content=result.content,
                author=result.author,
                excerpt=result.excerpt,
                source_type=self.source_type,
                tags=_merge_unique(result.tags, "wechat", "jina-fallback"),
                confidence_flags=_merge_unique(result.confidence_flags, "wechat", "jina"),
                extra=_with_collector_provenance(
                    result.extra,
                    transport="jina_reader",
                    collector_family="jina_fallback",
                ),
            )

        browser_result = self._parse_browser(url)
        if browser_result.success:
            return browser_result

        if "blocked by policy" in (result.error or "").lower():
            if not session_valid("wechat"):
                return ParseResult.failure(
                    url,
                    "WeChat blocked by Jina policy; run datapulse --login wechat to enable browser and native fallbacks.",
                )
            if not os.getenv(BRIDGE_CMD_ENV, "").strip():
                return ParseResult.failure(
                    url,
                    f"WeChat blocked by Jina policy; set {BRIDGE_CMD_ENV} to enable the native article path.",
                )

        failures: list[str] = []
        if native_result is not None and native_result.error:
            failures.append(f"native={native_result.error}")
        if result.error:
            failures.append(f"jina={result.error}")
        if browser_result.error:
            failures.append(f"browser={browser_result.error}")
        if failures:
            return ParseResult.failure(url, "; ".join(failures))
        return result

    def _parse_native(self, url: str) -> ParseResult | None:
        if not self._native_prerequisites_met():
            return None
        return _WeChatNativeBridgeCollector().parse(url)

    def _native_prerequisites_met(self) -> bool:
        return bool(os.getenv(BRIDGE_CMD_ENV, "").strip()) and session_valid("wechat")

    def _parse_browser(self, url: str) -> ParseResult:
        if not session_valid("wechat"):
            return ParseResult.failure(url, "browser_unavailable: missing wechat session")

        try:
            from .browser import BrowserCollector
        except Exception as exc:
            return ParseResult.failure(url, f"browser_unavailable: {exc}")

        result = BrowserCollector().parse(url, storage_state=session_path("wechat"))
        if result.success:
            result.source_type = self.source_type
            result.tags = _merge_unique(result.tags, "wechat", "browser-fallback")
            result.confidence_flags = _merge_unique(
                result.confidence_flags,
                "browser-fallback",
                "wechat-browser",
            )
            result.extra = _with_collector_provenance(
                result.extra,
                transport="browser_playwright",
                collector_family="browser_fallback",
                session_key="wechat",
            )
        return result
