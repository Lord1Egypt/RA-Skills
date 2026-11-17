#!/usr/bin/env python3
"""Shared bounded execution and evidence reporting for Dataify business skills."""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import statistics
import subprocess
import sys
from typing import Any
import urllib.error
import urllib.parse
import urllib.request
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[3]
if (Path(__file__).resolve().parents[1] / '_dependencies').is_dir():
    ROOT = Path(__file__).resolve().parents[1] / '_dependencies'
MODES = {"quick": 3, "standard": 6, "deep": 12}
CONFIG = {
    "price": {
        "title": "Price Intelligence",
        "input_flag": "--product",
        "input_help": "Product or service to compare.",
    },
    "review": {
        "title": "Review Intelligence",
        "input_flag": "--subject",
        "input_help": "Product, brand, app, or place whose reviews should be analyzed.",
    },
    "lead": {
        "title": "Lead Intelligence",
        "input_flag": "--ideal-customer-profile",
        "input_help": "Ideal customer profile or target-company description.",
    },
    "brand": {
        "title": "Brand Monitoring",
        "input_flag": "--brand",
        "input_help": "Brand to monitor.",
    },
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def slug(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip()).strip("-").lower() or "subject"


def parser(kind: str) -> argparse.ArgumentParser:
    config = CONFIG[kind]
    result = argparse.ArgumentParser(description="Run a bounded Dataify {} workflow.".format(config["title"]))
    result.add_argument(config["input_flag"], dest="subject", help=config["input_help"])
    result.add_argument("--competitor", action="append", default=[])
    result.add_argument("--keyword", action="append", default=[])
    result.add_argument("--source-url", action="append", default=[])
    result.add_argument("--official-domain")
    result.add_argument("--geography", default="US")
    result.add_argument("--freshness", default="12 months")
    result.add_argument("--mode", choices=tuple(MODES), default="quick")
    result.add_argument("--max-actions", type=int)
    result.add_argument("--output-dir", type=Path)
    result.add_argument("--resume", type=Path)
    result.add_argument("--dry-run", action="store_true")
    return result


def search_action(action_id: str, capability: str, query: str, subject: str) -> dict[str, Any]:
    return {"id": action_id, "type": "search", "capability": capability, "query": query, "url": None,
            "subject": subject, "stage": "discovery", "status": "pending", "attempts": 0, "output": None, "error": None}


def url_action(action_id: str, url: str, subject: str, kind: str) -> dict[str, Any]:
    host = urlsplit(url).netloc.lower()
    capability = "dataify-web-unlocker"
    if kind == "review" and "amazon." in host:
        capability = "scraper-amazon-comment"
    elif kind == "review" and "google." in host and "/maps" in url.lower():
        capability = "scraper-google-maps-reviews"
    return {"id": action_id, "type": "url", "capability": capability, "query": None, "url": url,
            "subject": subject, "stage": "detail", "status": "pending", "attempts": 0, "output": None, "error": None}


def make_actions(kind: str, subject: str, args: argparse.Namespace) -> list[dict[str, Any]]:
    terms = [subject, *args.competitor, *args.keyword]
    actions: list[dict[str, Any]] = [
        url_action("a{:02d}".format(index), url, subject, kind)
        for index, url in enumerate(args.source_url, 1)
    ]
    if kind == "price":
        for term in terms:
            actions.append(search_action("a{:02d}".format(len(actions) + 1), "dataify-google-shopping", term, term))
        query = "{} official pricing plans".format(subject)
        if args.official_domain:
            query = "site:{} {}".format(args.official_domain, query)
        actions.append(search_action("a{:02d}".format(len(actions) + 1), "dataify-google-search", query, subject))
    elif kind == "review":
        for term in terms:
            actions.append(search_action("a{:02d}".format(len(actions) + 1), "dataify-google-search",
                                         "{} reviews complaints praise {}".format(term, args.freshness), term))
    elif kind == "lead":
        actions.append(search_action("a{:02d}".format(len(actions) + 1), "dataify-google-search",
                                     "site:linkedin.com/company {} {}".format(subject, args.geography), subject))
        actions.append(search_action("a{:02d}".format(len(actions) + 1), "dataify-google-search",
                                     "site:crunchbase.com/organization {} {}".format(subject, args.geography), subject))
    else:
        exact = '"{}"'.format(subject)
        actions.append(search_action("a{:02d}".format(len(actions) + 1), "dataify-google-news", "{} {}".format(exact, " ".join(args.keyword)), subject))
        actions.append(search_action("a{:02d}".format(len(actions) + 1), "dataify-google-search",
                                     "{} reviews complaints news {}".format(exact, args.freshness), subject))
    for action in actions:
        action["geography"] = args.geography
    return actions


def command(action: dict[str, Any]) -> list[str]:
    capability = action["capability"]
    geo = str(action.get("geography", "")).strip().lower()
    geo_args = ["--gl", geo] if re.fullmatch(r"[a-z]{2}", geo) else []
    if capability == "dataify-google-shopping":
        return [sys.executable, str(ROOT / "skills/serp-google-shopping/scripts/google_shopping.py"), "--q", action["query"], "--json", "1", *geo_args]
    if capability == "dataify-google-news":
        return [sys.executable, str(ROOT / "skills/serp-google-news/scripts/google_news.py"), "--q", action["query"], "--json", "1", *geo_args]
    if capability == "dataify-google-search":
        return [sys.executable, str(ROOT / "skills/serp-google-search/scripts/google_search.py"), "--q", action["query"], "--json", "1", *geo_args]
    if capability == "scraper-amazon-comment":
        return [sys.executable, str(ROOT / "skills/scraper-amazon-comment/scripts/submit_amazon_comment.py"), "--url", action["url"]]
    if capability == "scraper-google-maps-reviews":
        return [sys.executable, str(ROOT / "skills/scraper-google-maps-reviews/scripts/google_maps_reviews.py"), "--url", action["url"]]
    return [sys.executable, str(ROOT / "skills/dataify-web-unlocker/scripts/invoke-dataify-web-unlocker.py"),
            "--url", action["url"], "--clean-content", "true"]


def direct_request(action: dict[str, Any], token: str) -> subprocess.CompletedProcess[str]:
    """Standalone fallback used when a ClawHub skill is installed without the full repository."""
    capability = action["capability"]
    try:
        if action["type"] == "search":
            engines = {"dataify-google-search": "google", "dataify-google-shopping": "google_shopping", "dataify-google-news": "google_news"}
            params = {"engine": engines[capability], "q": action["query"], "json": "1"}
            geo = str(action.get("geography", "")).strip().lower()
            if re.fullmatch(r"[a-z]{2}", geo):
                params["gl"] = geo
            request = urllib.request.Request(
                "https://scraperapi.dataify.com/request",
                data=urllib.parse.urlencode(params).encode("utf-8"),
                headers={"Authorization": "Bearer {}".format(token), "Content-Type": "application/x-www-form-urlencoded"},
                method="POST",
            )
        else:
            payload = {"url": action["url"], "type": "html", "js_render": "True", "clean_content": "true",
                       "country": str(action.get("geography", "us")).lower(), "follow_redirect": "True", "isjson": "1"}
            request = urllib.request.Request(
                "https://webunlocker.dataify.com/request",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Authorization": "Bearer {}".format(token), "Content-Type": "application/json"},
                method="POST",
            )
        with urllib.request.urlopen(request, timeout=120) as response:
            return subprocess.CompletedProcess([], 0, stdout=response.read().decode("utf-8", errors="replace"), stderr="")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        return subprocess.CompletedProcess([], 1, stdout="", stderr=detail or "HTTP {}".format(exc.code))
    except urllib.error.URLError as exc:
        return subprocess.CompletedProcess([], 1, stdout="", stderr="Request failed: {}".format(exc.reason))


def execute_action(action: dict[str, Any], token: str) -> subprocess.CompletedProcess[str]:
    invocation = command(action)
    if len(invocation) > 1 and Path(invocation[1]).exists():
        return subprocess.run(invocation, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    if action.get('capability', '').startswith('scraper-'):
        return subprocess.CompletedProcess([], 1, '', 'Required platform scraper is not installed; install it before executing this action.')
    return direct_request(action, token)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def decode_json_stream(text: str) -> Any:
    """Return the last complete JSON value from concatenated progress/final output."""
    decoder = json.JSONDecoder()
    index = 0
    values: list[Any] = []
    while index < len(text):
        while index < len(text) and text[index].isspace():
            index += 1
        if index >= len(text):
            break
        try:
            value, end = decoder.raw_decode(text, index)
        except json.JSONDecodeError:
            next_start = min((pos for pos in (text.find("{", index + 1), text.find("[", index + 1)) if pos >= 0), default=-1)
            if next_start < 0:
                break
            index = next_start
            continue
        values.append(value)
        index = end
    if not values:
        raise json.JSONDecodeError("No JSON value found", text, 0)
    return values[-1]


def visit_dicts(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from visit_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from visit_dicts(child)


SERP_COLLECTIONS = {
    "organic", "news", "news_results", "shopping", "shopping_results", "local_results",
    "jobs", "jobs_results", "videos", "images",
}


def record_items(payload: Any):
    """Traverse result-bearing collections, never SERP navigation or related-query metadata."""
    if isinstance(payload, dict) and any(key in payload for key in ("general", "input", "navigation", "related", "pagination")):
        for key in SERP_COLLECTIONS:
            value = payload.get(key)
            if isinstance(value, (list, dict)):
                yield from visit_dicts(value)
        return
    yield from visit_dicts(payload)


def first(item: dict[str, Any], names: tuple[str, ...]) -> Any:
    for name in names:
        value = item.get(name)
        if value not in (None, "", [], {}):
            return value
    return None


def currency_from(value: Any, explicit: Any) -> Any:
    if explicit:
        return explicit
    text = str(value or "")
    for marker in ("USD", "EUR", "GBP", "CNY", "RMB", "RM", "JPY", "CAD", "AUD"):
        if re.search(r"(?:^|\s){}(?:\s|$)".format(re.escape(marker)), text, re.I):
            return marker.upper()
    return "$" if "$" in text else "€" if "€" in text else "£" if "£" in text else None


def records_for(kind: str, payload: Any, evidence_id: str, subject: str = "") -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in record_items(payload):
        if kind == "price":
            price = first(item, ("price", "final_price", "extracted_price", "current_price", "sale_price"))
            title = first(item, ("title", "name", "product_name"))
            if price is None or title is None:
                continue
            product_tokens = [token.lower() for token in re.findall(r"[A-Za-z0-9-]+", subject) if len(token) > 2]
            if product_tokens and not all(token in str(title).lower() for token in product_tokens):
                continue
            variant_terms = ("bundle", "open box", "renewed", "refurbished", "used", "replacement", "earpad", "ear pad", "case", "cover", "cable",
                             "warranty", "protection plan", "axiom care", "sold without manufacturer warranty")
            comparable = not any(term in str(title).lower() for term in variant_terms)
            row = {"title": title, "price": price, "currency": currency_from(price, first(item, ("currency", "currency_code"))),
                   "seller": first(item, ("seller", "source", "merchant")), "url": first(item, ("link", "url", "product_link")),
                   "comparable": comparable, "evidence_id": evidence_id}
        elif kind == "review":
            body = first(item, ("review", "comment", "content", "text", "description", "snippet"))
            if body is None:
                continue
            row = {"text": str(body), "rating": first(item, ("rating", "score", "stars")),
                   "date": first(item, ("date", "review_date", "published_at")), "url": first(item, ("link", "url")), "evidence_id": evidence_id}
        elif kind == "lead":
            name = first(item, ("company", "company_name", "name", "title"))
            link = first(item, ("link", "url", "company_url"))
            if name is None or link is None:
                continue
            parsed = urlsplit(str(link))
            if not (("linkedin.com" in parsed.netloc and parsed.path.startswith("/company/")) or
                    ("crunchbase.com" in parsed.netloc and parsed.path.startswith("/organization/"))):
                continue
            signal = str(first(item, ("description", "snippet", "headline", "industry", "about")) or "")
            joined = (str(name) + " " + signal).casefold()
            hiring = bool(re.search(r"\b(hiring|job|opening|career|recruit)\w*\b", joined))
            target_role = bool(re.search(r"\b(data engineer|data engineering)\b", joined))
            company_detail = any(first(item, names) is not None for names in (("industry",), ("company_size", "employees"), ("headquarters", "location")))
            verified = company_detail and hiring and target_role
            score = 75 if verified else 45
            row = {"company": name, "url": link, "location": first(item, ("location", "country", "city")),
                   "signal": signal or None, "qualification_score": score,
                   "score_reasons": ["public company entity"] + (["company detail", "current hiring signal", "target role signal"] if verified else []),
                   "missing_fields": [] if verified else ["requires_detail_verification"],
                   "evidence_id": evidence_id}
        else:
            title = first(item, ("title", "name"))
            link = first(item, ("link", "url"))
            if title is None or link is None:
                continue
            haystack = " ".join(str(value) for value in (title, first(item, ("description", "snippet", "text")), link) if value)
            if subject and not re.search(r"(?<![A-Za-z0-9]){}(?![A-Za-z0-9])".format(re.escape(subject)), haystack, re.I):
                continue
            row = {"title": title, "url": link, "source": first(item, ("source", "publisher", "domain")),
                   "date": first(item, ("date", "published_at")), "snippet": first(item, ("description", "snippet", "text")), "evidence_id": evidence_id}
        if kind == "review":
            key = re.sub(r"\s+", " ", str(row.get("text", "")).strip().casefold())
        elif kind == "lead":
            key = str(row.get("url", "")).split("?", 1)[0].rstrip("/").casefold()
        else:
            key = json.dumps(row, ensure_ascii=False, sort_keys=True, default=str)
        if key not in seen:
            seen.add(key)
            result.append(row)
    return result[:500]


def parse_record_date(value: Any) -> datetime | None:
    if not value:
        return None
    text = str(value).strip()
    for candidate in (text, text.replace("Z", "+00:00")):
        try:
            parsed = datetime.fromisoformat(candidate)
            return parsed.replace(tzinfo=parsed.tzinfo or timezone.utc)
        except ValueError:
            pass
    for pattern in ("%b %d, %Y", "%B %d, %Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(text.replace("—", "").strip(), pattern).replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    return None


def freshness_cutoff(freshness: str, as_of: datetime) -> datetime | None:
    match = re.search(r"(\d+)\s*(day|week|month|year)s?", freshness or "", re.I)
    if not match:
        return None
    count = int(match.group(1))
    days = count * {"day": 1, "week": 7, "month": 30, "year": 365}[match.group(2).lower()]
    return as_of - timedelta(days=days)


def apply_scope_filters(kind: str, records: list[dict[str, Any]], freshness: str, geography: str,
                        as_of: str | None = None) -> tuple[list[dict[str, Any]], dict[str, int]]:
    reference = datetime.fromisoformat(as_of.replace("Z", "+00:00")) if as_of else datetime.now(timezone.utc)
    cutoff = freshness_cutoff(freshness, reference)
    kept: list[dict[str, Any]] = []
    excluded = {"outside_freshness": 0, "geography_mismatch": 0}
    geo_aliases = {
        "us": ("united states", "usa", "u.s.", "new york", "california", "texas", "washington", "massachusetts"),
        "de": ("germany", "deutschland", "berlin", "munich", "hamburg"),
        "cn": ("china", "中国", "beijing", "shanghai", "shenzhen", "guangzhou"),
    }
    foreign_markers = {
        "us": ("south africa", "germany", "deutschland", "china", "中国", "india", "canada", "united kingdom"),
        "de": ("united states", "usa", "south africa", "china", "中国", "india", "canada"),
        "cn": ("united states", "usa", "south africa", "germany", "deutschland", "india", "canada"),
    }
    target_geo = (geography or "").strip().casefold()
    for row in records:
        parsed = parse_record_date(row.get("date"))
        if cutoff and parsed and parsed < cutoff:
            excluded["outside_freshness"] += 1
            continue
        location = str(row.get("location") or "").casefold()
        if kind == "lead" and location and target_geo in foreign_markers:
            target_match = any(alias in location for alias in geo_aliases[target_geo])
            explicit_foreign = any(marker in location for marker in foreign_markers[target_geo])
            if explicit_foreign and not target_match:
                excluded["geography_mismatch"] += 1
                continue
        kept.append(row)
    return kept, excluded


def acceptance_gate(kind: str, records: list[dict[str, Any]], metrics: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    if kind == "brand" and not records:
        reasons.append("at least one verified external mention is required")
    elif kind == "lead" and not any(row.get("qualification_score", 0) >= 70 and not row.get("missing_fields") for row in records):
        reasons.append("at least one company must pass detail verification and qualification")
    elif kind == "price":
        comparable = [row for row in records if row.get("comparable") is not False and number(row.get("price")) is not None and row.get("url")]
        if len(comparable) < 2:
            reasons.append("at least two comparable, sourced prices are required")
        if not any(row.get("evidence_stage") == "detail" for row in comparable):
            reasons.append("at least one comparable price must be verified from a detail source")
    elif kind == "review":
        usable = [row for row in records if row.get("text") and row.get("url")]
        if len(usable) < 3:
            reasons.append("at least three sourced review records are required")
        if not any(row.get("evidence_stage") == "detail" for row in usable):
            reasons.append("at least one review must come from detail collection, not a search snippet")
    return {"accepted": not reasons, "reasons": reasons}


def discovery_links(payload: Any, subject: str, kind: str = "") -> list[str]:
    links: list[str] = []
    for item in record_items(payload):
        link = first(item, ("link", "url", "product_link"))
        title = first(item, ("title", "name"))
        if not link or not str(link).startswith(("http://", "https://")):
            continue
        if "google.com/search" in str(link):
            continue
        if kind != "lead" and subject and title and subject.casefold() not in (str(title) + " " + str(link)).casefold():
            continue
        if kind == "lead":
            parsed = urlsplit(str(link))
            if not (("linkedin.com" in parsed.netloc and parsed.path.startswith("/company/")) or
                    ("crunchbase.com" in parsed.netloc and parsed.path.startswith("/organization/"))):
                continue
        clean = str(link).split("#", 1)[0]
        if clean not in links:
            links.append(clean)
    return links


def add_detail_actions(state: dict[str, Any], payloads: dict[str, Any]) -> int:
    capacity = max(0, int(state.get("max_actions", 0)) - len(state["actions"]))
    if not capacity:
        return 0
    existing = {action.get("url") for action in state["actions"] if action.get("url")}
    candidates: list[str] = []
    for action in state["actions"]:
        if action.get("stage", "discovery") != "discovery" or action["id"] not in payloads:
            continue
        for link in discovery_links(payloads[action["id"]], state["subject"], state["kind"]):
            if link not in existing and link not in candidates:
                candidates.append(link)
    for link in candidates[:capacity]:
        action = url_action("a{:02d}".format(len(state["actions"]) + 1), link, state["subject"], state["kind"])
        action["geography"] = state.get("geography", "US")
        state["actions"].append(action)
    return min(capacity, len(candidates))


def validate_action_result(completed: subprocess.CompletedProcess[str]) -> tuple[bool, str | None]:
    if completed.returncode != 0:
        return False, (completed.stderr or completed.stdout or "collection failed")[-2000:]
    try:
        payload = decode_json_stream(completed.stdout)
    except json.JSONDecodeError:
        return (bool(completed.stdout.strip()), None if completed.stdout.strip() else "empty collection response")
    if isinstance(payload, dict):
        code = payload.get("code")
        if isinstance(code, int) and code >= 400:
            return False, "application response code {}: {}".format(code, str(payload.get("data") or payload.get("message") or "error")[:500])
        if payload.get("ok") is False or str(payload.get("status", "")).lower() in {"failed", "error"}:
            return False, str(payload.get("error") or payload.get("message") or "application response reported failure")[:2000]
    return True, None


def number(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        match = re.search(r"-?\d+(?:[,.]\d+)*", value)
        if match:
            try:
                return float(match.group(0).replace(",", ""))
            except ValueError:
                pass
    return None


def analyze(kind: str, records: list[dict[str, Any]]) -> dict[str, Any]:
    metrics: dict[str, Any] = {"record_count": len(records)}
    if kind == "price":
        grouped: dict[str, list[float]] = {}
        for row in records:
            if row.get("comparable") is False:
                continue
            value = number(row.get("price"))
            currency = str(row.get("currency") or "unknown")
            if value is not None:
                grouped.setdefault(currency, []).append(value)
        ranges = {currency: {"count": len(values), "minimum": min(values), "maximum": max(values)} for currency, values in grouped.items()}
        trusted: dict[str, dict[str, Any]] = {}
        outliers = 0
        for currency, values in grouped.items():
            median = statistics.median(values)
            accepted = [value for value in values if median * 0.5 <= value <= median * 2]
            outliers += len(values) - len(accepted)
            trusted[currency] = {"count": len(accepted), "minimum": min(accepted) if accepted else None,
                                 "maximum": max(accepted) if accepted else None, "median": median}
        metrics.update({"comparable_price_count": sum(len(values) for values in grouped.values()),
                        "observed_price_ranges_by_currency": ranges, "trusted_price_ranges_by_currency": trusted,
                        "price_anomaly_count": outliers})
        if len(grouped) == 1:
            only = next(iter(trusted.values()))
            metrics.update({"minimum_price": only["minimum"], "maximum_price": only["maximum"]})
    elif kind == "review":
        positive = ("great", "excellent", "love", "best", "好", "满意", "推荐")
        negative = ("bad", "poor", "issue", "problem", "slow", "差", "问题", "失望")
        texts = [str(row.get("text", "")).lower() for row in records]
        metrics.update({"positive_signal_count": sum(any(word in text for word in positive) for text in texts),
                        "negative_signal_count": sum(any(word in text for word in negative) for text in texts)})
        theme_terms = {
            "performance": ("slow", "performance", "lag", "速度", "卡顿"),
            "support": ("support", "service", "客服", "支持"),
            "billing": ("billing", "charge", "subscription", "refund", "扣费", "退款"),
            "usability": ("complex", "learning curve", "easy", "difficult", "复杂", "易用"),
        }
        metrics["themes"] = {theme: sum(any(term in text for term in terms) for text in texts)
                             for theme, terms in theme_terms.items() if any(any(term in text for term in terms) for text in texts)}
    elif kind == "lead":
        companies = {str(row.get("url", "")).split("?", 1)[0].rstrip("/").casefold() for row in records if row.get("url")}
        metrics["unique_company_count"] = len(companies)
        metrics["high_fit_count"] = sum(int(row.get("qualification_score", 0)) >= 70 for row in records)
    else:
        channels: dict[str, int] = {}
        for row in records:
            domain = urlsplit(str(row.get("url", ""))).netloc.lower() or "unknown"
            channels[domain] = channels.get(domain, 0) + 1
        metrics["channel_counts"] = dict(sorted(channels.items(), key=lambda item: item[1], reverse=True)[:20])
        negative = ("complaint", "problem", "outage", "breach", "lawsuit", "scam", "投诉", "故障", "泄露")
        metrics["risk_signal_count"] = sum(any(term in (str(row.get("title", "")) + " " + str(row.get("snippet", ""))).casefold()
                                                       for term in negative) for row in records)
    return metrics


def build_outputs(root: Path, state: dict[str, Any]) -> dict[str, Any]:
    evidence: list[dict[str, Any]] = []
    records: list[dict[str, Any]] = []
    for action in state["actions"]:
        if action["status"] != "success" or not action.get("output"):
            continue
        raw_path = root / action["output"]
        raw = raw_path.read_bytes()
        decoded = raw.decode("utf-8", errors="replace")
        try:
            payload = decode_json_stream(decoded)
        except (UnicodeDecodeError, json.JSONDecodeError):
            payload = {"text": decoded, "url": action.get("url")}
        evidence_id = "ev-{:04d}".format(len(evidence) + 1)
        evidence.append({"evidence_id": evidence_id, "action_id": action["id"], "capability": action["capability"],
                         "query": action.get("query"), "url": action.get("url"), "raw_path": action["output"],
                         "sha256": hashlib.sha256(raw).hexdigest(), "collected_at": state["updated_at"]})
        action_records = records_for(state["kind"], payload, evidence_id, state["subject"])
        for row in action_records:
            row["evidence_stage"] = action.get("stage", "discovery")
        records.extend(action_records)
    records, exclusions = apply_scope_filters(state["kind"], records, state.get("freshness", ""), state.get("geography", ""), state.get("updated_at"))
    metrics = analyze(state["kind"], records)
    metrics["excluded_by_scope"] = exclusions
    gate = acceptance_gate(state["kind"], records, metrics)
    failures = [{"action_id": a["id"], "error": a["error"]} for a in state["actions"] if a["status"] == "failed"]
    status = "complete" if gate["accepted"] else "insufficient_evidence" if evidence else "failed"
    report = {"workflow": state["kind"], "subject": state["subject"], "generated_at": now(),
              "status": status, "acceptance": gate, "metrics": metrics, "records": records,
              "evidence": evidence, "failures": [{"action_id": a["id"], "error": a["error"]} for a in state["actions"] if a["status"] == "failed"],
              "limitations": ["Automated signals require human review before commercial, pricing, product, or reputation decisions."]}
    write_json(root / "report.json", report)
    lines = ["# {} — {}".format(CONFIG[state["kind"]]["title"], state["subject"]), "", "Generated: {}".format(report["generated_at"]), "", "## Executive metrics", ""]
    lines.extend("- {}: {}".format(key.replace("_", " "), value) for key, value in metrics.items())
    lines.extend(["", "## Top records", ""])
    for row in records[:20]:
        label = row.get("title") or row.get("company") or str(row.get("text", ""))[:100]
        lines.append("- {} — {}".format(label, row.get("url") or row.get("price") or row.get("rating") or "source retained"))
    if not gate["accepted"]:
        lines.extend(["", "## Evidence gaps", ""])
        lines.extend("- {}".format(reason) for reason in gate["reasons"])
    if report["failures"]:
        lines.extend(["", "## Collection gaps", ""])
        lines.extend("- {}: {}".format(item["action_id"], item["error"]) for item in report["failures"])
    lines.extend(["", "## Limitations", "", "- " + report["limitations"][0], ""])
    (root / "report.md").write_text("\n".join(lines), encoding="utf-8")
    return report


def run(kind: str, argv: list[str] | None = None) -> int:
    args = parser(kind).parse_args(argv)
    if args.resume:
        root = args.resume if args.resume.is_dir() else args.resume.parent
        state_path = root / "state.json" if args.resume.is_dir() else args.resume
        state = json.loads(state_path.read_text(encoding="utf-8"))
    else:
        if not args.subject:
            parser(kind).error("{} is required unless --resume is used".format(CONFIG[kind]["input_flag"]))
        limit = args.max_actions if args.max_actions is not None else MODES[args.mode]
        if limit < 1:
            parser(kind).error("--max-actions must be at least 1")
        root = args.output_dir or Path("{}-intelligence-run".format(kind))
        actions = make_actions(kind, args.subject, args)[:limit]
        state = {"version": 2, "kind": kind, "subject": args.subject, "mode": args.mode, "max_actions": limit,
                 "geography": args.geography, "freshness": args.freshness, "official_domain": args.official_domain,
                 "created_at": now(), "updated_at": now(), "actions": actions}
        state_path = root / "state.json"
        write_json(state_path, state)
    if args.dry_run:
        print(json.dumps({"state": str(state_path), "actions": state["actions"]}, ensure_ascii=False, indent=2))
        return 0
    if not os.environ.get("DATAIFY_API_TOKEN", "").strip():
        print("DATAIFY_API_TOKEN is not configured. Configure it in your environment; never paste it into chat.", file=sys.stderr)
        return 1
    raw_dir = root / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    def execute_pending() -> None:
        for action in state["actions"]:
            if action["status"] in {"success", "submitting", "unknown"}:
                continue
            if action['status'] == 'failed' and action.get('capability', '').startswith('scraper-'):
                continue
            if action.get('capability', '').startswith('scraper-'):
                action['status'] = 'submitting'
                write_json(state_path, state)
            action["attempts"] += 1
            completed = execute_action(action, os.environ["DATAIFY_API_TOKEN"].strip())
            success, result_error = validate_action_result(completed)
            if success:
                path = raw_dir / "{}-{}.json".format(action["id"], slug(action["subject"]))
                path.write_text(completed.stdout, encoding="utf-8")
                action.update(status="success", output=str(path.relative_to(root)), error=None)
            else:
                action.update(status="failed", error=result_error)
            state["updated_at"] = now()
            write_json(state_path, state)

    execute_pending()
    payloads: dict[str, Any] = {}
    for action in state["actions"]:
        if action.get("stage", "discovery") != "discovery" or action.get("status") != "success" or not action.get("output"):
            continue
        try:
            payloads[action["id"]] = decode_json_stream((root / action["output"]).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
    if add_detail_actions(state, payloads):
        write_json(state_path, state)
        execute_pending()
    report = build_outputs(root, state)
    print(json.dumps({"status": report["status"], "workflow": kind, "subject": state["subject"],
                      "records": report["metrics"]["record_count"], "report": str(root / "report.md"),
                      "report_json": str(root / "report.json"), "state": str(state_path)}, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "complete" else 2 if report["status"] == "insufficient_evidence" else 1
