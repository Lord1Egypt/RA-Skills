"""Collector/router layer for DataPulse."""

from __future__ import annotations

import logging

from datapulse.collectors import (
    ArxivCollector,
    BaseCollector,
    BilibiliCollector,
    GenericCollector,
    GitHubCollector,
    HackerNewsCollector,
    JinaCollector,
    NativeBridgeCollector,
    ParseResult,
    RedditCollector,
    RssCollector,
    TelegramCollector,
    TrendingCollector,
    TwitterCollector,
    WeChatCollector,
    WeiboCollector,
    XiaohongshuCollector,
    YouTubeCollector,
)
from datapulse.core.utils import resolve_platform_hint

logger = logging.getLogger("datapulse.router")


def _is_policy_block(error: str) -> bool:
    text = (error or "").lower()
    return (
        "unavailable for legal reasons" in text
        or "blocked by policy" in text
        or "jina blocked by policy" in text
    )


class ParsePipeline:
    def __init__(self, extra_parsers: list[BaseCollector] | None = None):
        configured = extra_parsers or []
        self.parsers: list[BaseCollector] = []
        self.parsers.extend(configured)
        self.parsers.extend([
            TwitterCollector(),
            YouTubeCollector(),
            RedditCollector(),
            BilibiliCollector(),
            TelegramCollector(),
            NativeBridgeCollector(),
            WeChatCollector(),
            WeiboCollector(),
            XiaohongshuCollector(),
            ArxivCollector(),
            HackerNewsCollector(),
            GitHubCollector(),
            TrendingCollector(),
            RssCollector(),
            GenericCollector(),
            JinaCollector(),
        ])

    def register_parser(self, parser: BaseCollector, priority: bool = False) -> None:
        if priority:
            self.parsers.insert(0, parser)
        else:
            self.parsers.append(parser)

    @property
    def available_parsers(self) -> list[str]:
        return [p.name for p in self.parsers]

    def route(self, url: str) -> tuple[ParseResult, BaseCollector]:
        hint = resolve_platform_hint(url)
        prioritized: list[BaseCollector] = []
        fallback: list[BaseCollector] = []
        for parser in self.parsers:
            if parser.name == "native_bridge":
                prioritized.append(parser)
            elif parser.name == hint or parser.source_type.value == hint:
                prioritized.append(parser)
            else:
                fallback.append(parser)

        best_match: BaseCollector | None = None
        for parser in prioritized + fallback:
            try:
                if not parser.can_handle(url):
                    continue
                if best_match is None:
                    best_match = parser
                logger.info("Routing with %s for %s", parser.name, url)
                result = parser.parse(url)
                if result.success:
                    return result, parser

                if _is_policy_block(result.error):
                    logger.info("%s policy-blocked for %s: %s", parser.name, url, result.error)
                else:
                    logger.warning("%s failed for %s: %s", parser.name, url, result.error)
            except Exception as exc:
                message = str(exc)
                if _is_policy_block(message):
                    logger.info("%s policy-blocked for %s: %s", parser.name, url, message)
                else:
                    logger.warning("%s raised for %s: %s", parser.name, url, message)
                result = ParseResult.failure(url, str(exc))

        # Build actionable error with setup hint from best match
        chosen = best_match or self.parsers[-1]
        error_msg = f"No parser produced successful result for {url}"
        if chosen.setup_hint:
            error_msg += f"\nHint ({chosen.name}): {chosen.setup_hint}"
        return ParseResult.failure(url, error_msg), chosen

    def doctor(self) -> dict[str, list[dict[str, str | bool]]]:
        """Run health checks on all registered parsers, grouped by tier."""
        report: dict[str, list[dict[str, str | bool]]] = {
            "tier_0": [],
            "tier_1": [],
            "tier_2": [],
        }
        for parser in self.parsers:
            check = parser.check()
            status = str(check.get("status", "ok"))
            available = bool(check.get("available", True))
            raw_ok = check.get("ok")
            if isinstance(raw_ok, bool):
                ok = raw_ok
            else:
                ok = available and status in {"ok", "warn"}
            entry: dict[str, str | bool] = {
                "name": parser.name,
                "status": status,
                "message": check.get("message", ""),
                "available": available,
                "ok": ok,
                "setup_hint": parser.setup_hint,
            }
            tier_key = f"tier_{parser.tier}"
            if tier_key not in report:
                tier_key = "tier_2"
            report[tier_key].append(entry)
        return report
