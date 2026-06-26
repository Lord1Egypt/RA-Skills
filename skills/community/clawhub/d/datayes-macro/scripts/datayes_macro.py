#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit, urlunsplit
from urllib.request import Request, urlopen


API_INFO_URL = "https://gw.datayes.com/aladdin_llm_mgmt/web/mgr/api"
DEFAULT_TIMEOUT = 30
ALLOWED_HTTP_HOSTS = {
    "api.datayes.com",
    "api.wmcloud.com",
    "gw.datayes.com",
    "r.datayes.com",
}


class DatayesError(RuntimeError):
    pass


def get_token() -> str:
    token = os.environ.get("DATAYES_TOKEN", "").strip()
    if not token:
        raise DatayesError("Missing DATAYES_TOKEN environment variable.")
    return token


def clean_api_url(url: str) -> str:
    parts = urlsplit(url)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


def validate_http_url(url: str) -> str:
    parts = urlsplit(url)
    if parts.scheme != "https":
        raise DatayesError(f"Resolved httpUrl must use https: {url}")
    if not parts.netloc:
        raise DatayesError(f"Resolved httpUrl is missing a host: {url}")
    host = (parts.hostname or "").lower()
    if host not in ALLOWED_HTTP_HOSTS:
        allowed_hosts = ", ".join(sorted(ALLOWED_HTTP_HOSTS))
        raise DatayesError(
            f"Resolved httpUrl host {host or '<unknown>'} is not trusted. Allowed hosts: {allowed_hosts}"
        )
    return url


def request_json(url: str, params: dict[str, Any] | None = None) -> Any:
    if params:
        query = urlencode({key: value for key, value in params.items() if value is not None})
        url = f"{url}?{query}"

    req = Request(
        url,
        headers={
            "Authorization": f"Bearer {get_token()}",
            "Accept": "application/json",
            "User-Agent": "datayes-macro-skill/1.0",
        },
    )

    try:
        with urlopen(req, timeout=DEFAULT_TIMEOUT) as resp:
            return json.load(resp)
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise DatayesError(f"HTTP {exc.code} for {url}: {body}") from exc
    except URLError as exc:
        raise DatayesError(f"Request failed for {url}: {exc}") from exc


@lru_cache(maxsize=None)
def get_api_spec(name_en: str) -> dict[str, Any]:
    payload = request_json(API_INFO_URL, {"nameEn": name_en})
    data = payload.get("data")
    if not data:
        raise DatayesError(f"Unable to load API spec for {name_en}: {json.dumps(payload, ensure_ascii=False)}")
    return data


def get_api_url(name_en: str) -> str:
    return clean_api_url(validate_http_url(get_api_spec(name_en)["httpUrl"]))


def normalize_text(text: str | None) -> str:
    if not text:
        return ""
    text = text.lower()
    text = (
        text.replace("（", "(")
        .replace("）", ")")
        .replace("：", ":")
        .replace("，", ",")
        .replace("•", " ")
        .replace("·", " ")
    )
    text = re.sub(r"([0-9a-z])([\u4e00-\u9fff])", r"\1 \2", text)
    text = re.sub(r"([\u4e00-\u9fff])([0-9a-z])", r"\1 \2", text)
    text = re.sub(r"[^0-9a-z\u4e00-\u9fff:%]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def extract_tokens(text: str) -> list[str]:
    normalized = normalize_text(text)
    tokens: list[str] = []
    for token in re.findall(r"[0-9a-z]+|[\u4e00-\u9fff]+", normalized.replace(":", " ")):
        if len(token) >= 2:
            tokens.append(token)
    for chunk in re.findall(r"[\u4e00-\u9fff]{2,}", normalized):
        if len(chunk) <= 6:
            tokens.append(chunk)
        else:
            tokens.append(chunk)
            tokens.extend(chunk[idx : idx + 2] for idx in range(len(chunk) - 1))
    seen: set[str] = set()
    unique: list[str] = []
    for token in tokens:
        if token not in seen:
            seen.add(token)
            unique.append(token)
    return unique


def detect_frequency_hint(query: str, explicit: str | None) -> str | None:
    if explicit:
        return explicit.upper()

    patterns = {
        "D": ("日频", "日度", "每日", "按日", "日"),
        "W": ("周频", "周度", "每周", "按周", "周"),
        "M": ("月频", "月度", "每月", "按月", "月"),
        "Q": ("季频", "季度", "按季", "季"),
        "A": ("年频", "年度", "每年", "按年", "年"),
    }
    for code, keys in patterns.items():
        if any(key in query for key in keys):
            return code
    return None


def build_fallback_queries(keyword: str) -> list[str]:
    variants = [keyword.strip()]
    compact = re.sub(r"\s+", "", keyword)
    if compact and compact not in variants:
        variants.append(compact)

    simplified = compact
    for marker in ("中国", "全国", "同比", "环比", "累计", "累计同比", "当月", "当季", "当年"):
        simplified = simplified.replace(marker, "")
    if len(simplified) >= 2 and simplified not in variants:
        variants.append(simplified)

    return variants[:3]


def merge_candidates(v4_payload: dict[str, Any], default_payload: dict[str, Any], keyword: str) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}

    def upsert(raw: dict[str, Any], source_mode: str, rank: int) -> None:
        indicator_id = str(raw.get("id", "")).strip()
        if not indicator_id:
            return

        candidate = merged.setdefault(
            indicator_id,
            {
                "id": indicator_id,
                "name": raw.get("name", ""),
                "frequency": raw.get("frequency", ""),
                "frequency_code": raw.get("frequencyCode", ""),
                "unit": raw.get("unit", ""),
                "source": raw.get("infoSource", ""),
                "statistic": raw.get("statistic", ""),
                "matched_by": [],
                "keyword": keyword,
                "best_default_rank": None,
                "best_v4_rank": None,
            },
        )

        for field, raw_key in (
            ("name", "name"),
            ("frequency", "frequency"),
            ("frequency_code", "frequencyCode"),
            ("unit", "unit"),
            ("source", "infoSource"),
            ("statistic", "statistic"),
        ):
            if not candidate[field] and raw.get(raw_key):
                candidate[field] = raw.get(raw_key)

        if source_mode not in candidate["matched_by"]:
            candidate["matched_by"].append(source_mode)

        rank_key = "best_default_rank" if source_mode == "default" else "best_v4_rank"
        best_rank = candidate[rank_key]
        if best_rank is None or rank < best_rank:
            candidate[rank_key] = rank

    v4_rank = 0
    for item in v4_payload.get("data", {}).get("dataitems", []):
        for indicator in item.get("indicators", []):
            v4_rank += 1
            upsert(indicator, "version=4", v4_rank)

    default_rank = 0
    for indicator in default_payload.get("data", {}).get("param1", {}).get("suggestQuery", []):
        default_rank += 1
        upsert(indicator, "default", default_rank)

    return list(merged.values())


def score_candidate(candidate: dict[str, Any], query: str, frequency_hint: str | None) -> float:
    name = normalize_text(candidate.get("name"))
    statistic = normalize_text(candidate.get("statistic"))
    source = normalize_text(candidate.get("source"))
    query_norm = normalize_text(query)
    query_compact = query_norm.replace(" ", "")
    name_compact = name.replace(" ", "").replace(":", "")
    tokens = extract_tokens(query)
    score = 0.0

    if query_norm == name:
        score += 200
    if query_norm and query_norm in name:
        score += 120
    if name and name in query_norm:
        score += 60
    if query_compact and query_compact in name_compact:
        score += 40

    for token in tokens:
        if token in name:
            score += min(30, 8 + len(token) * 2)
        if token in statistic:
            score += 6

    if "同比" in query:
        if "同比" in name:
            score += 45
        elif "同比" in statistic:
            score += 20
    if "环比" in query:
        if "环比" in name:
            score += 45
        elif "环比" in statistic:
            score += 20
    if "累计" in query and "累计" in name:
        score += 30

    if "中国" in query or "全国" in query:
        if "中国" in name or "全国" in name:
            score += 12
    elif "中国" in name or "全国" in name:
        score += 6

    if frequency_hint and candidate.get("frequency_code", "").upper() == frequency_hint:
        score += 18

    default_rank = candidate.get("best_default_rank")
    if default_rank:
        score += max(0, 32 - default_rank * 3)
    v4_rank = candidate.get("best_v4_rank")
    if v4_rank:
        score += max(0, 14 - v4_rank)

    raw_name = candidate.get("name", "")
    if not any(marker in query for marker in ("香港", "澳门", "台湾")) and any(
        marker in raw_name for marker in ("香港", "澳门", "台湾")
    ):
        score -= 22

    if "datayes" in source:
        score += 1

    score -= len(candidate.get("name", "")) / 100
    return round(score, 2)


def search_once(keyword: str, size: int, offset: int) -> list[dict[str, Any]]:
    base_url = get_api_url("data_search")
    common = {"input": keyword, "size": size, "offset": offset}

    with ThreadPoolExecutor(max_workers=2) as executor:
        future_v4 = executor.submit(request_json, base_url, {**common, "version": 4})
        future_default = executor.submit(request_json, base_url, common)
        v4_payload = future_v4.result()
        default_payload = future_default.result()

    return merge_candidates(v4_payload, default_payload, keyword)


def search_indicators(keyword: str, size: int, offset: int, frequency_hint: str | None) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}

    for variant in build_fallback_queries(keyword):
        for candidate in search_once(variant, size, offset):
            existing = merged.get(candidate["id"])
            if not existing:
                merged[candidate["id"]] = candidate
                continue

            existing["matched_by"] = sorted(set(existing["matched_by"] + candidate["matched_by"]))
            if len(candidate["keyword"]) < len(existing["keyword"]):
                existing["keyword"] = candidate["keyword"]

    ranked = list(merged.values())
    for candidate in ranked:
        candidate["score"] = score_candidate(candidate, keyword, frequency_hint)

    ranked.sort(key=lambda item: (-item["score"], item["name"]))
    return ranked


def fetch_details(ids: list[str], begin_date: str | None, end_date: str | None) -> list[dict[str, Any]]:
    if not ids:
        return []

    params = {"ids": ",".join(ids)}
    if begin_date:
        params["beginDate"] = begin_date
    if end_date:
        params["endDate"] = end_date

    payload = request_json(get_api_url("Indicsdetail"), params)
    data = payload.get("data")
    if data is None:
        raise DatayesError(f"Unexpected detail response: {json.dumps(payload, ensure_ascii=False)}")
    return data


def validate_yyyymmdd(value: str | None) -> str | None:
    if value is None:
        return None
    if not re.fullmatch(r"\d{8}", value):
        raise DatayesError(f"Invalid date {value!r}; expected yyyymmdd.")
    return value


def to_search_output(candidates: list[dict[str, Any]], top: int) -> dict[str, Any]:
    return {"count": len(candidates), "candidates": candidates[:top]}


def to_query_output(
    keyword: str,
    candidates: list[dict[str, Any]],
    details: list[dict[str, Any]],
    top: int,
) -> dict[str, Any]:
    selected_ids = {item.get("indicId") or item.get("indic", {}).get("indicID") for item in details}
    return {
        "query": keyword,
        "candidates": candidates[:top],
        "selected": [item for item in candidates[:top] if item["id"] in selected_ids],
        "series": details,
    }


def format_search_text(candidates: list[dict[str, Any]], top: int) -> str:
    lines = []
    for index, item in enumerate(candidates[:top], start=1):
        lines.append(
            f"{index}. [{item['id']}] {item['name']} | score={item['score']} | "
            f"freq={item.get('frequency') or '-'} | unit={item.get('unit') or '-'} | "
            f"source={item.get('source') or '-'} | via={','.join(item.get('matched_by', []))}"
        )
    return "\n".join(lines) if lines else "No candidates found."


def format_detail_text(items: list[dict[str, Any]], limit: int) -> str:
    if not items:
        return "No series returned."

    blocks = []
    for item in items:
        meta = item.get("indic", {})
        header = (
            f"[{meta.get('indicName', '-')}] id={meta.get('indicID', '-')} "
            f"freq={meta.get('frequency', '-')} unit={meta.get('unit', '-')} "
            f"source={meta.get('infoSource', '-')}"
        )
        latest = f"latest: {meta.get('dataValue', '-')} ({meta.get('periodDate', '-')})"
        rows = sorted(item.get("data", []), key=lambda row: row.get("periodDate", ""), reverse=True)[:limit]
        row_lines = [f"{row.get('periodDate', '-'):<12} {row.get('dataValue', '-')}" for row in rows]
        blocks.append("\n".join([header, latest, "series:", *row_lines]))
    return "\n\n".join(blocks)


def print_output(payload: Any, as_json: bool) -> None:
    if as_json:
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return

    if isinstance(payload, str):
        sys.stdout.write(payload)
        sys.stdout.write("\n")
        return

    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Query Datayes macro indicators with Python stdlib only.")
    parser.add_argument("--json", action="store_true", help="Print JSON output.")

    subparsers = parser.add_subparsers(dest="command", required=True)

    spec_parser = subparsers.add_parser("spec", help="Show API spec.")
    spec_parser.add_argument("name_en", choices=["data_search", "Indicsdetail"])

    search_parser = subparsers.add_parser("search", help="Search indicator candidates.")
    search_parser.add_argument("keyword")
    search_parser.add_argument("--size", type=int, default=20)
    search_parser.add_argument("--offset", type=int, default=0)
    search_parser.add_argument("--top", type=int, default=10)
    search_parser.add_argument("--frequency")

    detail_parser = subparsers.add_parser("detail", help="Fetch indicator series by id.")
    detail_parser.add_argument("ids", nargs="+")
    detail_parser.add_argument("--begin-date")
    detail_parser.add_argument("--end-date")
    detail_parser.add_argument("--limit", type=int, default=12)

    query_parser = subparsers.add_parser("query", help="Search, rank, and fetch series in one step.")
    query_parser.add_argument("keyword")
    query_parser.add_argument("--size", type=int, default=20)
    query_parser.add_argument("--offset", type=int, default=0)
    query_parser.add_argument("--top", type=int, default=3)
    query_parser.add_argument("--pick", type=int, default=1)
    query_parser.add_argument("--begin-date")
    query_parser.add_argument("--end-date")
    query_parser.add_argument("--limit", type=int, default=12)
    query_parser.add_argument("--frequency")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "spec":
            print_output(get_api_spec(args.name_en), args.json)
            return 0

        if args.command == "search":
            frequency_hint = detect_frequency_hint(args.keyword, args.frequency)
            candidates = search_indicators(args.keyword, args.size, args.offset, frequency_hint)
            payload = to_search_output(candidates, args.top)
            print_output(payload if args.json else format_search_text(candidates, args.top), args.json)
            return 0

        if args.command == "detail":
            begin_date = validate_yyyymmdd(args.begin_date)
            end_date = validate_yyyymmdd(args.end_date)
            details = fetch_details([str(item) for item in args.ids], begin_date, end_date)
            print_output(details if args.json else format_detail_text(details, args.limit), args.json)
            return 0

        if args.command == "query":
            begin_date = validate_yyyymmdd(args.begin_date)
            end_date = validate_yyyymmdd(args.end_date)
            frequency_hint = detect_frequency_hint(args.keyword, args.frequency)
            candidates = search_indicators(args.keyword, args.size, args.offset, frequency_hint)
            chosen = [item["id"] for item in candidates[: max(1, args.pick)]]
            details = fetch_details(chosen, begin_date, end_date) if chosen else []
            payload = to_query_output(args.keyword, candidates, details, args.top)
            print_output(payload if args.json else format_detail_text(details, args.limit), args.json)
            return 0
    except DatayesError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
