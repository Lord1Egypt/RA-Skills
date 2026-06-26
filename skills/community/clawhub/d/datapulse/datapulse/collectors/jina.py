"""Jina enhanced collector with CSS targeting, caching control, and more."""

from __future__ import annotations

from urllib.parse import urlparse

from datapulse.core.jina_client import JinaAPIClient, JinaBlockedByPolicyError, JinaReadOptions
from datapulse.core.models import SourceType
from datapulse.core.retry import CircuitBreakerOpen
from datapulse.core.security import has_secret
from datapulse.core.utils import clean_text

from .base import BaseCollector, ParseResult


class JinaCollector(BaseCollector):
    name = "jina"
    source_type = SourceType.GENERIC
    reliability = 0.72
    tier = 1
    setup_hint = "Set JINA_API_KEY for higher rate limits"

    def check(self) -> dict[str, str | bool]:
        if has_secret("JINA_API_KEY"):
            return {"status": "ok", "message": "JINA_API_KEY set", "available": True}
        return {"status": "warn", "message": "JINA_API_KEY not set (anonymous rate limits apply)", "available": True}

    def __init__(
        self,
        *,
        target_selector: str = "",
        wait_for_selector: str = "",
        no_cache: bool = False,
        with_alt: bool = False,
        cookie: str = "",
        proxy_url: str = "",
        api_key: str = "",
    ):
        self.target_selector = target_selector
        self.wait_for_selector = wait_for_selector
        self.no_cache = no_cache
        self.with_alt = with_alt
        self.cookie = cookie
        self._client = JinaAPIClient(api_key=api_key, proxy_url=proxy_url)

    def can_handle(self, url: str) -> bool:
        return True

    def parse(self, url: str) -> ParseResult:
        parsed = urlparse(url)
        if not parsed.scheme:
            return ParseResult.failure(url, "Invalid URL: missing scheme")

        try:
            opts = JinaReadOptions(
                target_selector=self.target_selector,
                wait_for_selector=self.wait_for_selector,
                no_cache=self.no_cache,
                with_generated_alt=self.with_alt,
                cookie=self.cookie,
            )
            result = self._client.read(url, options=opts)
            text = result.content

            lines = [ln for ln in text.splitlines() if ln.strip()]
            title = ""
            if lines:
                title = lines[0].lstrip("#").strip()
                content = "\n".join(lines[1:]).strip()
            else:
                content = ""

            confidence_flags = self._build_confidence_flags()

            return ParseResult(
                url=url,
                title=clean_text(title)[:200],
                content=clean_text(content),
                author="",
                excerpt=self._safe_excerpt(content),
                source_type=self.source_type,
                tags=["jina", self.source_type.value],
                confidence_flags=confidence_flags,
                extra={"collector": "jina"},
            )
        except CircuitBreakerOpen as exc:
            return ParseResult.failure(url, f"Jina circuit open: {exc}")
        except JinaBlockedByPolicyError as exc:
            return ParseResult.failure(url, str(exc))
        except Exception as exc:
            return ParseResult.failure(url, f"JinaCollector failed: {exc}")

    def _build_confidence_flags(self) -> list[str]:
        flags = ["markdown_proxy"]
        if self.target_selector:
            flags.append("css_targeted")
        if self.with_alt:
            flags.append("image_captioned")
        return flags
