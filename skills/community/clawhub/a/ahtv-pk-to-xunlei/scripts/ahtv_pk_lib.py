from __future__ import annotations

import argparse
import html
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import date, datetime, timedelta
from pathlib import PurePosixPath
from typing import Dict, List, Optional, Sequence, Set, Tuple
from urllib.parse import quote, urljoin, urlparse
from urllib.request import Request, urlopen


DEFAULT_YEAR = 2026
SEARCH_URL = "https://www.ahtv.cn/search"
COLUMN_URL = "https://www.ahtv.cn/pindao/ahzh/pk"
KEYWORD = "快乐无敌大PK"
TARGET_ROOT = "/快乐无敌大PK/2026"
ALLOWED_EPISODE_PREFIX = "https://www.ahtv.cn/pindao/ahzh/pk/split/"
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/135.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}
UNSUPPORTED_TERMS = ("起", "以来", "前后", "本周", "最近几天")

ISO_DATE_RE = re.compile(r"^(?P<year>\d{4})[-/](?P<month>\d{1,2})[-/](?P<day>\d{1,2})$")
CHINESE_DATE_RE = re.compile(
    r"^(?:(?P<year>\d{4})年)?(?P<month>\d{1,2})月(?P<day>\d{1,2})(?:日|号)?$"
)
DAY_ONLY_RE = re.compile(r"^(?P<day>\d{1,2})(?:日|号)?$")
TITLE_DATE_RE = re.compile(r"(?P<year>20\d{2})-(?P<month>\d{1,2})-(?P<day>\d{1,2})")
SEARCH_BLOCK_RE = re.compile(
    r'<ul[^>]+id="searchListData"[^>]*>(?P<body>.*?)</ul>', re.S | re.I
)
LIST_ITEM_RE = re.compile(r"<li\b[^>]*>(?P<body>.*?)</li>", re.S | re.I)
ANCHOR_RE = re.compile(
    r'<a\b[^>]*href="(?P<href>[^"]+)"[^>]*title="(?P<title>[^"]*)"[^>]*>(?P<text>.*?)</a>',
    re.S | re.I,
)
PUBLISH_TIME_RE = re.compile(
    r'<span\b[^>]*class="[^"]*publish-time[^"]*"[^>]*>(?P<value>.*?)</span>',
    re.S | re.I,
)
M3U8_INPUT_RE = re.compile(
    r'<input\b[^>]*id="m3u8"[^>]*value="(?P<value>[^"]+)"[^>]*>|'
    r'<input\b[^>]*value="(?P<value2>[^"]+)"[^>]*id="m3u8"[^>]*>',
    re.S | re.I,
)
MAX_PAGE_QUERY_RE = re.compile(r"[?&]page=(\d+)")
MAX_PAGE_COLUMN_RE = re.compile(r"index_(\d+)\.html", re.I)


class ParseError(ValueError):
    pass


def normalize_expression(expr: str) -> str:
    value = expr.strip()
    if not value:
        return value
    replacements = {
        "，": ",",
        "；": ";",
        "～": "~",
        "—": "-",
        "–": "-",
        "－": "-",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
    }
    for src, dest in replacements.items():
        value = value.replace(src, dest)
    return re.sub(r"\s+", "", value)


def strip_tags(text: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", text or "")).strip()


def safe_date(year: int, month: int, day: int) -> date:
    return date(year, month, day)


def parse_date_token(
    token: str,
    *,
    inherited_year: Optional[int] = None,
    inherited_month: Optional[int] = None,
) -> date:
    token = normalize_expression(token)
    if not token:
        raise ParseError("empty date token")

    iso_match = ISO_DATE_RE.fullmatch(token)
    if iso_match:
        return safe_date(
            int(iso_match.group("year")),
            int(iso_match.group("month")),
            int(iso_match.group("day")),
        )

    chinese_match = CHINESE_DATE_RE.fullmatch(token)
    if chinese_match:
        year = int(chinese_match.group("year") or inherited_year or DEFAULT_YEAR)
        return safe_date(
            year,
            int(chinese_match.group("month")),
            int(chinese_match.group("day")),
        )

    day_match = DAY_ONLY_RE.fullmatch(token)
    if day_match and inherited_month is not None:
        year = inherited_year or DEFAULT_YEAR
        return safe_date(year, inherited_month, int(day_match.group("day")))

    raise ParseError(f"unsupported date token: {token}")


def expand_range(start: date, end: date) -> List[date]:
    if end < start:
        raise ParseError(f"range end {end.isoformat()} is earlier than start {start.isoformat()}")
    values: List[date] = []
    current = start
    while current <= end:
        values.append(current)
        current += timedelta(days=1)
    return values


def parse_list_segment(segment: str) -> List[date]:
    parts = [part for part in segment.split("、") if part]
    if not parts:
        raise ParseError("empty list segment")

    values: List[date] = []
    current_year: Optional[int] = None
    current_month: Optional[int] = None
    for part in parts:
        parsed = parse_date_token(
            part,
            inherited_year=current_year,
            inherited_month=current_month,
        )
        current_year = parsed.year
        current_month = parsed.month
        values.append(parsed)
    return values


def split_range_segment(segment: str) -> Tuple[str, str]:
    if "至" in segment:
        return segment.split("至", 1)
    if "~" in segment:
        return segment.split("~", 1)
    if "-" in segment and "月" in segment:
        return segment.split("-", 1)
    raise ParseError(f"unsupported range segment: {segment}")


def parse_segment(segment: str, *, latest_date: Optional[date]) -> Tuple[List[date], str]:
    for term in UNSUPPORTED_TERMS:
        if term in segment:
            raise ParseError(f"unsupported expression: {segment}")

    if segment.endswith("之后") or segment.endswith("以后"):
        if latest_date is None:
            raise ParseError("latest date is required for open ranges")
        base = parse_date_token(segment[:-2])
        start = base + timedelta(days=1)
        if start > latest_date:
            return [], "open_range"
        return expand_range(start, latest_date), "open_range"

    is_range = (
        "至" in segment
        or "~" in segment
        or ("-" in segment and "月" in segment and not ISO_DATE_RE.fullmatch(segment))
    )
    if is_range:
        start_token, end_token = split_range_segment(segment)
        start = parse_date_token(start_token)
        end = parse_date_token(
            end_token,
            inherited_year=start.year,
            inherited_month=start.month,
        )
        return expand_range(start, end), "range"

    if "、" in segment:
        return parse_list_segment(segment), "list"

    return [parse_date_token(segment)], "single"


@dataclass
class DateParseResult:
    input_expr: str
    mode: str
    normalized_dates: List[str]
    errors: List[str]
    latest_available_date: Optional[str]


def parse_date_expression(expr: str, *, latest_date: Optional[date] = None) -> DateParseResult:
    normalized_expr = normalize_expression(expr)
    if not normalized_expr:
        return DateParseResult(
            input_expr=expr,
            mode="list",
            normalized_dates=[],
            errors=["date expression is empty"],
            latest_available_date=latest_date.isoformat() if latest_date else None,
        )

    segments = [segment for segment in re.split(r"[,;]+", normalized_expr) if segment]
    values: List[date] = []
    errors: List[str] = []
    modes: List[str] = []

    for segment in segments:
        try:
            segment_values, segment_mode = parse_segment(segment, latest_date=latest_date)
        except ParseError as exc:
            errors.append(str(exc))
            continue
        values.extend(segment_values)
        modes.append(segment_mode)

    unique_values = sorted(set(values))

    if not modes:
        mode = "list"
    elif len(modes) == 1 and len(segments) == 1:
        mode = modes[0]
    elif len(unique_values) <= 1 and all(item == "single" for item in modes):
        mode = "single"
    else:
        mode = "list"

    return DateParseResult(
        input_expr=expr,
        mode=mode,
        normalized_dates=[value.isoformat() for value in unique_values],
        errors=errors,
        latest_available_date=latest_date.isoformat() if latest_date else None,
    )


@dataclass
class EpisodeCandidate:
    url: str
    title: str
    publish_time: Optional[str]
    air_date: str
    is_full_episode: bool
    source: str


@dataclass
class EpisodeResolutionItem:
    date: str
    status: str
    title: Optional[str] = None
    episode_url: Optional[str] = None
    video_url: Optional[str] = None
    target_filename: Optional[str] = None
    xunlei_path: Optional[str] = None
    message: str = ""

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


def build_target_filename(air_date: str, *, extension: str = ".mp4") -> str:
    stamp = air_date[5:7] + air_date[8:10]
    ext = extension if extension.startswith(".") else f".{extension}"
    return f"快乐无敌大PK.2026.S02E{stamp}{ext}"


def infer_extension(video_url: str) -> str:
    path = PurePosixPath(urlparse(video_url).path)
    suffix = path.suffix.lower()
    if suffix in {".mp4", ".m3u8", ".flv", ".mov"}:
        return suffix
    return ".mp4"


def extract_title_air_date(title: str) -> Optional[str]:
    match = TITLE_DATE_RE.search(title)
    if not match:
        return None
    return safe_date(
        int(match.group("year")),
        int(match.group("month")),
        int(match.group("day")),
    ).isoformat()


def parse_search_results(html_text: str) -> Tuple[List[EpisodeCandidate], int]:
    match = SEARCH_BLOCK_RE.search(html_text)
    if not match:
        return [], 1

    candidates: List[EpisodeCandidate] = []
    for li_match in LIST_ITEM_RE.finditer(match.group("body")):
        body = li_match.group("body")
        anchor = ANCHOR_RE.search(body)
        if not anchor:
            continue

        href = urljoin(SEARCH_URL, anchor.group("href"))
        if not href.startswith(ALLOWED_EPISODE_PREFIX):
            continue

        title = strip_tags(anchor.group("title") or anchor.group("text"))
        air_date = extract_title_air_date(title)
        if not air_date:
            continue

        publish_match = PUBLISH_TIME_RE.search(body)
        publish_time = strip_tags(publish_match.group("value")) if publish_match else None
        candidates.append(
            EpisodeCandidate(
                url=href,
                title=title,
                publish_time=publish_time,
                air_date=air_date,
                is_full_episode="整期" in title,
                source="search",
            )
        )

    pages = [int(value) for value in MAX_PAGE_QUERY_RE.findall(html_text)] or [1]
    return candidates, max(pages)


def parse_column_page(html_text: str) -> Tuple[List[EpisodeCandidate], int]:
    candidates: List[EpisodeCandidate] = []
    for anchor in ANCHOR_RE.finditer(html_text):
        href = urljoin(COLUMN_URL, anchor.group("href"))
        if not href.startswith(ALLOWED_EPISODE_PREFIX):
            continue

        title = strip_tags(anchor.group("title") or anchor.group("text"))
        air_date = extract_title_air_date(title)
        if not air_date:
            continue

        candidates.append(
            EpisodeCandidate(
                url=href,
                title=title,
                publish_time=None,
                air_date=air_date,
                is_full_episode="整期" in title,
                source="column",
            )
        )

    pages = [int(value) for value in MAX_PAGE_COLUMN_RE.findall(html_text)] or [1]
    return candidates, max(pages)


def extract_video_url(html_text: str) -> Optional[str]:
    match = M3U8_INPUT_RE.search(html_text)
    if not match:
        return None
    return html.unescape(match.group("value") or match.group("value2"))


class AhtvClient:
    def __init__(self, timeout: int = 30) -> None:
        self.timeout = timeout
        self._search_cache: Dict[int, Tuple[List[EpisodeCandidate], int]] = {}
        self._column_cache: Dict[int, Tuple[List[EpisodeCandidate], int]] = {}
        self._episode_cache: Dict[str, str] = {}
        self._column_date_index: Dict[str, Set[str]] = {}

    def _fetch_text(self, url: str, *, method: str = "GET", data: Optional[Dict[str, str]] = None) -> str:
        encoded = None
        if data is not None:
            encoded = "&".join(f"{quote(str(key))}={quote(str(value))}" for key, value in data.items()).encode(
                "utf-8"
            )
        request = Request(url, data=encoded, method=method, headers=DEFAULT_HEADERS)
        with urlopen(request, timeout=self.timeout) as response:
            raw = response.read()
            content_type = response.headers.get_content_charset()
            for charset in [content_type, "utf-8", "gb18030", "gbk"]:
                if not charset:
                    continue
                try:
                    return raw.decode(charset)
                except UnicodeDecodeError:
                    continue
        return raw.decode("utf-8", errors="replace")

    def fetch_search_page(self, page: int) -> Tuple[List[EpisodeCandidate], int]:
        if page in self._search_cache:
            return self._search_cache[page]
        if page == 1:
            html_text = self._fetch_text(SEARCH_URL, method="POST", data={"search_text": KEYWORD})
        else:
            html_text = self._fetch_text(
                f"{SEARCH_URL}/?search_text={quote(KEYWORD)}&column_sign=&page={page}"
            )
        result = parse_search_results(html_text)
        self._search_cache[page] = result
        return result

    def fetch_column_page(self, page: int) -> Tuple[List[EpisodeCandidate], int]:
        if page in self._column_cache:
            return self._column_cache[page]
        url = COLUMN_URL if page == 1 else f"{COLUMN_URL}/index_{page}.html"
        html_text = self._fetch_text(url)
        result = parse_column_page(html_text)
        self._column_cache[page] = result
        return result

    def fetch_episode_html(self, url: str) -> str:
        if url not in self._episode_cache:
            self._episode_cache[url] = self._fetch_text(url)
        return self._episode_cache[url]

    def discover_latest_episode_date(self) -> date:
        search_items, _ = self.fetch_search_page(1)
        column_items, _ = self.fetch_column_page(1)
        known_dates = [
            datetime.strptime(item.air_date, "%Y-%m-%d").date()
            for item in search_items + column_items
        ]
        if not known_dates:
            raise RuntimeError("unable to discover the latest 快乐无敌大PK episode date")
        return max(known_dates)

    def collect_search_candidates(self, target_dates: Sequence[str]) -> Dict[str, List[EpisodeCandidate]]:
        targets = set(target_dates)
        grouped: Dict[str, List[EpisodeCandidate]] = {target: [] for target in targets}
        page = 1
        last_page = 1
        while page <= last_page:
            items, last_page = self.fetch_search_page(page)
            for item in items:
                if item.air_date in grouped:
                    grouped[item.air_date].append(item)
            if all(grouped[target] for target in targets):
                break
            page += 1
        return grouped

    def find_column_urls_for_date(self, target_date: str) -> Set[str]:
        if target_date in self._column_date_index:
            return self._column_date_index[target_date]

        result: Set[str] = set()
        page = 1
        last_page = 1
        while page <= last_page:
            items, last_page = self.fetch_column_page(page)
            for item in items:
                if item.air_date == target_date:
                    result.add(item.url)
            if result:
                break
            page += 1

        self._column_date_index[target_date] = result
        return result

    def resolve_candidate(
        self, target_date: str, candidates: Sequence[EpisodeCandidate]
    ) -> Tuple[Optional[EpisodeCandidate], Optional[str]]:
        if not candidates:
            return None, "not-found"

        full_episodes = [candidate for candidate in candidates if candidate.is_full_episode]
        if len(full_episodes) == 1:
            return full_episodes[0], None
        if len(candidates) == 1:
            return candidates[0], None

        column_urls = self.find_column_urls_for_date(target_date)
        if column_urls:
            narrowed = [candidate for candidate in candidates if candidate.url in column_urls]
            narrowed_full = [candidate for candidate in narrowed if candidate.is_full_episode]
            if len(narrowed_full) == 1:
                return narrowed_full[0], None
            if len(narrowed) == 1:
                return narrowed[0], None

        return None, "ambiguous"


def resolve_dates(
    dates: Sequence[str],
    *,
    client: Optional[AhtvClient] = None,
) -> Dict[str, object]:
    search_client = client or AhtvClient()
    grouped = search_client.collect_search_candidates(dates)
    items: List[EpisodeResolutionItem] = []
    summary = {
        "total": len(dates),
        "ready": 0,
        "not_found": 0,
        "ambiguous": 0,
        "video_url_missing": 0,
        "error": 0,
    }

    for target_date in dates:
        try:
            candidate, failure = search_client.resolve_candidate(target_date, grouped.get(target_date, []))
            if failure == "not-found":
                summary["not_found"] += 1
                target_filename = build_target_filename(target_date)
                items.append(
                    EpisodeResolutionItem(
                        date=target_date,
                        status="not-found",
                        target_filename=target_filename,
                        xunlei_path=f"{TARGET_ROOT}/{target_filename}",
                        message="No 快乐无敌大PK episode candidate matched this date.",
                    )
                )
                continue
            if failure == "ambiguous":
                summary["ambiguous"] += 1
                target_filename = build_target_filename(target_date)
                items.append(
                    EpisodeResolutionItem(
                        date=target_date,
                        status="ambiguous",
                        target_filename=target_filename,
                        xunlei_path=f"{TARGET_ROOT}/{target_filename}",
                        message="Multiple candidate episode pages remain after the column-page cross-check.",
                    )
                )
                continue
            if candidate is None:
                summary["error"] += 1
                target_filename = build_target_filename(target_date)
                items.append(
                    EpisodeResolutionItem(
                        date=target_date,
                        status="error",
                        target_filename=target_filename,
                        xunlei_path=f"{TARGET_ROOT}/{target_filename}",
                        message="Unexpected empty candidate resolution.",
                    )
                )
                continue

            episode_html = search_client.fetch_episode_html(candidate.url)
            video_url = extract_video_url(episode_html)
            if not video_url:
                summary["video_url_missing"] += 1
                target_filename = build_target_filename(target_date)
                items.append(
                    EpisodeResolutionItem(
                        date=target_date,
                        status="video-url-missing",
                        title=candidate.title,
                        episode_url=candidate.url,
                        target_filename=target_filename,
                        xunlei_path=f"{TARGET_ROOT}/{target_filename}",
                        message="The episode page did not expose a hidden #m3u8 input.",
                    )
                )
                continue

            extension = infer_extension(video_url)
            target_filename = build_target_filename(target_date, extension=extension)
            summary["ready"] += 1
            items.append(
                EpisodeResolutionItem(
                    date=target_date,
                    status="ready",
                    title=candidate.title,
                    episode_url=candidate.url,
                    video_url=video_url,
                    target_filename=target_filename,
                    xunlei_path=f"{TARGET_ROOT}/{target_filename}",
                    message="Resolved a unique 快乐无敌大PK episode and extracted its real media URL.",
                )
            )
        except Exception as exc:  # pragma: no cover
            summary["error"] += 1
            target_filename = build_target_filename(target_date)
            items.append(
                EpisodeResolutionItem(
                    date=target_date,
                    status="error",
                    target_filename=target_filename,
                    xunlei_path=f"{TARGET_ROOT}/{target_filename}",
                    message=str(exc),
                )
            )

    return {
        "expanded_dates": list(dates),
        "summary": summary,
        "items": [item.to_dict() for item in items],
    }


def make_json_ready(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2)


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date-expr", required=True, help="User-provided 快乐无敌大PK date expression.")
    parser.add_argument(
        "--latest-date",
        help="Optional YYYY-MM-DD override for open ranges. Defaults to the latest discoverable AHTV episode date.",
    )
    return parser.parse_args(argv)


def resolve_latest_date(latest_date_value: Optional[str], client: Optional[AhtvClient] = None) -> date:
    if latest_date_value:
        return parse_date_token(latest_date_value)
    return (client or AhtvClient()).discover_latest_episode_date()


def cli_error(message: str) -> int:
    sys.stderr.write(f"{message}\n")
    return 1
