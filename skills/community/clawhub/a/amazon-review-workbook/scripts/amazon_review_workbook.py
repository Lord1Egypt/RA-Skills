from __future__ import annotations

import argparse
import glob
import json
import logging
import os
import re
import socket
import sqlite3
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlparse

import requests
import websocket

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from review_cache import (
    DEFAULT_DB_PATH,
    cleanup_stale_jobs,
    create_job,
    ensure_db,
    export_analysis_to_records,
    fetch_cached_analysis_map,
    fetch_cached_reviews,
    finish_job,
    get_cached_review_count,
    get_known_review_ids,
    get_keyword_history_map,
    get_searched_keywords,
    record_keyword_search,
    upsert_analysis_records,
    upsert_reviews,
)
from deeplx_translate import (
    probe_deeplx,
    read_env_value,
    resolve_api_key,
    resolve_api_url,
    translate_text,
    translate_texts_batch,
)
from label_workflow import (
    build_taxonomy_bootstrap,
    default_cache_path,
    load_cache,
    load_canonical_tags,
    merge_records_with_labels,
    prepare_tagging_payload,
    save_cache,
)
from review_delivery_schema import (
    build_review_link,
    normalize_helpful_votes,
    normalize_review_time,
    normalize_space,
    write_delivery_artifacts,
)

DEFAULT_OUTPUT_DIR = Path.cwd() / "amazon-review-output"
# Multi-combo strategy to bypass Amazon's 100-review-per-filter limit
# Each combo returns up to ~100 reviews; combining all combos yields all unique reviews
DEFAULT_COMBOS = [
    ("recent_all", "sortBy=recent"),
    ("helpful_all", "sortBy=helpful"),
    ("recent_5", "filterByStar=five_star&reviewerType=all_reviews&sortBy=recent"),
    ("helpful_5", "filterByStar=five_star&reviewerType=all_reviews&sortBy=helpful"),
    ("recent_4", "filterByStar=four_star&reviewerType=all_reviews&sortBy=recent"),
    ("helpful_4", "filterByStar=four_star&reviewerType=all_reviews&sortBy=helpful"),
    ("recent_3", "filterByStar=three_star&reviewerType=all_reviews&sortBy=recent"),
    ("helpful_3", "filterByStar=three_star&reviewerType=all_reviews&sortBy=helpful"),
    ("recent_2", "filterByStar=two_star&reviewerType=all_reviews&sortBy=recent"),
    ("helpful_2", "filterByStar=two_star&reviewerType=all_reviews&sortBy=helpful"),
    ("recent_1", "filterByStar=one_star&reviewerType=all_reviews&sortBy=recent"),
    ("helpful_1", "filterByStar=one_star&reviewerType=all_reviews&sortBy=helpful"),
    (
        "recent_media",
        "mediaType=media_reviews_only&reviewerType=all_reviews&sortBy=recent",
    ),
    (
        "helpful_media",
        "mediaType=media_reviews_only&reviewerType=all_reviews&sortBy=helpful",
    ),
    (
        "recent_5_avp",
        "filterByStar=five_star&reviewerType=avp_only_reviews&sortBy=recent",
    ),
    (
        "helpful_5_avp",
        "filterByStar=five_star&reviewerType=avp_only_reviews&sortBy=helpful",
    ),
    (
        "recent_current",
        "formatType=current_format&reviewerType=all_reviews&sortBy=recent",
    ),
    (
        "helpful_current",
        "formatType=current_format&reviewerType=all_reviews&sortBy=helpful",
    ),
]

FAST_COMBOS = [
    ("recent_all", "sortBy=recent"),
    ("helpful_all", "sortBy=helpful"),
]

FAST_KEYWORDS: list[str] = []

# Keyword presets are layered:
# - universal: broadly useful across many consumer products
# - electronics: common hardware/app/setup issues
# - dashcam: scenario-specific terms from our core delivery context
KEYWORD_LIBRARY = {
    "universal": [
        "quality",
        "problem",
        "broken",
        "refund",
        "return",
        "support",
        "durable",
        "price",
        "worth",
        "packaging",
        "recommend",
    ],
    "electronics": [
        "app",
        "setup",
        "install",
        "battery",
        "cable",
        "screen",
        "update",
        "firmware",
    ],
    "dashcam": [
        "video",
        "night",
        "parking",
        "gps",
        "wifi",
        "recording",
        "mount",
        "rear camera",
    ],
}

KEYWORD_PROFILES = {
    "generic": ["universal"],
    "electronics": ["universal", "electronics"],
    "dashcam": ["universal", "electronics", "dashcam"],
}

DEFAULT_KEYWORD_PROFILE = "electronics"

DEFAULT_MAX_PAGES = 10
DEFAULT_CDP_PORT = 9222
DEFAULT_COMBO_DELAY_SECONDS = 2.5
DEFAULT_KEYWORD_REUSE_SCOPE = "successful"
DEFAULT_ZERO_RESULT_RETRY_HOURS = 72.0
DEFAULT_KEYWORD_TUNING_TOP_K = 12

logger = logging.getLogger("amazon_review_workbook")

COUNTRY_MAP = {
    "united kingdom": "英国",
    "england": "英国",
    "united states": "美国",
    "usa": "美国",
    "italia": "意大利",
    "italy": "意大利",
    "germania": "德国",
    "germany": "德国",
    "france": "法国",
    "francia": "法国",
    "spain": "西班牙",
    "spagna": "西班牙",
    "canada": "加拿大",
    "japan": "日本",
}

HOST_COUNTRY_MAP = {
    "amazon.co.uk": "英国",
    "amazon.com": "美国",
    "amazon.it": "意大利",
    "amazon.de": "德国",
    "amazon.fr": "法国",
    "amazon.es": "西班牙",
    "amazon.ca": "加拿大",
    "amazon.co.jp": "日本",
}


def configure_stdio() -> None:
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8")


def parse_product_url(url: str) -> tuple[str, str]:
    parsed = urlparse(url)
    match = re.search(
        r"/(?:dp|gp/product|product-reviews)/([A-Z0-9]{10})", parsed.path, re.I
    )
    if not match:
        raise ValueError(f"无法从 URL 解析 ASIN: {url}")
    host = parsed.netloc or "www.amazon.com"
    return match.group(1).upper(), host


def build_review_url(host: str, asin: str) -> str:
    return f"https://{host}/product-reviews/{asin}/ref=cm_cr_dp_d_show_all_btm?ie=UTF8"


def build_collect_output_path(output_dir: Path, asin: str) -> Path:
    return build_machine_output_path(output_dir, asin)


def build_machine_output_path(output_dir: Path, asin: str) -> Path:
    return output_dir.expanduser() / f"amazon_{asin}_review_rows_machine.json"


def _record_keys(record: dict[str, Any]) -> list[str]:
    keys: list[str] = []
    for field in ("review_id", "seq", "序号", "position"):
        value = normalize_space(record.get(field))
        if value and value not in keys:
            keys.append(value)
    return keys


def load_layered_records(input_path: Path) -> list[dict[str, Any]]:
    records = load_json_records(input_path)
    asin = infer_asin_from_records(records, input_path)
    machine_path = build_machine_output_path(input_path.parent, asin)
    if not machine_path.exists() or machine_path.resolve() == input_path.resolve():
        return records

    machine_records = load_json_records(machine_path)
    supplemental_by_key: dict[str, dict[str, Any]] = {}
    for record in records:
        for key in _record_keys(record):
            supplemental_by_key.setdefault(key, record)

    layered: list[dict[str, Any]] = []
    for record in machine_records:
        row = dict(record)
        supplemental = None
        for key in _record_keys(record):
            supplemental = supplemental_by_key.get(key)
            if supplemental:
                break
        if supplemental:
            for field, value in supplemental.items():
                if normalize_space(value):
                    row[field] = value
        layered.append(row)
    return layered


def build_factual_output_paths(output_dir: Path, asin: str) -> tuple[Path, Path, Path]:
    base = output_dir.expanduser() / f"amazon_{asin}_review_rows_factual"
    return (
        base.with_suffix(".json"),
        base.with_suffix(".xlsx"),
        base.with_suffix(".csv"),
    )


def build_translated_output_paths(
    output_dir: Path, asin: str
) -> tuple[Path, Path, Path]:
    base = output_dir.expanduser() / f"amazon_{asin}_review_rows_translated"
    return (
        base.with_suffix(".json"),
        base.with_suffix(".xlsx"),
        base.with_suffix(".csv"),
    )


def build_final_output_paths(output_dir: Path, stem: str) -> tuple[Path, Path, Path]:
    base = output_dir.expanduser() / stem
    return (
        base.with_suffix(".json"),
        base.with_suffix(".xlsx"),
        base.with_suffix(".csv"),
    )


def build_prepare_output_path(output_dir: Path, asin: str) -> Path:
    return output_dir.expanduser() / f"amazon_{asin}_tagging_input.json"


def build_bootstrap_output_path(output_dir: Path, asin: str) -> Path:
    return output_dir.expanduser() / f"amazon_{asin}_taxonomy_bootstrap.json"


def default_keyword_tuning_state_path(output_dir: Path) -> Path:
    return output_dir.expanduser() / "keyword_tuning_state.json"


def dedupe_preserve_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def build_keyword_profile(profile: str) -> list[str]:
    layers = KEYWORD_PROFILES.get(profile, KEYWORD_PROFILES[DEFAULT_KEYWORD_PROFILE])
    combined: list[str] = []
    for layer in layers:
        combined.extend(KEYWORD_LIBRARY.get(layer, []))
    return dedupe_preserve_order(combined)


DEFAULT_KEYWORDS = build_keyword_profile(DEFAULT_KEYWORD_PROFILE)


def load_keyword_tuning_state(path: Path | None) -> dict[str, Any]:
    if path is None or not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def score_keyword_stats(stats: dict[str, Any]) -> float:
    best_new = float(stats.get("best_new_count") or 0)
    total_new = float(stats.get("total_new_count") or 0)
    positive_runs = float(stats.get("positive_runs") or 0)
    zero_runs = float(stats.get("zero_runs") or 0)
    total_runs = max(float(stats.get("total_runs") or 0), 1.0)
    hit_rate = positive_runs / total_runs
    return round(best_new * 5 + total_new * 2 + hit_rate * 10 - zero_runs * 1.5, 3)


def build_recommended_keywords_from_stats(
    profile: str,
    keyword_stats: dict[str, dict[str, Any]],
    *,
    top_k: int = DEFAULT_KEYWORD_TUNING_TOP_K,
) -> list[str]:
    base_keywords = build_keyword_profile(profile)
    ranked: list[tuple[float, int, int, str]] = []
    for base_index, keyword in enumerate(base_keywords):
        stats = keyword_stats.get(keyword, {})
        score = score_keyword_stats(stats)
        positive_runs = int(stats.get("positive_runs") or 0)
        total_new = int(stats.get("total_new_count") or 0)
        ranked.append((score, positive_runs, total_new, keyword))

    ranked.sort(key=lambda item: (-item[0], -item[1], -item[2], base_keywords.index(item[3])))
    positives = [item[3] for item in ranked if item[1] > 0]
    unexplored = [item[3] for item in ranked if item[1] == 0 and item[0] == 0]
    weak = [item[3] for item in ranked if item[1] == 0 and item[0] != 0]
    ordered = dedupe_preserve_order(positives + unexplored + weak)
    if top_k > 0:
        return ordered[:top_k]
    return ordered


def get_tuned_keywords(
    profile: str,
    *,
    tuning_state: dict[str, Any],
    top_k: int = DEFAULT_KEYWORD_TUNING_TOP_K,
) -> list[str]:
    profile_payload = (tuning_state.get("profiles") or {}).get(profile)
    if not isinstance(profile_payload, dict):
        return build_keyword_profile(profile)[:top_k]
    keywords = profile_payload.get("recommended_keywords") or []
    cleaned = dedupe_preserve_order(
        [normalize_space(item) for item in keywords if normalize_space(item)]
    )
    if cleaned:
        return cleaned[:top_k] if top_k > 0 else cleaned
    return build_keyword_profile(profile)[:top_k]


def resolve_keyword_plan(
    keywords: list[str] | None,
    keyword_profile: str,
    *,
    tuning_state: dict[str, Any] | None = None,
    top_k: int = DEFAULT_KEYWORD_TUNING_TOP_K,
) -> tuple[list[str], str]:
    if keywords is None:
        return [], "off"
    cleaned = dedupe_preserve_order(
        [normalize_space(item) for item in keywords if normalize_space(item)]
    )
    if cleaned:
        return cleaned, "custom"
    tuned = get_tuned_keywords(
        keyword_profile, tuning_state=tuning_state or {}, top_k=top_k
    )
    return tuned, f"profile:{keyword_profile}:tuned"


def parse_utc_timestamp(value: Any) -> datetime | None:
    text = normalize_space(value)
    if not text:
        return None
    for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"):
        try:
            return datetime.strptime(text, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def should_skip_keyword(
    history_entry: dict[str, Any] | None,
    *,
    reuse_scope: str,
    zero_result_retry_hours: float,
    now_utc: datetime | None = None,
) -> tuple[bool, str]:
    if not history_entry:
        return False, ""
    if reuse_scope == "none":
        return False, ""

    best_new_count = int(history_entry.get("best_new_count") or 0)
    if reuse_scope in {"successful", "all"} and best_new_count > 0:
        return True, "successful_history"

    if reuse_scope == "all":
        return True, "history"

    if zero_result_retry_hours <= 0:
        return False, ""

    searched_at = parse_utc_timestamp(history_entry.get("searched_at"))
    if not searched_at:
        return False, ""

    now = now_utc or datetime.now(timezone.utc)
    age_hours = (now - searched_at).total_seconds() / 3600
    if age_hours < zero_result_retry_hours:
        return True, "recent_zero_history"
    return False, ""


def merge_keyword_observation(
    bucket: dict[str, dict[str, Any]], keyword: str, new_count: int, source: str
) -> None:
    keyword = normalize_space(keyword)
    if not keyword:
        return
    stats = bucket.setdefault(
        keyword,
        {
            "keyword": keyword,
            "total_runs": 0,
            "positive_runs": 0,
            "zero_runs": 0,
            "total_new_count": 0,
            "best_new_count": 0,
            "sources": [],
        },
    )
    stats["total_runs"] += 1
    stats["total_new_count"] += int(new_count)
    stats["best_new_count"] = max(int(stats["best_new_count"]), int(new_count))
    if int(new_count) > 0:
        stats["positive_runs"] += 1
    else:
        stats["zero_runs"] += 1
    if source not in stats["sources"]:
        stats["sources"].append(source)


def aggregate_keyword_stats_from_db(db_path: Path) -> dict[str, dict[str, Any]]:
    if not db_path.exists():
        return {}
    conn = ensure_db(db_path)
    rows = conn.execute(
        """SELECT keyword, new_count, best_new_count, search_count
           FROM keyword_history"""
    ).fetchall()
    conn.close()
    result: dict[str, dict[str, Any]] = {}
    for keyword, new_count, best_new_count, search_count in rows:
        merge_keyword_observation(result, str(keyword), int(best_new_count or new_count or 0), "db_best")
        stats = result[str(keyword)]
        stats["total_runs"] = max(int(stats["total_runs"]), int(search_count or 1))
        stats["best_new_count"] = max(int(stats["best_new_count"]), int(best_new_count or 0))
        stats["total_new_count"] = max(int(stats["total_new_count"]), int(best_new_count or new_count or 0))
    return result


def aggregate_keyword_stats_from_reports(report_paths: list[Path]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for path in report_paths:
        if not path.exists():
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if not isinstance(payload, dict):
            continue
        stats_rows = payload.get("stats")
        if not isinstance(stats_rows, list):
            continue
        for row in stats_rows:
            if not isinstance(row, dict):
                continue
            keyword = normalize_space(row.get("kw") or row.get("keyword"))
            new_count = int(row.get("added_new") or row.get("new") or 0)
            merge_keyword_observation(result, keyword, new_count, path.name)
    return result


def combine_keyword_stats(*sources: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    combined: dict[str, dict[str, Any]] = {}
    for source in sources:
        for keyword, stats in source.items():
            entry = combined.setdefault(
                keyword,
                {
                    "keyword": keyword,
                    "total_runs": 0,
                    "positive_runs": 0,
                    "zero_runs": 0,
                    "total_new_count": 0,
                    "best_new_count": 0,
                    "sources": [],
                },
            )
            entry["total_runs"] += int(stats.get("total_runs") or 0)
            entry["positive_runs"] += int(stats.get("positive_runs") or 0)
            entry["zero_runs"] += int(stats.get("zero_runs") or 0)
            entry["total_new_count"] += int(stats.get("total_new_count") or 0)
            entry["best_new_count"] = max(
                int(entry["best_new_count"]), int(stats.get("best_new_count") or 0)
            )
            entry["sources"] = dedupe_preserve_order(
                list(entry["sources"]) + list(stats.get("sources") or [])
            )
    for entry in combined.values():
        entry["score"] = score_keyword_stats(entry)
    return combined


def build_keyword_tuning_state(
    *,
    keyword_stats: dict[str, dict[str, Any]],
    top_k: int = DEFAULT_KEYWORD_TUNING_TOP_K,
) -> dict[str, Any]:
    profiles: dict[str, Any] = {}
    for profile in sorted(KEYWORD_PROFILES):
        recommended = build_recommended_keywords_from_stats(
            profile, keyword_stats, top_k=top_k
        )
        profiles[profile] = {
            "recommended_keywords": recommended,
            "base_keywords": build_keyword_profile(profile),
        }
    global_top = sorted(
        keyword_stats.values(),
        key=lambda item: (-float(item.get("score") or 0), item["keyword"]),
    )
    return {
        "metadata": {
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "keyword_count": len(keyword_stats),
            "top_k": top_k,
        },
        "profiles": profiles,
        "global_keyword_stats": global_top,
    }


def refresh_keyword_tuning_state(
    *,
    db_path: Path,
    output_path: Path,
    report_paths: list[Path] | None = None,
    top_k: int = DEFAULT_KEYWORD_TUNING_TOP_K,
) -> dict[str, Any]:
    db_stats = aggregate_keyword_stats_from_db(db_path)
    report_stats = aggregate_keyword_stats_from_reports(report_paths or [])
    combined = combine_keyword_stats(db_stats, report_stats)
    payload = build_keyword_tuning_state(keyword_stats=combined, top_k=top_k)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload


def parse_count_token(token: str) -> int | None:
    digits = re.sub(r"[^\d]", "", token)
    if not digits:
        return None
    try:
        return int(digits)
    except ValueError:
        return None


def extract_named_count(
    texts: list[str], patterns: list[str]
) -> tuple[int | None, str]:
    for text in texts:
        collapsed = normalize_space(text)
        lowered = collapsed.lower()
        for pattern in patterns:
            match = re.search(pattern, lowered, re.I)
            if not match:
                continue
            value = parse_count_token(match.group(1))
            if value is not None:
                return value, collapsed
    return None, ""


def extract_page_totals(texts: list[str]) -> dict[str, Any]:
    review_patterns = [
        r"(?:showing|show)\s+\d+\s*-\s*\d+\s+(?:of|sur|von|de)\s+(\d[\d.,\s]*)\s+(?:customer\s+)?(?:global\s+)?(?:reviews?|recensioni|reseñas|avis|bewertungen)",
        r"(\d[\d.,\s]*)\s+(?:customer\s+)?(?:global\s+)?(?:reviews?|recensioni|reseñas|avis|bewertungen)",
    ]
    rating_patterns = [
        r"(?:showing|show)\s+\d+\s*-\s*\d+\s+(?:of|sur|von|de)\s+(\d[\d.,\s]*)\s+(?:global\s+)?(?:ratings|valutazioni|calificaciones|évaluations)",
        r"(\d[\d.,\s]*)\s+(?:global\s+)?(?:ratings|valutazioni|calificaciones|évaluations)",
    ]
    review_count, review_evidence = extract_named_count(texts, review_patterns)
    rating_count, rating_evidence = extract_named_count(texts, rating_patterns)
    return {
        "page_total_reviews": review_count,
        "page_total_reviews_evidence": review_evidence,
        "page_total_ratings": rating_count,
        "page_total_ratings_evidence": rating_evidence,
    }


def port_is_open(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1.5)
        return sock.connect_ex((host, port)) == 0


@dataclass
class PageSnapshot:
    href: str
    title: str
    next_href: str | None
    reviews: list[dict[str, Any]]


class BrowserSession:
    def __init__(self, port: int) -> None:
        self.port = port
        self.ws_url: str | None = None

    @property
    def http_base(self) -> str:
        return f"http://127.0.0.1:{self.port}"

    def wait_until_ready(self, timeout_seconds: int = 15) -> None:
        deadline = time.time() + timeout_seconds
        last_error = "Chrome remote debugging not ready"
        while time.time() < deadline:
            try:
                targets = requests.get(f"{self.http_base}/json", timeout=5).json()
                if not targets:
                    targets = [
                        requests.put(
                            f"{self.http_base}/json/new?about:blank", timeout=5
                        ).json()
                    ]
                pages = [
                    item
                    for item in targets
                    if item.get("type") == "page" and item.get("webSocketDebuggerUrl")
                ]
                if pages:
                    self.ws_url = str(pages[0]["webSocketDebuggerUrl"])
                    return
                last_error = "no page targets"
            except Exception as exc:  # noqa: BLE001
                last_error = str(exc)
            time.sleep(1)
        raise RuntimeError(last_error)

    def send(
        self, method: str, params: dict[str, Any] | None = None, *, timeout: int = 30
    ) -> Any:
        if not self.ws_url:
            raise RuntimeError("Browser target is not initialized")
        ws = websocket.create_connection(
            self.ws_url, suppress_origin=True, timeout=timeout
        )
        try:
            ws.send(
                json.dumps(
                    {
                        "id": 1,
                        "method": method,
                        "params": params or {},
                    }
                )
            )
            deadline = time.time() + timeout
            max_attempts = 200
            attempts = 0
            while time.time() < deadline and attempts < max_attempts:
                attempts += 1
                message = json.loads(ws.recv())
                if message.get("id") != 1:
                    continue
                result = message.get("result", {})
                if message.get("error"):
                    raise RuntimeError(
                        message["error"].get("message") or f"CDP {method} failed"
                    )
                return result
            raise RuntimeError(
                f"CDP {method} timed out after {timeout}s / {max_attempts} attempts"
            )
        finally:
            ws.close()

    def eval(self, expression: str, *, timeout: int = 30) -> Any:
        result = self.send(
            "Runtime.evaluate",
            {
                "expression": expression,
                "returnByValue": True,
                "awaitPromise": True,
            },
            timeout=timeout,
        )
        if result.get("exceptionDetails"):
            raise RuntimeError(
                result["exceptionDetails"].get("text") or "CDP evaluate failed"
            )
        return result.get("result", {}).get("value")

    def navigate(self, url: str) -> None:
        self.send("Page.navigate", {"url": url}, timeout=20)
        time.sleep(4)


def extract_page(browser: BrowserSession) -> PageSnapshot:
    expression = r"""
(() => {
  const normalize = (value) => (value || '').replace(/\s+/g, ' ').trim();
  // Use textContent from cloned DOM to bypass Edge/Chrome auto-translation
  // which only modifies the rendered innerText, not the original DOM text.
  const moreReviews = Array.from(document.querySelectorAll('a, button, input[type="button"], input[type="submit"]')).find((el) => {
    const label = ((el.innerText || el.value || el.getAttribute('aria-label') || '') + '').replace(/\s+/g, ' ').trim();
    return /^(show|load)\s+\d+\s+more reviews$/i.test(label) || /^(show|load)\s+more reviews$/i.test(label);
  });
  const reviews = Array.from(document.querySelectorAll('[data-hook="review"]')).map((el, index) => {
    const rawText = (selector) => {
      const node = el.querySelector(selector);
      if (!node) return '';
      const clone = node.cloneNode(true);
      const translateEls = clone.querySelectorAll('[translate="no"], [class*="translated"]');
      translateEls.forEach(e => e.remove());
      return normalize(clone.textContent || '');
    };
    const reviewEl = el;
    let reviewId = reviewEl.id || '';
    if (!reviewId) {
      const titleLink = reviewEl.querySelector('a[data-hook="review-title"]');
      if (titleLink && titleLink.href) {
        const m = titleLink.href.match(/\/R([A-Z0-9]+)/i);
        if (m) reviewId = 'R' + m[1];
      }
    }
    if (!reviewId) {
      const dataId = reviewEl.getAttribute('data-review-id') || reviewEl.getAttribute('data-contentid');
      if (dataId) reviewId = dataId;
    }
    return {
      position: index + 1,
      review_id: reviewId,
      title: rawText('[data-hook="review-title"]'),
      rating_text: rawText('[data-hook="review-star-rating"], [data-hook="cmps-review-star-rating"]'),
      country_date: rawText('[data-hook="review-date"]'),
      body: rawText('[data-hook="review-body"]'),
      author: rawText('.a-profile-name'),
      helpful_votes: rawText('[data-hook="helpful-vote-statement"], .cr-vote-text'),
      review_link: el.querySelector('a[data-hook="review-title"]')?.href || ''
    };
  });
  return {
    href: location.href,
    title: document.title,
    next_href: (moreReviews && (moreReviews.href || moreReviews.getAttribute('href'))) || document.querySelector('.a-pagination .a-last a')?.href || null,
    reviews
  };
})()
"""
    payload = browser.eval(expression)
    return PageSnapshot(
        href=str(payload.get("href", "")),
        title=str(payload.get("title", "")),
        next_href=str(payload["next_href"]) if payload.get("next_href") else None,
        reviews=list(payload.get("reviews") or []),
    )


def wait_loaded(browser: BrowserSession, timeout_seconds: int = 25) -> PageSnapshot:
    deadline = time.time() + timeout_seconds
    latest = extract_page(browser)
    while time.time() < deadline:
        if latest.reviews:
            return latest
        time.sleep(1)
        latest = extract_page(browser)
    return latest


def click_next(browser: BrowserSession) -> bool:
    expression = r"""
(() => {
  const candidates = Array.from(document.querySelectorAll('a, button, input[type="button"], input[type="submit"]'));
  const target = candidates.find((el) => {
    const label = ((el.innerText || el.value || el.getAttribute('aria-label') || '') + '').replace(/\s+/g, ' ').trim();
    return /^(show|load)\s+\d+\s+more reviews$/i.test(label) || /^(show|load)\s+more reviews$/i.test(label);
  }) || document.querySelector('.a-pagination .a-last a');
  if (!target) return false;
  target.click();
  return true;
})()
"""
    return bool(browser.eval(expression))


def wait_for_page_change(
    browser: BrowserSession, previous_snapshot: PageSnapshot, timeout_seconds: int = 20
) -> PageSnapshot:
    deadline = time.time() + timeout_seconds
    latest = extract_page(browser)
    while time.time() < deadline:
        reviews = latest.reviews
        first_id = reviews[0].get("review_id") if reviews else None
        last_id = reviews[-1].get("review_id") if reviews else None
        if (
            len(reviews) != len(previous_snapshot.reviews)
            or first_id
            != (
                previous_snapshot.reviews[0].get("review_id")
                if previous_snapshot.reviews
                else None
            )
            or last_id
            != (
                previous_snapshot.reviews[-1].get("review_id")
                if previous_snapshot.reviews
                else None
            )
        ):
            return latest
        time.sleep(2)
        latest = extract_page(browser)
    return latest


def fetch_review_page_totals(review_url: str, port: int) -> dict[str, Any]:
    browser = BrowserSession(port)
    browser.wait_until_ready()
    browser.navigate(review_url)
    _enforce_notranslate(browser)
    payload = browser.eval(
        r"""
(() => {
  const selectors = [
    '[data-hook="cr-filter-info-review-rating-count"]',
    '#filter-info-section',
    '#acrCustomerReviewText',
    '[data-hook="total-review-count"]',
    '.cr-filter-info-review-rating-count',
    '[data-hook="review"] [data-hook="review-date"]'
  ];
  const texts = [];
  for (const selector of selectors) {
    for (const node of document.querySelectorAll(selector)) {
      const text = (node.textContent || '').replace(/\s+/g, ' ').trim();
      if (text) texts.push(text);
    }
  }
  return {
    href: location.href,
    title: document.title,
    texts: Array.from(new Set(texts)).slice(0, 20)
  };
})()
"""
    )
    texts = [str(item) for item in payload.get("texts") or [] if normalize_space(item)]
    totals = extract_page_totals(texts)
    return {
        "probe_url": str(payload.get("href", review_url)),
        "probe_title": str(payload.get("title", "")),
        "probe_texts": texts,
        **totals,
    }


def infer_country(country_date: str, host: str) -> str:
    lowered = normalize_space(country_date).lower()
    for key, value in COUNTRY_MAP.items():
        if key in lowered:
            return value
    for key, value in HOST_COUNTRY_MAP.items():
        if key in host:
            return value
    return ""


def parse_rating(rating_text: str) -> str:
    match = re.search(r"(\d+(?:[.,]\d+)?)", str(rating_text))
    if not match:
        return ""
    value = match.group(1).replace(",", ".")
    if value.endswith(".0"):
        value = value[:-2]
    return value


def strip_rating_prefix(title: str) -> str:
    value = normalize_space(title)
    patterns = [
        r"^\s*\d+(?:[.,]\d+)?\s+out of\s+\d+\s+stars\s*",
        r"^\s*\d+(?:[.,]\d+)?\s+su\s+\d+\s+stelle\s*",
        r"^\s*\d+(?:[.,]\d+)?\s+de\s+\d+\s+estrellas\s*",
        r"^\s*\d+(?:[.,]\d+)?\s+sur\s+\d+\s+étoiles\s*",
    ]
    for pattern in patterns:
        value = re.sub(pattern, "", value, flags=re.I)
    return normalize_space(value)


def merge_review_row(target: dict[str, Any], source: dict[str, Any]) -> None:
    """Fill gaps in target from source. First-wins, fill-gaps strategy."""
    for key, value in source.items():
        if value in (None, "", []):
            continue
        if not target.get(key):
            target[key] = value


def _enforce_notranslate(browser: BrowserSession) -> None:
    """Disable Edge/Chrome auto-translation and reload page."""
    browser.eval("""
(() => {
  let translateMeta = document.querySelector('meta[name="google"]');
  if (!translateMeta) {
    const m = document.createElement('meta');
    m.name = 'google';
    m.content = 'notranslate';
    document.head.appendChild(m);
  }
  document.documentElement.setAttribute('translate', 'no');
  const htmlEl = document.documentElement;
  if (htmlEl.classList.contains('translated-yes')) {
    htmlEl.classList.remove('translated-yes');
    htmlEl.classList.add('translated-no');
  }
  if (document.body && document.body.classList.contains('translated-yes')) {
    document.body.classList.remove('translated-yes');
    document.body.classList.add('translated-no');
  }
  document.querySelectorAll('.goog-te-banner-frame, .goog-te-menu-frame, .skiptranslate, .translated-text').forEach(el => el.remove());
  return 'notranslate enforced';
})()
""")
    time.sleep(1)
    browser.eval("window.location.reload()")
    time.sleep(5)


def _collect_single_combo(
    browser: BrowserSession,
    combo_url: str,
    combo_name: str,
    *,
    max_pages: int,
    resume_from_page: int,
    host: str,
    asin: str,
    seen_review_ids: set[str],
    all_rows: list[dict[str, Any]],
) -> int:
    """Collect reviews from a single filter/sort combo. Returns new review count."""
    browser.navigate(combo_url)
    time.sleep(4)
    _enforce_notranslate(browser)

    page_title = browser.eval("document.title")
    if page_title and any(
        blocked in str(page_title).lower()
        for blocked in ("robot check", "captcha", "sorry", "problem loading")
    ):
        print(f"[{combo_name}] 阻断页面，跳过")
        return 0

    pages: list[dict[str, Any]] = []
    seen_signatures: set[tuple[str, str, int]] = set()
    current = wait_loaded(browser)

    if not current.reviews:
        print(f"[{combo_name}] 未检测到评论，跳过")
        return 0

    pages_to_skip = max(resume_from_page - 1, 0)
    while pages_to_skip > 0:
        if not current.next_href or not click_next(browser):
            print(f"[{combo_name}] 无法跳到第 {resume_from_page} 页，提前结束")
            return 0
        current = wait_for_page_change(browser, current)
        pages_to_skip -= 1

    start_page = max(resume_from_page, 1)
    for page_no in range(start_page, start_page + max_pages):
        if not current.reviews:
            break
        first_id = str(current.reviews[0].get("review_id") or "")
        last_id = str(current.reviews[-1].get("review_id") or "")
        signature = (first_id, last_id, len(current.reviews))
        if not first_id or signature in seen_signatures:
            break

        seen_signatures.add(signature)
        pages.append(
            {
                "page_no": page_no,
                "href": current.href,
                "title": current.title,
                "next_href": current.next_href,
                "reviews": current.reviews,
            }
        )

        if not current.next_href:
            break
        if not click_next(browser):
            break
        current = wait_for_page_change(browser, current)

    new_count = 0
    for page in pages:
        for review in page["reviews"]:
            review_id = str(review.get("review_id") or "")
            if review_id and review_id in seen_review_ids:
                continue
            if review_id:
                seen_review_ids.add(review_id)
            row = dict(review)
            row["seq"] = str(len(all_rows) + new_count + 1)
            row["page_no"] = page["page_no"]
            row["source_href"] = page["href"]
            row["host"] = host
            row["asin"] = asin
            row["review_time"] = normalize_review_time(row.get("country_date", ""))
            row["helpful_votes"] = normalize_helpful_votes(row.get("helpful_votes", ""))
            row["review_link"] = build_review_link(
                str(row.get("review_id") or ""), host, row.get("review_link")
            )
            all_rows.append(row)
            new_count += 1

    if new_count > 0:
        print(f"[{combo_name}] 新增 {new_count} 条评论（共 {len(pages)} 页）")
    else:
        print(f"[{combo_name}] 无新评论")
    return new_count


def collect_reviews(
    url: str,
    *,
    port: int,
    max_pages: int,
    resume_from: int = 0,
    mode: str = "deep",
    db_path: Path | None = None,
    refresh_cache: bool = False,
    keywords: list[str] | None = None,
    keyword_profile: str = DEFAULT_KEYWORD_PROFILE,
    keyword_reuse_scope: str = DEFAULT_KEYWORD_REUSE_SCOPE,
    zero_result_retry_hours: float = DEFAULT_ZERO_RESULT_RETRY_HOURS,
    keyword_tuning_state_path: Path | None = None,
    combo_delay_seconds: float = DEFAULT_COMBO_DELAY_SECONDS,
) -> dict[str, Any]:
    asin, host = parse_product_url(url)
    review_url = build_review_url(host, asin)

    # Setup cache
    if db_path is None:
        db_path = DEFAULT_DB_PATH
    conn = ensure_db(db_path)
    cleanup_stale_jobs(conn)

    cached_count = get_cached_review_count(conn, host, asin)
    known_ids = get_known_review_ids(conn, host, asin) if not refresh_cache else set()

    # Skip collection if cache is fresh and mode is fast
    if not refresh_cache and mode == "fast" and cached_count > 0:
        print(f"缓存已有 {cached_count} 条评论，fast 模式跳过采集。")
        cached_rows = fetch_cached_reviews(conn, host, asin)
        # Re-normalize
        for i, row in enumerate(cached_rows, start=1):
            row["seq"] = str(i)
            row["host"] = host
            row["asin"] = asin
        conn.close()
        return {
            "asin": asin,
            "host": host,
            "source_url": url,
            "review_url": review_url,
            "mode": mode,
            "combo_count": 0,
            "cached_total": cached_count,
            "row_count": len(cached_rows),
            "results": cached_rows,
        }

    # Create job
    job_id = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    create_job(conn, job_id, host, asin, url)

    browser = BrowserSession(port)
    browser.wait_until_ready()
    tuning_state = load_keyword_tuning_state(keyword_tuning_state_path)

    # Select combo strategy
    if mode == "fast":
        combos = FAST_COMBOS
        planned_keywords = FAST_KEYWORDS
        keyword_mode = "off"
    else:
        combos = DEFAULT_COMBOS
        planned_keywords, keyword_mode = resolve_keyword_plan(
            keywords,
            keyword_profile,
            tuning_state=tuning_state,
        )

    all_rows: list[dict[str, Any]] = []
    seen_review_ids: set[str] = set(known_ids)
    stats: list[dict[str, Any]] = []

    print(
        f"开始采集评论，模式: {mode}，{len(combos)} 个筛选组合 + {len(planned_keywords)} 个关键词"
    )
    if cached_count > 0:
        print(f"缓存已有 {cached_count} 条评论，本次只采集新增的")

    # Phase 1: Star/sort combos
    for combo_name, combo_params in combos:
        combo_url = f"https://{host}/product-reviews/{asin}/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&{combo_params}"
        new_count = _collect_single_combo(
            browser,
            combo_url,
            combo_name,
            max_pages=max_pages,
            resume_from_page=resume_from,
            host=host,
            asin=asin,
            seen_review_ids=seen_review_ids,
            all_rows=all_rows,
        )
        stats.append(
            {
                "combo": combo_name,
                "new": new_count,
                "total": len(all_rows),
            }
        )
        if combo_delay_seconds > 0 and (
            combo_name != combos[-1][0] or planned_keywords
        ):
            time.sleep(combo_delay_seconds)

    # Phase 2: Keyword search with history tracking and smart skip
    keyword_history = (
        get_keyword_history_map(conn, host, asin) if not refresh_cache else {}
    )
    skipped_keywords = 0
    skipped_successful_keywords = 0
    skipped_recent_zero_keywords = 0
    consecutive_zero_keywords = 0

    for kw in planned_keywords:
        should_skip, reason = should_skip_keyword(
            keyword_history.get(kw),
            reuse_scope=keyword_reuse_scope,
            zero_result_retry_hours=zero_result_retry_hours,
        )
        if should_skip:
            skipped_keywords += 1
            if reason == "successful_history":
                skipped_successful_keywords += 1
            elif reason == "recent_zero_history":
                skipped_recent_zero_keywords += 1
            continue

        kw_name = kw.replace(" ", "_")
        kw_params = f"filterByStar=all_stars&reviewerType=all_reviews&sortBy=recent&filterByKeyword={quote(kw)}"
        combo_url = f"https://{host}/product-reviews/{asin}/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&{kw_params}"
        new_count = _collect_single_combo(
            browser,
            combo_url,
            f"kw_{kw_name}",
            max_pages=max_pages,
            resume_from_page=resume_from,
            host=host,
            asin=asin,
            seen_review_ids=seen_review_ids,
            all_rows=all_rows,
        )
        stats.append(
            {
                "combo": f"kw_{kw_name}",
                "keyword": kw,
                "new": new_count,
                "total": len(all_rows),
            }
        )
        # Record keyword search in history
        record_keyword_search(conn, host, asin, kw, job_id, new_count, len(all_rows))

        # Smart early termination:
        # - If no new reviews from last 3 keywords, stop
        # - If we have 500+ reviews, stop
        if new_count == 0:
            consecutive_zero_keywords += 1
        else:
            consecutive_zero_keywords = 0
        if len(all_rows) >= 500:
            print(f"已达到 500+ 条评论，停止关键词搜索")
            break
        if consecutive_zero_keywords >= 3:
            print("连续 3 个关键词没有新增评论，停止关键词搜索")
            break
        if combo_delay_seconds > 0 and kw != planned_keywords[-1]:
            time.sleep(combo_delay_seconds)

    if skipped_keywords > 0:
        print(f"跳过 {skipped_keywords} 个已搜索过的关键词")
    if skipped_successful_keywords > 0:
        print(f"其中 {skipped_successful_keywords} 个关键词因历史命中过结果被复用跳过")
    if skipped_recent_zero_keywords > 0:
        print(
            f"其中 {skipped_recent_zero_keywords} 个关键词因近期零结果记录被临时跳过"
        )

    # Save to cache
    new_in_session = len(all_rows)
    upsert_reviews(conn, host, asin, job_id, all_rows)
    final_cached_count = get_cached_review_count(conn, host, asin)
    finish_job(
        conn,
        job_id,
        "success",
        current_seen_count=len(all_rows),
        new_review_count=new_in_session,
        cached_total=final_cached_count,
        stats=stats,
    )

    # Load full cache for output (includes previously cached reviews)
    cached_rows = fetch_cached_reviews(conn, host, asin)
    conn.close()

    if keyword_tuning_state_path:
        try:
            refresh_keyword_tuning_state(
                db_path=db_path,
                output_path=keyword_tuning_state_path,
            )
        except Exception as exc:  # noqa: BLE001
            print(f"keyword_tuning_state_refresh_failed={exc}")

    # Re-number and normalize
    for i, row in enumerate(cached_rows, start=1):
        row["seq"] = str(i)
        row["host"] = host
        row["asin"] = asin

    return {
        "asin": asin,
        "host": host,
        "source_url": url,
        "review_url": review_url,
        "mode": mode,
        "combo_count": len(combos),
        "keyword_count": len(planned_keywords),
        "keyword_mode": keyword_mode,
        "keyword_profile": keyword_profile,
        "keyword_tuning_state_path": str(keyword_tuning_state_path)
        if keyword_tuning_state_path
        else "",
        "keyword_reuse_scope": keyword_reuse_scope,
        "skipped_keywords": skipped_keywords,
        "skipped_successful_keywords": skipped_successful_keywords,
        "skipped_recent_zero_keywords": skipped_recent_zero_keywords,
        "new_in_session": new_in_session,
        "cached_total": final_cached_count,
        "row_count": len(cached_rows),
        "stats": stats,
        "results": cached_rows,
    }


def load_json_records(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        for key in ("records", "items", "data", "results"):
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
    raise SystemExit(f"无法从 JSON 解析记录数组: {path}")


def infer_asin_from_records(records: list[dict[str, Any]], input_path: Path) -> str:
    for record in records:
        for key in ("asin", "ASIN"):
            value = normalize_space(record.get(key))
            if re.fullmatch(r"[A-Z0-9]{10}", value):
                return value
        review_link = normalize_space(
            record.get("评论链接网址") or record.get("review_link")
        )
        if review_link:
            try:
                asin, _ = parse_product_url(review_link)
                return asin
            except Exception:  # noqa: BLE001
                pass
    match = re.search(r"([A-Z0-9]{10})", input_path.stem, re.I)
    if match:
        return match.group(1).upper()
    return "amazon_reviews"


def default_build_stem(input_path: Path) -> str:
    stem = input_path.stem
    if stem.endswith("_review_rows_machine"):
        return stem.removesuffix("_review_rows_machine") + "_review_workbook"
    if stem.endswith("_review_rows_translated_labeled"):
        return stem.removesuffix("_review_rows_translated_labeled") + "_review_workbook"
    if stem.endswith("_review_rows_translated"):
        return stem.removesuffix("_review_rows_translated") + "_review_workbook"
    if stem.endswith("_review_rows_factual"):
        return stem.removesuffix("_review_rows_factual") + "_review_workbook"
    if stem.endswith("_translated"):
        return stem.removesuffix("_translated") + "_review_workbook"
    if stem.endswith("_labeled"):
        return stem
    return stem + "_review_workbook"


def build_factual_records(payload: dict[str, Any]) -> list[dict[str, Any]]:
    host = str(payload["host"])
    raw_rows = [item for item in payload.get("results", []) if isinstance(item, dict)]
    rows: list[dict[str, Any]] = []
    for index, item in enumerate(raw_rows, start=1):
        clean_title = strip_rating_prefix(str(item.get("title", "")))
        review_text = normalize_space(str(item.get("body", ""))) or clean_title
        rows.append(
            {
                "序号": str(index),
                "评论用户名": normalize_space(str(item.get("author", ""))),
                "国家": infer_country(str(item.get("country_date", "")), host),
                "星级评分": parse_rating(str(item.get("rating_text", ""))),
                "评论原文": review_text,
                "评论中文版": "",
                "评论概括": "",
                "情感倾向": "",
                "类别分类": "",
                "标签": "",
                "重点标记": "",
                "评论链接网址": build_review_link(
                    str(item.get("review_id", "")), host, item.get("review_link")
                ),
                "评论时间": normalize_review_time(
                    item.get("review_time") or item.get("country_date", "")
                ),
                "评论点赞数": normalize_helpful_votes(item.get("helpful_votes", "")),
                "host": host,
                "review_id": str(item.get("review_id", "")),
            }
        )
    return rows


def translate_records(
    records: list[dict[str, Any]],
    *,
    api_url: str,
    api_key: str,
    source_lang: str,
    target_lang: str,
    timeout: int,
    retries: int,
) -> list[dict[str, Any]]:
    texts_to_translate = []
    text_indices = []
    for index, record in enumerate(records):
        source_text = normalize_space(record.get("评论原文"))
        target_text = normalize_space(record.get("评论中文版"))
        if source_text and not target_text:
            texts_to_translate.append(source_text)
            text_indices.append(index)

    if texts_to_translate:
        translated = translate_texts_batch(
            texts_to_translate,
            api_url=api_url,
            api_key=api_key,
            source_lang=source_lang,
            target_lang=target_lang,
            timeout=timeout,
            retries=retries,
            batch_size=50,
        )
        for i, translated_text in enumerate(translated):
            record_index = text_indices[i]
            records[record_index]["评论中文版"] = translated_text
            if (i + 1) % 20 == 0:
                print(f"translate_progress={i + 1}/{len(texts_to_translate)}")

    return records


def command_doctor(args: argparse.Namespace) -> int:
    asin, host = parse_product_url(args.url)
    api_url = args.api_url or read_env_value("DEEPLX_API_URL") or ""
    api_key = args.api_key or read_env_value("DEEPLX_API_KEY") or ""
    deeplx_ready = False
    deeplx_probe = "missing_api_url"
    if api_url:
        deeplx_ready, deeplx_probe = probe_deeplx(api_url, api_key)
    print(
        json.dumps(
            {"asin": asin, "host": host, "review_url": build_review_url(host, asin)},
            ensure_ascii=False,
        )
    )
    print(
        json.dumps(
            {
                "chrome_debug_ready": port_is_open("127.0.0.1", args.cdp_port),
                "cdp_port": args.cdp_port,
            },
            ensure_ascii=False,
        )
    )
    print(
        json.dumps(
            {
                "deeplx_env_ready": bool(api_url),
                "deeplx_api_url_present": bool(api_url),
                "deeplx_reachable": deeplx_ready,
                "deeplx_probe": deeplx_probe,
                "translation_fallback": "model" if not deeplx_ready else "deeplx",
            },
            ensure_ascii=False,
        )
    )
    return 0


def command_coverage_check(args: argparse.Namespace) -> int:
    asin, host = parse_product_url(args.url)
    review_url = build_review_url(host, asin)
    db_path = Path(args.db_path).expanduser()
    cached_count = 0
    searched_keyword_count = 0
    successful_keywords: list[dict[str, Any]] = []
    recent_zero_keywords: list[dict[str, Any]] = []
    if db_path.exists():
        conn = ensure_db(db_path)
        cached_count = get_cached_review_count(conn, host, asin)
        keyword_history = get_keyword_history_map(conn, host, asin)
        searched_keyword_count = len(keyword_history)
        for keyword, entry in keyword_history.items():
            if int(entry.get("best_new_count") or 0) > 0:
                successful_keywords.append(
                    {
                        "keyword": keyword,
                        "best_new_count": int(entry.get("best_new_count") or 0),
                        "search_count": int(entry.get("search_count") or 0),
                    }
                )
            else:
                recent_zero_keywords.append(
                    {
                        "keyword": keyword,
                        "searched_at": entry.get("searched_at", ""),
                    }
                )
        conn.close()
    successful_keywords = sorted(
        successful_keywords,
        key=lambda item: (-item["best_new_count"], item["keyword"]),
    )

    input_count = 0
    if args.input_json:
        input_count = len(load_layered_records(Path(args.input_json).expanduser()))

    chrome_debug_ready = port_is_open("127.0.0.1", args.cdp_port)
    page_probe: dict[str, Any] = {
        "page_total_reviews": None,
        "page_total_reviews_evidence": "",
        "page_total_ratings": None,
        "page_total_ratings_evidence": "",
        "probe_url": review_url,
        "probe_title": "",
        "probe_texts": [],
    }
    if chrome_debug_ready:
        try:
            page_probe = fetch_review_page_totals(review_url, args.cdp_port)
        except Exception as exc:  # noqa: BLE001
            page_probe["probe_error"] = str(exc)

    current_count = input_count or cached_count
    coverage_ratio = None
    if page_probe.get("page_total_reviews"):
        coverage_ratio = round(current_count / page_probe["page_total_reviews"], 3)

    print(
        json.dumps(
            {
                "asin": asin,
                "host": host,
                "review_url": review_url,
                "chrome_debug_ready": chrome_debug_ready,
                "current_count": current_count,
                "current_count_source": "input_json" if input_count else "cache_db",
                "cache_db_count": cached_count,
                "input_json_count": input_count,
                "searched_keyword_count": searched_keyword_count,
                "successful_keyword_count": len(successful_keywords),
                "successful_keywords_top": successful_keywords[:10],
                "recent_zero_keywords_top": recent_zero_keywords[:10],
                "coverage_ratio": coverage_ratio,
                **page_probe,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def command_keyword_autotune(args: argparse.Namespace) -> int:
    output_dir = Path(args.output_dir).expanduser()
    db_path = Path(args.db_path).expanduser()
    output_path = (
        Path(args.keyword_tuning_state).expanduser()
        if args.keyword_tuning_state
        else default_keyword_tuning_state_path(output_dir)
    )
    report_paths: list[Path] = []
    for pattern in args.report_glob or []:
        for matched in glob.glob(pattern):
            report_paths.append(Path(matched).expanduser())
    payload = refresh_keyword_tuning_state(
        db_path=db_path,
        output_path=output_path,
        report_paths=report_paths,
        top_k=args.top_k,
    )
    summary = {
        "keyword_count": payload["metadata"]["keyword_count"],
        "top_k": payload["metadata"]["top_k"],
        "profiles": {
            profile: profile_payload.get("recommended_keywords", [])
            for profile, profile_payload in (payload.get("profiles") or {}).items()
        },
        "output_path": str(output_path),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


def command_collect(args: argparse.Namespace) -> int:
    output_dir = Path(args.output_dir)
    payload = collect_reviews(
        args.url,
        port=args.cdp_port,
        max_pages=args.max_pages,
        resume_from=args.resume_from_page,
        mode=getattr(args, "mode", "deep"),
        db_path=Path(args.db_path)
        if hasattr(args, "db_path") and args.db_path
        else None,
        refresh_cache=getattr(args, "refresh_cache", False),
        keywords=getattr(args, "keywords", None),
        keyword_profile=getattr(args, "keyword_profile", DEFAULT_KEYWORD_PROFILE),
        keyword_reuse_scope=getattr(
            args, "keyword_reuse_scope", DEFAULT_KEYWORD_REUSE_SCOPE
        ),
        zero_result_retry_hours=getattr(
            args, "zero_result_retry_hours", DEFAULT_ZERO_RESULT_RETRY_HOURS
        ),
        keyword_tuning_state_path=Path(args.keyword_tuning_state).expanduser()
        if getattr(args, "keyword_tuning_state", "")
        else default_keyword_tuning_state_path(output_dir),
        combo_delay_seconds=getattr(args, "combo_delay", DEFAULT_COMBO_DELAY_SECONDS),
    )
    raw_json = build_collect_output_path(output_dir, payload["asin"])
    raw_json.parent.mkdir(parents=True, exist_ok=True)
    raw_json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(raw_json)
    print(
        json.dumps(
            {
                "asin": payload["asin"],
                "combo_count": payload.get("combo_count", 1),
                "keyword_count": payload.get("keyword_count", 0),
                "keyword_mode": payload.get("keyword_mode", "off"),
                "keyword_profile": payload.get("keyword_profile", ""),
                "skipped_keywords": payload.get("skipped_keywords", 0),
                "row_count": payload["row_count"],
            },
            ensure_ascii=False,
        )
    )
    return 0


def command_intake(args: argparse.Namespace) -> int:
    output_dir = Path(args.output_dir)
    payload = collect_reviews(
        args.url,
        port=args.cdp_port,
        max_pages=args.max_pages,
        resume_from=args.resume_from_page,
        mode=getattr(args, "mode", "deep"),
        db_path=Path(args.db_path)
        if hasattr(args, "db_path") and args.db_path
        else None,
        refresh_cache=getattr(args, "refresh_cache", False),
        keywords=getattr(args, "keywords", None),
        keyword_profile=getattr(args, "keyword_profile", DEFAULT_KEYWORD_PROFILE),
        keyword_reuse_scope=getattr(
            args, "keyword_reuse_scope", DEFAULT_KEYWORD_REUSE_SCOPE
        ),
        zero_result_retry_hours=getattr(
            args, "zero_result_retry_hours", DEFAULT_ZERO_RESULT_RETRY_HOURS
        ),
        keyword_tuning_state_path=Path(args.keyword_tuning_state).expanduser()
        if getattr(args, "keyword_tuning_state", "")
        else default_keyword_tuning_state_path(output_dir),
        combo_delay_seconds=getattr(args, "combo_delay", DEFAULT_COMBO_DELAY_SECONDS),
    )
    raw_json = build_collect_output_path(output_dir, payload["asin"])
    factual_json, factual_xlsx, factual_csv = build_factual_output_paths(
        output_dir, payload["asin"]
    )
    raw_json.parent.mkdir(parents=True, exist_ok=True)
    raw_json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    factual_records = build_factual_records(payload)
    result = write_delivery_artifacts(
        factual_records, factual_json, factual_xlsx, factual_csv, strict=False
    )
    if result["warnings"]:
        print("warnings=")
        for warning in result["warnings"]:
            print(f"- {warning}")

    print(raw_json)
    print(factual_json)
    print(factual_xlsx)
    print(factual_csv)
    return 0


def command_translate(args: argparse.Namespace) -> int:
    input_json = Path(args.input_json).expanduser()
    records = load_layered_records(input_json)
    asin = infer_asin_from_records(records, input_json)
    output_dir = Path(args.output_dir)
    output_json, output_xlsx, output_csv = build_translated_output_paths(
        output_dir, asin
    )
    translation_mode = "deeplx"
    translated_records = records
    deeplx_failed = False
    try:
        api_url = resolve_api_url(args.api_url)
        api_key = resolve_api_key(args.api_key)
        deeplx_ready, deeplx_probe = probe_deeplx(
            api_url, api_key, timeout=min(args.timeout, 12)
        )
        if not deeplx_ready:
            translation_mode = "model_fallback"
            deeplx_failed = True
            print(
                json.dumps(
                    {"translation_mode": translation_mode, "reason": deeplx_probe},
                    ensure_ascii=False,
                )
            )
        else:
            translated_records = translate_records(
                records,
                api_url=api_url,
                api_key=api_key,
                source_lang=args.source_lang,
                target_lang=args.target_lang,
                timeout=args.timeout,
                retries=args.retries,
            )
    except SystemExit as exc:
        translation_mode = "model_fallback"
        deeplx_failed = True
        reason = str(exc) if exc else "missing_deeplx_config"
        print(
            json.dumps(
                {"translation_mode": translation_mode, "reason": reason},
                ensure_ascii=False,
            )
        )

    if deeplx_failed:
        # Output pending translation list for AI to translate
        pending_texts = []
        for index, record in enumerate(translated_records):
            source = normalize_space(record.get("评论原文"))
            target = normalize_space(record.get("评论中文版"))
            if source and not target:
                pending_texts.append({"index": index + 1, "text": source})

        if pending_texts:
            pending_file = output_dir / f"amazon_{asin}_pending_translation.json"
            pending_file.parent.mkdir(parents=True, exist_ok=True)
            pending_file.write_text(
                json.dumps(pending_texts, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            print(f"\nDeepLX 不可用，{len(pending_texts)} 条评论待翻译。")
            print(f"待翻译清单已保存：{pending_file}")
            print("请把待翻译文本发给 AI（Sen），由 AI 翻译后填回。")
            for record in translated_records:
                source = normalize_space(record.get("评论原文", ""))
                target = normalize_space(record.get("评论中文版", ""))
                if source and not target:
                    record["评论中文版"] = "[待翻译]"

    result = write_delivery_artifacts(
        translated_records, output_json, output_xlsx, output_csv, strict=False
    )
    if result["warnings"]:
        print("warnings=")
        for warning in result["warnings"]:
            print(f"- {warning}")
    print(json.dumps({"translation_mode": translation_mode}, ensure_ascii=False))
    print(output_json)
    print(output_xlsx)
    print(output_csv)
    return 0


def command_build(args: argparse.Namespace) -> int:
    input_json = Path(args.input_json).expanduser()
    records = load_json_records(input_json)
    output_dir = Path(args.output_dir)
    stem = args.output_stem or default_build_stem(input_json)
    output_json, output_xlsx, output_csv = build_final_output_paths(output_dir, stem)
    result = write_delivery_artifacts(
        records, output_json, output_xlsx, output_csv, strict=args.strict
    )
    if result["warnings"]:
        print("warnings=")
        for warning in result["warnings"]:
            print(f"- {warning}")
    print(output_json)
    print(output_xlsx)
    print(output_csv)
    return 0


def command_prepare_tagging(args: argparse.Namespace) -> int:
    input_json = Path(args.input_json).expanduser()
    records = load_layered_records(input_json)
    asin = infer_asin_from_records(records, input_json)
    output_dir = Path(args.output_dir)
    output_path = build_prepare_output_path(output_dir, asin)
    canonical_tags = (
        load_canonical_tags(Path(args.canonical_tags_json).expanduser())
        if args.canonical_tags_json
        else []
    )
    cache_path = (
        Path(args.cache_file).expanduser()
        if args.cache_file
        else default_cache_path(output_dir)
    )
    cache_entries = load_cache(cache_path, ttl_hours=args.cache_ttl_hours)
    payload = prepare_tagging_payload(
        records,
        taxonomy_version=args.taxonomy_version,
        cache_entries=cache_entries,
        canonical_tags=canonical_tags,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(output_path)
    print(json.dumps(payload["metadata"], ensure_ascii=False))
    return 0


def command_taxonomy_bootstrap(args: argparse.Namespace) -> int:
    input_json = Path(args.input_json).expanduser()
    records = load_layered_records(input_json)
    asin = infer_asin_from_records(records, input_json)
    output_dir = Path(args.output_dir)
    output_path = build_bootstrap_output_path(output_dir, asin)
    payload = build_taxonomy_bootstrap(
        records,
        taxonomy_version=args.taxonomy_version,
        sample_size=args.sample_size,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(output_path)
    print(json.dumps(payload["metadata"], ensure_ascii=False))
    return 0


def command_merge_build(args: argparse.Namespace) -> int:
    base_json = Path(args.base_json).expanduser()
    labels_json = Path(args.labels_json).expanduser()
    base_records = load_layered_records(base_json)
    labels_payload = json.loads(labels_json.read_text(encoding="utf-8"))
    output_dir = Path(args.output_dir)
    cache_path = (
        Path(args.cache_file).expanduser()
        if args.cache_file
        else default_cache_path(output_dir)
    )
    cache_entries = load_cache(cache_path, ttl_hours=args.cache_ttl_hours)
    merged_records, updated_cache, stats = merge_records_with_labels(
        base_records,
        labels_payload=labels_payload,
        taxonomy_version=args.taxonomy_version,
        cache_entries=cache_entries,
    )
    save_cache(cache_path, updated_cache)
    stem = args.output_stem or default_build_stem(base_json)
    output_json, output_xlsx, output_csv = build_final_output_paths(output_dir, stem)
    result = write_delivery_artifacts(
        merged_records, output_json, output_xlsx, output_csv, strict=args.strict
    )
    if result["warnings"]:
        print("warnings=")
        for warning in result["warnings"]:
            print(f"- {warning}")
    print(json.dumps({"cache_file": str(cache_path), **stats}, ensure_ascii=False))
    print(output_json)
    print(output_xlsx)
    print(output_csv)
    return 0


def print_summary(
    records: list[dict[str, Any]],
    *,
    asin: str = "",
    translation_ok: int = 0,
    cache_hits: int = 0,
    cache_total: int = 0,
) -> None:
    total = len(records)
    rating_counter: dict[str, int] = {}
    sentiment_counter: dict[str, int] = {}
    category_counter: dict[str, int] = {}
    for record in records:
        rating = normalize_space(record.get("星级评分"))
        if rating:
            rating_counter[rating] = rating_counter.get(rating, 0) + 1
        sentiment = normalize_space(record.get("情感倾向"))
        if sentiment:
            sentiment_counter[sentiment] = sentiment_counter.get(sentiment, 0) + 1
        category = normalize_space(record.get("类别分类"))
        if category:
            for cat in category.split(" / "):
                cat = cat.strip()
                if cat:
                    category_counter[cat] = category_counter.get(cat, 0) + 1

    summary = {
        "asin": asin,
        "total_reviews": total,
        "rating_distribution": dict(
            sorted(rating_counter.items(), key=lambda x: x[0], reverse=True)
        ),
        "sentiment_distribution": sentiment_counter,
        "category_distribution": dict(
            sorted(category_counter.items(), key=lambda x: x[1], reverse=True)
        ),
        "translation_filled": translation_ok,
        "cache_stats": {
            "hits": cache_hits,
            "total": cache_total,
            "hit_rate": round(cache_hits / cache_total, 2) if cache_total else 0,
        },
    }
    print(json.dumps({"summary": summary}, ensure_ascii=False, indent=2))


def command_batch_intake(args: argparse.Namespace) -> int:
    url_file = Path(args.url_file).expanduser()
    if not url_file.exists():
        raise SystemExit(f"URL 文件不存在: {url_file}")

    urls = [
        line.strip()
        for line in url_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]
    if not urls:
        raise SystemExit("URL 文件为空")

    output_dir = Path(args.output_dir)
    results: list[dict[str, Any]] = []
    for idx, url in enumerate(urls, start=1):
        print(f"[{idx}/{len(urls)}] processing: {url}")
        try:
            payload = collect_reviews(
                url,
                port=args.cdp_port,
                max_pages=args.max_pages,
                mode=getattr(args, "mode", "deep"),
                db_path=Path(args.db_path)
                if hasattr(args, "db_path") and args.db_path
                else None,
                refresh_cache=getattr(args, "refresh_cache", False),
                keywords=getattr(args, "keywords", None),
                keyword_profile=getattr(
                    args, "keyword_profile", DEFAULT_KEYWORD_PROFILE
                ),
                keyword_reuse_scope=getattr(
                    args, "keyword_reuse_scope", DEFAULT_KEYWORD_REUSE_SCOPE
                ),
                zero_result_retry_hours=getattr(
                    args,
                    "zero_result_retry_hours",
                    DEFAULT_ZERO_RESULT_RETRY_HOURS,
                ),
                keyword_tuning_state_path=Path(args.keyword_tuning_state).expanduser()
                if getattr(args, "keyword_tuning_state", "")
                else default_keyword_tuning_state_path(output_dir),
                combo_delay_seconds=getattr(
                    args, "combo_delay", DEFAULT_COMBO_DELAY_SECONDS
                ),
            )
            raw_json = build_collect_output_path(output_dir, payload["asin"])
            factual_json, factual_xlsx, factual_csv = build_factual_output_paths(
                output_dir, payload["asin"]
            )
            raw_json.parent.mkdir(parents=True, exist_ok=True)
            raw_json.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            factual_records = build_factual_records(payload)
            result = write_delivery_artifacts(
                factual_records, factual_json, factual_xlsx, factual_csv, strict=False
            )
            results.append(
                {
                    "url": url,
                    "asin": payload["asin"],
                    "rows": payload["row_count"],
                    "status": "ok",
                }
            )
        except Exception as exc:  # noqa: BLE001
            results.append(
                {
                    "url": url,
                    "asin": "",
                    "rows": 0,
                    "status": "error",
                    "error": str(exc),
                }
            )

    summary_path = output_dir / "batch_intake_summary.json"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(
            {"total_urls": len(urls), "results": results}, ensure_ascii=False, indent=2
        ),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "batch_summary": {
                    "total_urls": len(urls),
                    "success": sum(1 for r in results if r["status"] == "ok"),
                    "failed": sum(1 for r in results if r["status"] == "error"),
                }
            },
            ensure_ascii=False,
        )
    )
    print(summary_path)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Collect Amazon reviews via Chrome CDP and export a 14-column workbook."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser(
        "doctor", help="Check URL parsing and Chrome debug availability."
    )
    doctor.add_argument("--url", required=True)
    doctor.add_argument("--cdp-port", type=int, default=DEFAULT_CDP_PORT)
    doctor.add_argument("--api-url", help="Optional DeepLX API URL override.")
    doctor.add_argument("--api-key", help="Optional DeepLX API key override.")

    coverage = subparsers.add_parser(
        "coverage-check",
        help="Compare current cached/input rows against Amazon's visible review totals.",
    )
    coverage.add_argument("--url", required=True)
    coverage.add_argument("--db-path", default=str(DEFAULT_DB_PATH))
    coverage.add_argument("--input-json")
    coverage.add_argument("--cdp-port", type=int, default=DEFAULT_CDP_PORT)

    autotune = subparsers.add_parser(
        "keyword-autotune",
        help="Aggregate historical keyword hit data and build a tuned keyword state file.",
    )
    autotune.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    autotune.add_argument("--db-path", default=str(DEFAULT_DB_PATH))
    autotune.add_argument(
        "--report-glob",
        nargs="*",
        default=[],
        help="Optional glob patterns for historical keyword result JSON files.",
    )
    autotune.add_argument(
        "--keyword-tuning-state",
        help="Optional output path for the tuned keyword state JSON.",
    )
    autotune.add_argument(
        "--top-k",
        type=int,
        default=DEFAULT_KEYWORD_TUNING_TOP_K,
        help="How many recommended keywords to keep per profile. Default: 12",
    )

    collect = subparsers.add_parser(
        "collect", help="Collect all paginated reviews into raw JSON."
    )
    collect.add_argument("--url", required=True)
    collect.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    collect.add_argument("--max-pages", type=int, default=DEFAULT_MAX_PAGES)
    collect.add_argument("--cdp-port", type=int, default=DEFAULT_CDP_PORT)
    collect.add_argument(
        "--resume-from-page",
        type=int,
        default=0,
        help="Skip pages already collected (1-based).",
    )
    collect.add_argument(
        "--mode",
        choices=["fast", "deep"],
        default="deep",
        help="fast=2 combos (~200 reviews), deep=18 combos only. Keywords are manual via --keywords.",
    )
    collect.add_argument(
        "--refresh-cache",
        action="store_true",
        help="Force re-collection even if cache exists.",
    )
    collect.add_argument(
        "--db-path",
        default=str(DEFAULT_DB_PATH),
        help="Path to SQLite cache file.",
    )
    collect.add_argument(
        "--keywords",
        nargs="*",
        help="Manual keyword pass. Omit the flag to skip keywords; pass --keywords with no values to use the default high-yield preset; or provide an explicit list.",
    )
    collect.add_argument(
        "--keyword-profile",
        choices=sorted(KEYWORD_PROFILES.keys()),
        default=DEFAULT_KEYWORD_PROFILE,
        help="Built-in keyword preset profile used when --keywords has no explicit values.",
    )
    collect.add_argument(
        "--keyword-reuse-scope",
        choices=["successful", "all", "none"],
        default=DEFAULT_KEYWORD_REUSE_SCOPE,
        help="successful=skip keywords that have produced results before; all=skip every previously searched keyword; none=always rerun keywords.",
    )
    collect.add_argument(
        "--zero-result-retry-hours",
        type=float,
        default=DEFAULT_ZERO_RESULT_RETRY_HOURS,
        help="How long to suppress recently searched zero-result keywords. Default: 72",
    )
    collect.add_argument(
        "--keyword-tuning-state",
        help="Optional tuned keyword state JSON. Defaults to <output-dir>/keyword_tuning_state.json if present.",
    )
    collect.add_argument(
        "--combo-delay",
        type=float,
        default=DEFAULT_COMBO_DELAY_SECONDS,
        help="Delay in seconds between combo or keyword requests. Default: 2.5",
    )

    intake = subparsers.add_parser(
        "intake",
        help="Collect reviews and export a factual workbook with analysis columns left blank.",
    )
    intake.add_argument("--url", required=True)
    intake.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    intake.add_argument("--max-pages", type=int, default=DEFAULT_MAX_PAGES)
    intake.add_argument("--cdp-port", type=int, default=DEFAULT_CDP_PORT)
    intake.add_argument(
        "--resume-from-page",
        type=int,
        default=0,
        help="Skip pages already collected (1-based).",
    )
    intake.add_argument(
        "--mode",
        choices=["fast", "deep"],
        default="deep",
        help="fast=2 combos (~200 reviews), deep=18 combos only. Keywords are manual via --keywords.",
    )
    intake.add_argument(
        "--refresh-cache",
        action="store_true",
        help="Force re-collection even if cache exists.",
    )
    intake.add_argument(
        "--db-path",
        default=str(DEFAULT_DB_PATH),
        help="Path to SQLite cache file.",
    )
    intake.add_argument(
        "--keywords",
        nargs="*",
        help="Manual keyword pass. Omit the flag to skip keywords; pass --keywords with no values to use the default high-yield preset; or provide an explicit list.",
    )
    intake.add_argument(
        "--keyword-profile",
        choices=sorted(KEYWORD_PROFILES.keys()),
        default=DEFAULT_KEYWORD_PROFILE,
        help="Built-in keyword preset profile used when --keywords has no explicit values.",
    )
    intake.add_argument(
        "--keyword-reuse-scope",
        choices=["successful", "all", "none"],
        default=DEFAULT_KEYWORD_REUSE_SCOPE,
        help="successful=skip keywords that have produced results before; all=skip every previously searched keyword; none=always rerun keywords.",
    )
    intake.add_argument(
        "--zero-result-retry-hours",
        type=float,
        default=DEFAULT_ZERO_RESULT_RETRY_HOURS,
        help="How long to suppress recently searched zero-result keywords. Default: 72",
    )
    intake.add_argument(
        "--keyword-tuning-state",
        help="Optional tuned keyword state JSON. Defaults to <output-dir>/keyword_tuning_state.json if present.",
    )
    intake.add_argument(
        "--combo-delay",
        type=float,
        default=DEFAULT_COMBO_DELAY_SECONDS,
        help="Delay in seconds between combo or keyword requests. Default: 2.5",
    )

    translate = subparsers.add_parser(
        "translate",
        help="Fill 评论中文版 via DeepLX while preserving other factual columns.",
    )
    translate.add_argument("--input-json", required=True)
    translate.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    translate.add_argument(
        "--api-url", help="DeepLX translate endpoint. Defaults to DEEPLX_API_URL env."
    )
    translate.add_argument(
        "--api-key", help="Optional DeepLX API key. Defaults to DEEPLX_API_KEY env."
    )
    translate.add_argument("--source-lang", default="auto")
    translate.add_argument("--target-lang", default="ZH")
    translate.add_argument("--timeout", type=int, default=30)
    translate.add_argument("--retries", type=int, default=3)

    build = subparsers.add_parser(
        "build",
        help="Build the final workbook from a JSON file that already contains labeled rows.",
    )
    build.add_argument("--input-json", required=True)
    build.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    build.add_argument(
        "--output-stem", help="Optional custom file stem without extension."
    )
    build.add_argument(
        "--strict",
        action="store_true",
        help="Fail when required analysis fields are still missing.",
    )

    prepare = subparsers.add_parser(
        "prepare-tagging",
        help="Create a lightweight tagging JSON with cache-aware pending rows.",
    )
    prepare.add_argument("--input-json", required=True)
    prepare.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    prepare.add_argument("--taxonomy-version", default="v1")
    prepare.add_argument("--cache-file", help="Optional label cache file path.")
    prepare.add_argument(
        "--cache-ttl-hours",
        type=float,
        default=0,
        help="Skip cache entries older than this many hours (0 = no expiry).",
    )
    prepare.add_argument(
        "--canonical-tags-json", help="Optional canonical tags JSON file."
    )

    bootstrap = subparsers.add_parser(
        "taxonomy-bootstrap",
        help="Create representative sample rows for canonical tag design.",
    )
    bootstrap.add_argument("--input-json", required=True)
    bootstrap.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    bootstrap.add_argument("--taxonomy-version", default="v1")
    bootstrap.add_argument("--sample-size", type=int, default=30)

    merge_build = subparsers.add_parser(
        "merge-build",
        help="Merge factual/translated rows with labeled rows, update cache, and build final workbook.",
    )
    merge_build.add_argument("--base-json", required=True)
    merge_build.add_argument("--labels-json", required=True)
    merge_build.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    merge_build.add_argument(
        "--output-stem", help="Optional custom file stem without extension."
    )
    merge_build.add_argument("--taxonomy-version", default="v1")
    merge_build.add_argument("--cache-file", help="Optional label cache file path.")
    merge_build.add_argument(
        "--cache-ttl-hours",
        type=float,
        default=0,
        help="Skip cache entries older than this many hours (0 = no expiry).",
    )
    merge_build.add_argument(
        "--strict",
        action="store_true",
        help="Fail when required analysis fields are still missing.",
    )

    batch = subparsers.add_parser(
        "batch-intake", help="Collect reviews from multiple URLs listed in a file."
    )
    batch.add_argument(
        "--url-file",
        required=True,
        help="Path to a text file with one Amazon URL per line.",
    )
    batch.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    batch.add_argument("--max-pages", type=int, default=DEFAULT_MAX_PAGES)
    batch.add_argument("--cdp-port", type=int, default=DEFAULT_CDP_PORT)
    batch.add_argument(
        "--mode",
        choices=["fast", "deep"],
        default="deep",
        help="fast=2 combos (~200 reviews), deep=18 combos only. Keywords are manual via --keywords.",
    )
    batch.add_argument(
        "--db-path",
        default=str(DEFAULT_DB_PATH),
        help="Path to SQLite cache file.",
    )
    batch.add_argument(
        "--refresh-cache",
        action="store_true",
        help="Force re-collection even if cache exists.",
    )
    batch.add_argument(
        "--keywords",
        nargs="*",
        help="Manual keyword pass. Omit the flag to skip keywords; pass --keywords with no values to use the default high-yield preset; or provide an explicit list.",
    )
    batch.add_argument(
        "--keyword-profile",
        choices=sorted(KEYWORD_PROFILES.keys()),
        default=DEFAULT_KEYWORD_PROFILE,
        help="Built-in keyword preset profile used when --keywords has no explicit values.",
    )
    batch.add_argument(
        "--keyword-reuse-scope",
        choices=["successful", "all", "none"],
        default=DEFAULT_KEYWORD_REUSE_SCOPE,
        help="successful=skip keywords that have produced results before; all=skip every previously searched keyword; none=always rerun keywords.",
    )
    batch.add_argument(
        "--zero-result-retry-hours",
        type=float,
        default=DEFAULT_ZERO_RESULT_RETRY_HOURS,
        help="How long to suppress recently searched zero-result keywords. Default: 72",
    )
    batch.add_argument(
        "--keyword-tuning-state",
        help="Optional tuned keyword state JSON. Defaults to <output-dir>/keyword_tuning_state.json if present.",
    )
    batch.add_argument(
        "--combo-delay",
        type=float,
        default=DEFAULT_COMBO_DELAY_SECONDS,
        help="Delay in seconds between combo or keyword requests. Default: 2.5",
    )

    summary = subparsers.add_parser(
        "summary", help="Print a structured summary from an existing workbook JSON."
    )
    summary.add_argument("--input-json", required=True)
    summary.add_argument(
        "--cache-file", help="Optional label cache file for hit-rate stats."
    )

    return parser


def main() -> int:
    configure_stdio()
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "doctor":
        return command_doctor(args)
    if args.command == "coverage-check":
        return command_coverage_check(args)
    if args.command == "keyword-autotune":
        return command_keyword_autotune(args)
    if args.command == "collect":
        return command_collect(args)
    if args.command == "intake":
        return command_intake(args)
    if args.command == "translate":
        return command_translate(args)
    if args.command == "build":
        return command_build(args)
    if args.command == "prepare-tagging":
        return command_prepare_tagging(args)
    if args.command == "taxonomy-bootstrap":
        return command_taxonomy_bootstrap(args)
    if args.command == "merge-build":
        return command_merge_build(args)
    if args.command == "batch-intake":
        return command_batch_intake(args)
    if args.command == "summary":
        input_json = Path(args.input_json).expanduser()
        records = load_layered_records(input_json)
        asin = infer_asin_from_records(records, input_json)
        cache_hits = 0
        cache_total = 0
        if args.cache_file:
            cache_entries = load_cache(Path(args.cache_file).expanduser())
            cache_total = len(cache_entries)
            cache_hits = sum(1 for v in cache_entries.values() if v.get("fields"))
        print_summary(
            records, asin=asin, cache_hits=cache_hits, cache_total=cache_total
        )
        return 0
    raise SystemExit(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
