#!/usr/bin/env python3
"""Fast radar/index fetch for AI conference deadline lookup.

This helper is intentionally shallow: it fetches a few radar/index pages quickly
and returns snippets for a query. Decision-critical dates still require official
CFP/OpenReview/submission-page verification by the calling agent.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import email.utils
import gzip
import html
import json
import os
import re
import tempfile
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Optional


VERSION = "0.1.0"
REPORT_SCHEMA_VERSION = "1"
DEFAULT_CACHE_TTL_SECONDS = 900
FAILURE_CACHE_TTL_SECONDS = 60
DEFAULT_TIMEOUT_SECONDS = 3.0
DEFAULT_MIN_OK_SOURCES = 2
DEFAULT_MAX_WORKERS = 2
MAX_QUERY_TERMS = 16

VENUE_ALIASES = {
    "aaai": ("aaai",),
    "iclr": ("iclr", "international conference on learning representations"),
    "aistats": ("aistats", "artificial intelligence and statistics"),
    "clear": ("clear", "conference on causal learning and reasoning", "causal learning and reasoning"),
    "wsdm": ("wsdm", "web search and data mining"),
    "acl": ("acl", "annual meeting of the association for computational linguistics"),
    "arr": ("arr", "acl rolling review", "rolling review"),
    "eacl": ("eacl", "european chapter of the association for computational linguistics"),
    "emnlp": ("emnlp", "empirical methods in natural language processing"),
    "neurips": ("neurips", "nips", "neural information processing systems"),
    "icml": ("icml", "international conference on machine learning"),
    "cvpr": ("cvpr", "computer vision and pattern recognition"),
}

STAGE_ALIASES = {
    "abstract": ("abstract", "registration", "paper registration", "摘要", "摘要截稿", "注册", "报名"),
    "full": ("full", "full paper", "paper deadline", "submission deadline", "截稿", "截稿日期", "投稿截止", "全文"),
    "supplement": ("supplement", "supplementary", "supp", "code", "补充", "补充材料", "附录", "代码"),
    "rebuttal": ("rebuttal", "response", "author response", "回复", "反驳"),
    "notification": ("notification", "decision", "acceptance notification", "通知", "录用通知"),
    "camera_ready": ("camera-ready", "camera ready", "final version", "终稿"),
}

SOURCES = [
    {
        "name": "mlciv-ai-deadlines",
        "role": "primary_radar",
        "url": "https://mlciv.com/ai-deadlines/?sub=ML,CV,CG,NLP,RO,SP,DM,AP,KR,HCI,EDU",
        "format": "html",
    },
    {
        "name": "ccfddl-rss",
        "role": "structured_ccf_radar",
        "url": "https://ccfddl.com/conference/deadlines_zh.xml",
        "format": "ccfddl_rss",
        "accept_gzip": True,
        "max_bytes": 2_000_000,
    },
    {
        "name": "aideadlin-es",
        "role": "radar_alt",
        "url": "https://aideadlin.es/",
        "format": "html",
    },
    {
        "name": "aideadlines-org",
        "role": "radar",
        "url": "https://aideadlines.org/",
        "format": "html",
    },
]


FAST_SOURCE_ORDER = [
    "mlciv-ai-deadlines",
    "ccfddl-rss",
    "aideadlin-es",
    "aideadlines-org",
]


def default_cache_path() -> str:
    override = os.environ.get("AI_CONFERENCE_DEADLINE_RADAR_CACHE")
    if override:
        return override
    return os.path.join(tempfile.gettempdir(), "ai-conference-deadline-radar-cache.json")


def load_cache(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_cache(cache: dict, path: str) -> None:
    try:
        parent = os.path.dirname(path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(cache, fh, ensure_ascii=False)
        os.replace(tmp, path)
    except Exception:
        # Cache failure should never prevent the lookup result.
        return


def strip_html(text: str) -> str:
    text = re.sub(r"(?is)<script.*?</script>|<style.*?</style>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def normalized_match_blob(text: str) -> str:
    text = text.lower().replace("_", " ")
    text = re.sub(r"[^a-z0-9+\-\u4e00-\u9fff]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def alias_matches(blob: str, alias: str) -> bool:
    alias_blob = normalized_match_blob(alias)
    if not alias_blob:
        return False
    if re.search(r"[\u4e00-\u9fff]", alias_blob):
        return alias_blob in blob
    return f" {alias_blob} " in f" {blob} "


def query_venue_terms(query: str) -> list[str]:
    blob = normalized_match_blob(query)
    terms = []
    for canonical, aliases in VENUE_ALIASES.items():
        if any(alias_matches(blob, alias) for alias in aliases):
            terms.append(canonical)
    return terms


def query_stage_terms(query: str) -> list[str]:
    blob = normalized_match_blob(query)
    terms = []
    for canonical, aliases in STAGE_ALIASES.items():
        if any(alias_matches(blob, alias) for alias in aliases):
            terms.append(canonical)
    return terms


def append_unique(items: list[str], value: str) -> None:
    if value and value not in items:
        items.append(value)


def query_terms(query: str) -> list[str]:
    raw_terms = re.findall(r"[A-Za-z][A-Za-z0-9+-]{1,}|\b20\d{2}\b|[\u4e00-\u9fff]{2,}", query)
    terms = []
    for term in [*query_venue_terms(query), *query_stage_terms(query)]:
        append_unique(terms, term)
    for term in raw_terms:
        normalized = term.lower()
        append_unique(terms, normalized)
    return terms[:MAX_QUERY_TERMS]


def is_year_term(term: str) -> bool:
    return bool(re.fullmatch(r"20\d{2}", term))


def snippets(text: str, query: str, limit: Optional[int] = None) -> list[str]:
    plain = strip_html(text)
    lower = plain.lower()
    windows = []
    terms = query_terms(query)
    match_terms = [term for term in terms if not is_year_term(term)] or terms
    if limit is None:
        limit = min(max(3, len(match_terms)), 8)
    for term in match_terms:
        idx = lower.find(term)
        if idx >= 0:
            start = max(0, idx - 180)
            end = min(len(plain), idx + 420)
            windows.append(plain[start:end])
        if len(windows) >= limit:
            break
    if not windows:
        windows = [plain[:600]]
    return windows


def clean_label(text: str) -> str:
    return strip_html(text).strip()


def link_kind(url: str, label: str) -> str:
    blob = f"{url} {label}".lower()
    if "openreview.net" in blob:
        return "openreview_candidate"
    if any(hint in blob for hint in ["submission", "submit", "cmt3", "softconf"]):
        return "submission_candidate"
    if any(hint in blob for hint in ["cfp", "call-for-papers", "callforpapers", "call_for_papers", "call for papers", "important-dates", "dates"]):
        return "official_dates_candidate"
    return "radar_link"


def parse_pub_date(text: str) -> Optional[dt.datetime]:
    if not text:
        return None
    try:
        parsed = email.utils.parsedate_to_datetime(text)
    except Exception:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed


def parse_timezone_label(label: str) -> Optional[dt.tzinfo]:
    if not label:
        return None
    match = re.search(r"UTC\s*([+-])\s*(\d{1,2})(?::?(\d{2}))?", label, re.IGNORECASE)
    if not match:
        return None
    sign = -1 if match.group(1) == "-" else 1
    hours = int(match.group(2))
    minutes = int(match.group(3) or "0")
    return dt.timezone(sign * dt.timedelta(hours=hours, minutes=minutes))


def parse_deadline_datetime(deadline: str, timezone_label: str) -> Optional[dt.datetime]:
    match = re.search(r"(20\d{2}-\d{2}-\d{2})(?:[ T](\d{2}:\d{2}(?::\d{2})?))?", deadline)
    if not match:
        return None
    time_part = match.group(2) or "23:59:59"
    if len(time_part) == 5:
        time_part += ":00"
    try:
        parsed = dt.datetime.fromisoformat(f"{match.group(1)}T{time_part}")
    except ValueError:
        return None
    return parsed.replace(tzinfo=parse_timezone_label(timezone_label) or dt.timezone.utc)


def ccfddl_description_field(description: str, label: str) -> str:
    for line in description.splitlines():
        cleaned = line.strip()
        if cleaned.startswith(label) and ":" in cleaned:
            return cleaned.split(":", 1)[1].strip()
    return ""


def ccfddl_rank(description: str) -> str:
    for line in description.splitlines():
        cleaned = line.strip()
        if "CCF " in cleaned or cleaned.startswith("CCF"):
            return cleaned
    return ""


def ccfddl_deadline_parts(description: str) -> tuple[str, str]:
    for line in description.splitlines():
        cleaned = line.strip()
        if not cleaned.startswith("截止时间"):
            continue
        timezone_match = re.search(r"\(([^()]+)\)", cleaned)
        timezone_label = timezone_match.group(1).strip() if timezone_match else ""
        deadline = cleaned.split(":", 1)[1].strip() if ":" in cleaned else ""
        return deadline, timezone_label
    return "", ""


def ccfddl_stage(title: str, guid: str) -> str:
    return normalize_stage(f"{title} {guid}") or "full"


def normalize_stage(text: str) -> Optional[str]:
    blob = normalized_match_blob(text)
    # Keep narrower stages before full because titles often contain "deadline".
    for canonical in ["abstract", "supplement", "rebuttal", "notification", "camera_ready", "full"]:
        aliases = STAGE_ALIASES[canonical]
        if any(alias_matches(blob, alias) for alias in aliases):
            return canonical
    return None


def ccfddl_item_record(item: ET.Element) -> Optional[dict]:
    title = clean_label(item.findtext("title") or "")
    description = html.unescape(item.findtext("description") or "")
    link = clean_label(item.findtext("link") or "")
    guid = clean_label(item.findtext("guid") or "")
    category = clean_label(item.findtext("category") or "")
    pub_date = parse_pub_date(item.findtext("pubDate") or "")
    title_match = re.match(r"^\s*([A-Za-z0-9.+-]+)\s+(20\d{2})\s+(.+?)\s*$", title)
    if not title_match:
        return None
    deadline, timezone_label = ccfddl_deadline_parts(description)
    deadline_dt = parse_deadline_datetime(deadline, timezone_label) or pub_date
    if deadline_dt is None:
        return None
    full_name = clean_label(description.splitlines()[0] if description.splitlines() else "")
    website = ccfddl_description_field(description, "会议官网") or link
    record = {
        "venue": title_match.group(1),
        "year": title_match.group(2),
        "stage": ccfddl_stage(title, guid),
        "deadline": deadline,
        "deadline_iso": deadline_dt.isoformat(),
        "timezone": timezone_label,
        "conference_dates": ccfddl_description_field(description, "会议时间"),
        "location": ccfddl_description_field(description, "会议地点"),
        "category": category or ccfddl_description_field(description, "分类"),
        "rank": ccfddl_rank(description),
        "full_name": full_name,
        "source_url": website,
        "source_kind": "radar_hint",
    }
    return record


def ccfddl_record_matches(record: dict, query: str) -> list[str]:
    terms = query_terms(query)
    if not terms:
        return []
    venue_terms = query_venue_terms(query)
    stage_terms = query_stage_terms(query)
    blob = " ".join(
        str(record.get(key, ""))
        for key in [
            "venue",
            "year",
            "stage",
            "full_name",
            "conference_dates",
            "location",
            "category",
            "rank",
            "source_url",
        ]
    ).lower()
    matches = [term for term in terms if term in blob]
    if venue_terms and not any(term in matches for term in venue_terms):
        return []
    if stage_terms and not any(term in matches for term in stage_terms):
        return []
    return matches


def ccfddl_records(text: str, query: str, limit: int = 12) -> list[dict]:
    try:
        root = ET.fromstring(text.strip())
    except ET.ParseError:
        return []
    now = dt.datetime.now(dt.timezone.utc)
    scored: list[tuple[dt.datetime, int, dict]] = []
    for index, item in enumerate(root.findall(".//item")):
        record = ccfddl_item_record(item)
        if not record:
            continue
        deadline_dt = dt.datetime.fromisoformat(record["deadline_iso"])
        if deadline_dt.astimezone(dt.timezone.utc) < now:
            continue
        matches = ccfddl_record_matches(record, query)
        if query_terms(query) and not matches:
            continue
        record["matches"] = matches
        scored.append((deadline_dt.astimezone(dt.timezone.utc), index, record))
    scored.sort(key=lambda row: (row[0], row[1]))
    return [record for _deadline, _index, record in scored[:limit]]


def ccfddl_snippets(records: list[dict]) -> list[str]:
    snippets_out = []
    for record in records:
        snippets_out.append(
            " | ".join(
                part
                for part in [
                    f"{record['venue']} {record['year']} {record['stage']}",
                    f"deadline {record['deadline']} {record['timezone']}".strip(),
                    record.get("full_name", ""),
                    record.get("conference_dates", ""),
                    record.get("location", ""),
                    record.get("rank", ""),
                    f"source {record.get('source_url', '')}",
                ]
                if part
            )
        )
    return snippets_out


def ccfddl_candidate_links(records: list[dict], limit: int) -> list[dict]:
    links = []
    seen: set[str] = set()
    for record in records:
        url = str(record.get("source_url", "")).strip()
        if not url:
            continue
        key = url.lower()
        if key in seen:
            continue
        seen.add(key)
        label = f"{record.get('venue')} {record.get('year')} {record.get('stage')}"
        links.append(
            {
                "url": url,
                "label": label,
                "kind": link_kind(url, label),
                "matches": record.get("matches", [])[:4],
            }
        )
        if len(links) >= limit:
            break
    return links


def is_generic_link_label(label: str) -> bool:
    normalized = re.sub(r"[^a-z0-9]+", " ", label.lower()).strip()
    return normalized in {"here", "more info", "website", "link", "cfp", "call for papers", "dates"}


def candidate_links(text: str, base_url: str, query: str, limit: int = 8) -> list[dict]:
    terms = query_terms(query)
    venue_terms = query_venue_terms(query) or [term for term in terms if not is_year_term(term)]
    year_terms = [term for term in terms if is_year_term(term)]
    base_host = urllib.parse.urlparse(base_url).netloc
    seen: set[str] = set()
    scored = []
    pattern = re.compile(r"(?is)<a\b[^>]*?\bhref\s*=\s*(['\"])(.*?)\1[^>]*>(.*?)</a>")

    for index, match in enumerate(pattern.finditer(text)):
        href = html.unescape(match.group(2)).strip()
        if not href or href.startswith(("#", "javascript:", "mailto:", "tel:")):
            continue

        parsed = urllib.parse.urlparse(urllib.parse.urljoin(base_url, href))
        if parsed.scheme not in {"http", "https"}:
            continue
        url = parsed._replace(fragment="").geturl()
        key = url.lower()
        if key in seen:
            continue
        seen.add(key)

        label = clean_label(match.group(3))[:140] or url
        context_start = max(0, match.start() - 160)
        context_end = min(len(text), match.end() + 160)
        context = clean_label(text[context_start:context_end])
        direct_blob = f"{url} {label}".lower()
        context_blob = context.lower()
        matched_direct_venue_terms = [term for term in venue_terms if term in direct_blob]
        matched_context_venue_terms = (
            [term for term in venue_terms if term in context_blob]
            if is_generic_link_label(label)
            else []
        )
        matched_venue_terms = []
        for term in [*matched_direct_venue_terms, *matched_context_venue_terms]:
            if term not in matched_venue_terms:
                matched_venue_terms.append(term)
        link_blob = direct_blob if matched_direct_venue_terms else f"{direct_blob} {context_blob}"
        matched_year_terms = [term for term in year_terms if term in link_blob]
        matched_terms = [*matched_venue_terms, *matched_year_terms]
        if venue_terms and not matched_venue_terms:
            continue
        if terms and not matched_terms:
            continue
        score = 4 * len(matched_venue_terms) + 3 * len(matched_year_terms)
        if link_kind(url, label) != "radar_link":
            score += 5
        if parsed.netloc and parsed.netloc != base_host:
            score += 1

        scored.append(
            (
                -score,
                index,
                {
                    "url": url,
                    "label": label,
                    "kind": link_kind(url, label),
                    "matches": matched_terms[:4],
                },
            )
        )

    scored.sort(key=lambda item: (item[0], item[1]))
    if not terms:
        return [item for _score, _index, item in scored[:limit]]

    selected = []
    selected_urls: set[str] = set()
    per_term_count: dict[str, int] = {}
    per_term_limit = 2
    for _score, _index, item in scored:
        primary = next(
            (term for term in item["matches"] if not is_year_term(term)),
            item["matches"][0] if item["matches"] else "",
        )
        if per_term_count.get(primary, 0) >= per_term_limit:
            continue
        selected.append(item)
        selected_urls.add(item["url"])
        per_term_count[primary] = per_term_count.get(primary, 0) + 1
        if len(selected) >= limit:
            return selected

    for _score, _index, item in scored:
        if item["url"] in selected_urls:
            continue
        selected.append(item)
        if len(selected) >= limit:
            break
    return selected


def cached_entry_is_fresh(cached: dict, now: float, ttl: int) -> bool:
    fetched_at = cached.get("fetched_at", 0)
    if not isinstance(fetched_at, (int, float)):
        return False
    age = now - fetched_at
    if cached.get("ok"):
        return age < ttl
    return age < min(ttl, FAILURE_CACHE_TTL_SECONDS)


def fetch_source(source: dict, timeout: float, max_bytes: int, cache: dict, ttl: int) -> dict:
    url = source["url"]
    now = time.time()
    cached = cache.get(url)
    if isinstance(cached, dict) and cached_entry_is_fresh(cached, now, ttl):
        return {
            **source,
            "ok": cached.get("ok", False),
            "cached": True,
            "elapsed_ms": 0,
            "text": cached.get("text", ""),
            "error": cached.get("error"),
            "http_status": cached.get("http_status"),
            "bytes": len(cached.get("text", "").encode("utf-8", "ignore")),
        }

    started = time.time()
    try:
        headers = {
            "User-Agent": f"Mozilla/5.0 ai-conference-deadline-radar/{VERSION}",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        if source.get("accept_gzip"):
            headers["Accept-Encoding"] = "gzip"
        request = urllib.request.Request(
            url,
            headers=headers,
        )
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read(source.get("max_bytes", max_bytes))
            content_encoding = (response.headers.get("Content-Encoding") or "").lower()
        decoded = gzip.decompress(raw) if "gzip" in content_encoding else raw
        text = decoded.decode("utf-8", "replace")
        http_status = getattr(response, "status", None)
        result = {
            **source,
            "ok": True,
            "cached": False,
            "elapsed_ms": int((time.time() - started) * 1000),
            "text": text,
            "error": None,
            "http_status": http_status,
            "bytes": len(raw),
        }
    except Exception as exc:  # network variability should not abort all sources
        result = {
            **source,
            "ok": False,
            "cached": False,
            "elapsed_ms": int((time.time() - started) * 1000),
            "text": "",
            "error": f"{type(exc).__name__}: {exc}",
            "http_status": None,
            "bytes": 0,
        }

    cache[url] = {
        "fetched_at": time.time(),
        "ok": result["ok"],
        "text": result["text"],
        "error": result["error"],
        "http_status": result["http_status"],
    }
    return result


def source_order(wait_all: bool) -> list[dict]:
    by_name = {source["name"]: source for source in SOURCES}
    if wait_all:
        return SOURCES
    return [by_name[name] for name in FAST_SOURCE_ORDER if name in by_name]


def skipped_source(source: dict) -> dict:
    return {
        **source,
        "ok": None,
        "cached": False,
        "elapsed_ms": 0,
        "error": "skipped: enough faster radar sources succeeded",
        "http_status": None,
        "bytes": 0,
        "text": "",
    }


def shutdown_pool(pool: object) -> None:
    try:
        pool.shutdown(wait=False, cancel_futures=True)
    except TypeError:
        # Python 3.8 ThreadPoolExecutor has no cancel_futures keyword.
        pool.shutdown(wait=False)


def fetch_sources(args: argparse.Namespace, cache: dict) -> list[dict]:
    ordered = source_order(args.wait_all)
    fetched_by_name: dict[str, dict] = {}
    next_index = 0
    ok_count = 0
    max_workers = max(1, min(args.max_workers, len(ordered)))
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
    futures: dict[concurrent.futures.Future, str] = {}

    def submit_next() -> None:
        nonlocal next_index
        if next_index >= len(ordered):
            return
        source = ordered[next_index]
        next_index += 1
        future = pool.submit(fetch_source, source, args.timeout, args.max_bytes, cache, args.cache_ttl)
        futures[future] = source["name"]

    try:
        for _ in range(max_workers):
            submit_next()

        while futures:
            done, _pending = concurrent.futures.wait(
                futures,
                return_when=concurrent.futures.FIRST_COMPLETED,
            )
            for future in done:
                name = futures.pop(future)
                item = future.result()
                fetched_by_name[name] = item
                if item["ok"]:
                    ok_count += 1

            if not args.wait_all and ok_count >= args.min_ok_sources:
                break

            while (
                next_index < len(ordered)
                and len(futures) < max_workers
                and (args.wait_all or ok_count + len(futures) < args.min_ok_sources)
            ):
                submit_next()
    finally:
        for future in futures:
            future.cancel()
        shutdown_pool(pool)

    fetched = []
    for source in SOURCES:
        if source["name"] in fetched_by_name:
            fetched.append(fetched_by_name[source["name"]])
        elif args.wait_all:
            fetched.append(skipped_source(source))
        elif source["name"] in {item["name"] for item in ordered}:
            fetched.append(skipped_source(source))
    return fetched


def build_report(args: argparse.Namespace) -> dict:
    cache = {} if args.no_cache else load_cache(args.cache_path)
    fetched = fetch_sources(args, cache)
    if not args.no_cache:
        save_cache(cache, args.cache_path)

    sources = []
    for item in fetched:
        text = item.pop("text", "")
        structured_records = []
        if item["ok"] and item.get("format") == "ccfddl_rss":
            structured_records = ccfddl_records(text, args.query, args.record_limit)
        item["structured_records"] = structured_records
        if item["ok"] and structured_records:
            item["snippets"] = ccfddl_snippets(structured_records)
            item["candidate_links"] = ccfddl_candidate_links(structured_records, args.link_limit)
        else:
            item["snippets"] = snippets(text, args.query) if item["ok"] else []
            item["candidate_links"] = (
                candidate_links(text, item["url"], args.query, args.link_limit)
                if item["ok"]
                else []
            )
        sources.append(item)

    return {
        "helper_version": VERSION,
        "schema_version": REPORT_SCHEMA_VERSION,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "query": args.query,
        "sources": sources,
        "ok_sources": sum(1 for source in sources if source["ok"] is True),
        "mode": "wait-all" if args.wait_all else "fast",
        "decision_rule": "Use radar/index output for discovery only; verify official CFP/OpenReview/submission pages before acting.",
    }


def print_markdown(report: dict) -> None:
    print("# Deadline Radar Fast Fetch\n")
    print(f"Query: `{report['query']}`\n")
    print(f"Mode: `{report['mode']}`\n")
    print(f"Helper: `{report['helper_version']}`\n")
    print(f"Schema: `{report['schema_version']}`\n")
    for source in report["sources"]:
        if source["ok"] is True:
            status = "ok"
        elif source["ok"] is None:
            status = "skipped"
        else:
            status = "failed"
        cache = "cached" if source["cached"] else f"{source['elapsed_ms']}ms"
        print(f"## {source['name']} ({status}, {cache})")
        print(f"- Role: `{source['role']}`")
        print(f"- URL: {source['url']}")
        if source.get("http_status"):
            print(f"- HTTP: `{source['http_status']}`")
        if source.get("bytes"):
            print(f"- Bytes: `{source['bytes']}`")
        if source["error"]:
            print(f"- Error: `{source['error']}`")
        for link in source.get("candidate_links", []):
            print(f"- Candidate link ({link['kind']}): {link['label']} - {link['url']}")
        for record in source.get("structured_records", []):
            print(
                "- Structured record: "
                f"{record['venue']} {record['year']} {record['stage']} "
                f"{record['deadline']} {record['timezone']} "
                f"({record['source_kind']}) - {record['source_url']}"
            )
        for snippet in source["snippets"]:
            print(f"- Snippet: {snippet[:700]}")
        print()
    print(f"Decision rule: {report['decision_rule']}")


def run_self_test() -> None:
    filler = "filler " * 220
    sample = f"""
    <html><head><style>.x{{}}</style></head><body>
    <p>3DV 2027 should not match unless 3DV is requested.</p>
    <p>filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler filler</p>
    <h1>AAAI 2027</h1>
    <a href="/aaai/aaai-27/call-for-papers/">AAAI 2027 CFP</a>
    <a href="https://openreview.net/group?id=ICLR.cc/2027/Conference">ICLR OpenReview</a>
    <a href="https://cvpr.thecvf.com/Conferences/2027/CallForPapers">CVPR 2027 CFP</a>
    <a href="mailto:chairs@example.org">Mail chairs</a>
    <p>Note: Predicted ICLR deadline based on historical pattern.</p>
    <p>AISTATS, CLeaR, and WSDM planning entries appear in the same radar page.</p>
    <script>ignore()</script>
    </body></html>
    """
    ccfddl_sample = """
    <?xml version='1.0' encoding='utf-8'?>
    <rss version="2.0"><channel>
      <item>
        <title>AAAI 2099 摘要截稿</title>
        <link>https://aaai.org/conference/aaai/aaai-99/</link>
        <description>AAAI Conference on Artificial Intelligence
会议时间: February 16-23, 2099
会议地点: Montréal, Canada
截止时间 (UTC-12): 2098-07-24 23:59:59
分类: 人工智能 (AI)
CCF A, CORE A*, THCPL A
会议官网: https://aaai.org/conference/aaai/aaai-99/
DBLP索引: https://dblp.org/db/conf/aaai</description>
        <pubDate>Sat, 24 Jul 2098 23:59:59 -1200</pubDate>
        <guid isPermaLink="false">AAAI-2099-abstract-2098-07-24 23:59:59@ccfddl.com</guid>
        <category>AI</category>
      </item>
      <item>
        <title>WSDM 2099 截稿日期</title>
        <link>https://www.wsdm-conference.org/2099/</link>
        <description>ACM International Conference on Web Search and Data Mining
会议时间: March 10-14, 2099
会议地点: TBA
截止时间 (UTC-12): 2098-08-12 23:59:59
分类: 数据挖掘 (DM)
CCF B, CORE A*
会议官网: https://www.wsdm-conference.org/2099/</description>
        <pubDate>Mon, 12 Aug 2098 23:59:59 -1200</pubDate>
        <guid isPermaLink="false">WSDM-2099-deadline-2098-08-12 23:59:59@ccfddl.com</guid>
        <category>DM</category>
      </item>
      <item>
        <title>CVPR 2099 截稿日期</title>
        <link>https://cvpr.thecvf.com/Conferences/2099</link>
        <description>Computer Vision and Pattern Recognition
截止时间 (UTC-12): 2098-11-12 23:59:59
会议官网: https://cvpr.thecvf.com/Conferences/2099</description>
        <pubDate>Wed, 12 Nov 2098 23:59:59 -1200</pubDate>
        <guid isPermaLink="false">CVPR-2099-deadline-2098-11-12 23:59:59@ccfddl.com</guid>
        <category>CG</category>
      </item>
    </channel></rss>
    """
    plain = strip_html(sample)
    terms = query_terms("AAAI 2027 ICLR 2027 AISTATS CLeaR WSDM")
    long_name_terms = query_terms("International Conference on Learning Representations 2027")
    stage_terms = query_terms("AAAI 摘要截稿 supplementary camera ready full paper")
    sample_snippets = snippets(sample, "AAAI ICLR AISTATS CLeaR WSDM")
    year_snippets = snippets(sample, "AAAI 2027 ICLR 2027 AISTATS CLeaR WSDM")
    assert "ignore" not in plain
    assert "aaai" in terms and "iclr" in terms and "2027" in terms
    assert terms.count("2027") == 1
    assert "iclr" in long_name_terms and "2027" in long_name_terms
    assert query_venue_terms("NIPS and Computer Vision and Pattern Recognition") == ["neurips", "cvpr"]
    assert query_stage_terms("AAAI 摘要截稿 supplementary camera ready full paper") == [
        "abstract",
        "full",
        "supplement",
        "camera_ready",
    ]
    assert "abstract" in stage_terms and "supplement" in stage_terms and "camera_ready" in stage_terms
    assert normalize_stage("supplementary material and code due") == "supplement"
    assert normalize_stage("camera-ready final version") == "camera_ready"
    assert len(sample_snippets) >= 5
    assert any("Predicted ICLR" in snippet for snippet in sample_snippets)
    assert any("WSDM" in snippet for snippet in sample_snippets)
    assert not any("3DV 2027" in snippet for snippet in year_snippets)
    links = candidate_links(sample, "https://aaai.org/conference/aaai/aaai-27/", "AAAI 2027 ICLR 2027")
    assert links[0]["kind"] == "openreview_candidate"
    assert "iclr" in links[0]["matches"] and "2027" in links[0]["matches"]
    assert any(link["kind"] == "official_dates_candidate" for link in links)
    assert all("cvpr" not in link["url"].lower() for link in links)
    assert all(not link["url"].startswith("mailto:") for link in links)
    rss_records = ccfddl_records(ccfddl_sample, "AAAI WSDM 2099", limit=4)
    assert [record["venue"] for record in rss_records] == ["AAAI", "WSDM"]
    abstract_records = ccfddl_records(ccfddl_sample, "AAAI abstract 2099", limit=4)
    assert len(abstract_records) == 1 and abstract_records[0]["stage"] == "abstract"
    full_name_records = ccfddl_records(
        ccfddl_sample,
        "ACM International Conference on Web Search and Data Mining full paper 2099",
        limit=4,
    )
    assert len(full_name_records) == 1
    assert full_name_records[0]["venue"] == "WSDM" and full_name_records[0]["stage"] == "full"
    assert rss_records[0]["stage"] == "abstract"
    assert rss_records[0]["timezone"] == "UTC-12"
    assert rss_records[0]["source_kind"] == "radar_hint"
    assert "CCF A" in rss_records[0]["rank"]
    assert "aaai" in rss_records[0]["matches"] and "2099" in rss_records[0]["matches"]
    rss_links = ccfddl_candidate_links(rss_records, limit=4)
    assert rss_links[0]["url"].startswith("https://aaai.org/")
    assert "aaai" in rss_links[0]["matches"]
    assert any("WSDM 2099 full" in snippet for snippet in ccfddl_snippets(rss_records))
    assert parse_deadline_datetime("2098-07-24 23:59:59", "UTC-12").utcoffset() == dt.timedelta(hours=-12)
    assert default_cache_path()
    assert VERSION == "0.1.0"
    assert REPORT_SCHEMA_VERSION == "1"
    assert [source["name"] for source in source_order(False)] == FAST_SOURCE_ORDER
    assert [source["name"] for source in source_order(True)] == [source["name"] for source in SOURCES]
    assert FAST_SOURCE_ORDER[0] == "mlciv-ai-deadlines"
    assert FAST_SOURCE_ORDER[1] == "ccfddl-rss"
    assert FAST_SOURCE_ORDER[-1] == "aideadlines-org"
    assert set(FAST_SOURCE_ORDER) == {source["name"] for source in SOURCES}
    assert DEFAULT_MAX_WORKERS == DEFAULT_MIN_OK_SOURCES
    class LegacyPool:
        def __init__(self) -> None:
            self.called_without_cancel = False

        def shutdown(self, wait: bool = False, cancel_futures: Optional[bool] = None) -> None:
            if cancel_futures is not None:
                raise TypeError("cancel_futures unsupported")
            self.called_without_cancel = wait is False

    legacy_pool = LegacyPool()
    shutdown_pool(legacy_pool)
    assert legacy_pool.called_without_cancel
    now = time.time()
    assert cached_entry_is_fresh({"fetched_at": now, "ok": True}, now, DEFAULT_CACHE_TTL_SECONDS)
    assert cached_entry_is_fresh({"fetched_at": now, "ok": False}, now, DEFAULT_CACHE_TTL_SECONDS)
    assert not cached_entry_is_fresh(
        {"fetched_at": now - FAILURE_CACHE_TTL_SECONDS - 1, "ok": False},
        now,
        DEFAULT_CACHE_TTL_SECONDS,
    )
    print("self-test ok")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", default="", help="Venue names or planning question to snippet-match.")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT_SECONDS, help="Per-source timeout in seconds.")
    parser.add_argument("--cache-ttl", type=int, default=DEFAULT_CACHE_TTL_SECONDS, help="Temp cache TTL in seconds.")
    parser.add_argument("--cache-path", default=default_cache_path(), help="Cache file path; also configurable via AI_CONFERENCE_DEADLINE_RADAR_CACHE.")
    parser.add_argument("--max-bytes", type=int, default=500_000, help="Max bytes to read per source.")
    parser.add_argument("--min-ok-sources", type=int, default=DEFAULT_MIN_OK_SOURCES, help="Fast mode returns after this many successful sources.")
    parser.add_argument("--max-workers", type=int, default=DEFAULT_MAX_WORKERS, help="Concurrent source fetches.")
    parser.add_argument("--link-limit", type=int, default=8, help="Max candidate verification links per source.")
    parser.add_argument("--record-limit", type=int, default=12, help="Max structured records per source.")
    parser.add_argument("--wait-all", action="store_true", help="Fetch all sources for diagnostics instead of returning after enough successes.")
    parser.add_argument("--no-cache", action="store_true", help="Disable temp cache for this run.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    parser.add_argument("--self-test", action="store_true", help="Run a no-network install smoke test.")
    parser.add_argument("--version", action="store_true", help="Print helper version and exit.")
    args = parser.parse_args()
    args.min_ok_sources = max(1, min(args.min_ok_sources, len(SOURCES)))
    args.max_workers = max(1, min(args.max_workers, len(SOURCES)))
    args.link_limit = max(0, args.link_limit)
    args.record_limit = max(0, args.record_limit)

    if args.version:
        print(VERSION)
        return
    if args.self_test:
        run_self_test()
        return

    report = build_report(args)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_markdown(report)


if __name__ == "__main__":
    main()
