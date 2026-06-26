#!/usr/bin/env python3
"""CryptoRank free-layer demo CLI.

This script recreates several high-signal CryptoRank views by combining:
1. public page bootstrap data from `__NEXT_DATA__`
2. public website endpoints used by the frontend

It is intentionally dependency-free so it can be demoed in a fresh Python
environment without extra installation steps.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/136.0.0.0 Safari/537.36"
)
SITE_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}
JSON_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "application/json, text/plain, */*",
}
AIRDROP_HEADERS = {
    **JSON_HEADERS,
    "Origin": "https://cryptorank.io",
    "Referer": "https://cryptorank.io/drophunting",
}
OUTPUT_LANG = "zh"
SUPPORT_LINKS = {
    "community": "https://t.me/hollyink",
    "bot": "https://t.me/yongzhuan_bot",
    "tutorial": "https://www.youtube.com/@0xcii",
}

TRANSLATIONS = {
    "zh": {
        "na": "暂无",
        "today": "今天",
        "in_1d": "1天后",
        "days_ago": "{days}天前",
        "in_days": "{days}天后",
        "market": "市场总览",
        "top_coins": "头部币种",
        "top_gainers": "涨幅榜",
        "top_losers": "跌幅榜",
        "upcoming_sales": "即将开始的 IDO/ICO",
        "recent_funding": "近期融资",
        "recent_rounds": "近期轮次",
        "airdrop_activities": "空投 / 活动雷达",
        "daily_brief": "CryptoRank 每日简报",
        "market_snapshot": "市场快照",
        "watch_today": "今天值得看",
        "momentum_leaders": "趋势领涨",
        "overview": "概览",
        "timestamp": "生成时间",
        "project": "项目",
        "coin": "币种",
        "price": "价格",
        "mcap": "市值",
        "category": "类别",
        "launchpad": "平台",
        "when": "时间",
        "raise": "融资额",
        "funds": "机构",
        "stage": "阶段",
        "date": "日期",
        "signal": "信号",
        "type": "类型",
        "status": "状态",
        "updated": "更新",
        "rate": "评分",
        "moni": "Moni",
        "btc_dominance": "BTC 占比",
        "eth_dominance": "ETH 占比",
        "market_cap": "总市值",
        "volume_24h": "24h 成交额",
        "funding_prefix": "融资",
        "upcoming_prefix": "预告",
        "airdrop_prefix": "空投",
        "on": "平台",
        "rating_word": "评分",
        "track": "继续跟踪",
        "best_tier": "最佳基金层级 T{tier}",
        "valuation": "估值",
        "confirmed": "已确认",
        "potential": "潜在",
        "ended": "已结束",
        "ongoing": "进行中",
        "verification": "验证中",
        "bounty_platform": "赏金平台",
        "post_ipo_debt": "上市后债务融资",
        "extended_series_b": "扩展 B 轮",
        "m_and_a": "并购",
        "hold": "持仓",
        "liquidity": "做市",
        "trading": "交易",
        "mainnet": "主网",
        "testnet": "测试网",
        "mint_nft": "铸造 NFT",
        "social": "社媒",
        "discord": "Discord",
        "invite": "邀请",
        "quest": "任务",
        "bridge": "跨链",
        "swap": "兑换",
        "deposit": "存款",
        "borrow": "借贷",
        "stake": "质押",
        "wallet": "钱包",
        "download": "下载",
        "angel": "天使轮",
        "pre_seed": "Pre-Seed",
        "seed": "Seed",
        "strategic": "战略轮",
        "series_a": "A 轮",
        "series_b": "B 轮",
        "series_c": "C 轮",
        "series_d": "D 轮",
        "grant": "Grant",
        "private_token_sale": "私募轮",
        "debt_financing": "债务融资",
        "pre_sale": "预售",
        "ido": "IDO",
        "ico": "ICO",
        "ieo": "IEO",
        "support_title": "如果你在安装、调用或使用中遇到问题，可继续：",
        "support_community": "社区排障",
        "support_bot": "机器人版本",
        "support_tutorial": "视频教程",
    },
    "en": {
        "na": "N/A",
        "today": "today",
        "in_1d": "in 1d",
        "days_ago": "{days}d ago",
        "in_days": "in {days}d",
        "market": "Market",
        "top_coins": "Top Coins",
        "top_gainers": "Top Gainers",
        "top_losers": "Top Losers",
        "upcoming_sales": "Upcoming Sales",
        "recent_funding": "Recent Funding",
        "recent_rounds": "Recent Rounds",
        "airdrop_activities": "Airdrop Activities",
        "daily_brief": "CryptoRank Daily Brief",
        "market_snapshot": "Market Snapshot",
        "watch_today": "Watch Today",
        "momentum_leaders": "Momentum Leaders",
        "overview": "Overview",
        "timestamp": "Timestamp",
        "project": "Project",
        "coin": "Coin",
        "price": "Price",
        "mcap": "MCap",
        "category": "Category",
        "launchpad": "Launchpad",
        "when": "When",
        "raise": "Raise",
        "funds": "Funds",
        "stage": "Stage",
        "date": "Date",
        "signal": "Signal",
        "type": "Type",
        "status": "Status",
        "updated": "Updated",
        "rate": "Rate",
        "moni": "Moni",
        "btc_dominance": "BTC Dominance",
        "eth_dominance": "ETH Dominance",
        "market_cap": "Market Cap",
        "volume_24h": "24h Volume",
        "funding_prefix": "Funding",
        "upcoming_prefix": "Upcoming",
        "airdrop_prefix": "Airdrop",
        "on": "on",
        "rating_word": "rating",
        "track": "track",
        "best_tier": "best tier T{tier}",
        "valuation": "valuation",
        "support_title": "If you run into setup, call, or usage issues, continue here:",
        "support_community": "Community",
        "support_bot": "Bot",
        "support_tutorial": "Tutorial",
    },
}

VALUE_MAP = {
    "zh": {
        "CONFIRMED": "已确认",
        "POTENTIAL": "潜在",
        "ENDED": "已结束",
        "ONGOING": "进行中",
        "VERIFICATION": "验证中",
        "Bounty Platform": "赏金平台",
        "Post-IPO Debt": "上市后债务融资",
        "Extended Series B": "扩展 B 轮",
        "M&A": "并购",
        "Hold": "持仓",
        "Liquidity": "做市",
        "Trading": "交易",
        "Mainnet": "主网",
        "Testnet": "测试网",
        "Mint NFT": "铸造 NFT",
        "Social": "社媒",
        "Discord": "Discord",
        "Invite": "邀请",
        "Quest": "任务",
        "Bridge": "跨链",
        "Swap": "兑换",
        "Deposit": "存款",
        "Borrow": "借贷",
        "Stake": "质押",
        "Wallet": "钱包",
        "Download": "下载",
        "ANGEL": "天使轮",
        "PRE SEED": "Pre-Seed",
        "SEED": "Seed",
        "STRATEGIC": "战略轮",
        "SERIES A": "A 轮",
        "SERIES B": "B 轮",
        "SERIES C": "C 轮",
        "SERIES D": "D 轮",
        "Grant": "Grant",
        "Debt Financing": "债务融资",
        "Private Token Sale": "私募轮",
        "Pre-sale": "预售",
        "IDO": "IDO",
        "ICO": "ICO",
        "IEO": "IEO",
    }
}


class FetchError(RuntimeError):
    """Raised when CryptoRank data cannot be fetched or parsed."""


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def t(lang: str, key: str, **kwargs: Any) -> str:
    value = TRANSLATIONS.get(lang, {}).get(key)
    if value is None:
        value = TRANSLATIONS["en"].get(key, key)
    if kwargs:
        return value.format(**kwargs)
    return value


def translate_value(value: Any, lang: str) -> str:
    text = safe_text(value)
    return VALUE_MAP.get(lang, {}).get(text, text)


def compact_number(value: Any) -> str:
    if value is None:
        return t(OUTPUT_LANG, "na")
    try:
        num = float(value)
    except (TypeError, ValueError):
        return str(value)
    sign = "-" if num < 0 else ""
    num = abs(num)
    units = [
        (1_000_000_000_000, "T"),
        (1_000_000_000, "B"),
        (1_000_000, "M"),
        (1_000, "K"),
    ]
    for threshold, suffix in units:
        if num >= threshold:
            return f"{sign}{num / threshold:.2f}{suffix}"
    if num >= 100:
        return f"{sign}{num:.0f}"
    if num >= 1:
        return f"{sign}{num:.2f}"
    return f"{sign}{num:.4f}"


def money(value: Any) -> str:
    if value is None:
        return t(OUTPUT_LANG, "na")
    return f"${compact_number(value)}"


def pct(value: Any) -> str:
    if value is None:
        return t(OUTPUT_LANG, "na")
    try:
        return f"{float(value):+.2f}%"
    except (TypeError, ValueError):
        return str(value)


def usd_value(value: Any) -> Any:
    if isinstance(value, dict):
        return value.get("USD")
    return value


def safe_text(value: Any) -> str:
    if value is None:
        return t(OUTPUT_LANG, "na")
    text = str(value).replace("\n", " ").strip()
    return re.sub(r"\s+", " ", text)


def normalize_url(value: Any) -> str | None:
    text = safe_text(value)
    if text == t(OUTPUT_LANG, "na"):
        return None
    if text.startswith(("http://", "https://")):
        return text
    if text.startswith("/"):
        return f"https://cryptorank.io{text}"
    return f"https://{text}"


def build_price_url(key: Any) -> str | None:
    text = safe_text(key)
    if text == t(OUTPUT_LANG, "na"):
        return None
    return f"https://cryptorank.io/price/{text}"


def build_funding_url(key: Any) -> str | None:
    text = safe_text(key)
    if text == t(OUTPUT_LANG, "na"):
        return None
    return f"https://cryptorank.io/ico/{text}"


def build_links(*pairs: tuple[str, Any]) -> list[dict[str, str]]:
    links: list[dict[str, str]] = []
    for label, raw in pairs:
        url = normalize_url(raw)
        if url:
            links.append({"label": label, "url": url})
    return links


def links_text(links: list[dict[str, str]], width: int = 28) -> str:
    if not links:
        return t(OUTPUT_LANG, "na")
    return trim(" | ".join(link["url"] for link in links), width)


def support_footer(lang: str) -> str:
    return "\n".join(
        [
            "",
            t(lang, "support_title"),
            f"- {t(lang, 'support_community')}: {SUPPORT_LINKS['community']}",
            f"- {t(lang, 'support_bot')}: {SUPPORT_LINKS['bot']}",
            f"- {t(lang, 'support_tutorial')}: {SUPPORT_LINKS['tutorial']}",
        ]
    )


def parse_date(value: Any) -> datetime | None:
    if not value:
        return None
    text = re.sub(r"\s+\([^)]*\)$", "", str(value).strip())
    for fmt in (
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ",
        "%a %b %d %Y %H:%M:%S GMT%z",
        "%Y-%m-%d",
    ):
        try:
            dt = datetime.strptime(text, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)
        except ValueError:
            continue
    return None


def relative_date(value: Any, lang: str) -> str:
    dt = parse_date(value)
    if not dt:
        return safe_text(value)
    delta = dt - now_utc()
    days = math.ceil(delta.total_seconds() / 86400) if delta.total_seconds() > 0 else math.floor(delta.total_seconds() / 86400)
    if abs(days) <= 1:
        if days == 0:
            return t(lang, "today")
        if days == 1:
            return t(lang, "in_1d")
        return t(lang, "days_ago", days=1)
    if days > 0:
        return t(lang, "in_days", days=days)
    return t(lang, "days_ago", days=abs(days))


def join_names(items: list[dict[str, Any]] | None, field: str = "name", limit: int = 3, lang: str = "zh") -> str:
    if not items:
        return t(lang, "na")
    names = []
    for item in items:
        if isinstance(item, dict):
            raw = item.get(field)
        else:
            raw = item
        if raw:
            names.append(translate_value(raw, lang))
    if not names:
        return t(lang, "na")
    head = names[:limit]
    extra = len(names) - len(head)
    if extra > 0:
        return ", ".join(head) + f" +{extra}"
    return ", ".join(head)


def trim(text: Any, width: int) -> str:
    value = safe_text(text)
    if len(value) <= width:
        return value
    if width <= 3:
        return value[:width]
    return value[: width - 3] + "..."


def render_table(title: str, columns: list[tuple[str, int]], rows: list[list[Any]]) -> str:
    header = " | ".join(trim(name, width).ljust(width) for name, width in columns)
    divider = "-+-".join("-" * width for _, width in columns)
    lines = [title, header, divider]
    for row in rows:
        lines.append(
            " | ".join(trim(cell, width).ljust(width) for cell, (_, width) in zip(row, columns))
        )
    return "\n".join(lines)


def fetch_text(url: str, headers: dict[str, str] | None = None) -> str:
    request = urllib.request.Request(url, headers=headers or SITE_HEADERS)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as exc:
        raise FetchError(f"HTTP {exc.code} while requesting {url}") from exc
    except urllib.error.URLError as exc:
        raise FetchError(f"Network error while requesting {url}: {exc}") from exc


def fetch_json(url: str, headers: dict[str, str] | None = None) -> Any:
    body = fetch_text(url, headers=headers or JSON_HEADERS)
    try:
        return json.loads(body)
    except json.JSONDecodeError as exc:
        raise FetchError(f"Invalid JSON returned by {url}") from exc


def extract_next_data(url: str) -> dict[str, Any]:
    html = fetch_text(url, headers=SITE_HEADERS)
    match = re.search(
        r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
        html,
        re.DOTALL,
    )
    if not match:
        raise FetchError(f"Could not locate __NEXT_DATA__ on {url}")
    try:
        payload = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        raise FetchError(f"Could not parse __NEXT_DATA__ from {url}") from exc
    page_props = payload.get("props", {}).get("pageProps")
    if not isinstance(page_props, dict):
        raise FetchError(f"Unexpected pageProps shape on {url}")
    return page_props


@dataclass
class CryptoRankClient:
    """Thin data access layer for the demo."""

    lang: str = "zh"

    def homepage(self) -> dict[str, Any]:
        return extract_next_data("https://cryptorank.io/")

    def funding_page(self) -> dict[str, Any]:
        return extract_next_data("https://cryptorank.io/funding-rounds")

    def upcoming_page(self) -> dict[str, Any]:
        return extract_next_data("https://cryptorank.io/upcoming-ico")

    def airdrops(self, limit: int) -> dict[str, Any]:
        params = urllib.parse.urlencode(
            {
                "limit": limit,
                "offset": 0,
                "orderBy": "STATUS_UPDATE",
                "orderDirection": "DESC",
                "locale": "zh" if self.lang == "zh" else "en",
            }
        )
        return fetch_json(
            f"https://api.cryptorank.io/v0/drop-hunting/activities/table/public?{params}",
            headers=AIRDROP_HEADERS,
        )


def homepage_radar(client: CryptoRankClient, limit: int) -> str:
    lang = client.lang
    data = client.homepage()
    global_data = data["initData"]["globalData"]
    top = data["fallbackCoins"][:limit]
    gainers = data["gainersCoins"][:limit]
    losers = data["losersCoins"][:limit]
    upcoming = data["upcomingIco"][:limit]
    funding = data["fallbackRecentFundingRounds"][:limit]

    blocks = []
    blocks.append("CRYPTO RANK 中文雷达" if lang == "zh" else "CRYPTO RANK RADAR")
    blocks.append("=" * 72)
    blocks.append(
        f"{t(lang, 'market')}: "
        f"{t(lang, 'btc_dominance')} {global_data.get('btcDominance', 'N/A'):.2f}% "
        f"({pct(global_data.get('btcDominanceChangePercent'))}) | "
        f"{t(lang, 'eth_dominance')} {global_data.get('ethDominance', 'N/A'):.2f}% "
        f"({pct(global_data.get('ethDominanceChangePercent'))}) | "
        f"{t(lang, 'market_cap')} {money(global_data.get('totalMarketCap'))} "
        f"({pct(global_data.get('totalMarketCapChangePercent'))}) | "
        f"{t(lang, 'volume_24h')} {money(global_data.get('totalVolume24h'))} "
        f"({pct(global_data.get('totalVolume24hChangePercent'))})"
    )
    blocks.append("")
    blocks.append(
        render_table(
            t(lang, "top_coins"),
            [(t(lang, "coin"), 24), (t(lang, "price"), 12), (t(lang, "mcap"), 12), ("24h", 8), ("URL", 28)],
            [
                [
                    f"{coin.get('name')} ({coin.get('symbol')})",
                    money(usd_value(coin.get("price"))),
                    money(usd_value(coin.get("marketCap"))),
                    pct(coin.get("percentChange", {}).get("24h")),
                    links_text(build_links(("CryptoRank", build_price_url(coin.get("key"))))),
                ]
                for coin in top
            ],
        )
    )
    blocks.append("")
    blocks.append(
        render_table(
            t(lang, "top_gainers"),
            [(t(lang, "coin"), 24), (t(lang, "category"), 14), ("24h", 8), ("7d", 8), ("URL", 28)],
            [
                [
                    f"{coin.get('name')} ({coin.get('symbol')})",
                    translate_value(coin.get("category"), lang),
                    pct(coin.get("historyPrice", {}).get("24H")),
                    pct(coin.get("historyPrice", {}).get("7D")),
                    links_text(build_links(("CryptoRank", build_price_url(coin.get("key"))))),
                ]
                for coin in gainers
            ],
        )
    )
    blocks.append("")
    blocks.append(
        render_table(
            t(lang, "top_losers"),
            [(t(lang, "coin"), 24), (t(lang, "category"), 14), ("24h", 8), ("7d", 8), ("URL", 28)],
            [
                [
                    f"{coin.get('name')} ({coin.get('symbol')})",
                    translate_value(coin.get("category"), lang),
                    pct(coin.get("historyPrice", {}).get("24H")),
                    pct(coin.get("historyPrice", {}).get("7D")),
                    links_text(build_links(("CryptoRank", build_price_url(coin.get("key"))))),
                ]
                for coin in losers
            ],
        )
    )
    blocks.append("")
    blocks.append(
        render_table(
            t(lang, "upcoming_sales"),
            [(t(lang, "project"), 22), (t(lang, "launchpad"), 14), (t(lang, "when"), 10), (t(lang, "raise"), 10), ("URL", 28)],
            [
                [
                    f"{item.get('coin', {}).get('name')} ({item.get('coin', {}).get('symbol')})",
                    safe_text((item.get("platform") or {}).get("name")),
                    relative_date(item.get("date"), lang),
                    money(item.get("raise")),
                    links_text(
                        build_links(
                            ("CryptoRank", build_price_url(item.get("coin", {}).get("key"))),
                            ("Sale", build_funding_url(item.get("coin", {}).get("key"))),
                        )
                    ),
                ]
                for item in upcoming
            ],
        )
    )
    blocks.append("")
    blocks.append(
        render_table(
            t(lang, "recent_funding"),
            [(t(lang, "project"), 20), (t(lang, "stage"), 12), (t(lang, "raise"), 10), (t(lang, "funds"), 18), ("URL", 28)],
            [
                [
                    (item.get("coin") or {}).get("name")
                    or (item.get("fund") or {}).get("name")
                    or "Unknown",
                    translate_value(item.get("type"), lang),
                    money(item.get("raise")),
                    join_names(item.get("funds"), lang=lang),
                    links_text(
                        build_links(
                            ("CryptoRank", build_price_url((item.get("coin") or {}).get("key"))),
                            ("Funding", build_funding_url((item.get("coin") or {}).get("key"))),
                        )
                    ),
                ]
                for item in funding
            ],
        )
    )
    return "\n".join(blocks)


def funding_radar(client: CryptoRankClient, limit: int) -> str:
    lang = client.lang
    home = client.homepage()
    page = client.funding_page()
    rounds = home["fallbackRecentFundingRounds"][:limit]
    overview = page.get("initData", {}).get("globalData", {})

    blocks = []
    blocks.append("CryptoRank 融资雷达" if lang == "zh" else "CRYPTO RANK FUNDING RADAR")
    blocks.append("=" * 72)
    if overview:
        blocks.append(
            f"{t(lang, 'overview')}: "
            f"{t(lang, 'btc_dominance')} {overview.get('btcDominance', 0):.2f}% | "
            f"{t(lang, 'market_cap')} {money(overview.get('totalMarketCap'))} | "
            f"{t(lang, 'volume_24h')} {money(overview.get('totalVolume24h'))}"
        )
        blocks.append("")

    rows = []
    for item in rounds:
        project = item.get("coin", {}).get("name") or item.get("fund", {}).get("name") or "Unknown"
        conviction = []
        if item.get("raise"):
            conviction.append(f"{t(lang, 'raise')} {money(item.get('raise'))}")
        if item.get("valuation"):
            conviction.append(f"{t(lang, 'valuation')} {money(item.get('valuation'))}")
        tiers = [fund.get("tier") for fund in item.get("funds", []) if fund.get("tier") is not None]
        if tiers:
            conviction.append(t(lang, "best_tier", tier=min(tiers)))
        rows.append(
            [
                project,
                translate_value(item.get("type"), lang),
                money(item.get("raise")),
                join_names(item.get("funds"), lang=lang),
                relative_date(item.get("date"), lang),
                " | ".join(conviction) or t(lang, "track"),
            ]
        )

    blocks.append(
        render_table(
            t(lang, "recent_rounds"),
            [
                (t(lang, "project"), 16),
                (t(lang, "stage"), 12),
                (t(lang, "raise"), 10),
                (t(lang, "funds"), 16),
                (t(lang, "date"), 8),
                (t(lang, "signal"), 18),
                ("URL", 28),
            ],
            [
                row
                + [
                    links_text(
                        build_links(
                            ("CryptoRank", build_price_url(item.get("coin", {}).get("key"))),
                            ("Funding", build_funding_url(item.get("coin", {}).get("key"))),
                        )
                    )
                ]
                for row, item in zip(rows, rounds)
            ],
        )
    )
    return "\n".join(blocks)


def upcoming_radar(client: CryptoRankClient, limit: int) -> str:
    lang = client.lang
    page = client.upcoming_page()
    items = page["fallbackRounds"]["data"][:limit]
    rows = []
    for item in items:
        project = f"{item.get('name')} ({item.get('symbol') or '?'})"
        rows.append(
            [
                project,
                ", ".join(translate_value(v, lang) for v in item.get("type", [])) or t(lang, "na"),
                join_names(item.get("launchpads"), limit=2, lang=lang),
                relative_date(item.get("when"), lang),
                money(item.get("raise")),
                compact_number(item.get("moniScore")),
            ]
        )
    return "\n".join(
        [
            "CryptoRank 即将开售雷达" if lang == "zh" else "CRYPTO RANK UPCOMING SALES",
            "=" * 72,
            render_table(
                t(lang, "upcoming_sales"),
                [
                    (t(lang, "project"), 22),
                    (t(lang, "type"), 12),
                    (t(lang, "launchpad"), 14),
                    (t(lang, "when"), 10),
                    (t(lang, "raise"), 10),
                    (t(lang, "moni"), 8),
                    ("URL", 28),
                ],
                [
                    row
                    + [
                        links_text(
                            build_links(
                                ("CryptoRank", build_price_url(item.get("key"))),
                                ("Sale", build_funding_url(item.get("key"))),
                                ("Launchpad", build_price_url((item.get("launchpads") or [{}])[0].get("key") if item.get("launchpads") else None)),
                            )
                        )
                    ]
                    for row, item in zip(rows, items)
                ],
            ),
        ]
    )


def airdrop_radar(client: CryptoRankClient, limit: int) -> str:
    lang = client.lang
    payload = client.airdrops(limit)
    items = payload.get("data", [])[:limit]
    rows = []
    for item in items:
        coin = item.get("coin", {})
        rows.append(
            [
                f"{coin.get('name')} ({coin.get('symbol')})",
                compact_number(item.get("rating")),
                join_names(item.get("activityTypes"), field="name", limit=2, lang=lang),
                translate_value(item.get("status"), lang),
                relative_date(item.get("statusUpdatedAt"), lang),
                join_names(coin.get("funds"), limit=2, lang=lang),
            ]
        )
    return "\n".join(
        [
            "CryptoRank 空投雷达" if lang == "zh" else "CRYPTO RANK AIRDROP RADAR",
            "=" * 72,
            render_table(
                t(lang, "airdrop_activities"),
                [
                    (t(lang, "project"), 20),
                    (t(lang, "rate"), 6),
                    (t(lang, "type"), 16),
                    (t(lang, "status"), 14),
                    (t(lang, "updated"), 10),
                    (t(lang, "funds"), 16),
                    ("URL", 28),
                ],
                [
                    row
                    + [
                        links_text(
                            build_links(
                                ("CryptoRank", build_price_url((item.get("coin") or {}).get("key"))),
                                ("Task", item.get("checkLink")),
                                ("Claim", item.get("linkToClaim")),
                            )
                        )
                    ]
                    for row, item in zip(rows, items)
                ],
            ),
        ]
    )


def daily_brief(client: CryptoRankClient, limit: int) -> str:
    lang = client.lang
    home = client.homepage()
    airdrops = client.airdrops(limit).get("data", [])[:limit]
    global_data = home["initData"]["globalData"]
    funding = home["fallbackRecentFundingRounds"][:limit]
    upcoming = home["upcomingIco"][:limit]
    gainers = home["gainersCoins"][:limit]

    lines = [
        t(lang, "daily_brief"),
        "=" * 72,
        f"{t(lang, 'timestamp')}: {now_utc().strftime('%Y-%m-%d %H:%M:%S UTC')}",
        "",
        t(lang, "market_snapshot"),
        (
            f"- {t(lang, 'btc_dominance')}: {global_data.get('btcDominance', 0):.2f}% "
            f"({pct(global_data.get('btcDominanceChangePercent'))})"
        ),
        (
            f"- {t(lang, 'eth_dominance')}: {global_data.get('ethDominance', 0):.2f}% "
            f"({pct(global_data.get('ethDominanceChangePercent'))})"
        ),
        (
            f"- {t(lang, 'market_cap')}: {money(global_data.get('totalMarketCap'))} "
            f"({pct(global_data.get('totalMarketCapChangePercent'))})"
        ),
        (
            f"- {t(lang, 'volume_24h')}: {money(global_data.get('totalVolume24h'))} "
            f"({pct(global_data.get('totalVolume24hChangePercent'))})"
        ),
        "",
        t(lang, "watch_today"),
    ]

    for item in funding[:3]:
        links = build_links(
            ("CryptoRank", build_price_url(item.get('coin', {}).get('key'))),
            ("Funding", build_funding_url(item.get('coin', {}).get('key'))),
        )
        lines.append(
            f"- {t(lang, 'funding_prefix')}: "
            f"{item.get('coin', {}).get('name')} {translate_value(item.get('type'), lang)} "
            f"{money(item.get('raise'))} | {t(lang, 'funds')}: {join_names(item.get('funds'), lang=lang)}"
            f" | URL: {', '.join(link['url'] for link in links) if links else t(lang, 'na')}"
        )
    for item in upcoming[:3]:
        links = build_links(
            ("CryptoRank", build_price_url(item.get('coin', {}).get('key'))),
            ("Sale", build_funding_url(item.get('coin', {}).get('key'))),
        )
        lines.append(
            f"- {t(lang, 'upcoming_prefix')}: "
            f"{item.get('coin', {}).get('name')} {t(lang, 'on')} {safe_text((item.get('platform') or {}).get('name'))} "
            f"{relative_date(item.get('date'), lang)}"
            f" | URL: {', '.join(link['url'] for link in links) if links else t(lang, 'na')}"
        )
    for item in airdrops[:3]:
        links = build_links(
            ("CryptoRank", build_price_url(item.get('coin', {}).get('key'))),
            ("Task", item.get('checkLink')),
            ("Claim", item.get('linkToClaim')),
        )
        lines.append(
            f"- {t(lang, 'airdrop_prefix')}: "
            f"{item.get('coin', {}).get('name')} {t(lang, 'rating_word')} {compact_number(item.get('rating'))} "
            f"| {translate_value(item.get('status'), lang)}"
            f" | URL: {', '.join(link['url'] for link in links) if links else t(lang, 'na')}"
        )
    lines.append("")
    lines.append(t(lang, "momentum_leaders"))
    for item in gainers[:5]:
        lines.append(
            "- "
            f"{item.get('name')} ({item.get('symbol')}): "
            f"24h {pct(item.get('historyPrice', {}).get('24H'))}, "
            f"7d {pct(item.get('historyPrice', {}).get('7D'))}"
        )
    return "\n".join(lines)


def json_dump(client: CryptoRankClient, mode: str, limit: int) -> str:
    if mode == "home":
        return json.dumps(client.homepage(), indent=2, ensure_ascii=False)
    if mode == "funding":
        return json.dumps(client.funding_page(), indent=2, ensure_ascii=False)
    if mode == "upcoming":
        return json.dumps(client.upcoming_page(), indent=2, ensure_ascii=False)
    if mode == "airdrops":
        return json.dumps(client.airdrops(limit), indent=2, ensure_ascii=False)
    raise FetchError(f"Unsupported raw mode: {mode}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CryptoRank 免费层 CLI 演示工具，支持融资、Upcoming、空投和每日简报。"
    )
    parser.add_argument(
        "mode",
        choices=["radar", "funding", "upcoming", "airdrops", "brief", "raw"],
        help="要输出的视图模式。",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="每个模块展示多少条，默认 5。",
    )
    parser.add_argument(
        "--raw-mode",
        choices=["home", "funding", "upcoming", "airdrops"],
        default="home",
        help="仅在 mode=raw 时使用。",
    )
    parser.add_argument(
        "--lang",
        choices=["zh", "en"],
        default="zh",
        help="输出语言，默认 zh。",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    global OUTPUT_LANG
    OUTPUT_LANG = args.lang
    client = CryptoRankClient(lang=args.lang)

    try:
        if args.mode == "radar":
            output = homepage_radar(client, args.limit)
        elif args.mode == "funding":
            output = funding_radar(client, args.limit)
        elif args.mode == "upcoming":
            output = upcoming_radar(client, args.limit)
        elif args.mode == "airdrops":
            output = airdrop_radar(client, args.limit)
        elif args.mode == "brief":
            output = daily_brief(client, args.limit)
        else:
            output = json_dump(client, args.raw_mode, args.limit)
    except FetchError as exc:
        print(f"[CryptoRank Demo Error] {exc}", file=sys.stderr)
        print(support_footer(args.lang), file=sys.stderr)
        return 1

    if args.mode != "raw":
        output = f"{output}\n{support_footer(args.lang)}"

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
