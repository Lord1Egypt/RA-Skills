#!/usr/bin/env python3
"""
Extract publish date from HTML or plain text using multiple strategies.

When given HTML:
  1. JSON-LD structured data (most reliable)
  2. OpenGraph / meta tags
  3. <time> element with datetime attribute
  4. Date patterns in early text

When given plain text (markdown):
  5. Relative time expressions ("4h ago", "2 days ago", "3小时前")
  6. Absolute date patterns in first 3000 chars

Also extracts from URL path (/2026/04/08/).
"""
import re
from datetime import datetime, timezone, timedelta


def extract_publish_date(content: str, url: str = "") -> str | None:
    """Extract publish date from HTML, text, or URL.

    Works with both raw HTML and plain text (markdown).
    Returns ISO 8601 string or None.
    """
    if not content and not url:
        return None

    candidates = []

    # --- HTML-specific strategies (only when content looks like HTML) ---
    is_html = content and ("<meta" in content[:5000] or "<html" in content[:500] or "<!DOCTYPE" in content[:500].upper())

    if is_html:
        # Strategy 1: JSON-LD datePublished / dateCreated
        ld_dates = re.findall(
            r'"date(?:Published|Created|Issued)"\s*:\s*"([^"]+)"', content, re.IGNORECASE
        )
        for d in ld_dates:
            parsed = _try_parse(d)
            if parsed:
                candidates.append(("json-ld", parsed))

        # Strategy 2: <meta> tags
        meta_patterns = [
            r'<meta[^>]+property=["\']article:published_time["\'][^>]+content=["\']([^"\']+)',
            r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']article:published_time',
            r'<meta[^>]+name=["\'](?:publish[_-]?date|pubdate|date|DC\.date)["\'][^>]+content=["\']([^"\']+)',
            r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\'](?:publish[_-]?date|pubdate|date)',
            r'<meta[^>]+property=["\']og:updated_time["\'][^>]+content=["\']([^"\']+)',
            r'<meta[^>]+property=["\']article:modified_time["\'][^>]+content=["\']([^"\']+)',
        ]
        for pat in meta_patterns:
            for m in re.findall(pat, content, re.IGNORECASE):
                parsed = _try_parse(m)
                if parsed:
                    candidates.append(("meta", parsed))

        # Strategy 3: <time> elements
        for d in re.findall(r'<time[^>]+datetime=["\']([^"\']+)["\']', content, re.IGNORECASE):
            parsed = _try_parse(d)
            if parsed:
                candidates.append(("time-element", parsed))

    # --- URL path strategy (works for all content types) ---
    if url:
        url_match = re.search(r'/(20\d{2})[/-](0[1-9]|1[0-2])[/-](0[1-9]|[12]\d|3[01])', url)
        if url_match:
            try:
                dt = datetime(int(url_match.group(1)), int(url_match.group(2)),
                              int(url_match.group(3)), tzinfo=timezone.utc)
                if 2020 <= dt.year <= 2030:
                    candidates.append(("url-path", dt))
            except ValueError:
                pass

    # --- Text-based strategies (works for both HTML text and markdown) ---
    if content:
        head = content[:3000]

        # Strategy 5: Relative time expressions
        rel = _parse_relative_time(head)
        if rel:
            candidates.append(("relative-time", rel))

        # Strategy 6: Absolute date patterns
        abs_dates = _parse_absolute_dates(head)
        for dt in abs_dates:
            candidates.append(("text-pattern", dt))

    if not candidates:
        return None

    # Prefer by source reliability
    priority = {"json-ld": 0, "meta": 1, "time-element": 2, "url-path": 3,
                "relative-time": 4, "text-pattern": 5}
    candidates.sort(key=lambda x: priority.get(x[0], 99))

    best = candidates[0][1]

    # Sanity check: if the best (structured) date is much older than a text-pattern
    # date, prefer the newer one. This catches stale template dates in HTML.
    text_dates = [dt for src, dt in candidates if src == "text-pattern"]
    if text_dates and best < max(text_dates) - timedelta(days=90):
        best = max(text_dates)

    return best.isoformat()


# ─── Relative time parsing ────────────────────────────────────────────────────

_RELATIVE_PATTERNS = [
    # English: "4h", "4 hours ago", "2 days ago", "30 minutes ago"
    (r'(\d{1,3})\s*(?:h|hr|hrs|hour|hours)(?:\s+ago)?\b', 'hours'),
    (r'(\d{1,3})\s*(?:d|day|days)(?:\s+ago)?\b', 'days'),
    (r'(\d{1,3})\s*(?:min|mins|minute|minutes)(?:\s+ago)?\b', 'minutes'),
    # Chinese: "4小时前", "2天前", "30分钟前"
    (r'(\d{1,3})\s*小时前', 'hours'),
    (r'(\d{1,3})\s*天前', 'days'),
    (r'(\d{1,3})\s*分钟前', 'minutes'),
    # "yesterday" / "昨天"
    (r'\byesterday\b', 'yesterday'),
    (r'昨天', 'yesterday'),
]


def _parse_relative_time(text: str) -> datetime | None:
    """Extract publish date from relative time expressions."""
    now = datetime.now(timezone.utc)
    for pattern, unit in _RELATIVE_PATTERNS:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            if unit == 'yesterday':
                return (now - timedelta(days=1)).replace(hour=12, minute=0, second=0)
            val = int(m.group(1))
            if val <= 0 or val > 365:
                continue
            if unit == 'hours' and val <= 72:
                return now - timedelta(hours=val)
            elif unit == 'days' and val <= 30:
                return now - timedelta(days=val)
            elif unit == 'minutes' and val <= 1440:
                return now - timedelta(minutes=val)
    return None


# ─── Absolute date parsing ────────────────────────────────────────────────────

_MONTH_MAP = {
    'jan': 1, 'january': 1, 'feb': 2, 'february': 2, 'mar': 3, 'march': 3,
    'apr': 4, 'april': 4, 'may': 5, 'jun': 6, 'june': 6,
    'jul': 7, 'july': 7, 'aug': 8, 'august': 8, 'sep': 9, 'september': 9,
    'oct': 10, 'october': 10, 'nov': 11, 'november': 11, 'dec': 12, 'december': 12,
}


def _parse_absolute_dates(text: str) -> list[datetime]:
    """Extract absolute dates from text. Returns list of datetime objects."""
    results = []
    now = datetime.now(timezone.utc)

    # Pattern 1: ISO-like with time: 2026-04-08T10:00:00
    for m in re.finditer(r'(20\d{2})[-/](0[1-9]|1[0-2])[-/](0[1-9]|[12]\d|3[01])[T ]\d{1,2}:\d{2}', text):
        parsed = _try_parse(m.group(0))
        if parsed and 2020 <= parsed.year <= 2030:
            results.append(parsed)

    # Pattern 2: ISO-like date only: 2026-04-08, 2026/04/08
    for m in re.finditer(r'(20\d{2})[-/](0[1-9]|1[0-2])[-/](0[1-9]|[12]\d|3[01])', text):
        try:
            dt = datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), tzinfo=timezone.utc)
            if 2020 <= dt.year <= 2030:
                results.append(dt)
        except ValueError:
            pass

    # Pattern 3: "April 8, 2026" / "Apr 8, 2026"
    for m in re.finditer(r'(\w+)\s+(\d{1,2}),?\s+(20\d{2})', text):
        mon = _MONTH_MAP.get(m.group(1).lower())
        if mon:
            try:
                dt = datetime(int(m.group(3)), mon, int(m.group(2)), tzinfo=timezone.utc)
                results.append(dt)
            except ValueError:
                pass

    # Pattern 4: "8 April 2026"
    for m in re.finditer(r'(\d{1,2})\s+(\w+)\s+(20\d{2})', text):
        mon = _MONTH_MAP.get(m.group(2).lower())
        if mon:
            try:
                dt = datetime(int(m.group(3)), mon, int(m.group(1)), tzinfo=timezone.utc)
                results.append(dt)
            except ValueError:
                pass

    # Pattern 5: Chinese "2026年4月8日"
    for m in re.finditer(r'(20\d{2})年(\d{1,2})月(\d{1,2})日', text):
        try:
            dt = datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), tzinfo=timezone.utc)
            results.append(dt)
        except ValueError:
            pass

    # Pattern 6: Short date without year — "Apr 09", "April 4" (infer current year)
    for m in re.finditer(r'(\w{3,9})\s+(\d{1,2})(?:\s*,\s*(\d{1,2}:\d{2}))?(?:\s+(?:AM|PM))?\s+(?:[A-Z]{2,4})\b', text):
        mon = _MONTH_MAP.get(m.group(1).lower())
        if mon:
            day = int(m.group(2))
            if 1 <= day <= 31:
                try:
                    dt = datetime(now.year, mon, day, tzinfo=timezone.utc)
                    # If the date is in the future by more than 7 days, assume last year
                    if dt > now + timedelta(days=7):
                        dt = dt.replace(year=now.year - 1)
                    results.append(dt)
                except ValueError:
                    pass

    # Deduplicate and filter
    seen = set()
    unique = []
    for dt in results:
        key = dt.strftime("%Y-%m-%d")
        if key not in seen and 2020 <= dt.year <= 2030:
            seen.add(key)
            unique.append(dt)

    return unique


def _try_parse(raw: str) -> datetime | None:
    """Try to parse a date string into datetime."""
    if not raw or not isinstance(raw, str):
        return None
    raw = raw.strip()

    formats = [
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
        "%Y/%m/%d",
        "%B %d, %Y",
        "%B %d %Y",
        "%d %B %Y",
        "%b %d, %Y",
        "%b %d %Y",
        "%d %b %Y",
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(raw, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue

    return None
