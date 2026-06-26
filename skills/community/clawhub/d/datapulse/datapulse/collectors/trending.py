"""Trending topics collector via trends24.in (server-side rendered)."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from urllib.parse import quote, urlparse

import requests
from bs4 import BeautifulSoup

from datapulse.core.models import SourceType
from datapulse.core.retry import retry
from datapulse.core.utils import generate_excerpt

from .base import BaseCollector, ParseResult

logger = logging.getLogger("datapulse.collectors.trending")

# Location aliases: shortcut → trends24.in path slug
LOCATION_ALIASES: dict[str, str] = {
    "us": "united-states",
    "usa": "united-states",
    "uk": "united-kingdom",
    "gb": "united-kingdom",
    "jp": "japan",
    "in": "india",
    "de": "germany",
    "fr": "france",
    "br": "brazil",
    "ca": "canada",
    "au": "australia",
    "kr": "south-korea",
    "mx": "mexico",
    "es": "spain",
    "it": "italy",
    "tr": "turkey",
    "sa": "saudi-arabia",
    "ae": "united-arab-emirates",
    "id": "indonesia",
    "ng": "nigeria",
    "ph": "philippines",
    "th": "thailand",
    "eg": "egypt",
    "pk": "pakistan",
    "co": "colombia",
    "ar": "argentina",
    "my": "malaysia",
    "sg": "singapore",
    "za": "south-africa",
    "worldwide": "",
    "global": "",
}

_VOLUME_PATTERN = re.compile(r"([\d,.]+)\s*([KkMm])?")
_GENERIC_PLACEHOLDER_MARKERS = (
    "youtube trending videos",
    "explore more apps",
    "top charts",
    "popular apps",
)


@dataclass
class TrendItem:
    rank: int
    name: str
    url: str = ""
    volume: str = ""
    volume_raw: int = 0


@dataclass
class TrendSnapshot:
    timestamp: str = ""
    timestamp_utc: str = ""
    trends: list[TrendItem] = field(default_factory=list)


def parse_volume(text: str) -> tuple[str, int]:
    """Parse volume text like '125K', '1.2M', '45,200' → (display, raw int)."""
    if not text or not text.strip():
        return "", 0
    cleaned = text.strip()
    m = _VOLUME_PATTERN.search(cleaned)
    if not m:
        return cleaned, 0
    num_str = m.group(1).replace(",", "")
    suffix = (m.group(2) or "").upper()
    try:
        num = float(num_str)
    except ValueError:
        return cleaned, 0
    if suffix == "K":
        raw = int(num * 1_000)
    elif suffix == "M":
        raw = int(num * 1_000_000)
    else:
        raw = int(num)
    return cleaned, raw


def normalize_location(location: str) -> str:
    """Normalize location input to trends24.in URL slug."""
    if not location or not location.strip():
        return ""
    key = location.strip().lower()
    if key in LOCATION_ALIASES:
        return LOCATION_ALIASES[key]
    # Already a slug or custom location
    return key.replace(" ", "-")


def build_trending_url(location: str = "") -> str:
    """Build full trends24.in URL for a location."""
    slug = normalize_location(location)
    if not slug:
        return "https://trends24.in/"
    return f"https://trends24.in/{quote(slug, safe='-')}/"


class TrendingCollector(BaseCollector):
    name = "trending"
    source_type = SourceType.TRENDING
    reliability = 0.78
    tier = 1
    setup_hint = ""

    def check(self) -> dict[str, str | bool]:
        return {"status": "ok", "message": "bs4 available", "available": True}

    def can_handle(self, url: str) -> bool:
        parsed = urlparse(url)
        return (parsed.hostname or "").lower() in {"trends24.in", "www.trends24.in"}

    def parse(self, url: str) -> ParseResult:
        """Parse a trends24.in page and return the latest snapshot as content."""
        try:
            html = self._fetch_page(url)
        except requests.RequestException as exc:
            return ParseResult.failure(url, f"Trending fetch failed: {exc}")

        snapshots = self._parse_html(html, url)
        if not snapshots:
            return ParseResult.failure(url, "No trending data found on page")

        latest = snapshots[0]
        location_slug = self._extract_location(url)
        if self._is_low_signal_snapshot(latest) and location_slug not in {"", "worldwide", "global"}:
            return ParseResult.failure(url, "Trending data degraded: low-signal placeholder topics")
        location = location_slug
        location_display = location.replace("-", " ").title() if location else "Worldwide"

        # Build LLM-friendly content
        content = self._format_content(latest, location_display)

        # Build extra data for programmatic use
        trends_data = [
            {
                "rank": t.rank,
                "name": t.name,
                "volume": t.volume,
                "volume_raw": t.volume_raw,
                "twitter_search_url": f"https://x.com/search?q={quote(t.name)}",
            }
            for t in latest.trends
        ]

        flags: list[str] = ["trending_snapshot"]
        has_volumes = any(t.volume_raw > 0 for t in latest.trends)
        if has_volumes:
            flags.append("rich_data")

        return ParseResult(
            url=url,
            title=f"Trending Topics on X ({location_display})",
            content=content,
            author="trends24.in",
            excerpt=generate_excerpt(content),
            source_type=self.source_type,
            tags=["trending", "twitter", "x"],
            confidence_flags=flags,
            extra={
                "location": location or "worldwide",
                "location_display": location_display,
                "snapshot_time": latest.timestamp_utc or latest.timestamp,
                "trend_count": len(latest.trends),
                "trends": trends_data,
            },
        )

    def fetch_snapshots(
        self, location: str = "", top_n: int = 20
    ) -> list[TrendSnapshot]:
        """Public method for reader.trending() — returns all hourly snapshots."""
        url = build_trending_url(location)
        html = self._fetch_page(url)
        snapshots = self._parse_html(html, url)
        # Limit trends per snapshot
        if top_n > 0:
            for snap in snapshots:
                snap.trends = snap.trends[:top_n]
        location_slug = normalize_location(location)
        if (
            snapshots
            and self._is_low_signal_snapshot(snapshots[0])
            and location_slug not in {"", "worldwide", "global"}
        ):
            raise ValueError("Low-signal trending snapshot (placeholder topics)")
        return snapshots

    @staticmethod
    def _is_placeholder_topic(name: str) -> bool:
        lowered = (name or "").strip().lower()
        if not lowered:
            return True
        return any(marker in lowered for marker in _GENERIC_PLACEHOLDER_MARKERS)

    def _is_low_signal_snapshot(self, snapshot: TrendSnapshot) -> bool:
        trends = snapshot.trends or []
        if not trends:
            return True
        if len(trends) == 1:
            topic = trends[0]
            return self._is_placeholder_topic(topic.name) or topic.volume_raw <= 0
        if len(trends) <= 3:
            return all(self._is_placeholder_topic(t.name) for t in trends)
        return False

    @retry(max_attempts=2, retryable=(requests.RequestException,))
    def _fetch_page(self, url: str) -> str:
        resp = requests.get(
            url,
            timeout=20,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml",
                "Accept-Language": "en-US,en;q=0.9",
            },
        )
        resp.raise_for_status()
        return resp.text

    def _parse_html(self, html: str, url: str) -> list[TrendSnapshot]:
        """Parse trends24.in HTML into TrendSnapshot list."""
        soup = BeautifulSoup(html, "lxml")
        snapshots: list[TrendSnapshot] = []

        # Primary: look for .trend-card elements
        cards = soup.select(".trend-card")
        if cards:
            for card in cards:
                snap = self._parse_card(card)
                if snap and snap.trends:
                    snapshots.append(snap)
            return snapshots

        # Fallback: structural h3 + ol/ul pattern
        headers = soup.find_all("h3")
        for h3 in headers:
            timestamp = h3.get_text(strip=True)
            if not timestamp:
                continue
            trend_list = h3.find_next(["ol", "ul"])
            if not trend_list:
                continue
            items = self._parse_list(trend_list)
            if items:
                snapshots.append(
                    TrendSnapshot(timestamp=timestamp, trends=items)
                )

        return snapshots

    def _parse_card(self, card) -> TrendSnapshot | None:
        """Parse a single .trend-card element."""
        # Timestamp from h3 inside card
        h3 = card.find("h3")
        timestamp = h3.get_text(strip=True) if h3 else ""

        # Try to extract UTC time from time tag or data attribute
        time_tag = card.find("time")
        timestamp_utc = ""
        if time_tag:
            timestamp_utc = time_tag.get("datetime", "")

        # Trend list
        trend_list = card.select_one(".trend-card__list")
        if trend_list:
            items = self._parse_list(trend_list)
        else:
            # Fallback: any ol/ul inside card
            list_el = card.find(["ol", "ul"])
            items = self._parse_list(list_el) if list_el else []

        if not items:
            return None

        return TrendSnapshot(
            timestamp=timestamp,
            timestamp_utc=timestamp_utc,
            trends=items,
        )

    def _parse_list(self, list_el) -> list[TrendItem]:
        """Parse an ol/ul element into TrendItem list."""
        items: list[TrendItem] = []
        for idx, li in enumerate(list_el.find_all("li"), 1):
            link = li.find("a")
            name = link.get_text(strip=True) if link else li.get_text(strip=True)
            if not name:
                continue

            href = ""
            if link and link.get("href"):
                href = link["href"]

            # Volume: look for a span with tweet volume info
            vol_text = ""
            vol_span = li.find("span", class_=re.compile(r"trend-card__count|tweet-count|volume", re.I))
            if vol_span:
                vol_text = vol_span.get_text(strip=True)
            else:
                # Check for any small/span after the link
                for sibling in li.find_all(["span", "small"]):
                    text = sibling.get_text(strip=True)
                    if text and _VOLUME_PATTERN.search(text):
                        vol_text = text
                        break

            volume_display, volume_raw = parse_volume(vol_text)

            items.append(
                TrendItem(
                    rank=idx,
                    name=name,
                    url=href,
                    volume=volume_display,
                    volume_raw=volume_raw,
                )
            )
        return items

    def _extract_location(self, url: str) -> str:
        """Extract location slug from URL path."""
        parsed = urlparse(url)
        path = parsed.path.strip("/")
        if not path:
            return ""
        # First segment is location
        return path.split("/")[0]

    def _format_content(self, snapshot: TrendSnapshot, location: str) -> str:
        """Format snapshot as LLM-friendly markdown."""
        lines = [f"## Trending Topics on X ({location})"]
        ts = snapshot.timestamp_utc or snapshot.timestamp
        if ts:
            lines.append(f"**Snapshot time:** {ts}")
        lines.append("")

        for t in snapshot.trends:
            vol_part = f" ({t.volume})" if t.volume else ""
            lines.append(f"{t.rank}. {t.name}{vol_part}")

        lines.append(f"\nTotal trending topics: {len(snapshot.trends)}")
        return "\n".join(lines)
