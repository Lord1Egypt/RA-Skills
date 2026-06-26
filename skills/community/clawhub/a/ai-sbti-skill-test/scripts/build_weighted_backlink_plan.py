#!/usr/bin/env python3
"""Build a weighted backlink execution plan for aisbti.com."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Dict, Iterable, List
from urllib.parse import urlparse

PLACEMENT_FACTORS = {
    "editorial": 1.00,
    "guest-post": 0.95,
    "directory": 0.80,
    "profile": 0.60,
    "forum": 0.55,
    "comment": 0.35,
}

LINK_TYPE_FACTORS = {
    "dofollow": 1.00,
    "nofollow": 0.45,
    "ugc": 0.35,
    "sponsored": 0.30,
}

WEIGHTS = {
    "authority": 0.35,
    "relevance": 0.25,
    "traffic": 0.15,
    "indexed": 0.10,
    "link_type": 0.10,
    "placement": 0.05,
}


def normalize_domain(value: str) -> str:
    host = urlparse(value).netloc or value
    host = host.lower().strip()
    if host.startswith("www."):
        host = host[4:]
    return host


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def parse_float(value: str, default: float = 0.0) -> float:
    if value is None:
        return default
    text = str(value).strip()
    if not text:
        return default
    try:
        return float(text)
    except ValueError:
        return default


def parse_bool(value: str) -> bool:
    text = str(value or "").strip().lower()
    return text in {"1", "true", "t", "yes", "y"}


def normalize_traffic(traffic: float) -> float:
    if traffic <= 0:
        return 0.0
    return clamp(math.log10(traffic + 1.0) / 6.0, 0.0, 1.0)


def outbound_penalty(outbound_links: float) -> float:
    # More outbound links generally dilute per-link value.
    penalty = 1.0 / math.log2(max(outbound_links, 0.0) + 2.0)
    return clamp(penalty * 2.2, 0.20, 1.00)


def anchor_category(anchor_text: str, domain: str, money_keywords: Iterable[str]) -> str:
    anchor = (anchor_text or "").strip().lower()
    if not anchor:
        return "generic"
    if anchor.startswith("http://") or anchor.startswith("https://"):
        return "url"
    if "aisbti" in anchor or domain in anchor:
        return "branded"

    normalized_keywords = [kw.strip().lower() for kw in money_keywords if kw.strip()]
    if anchor in normalized_keywords:
        return "exact"
    if any(kw in anchor for kw in normalized_keywords):
        return "partial"
    return "generic"


def score_row(row: Dict[str, str]) -> Dict[str, float]:
    authority = clamp(parse_float(row.get("authority")) / 100.0, 0.0, 1.0)
    relevance = clamp(parse_float(row.get("relevance")), 0.0, 1.0)
    traffic = normalize_traffic(parse_float(row.get("estimated_traffic")))
    indexed = 1.0 if parse_bool(row.get("indexed", "1")) else 0.0

    link_type = (row.get("link_type") or "nofollow").strip().lower()
    link_type_factor = LINK_TYPE_FACTORS.get(link_type, 0.40)

    placement = (row.get("placement") or "directory").strip().lower()
    placement_factor = PLACEMENT_FACTORS.get(placement, 0.65)

    outbound_links = max(parse_float(row.get("outbound_links"), 80.0), 0.0)
    dilution_penalty = outbound_penalty(outbound_links)

    weighted = (
        WEIGHTS["authority"] * authority
        + WEIGHTS["relevance"] * relevance
        + WEIGHTS["traffic"] * traffic
        + WEIGHTS["indexed"] * indexed
        + WEIGHTS["link_type"] * link_type_factor
        + WEIGHTS["placement"] * placement_factor
    )

    score = round(100.0 * weighted * dilution_penalty, 2)
    transfer = round(score * (0.90 if link_type == "dofollow" else 0.45) * (1.0 if indexed else 0.2), 2)

    return {
        "authority_n": round(authority, 4),
        "relevance_n": round(relevance, 4),
        "traffic_n": round(traffic, 4),
        "indexed_n": round(indexed, 4),
        "link_type_n": round(link_type_factor, 4),
        "placement_n": round(placement_factor, 4),
        "dilution_penalty": round(dilution_penalty, 4),
        "score": score,
        "transfer_score": transfer,
    }


def read_csv_rows(path: str) -> List[Dict[str, str]]:
    with open(path, "r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = [dict(row) for row in reader]
    return rows


def load_relay_map(path: str) -> Dict[str, List[Dict[str, float]]]:
    if not path:
        return {}
    relay_map: Dict[str, List[Dict[str, float]]] = defaultdict(list)
    for row in read_csv_rows(path):
        landing = (row.get("landing_url") or "").strip()
        relay_url = (row.get("relay_url") or "").strip()
        ratio = clamp(parse_float(row.get("relay_ratio"), 0.0), 0.0, 1.0)
        if not landing or not relay_url or ratio <= 0:
            continue
        relay_map[landing].append({"relay_url": relay_url, "relay_ratio": ratio})
    return relay_map


def format_pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def build_markdown(
    *,
    site_url: str,
    min_score: float,
    top_n: int,
    rows_total: int,
    selected: List[Dict[str, object]],
    rejected: List[Dict[str, object]],
    anchor_mix: Dict[str, float],
    relay_summary: List[Dict[str, object]],
    alerts: List[str],
) -> str:
    lines: List[str] = []
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")

    lines.append(f"# Weighted Backlink Plan for {site_url}")
    lines.append("")
    lines.append(f"- Generated at: `{now}`")
    lines.append(f"- Candidates scanned: `{rows_total}`")
    lines.append(f"- Selected (`score >= {min_score}`): `{len(selected)}`")
    lines.append(f"- Rejected: `{len(rejected)}`")
    lines.append(f"- Top limit: `{top_n}`")
    lines.append("")

    lines.append("## Anchor Mix")
    lines.append("")
    for bucket in ["branded", "url", "partial", "exact", "generic"]:
        lines.append(f"- {bucket}: `{format_pct(anchor_mix.get(bucket, 0.0))}`")
    lines.append("")

    if alerts:
        lines.append("## Alerts")
        lines.append("")
        for alert in alerts:
            lines.append(f"- {alert}")
        lines.append("")

    lines.append("## Top Opportunities")
    lines.append("")
    lines.append("| # | Source Domain | Target URL | Anchor | Link Type | Placement | Score | Transfer |")
    lines.append("|---|---|---|---|---|---|---:|---:|")
    for idx, item in enumerate(selected, start=1):
        lines.append(
            "| {idx} | {source_domain} | {target_url} | {anchor_text} | {link_type} | {placement} | {score:.2f} | {transfer_score:.2f} |".format(
                idx=idx,
                source_domain=item.get("source_domain", ""),
                target_url=item.get("target_url", ""),
                anchor_text=(item.get("anchor_text", "") or "").replace("|", " "),
                link_type=item.get("link_type", ""),
                placement=item.get("placement", ""),
                score=float(item.get("score", 0.0)),
                transfer_score=float(item.get("transfer_score", 0.0)),
            )
        )
    lines.append("")

    lines.append("## Internal Weight Relay")
    lines.append("")
    if relay_summary:
        lines.append("| Relay URL | Aggregated Weight | Source Count |")
        lines.append("|---|---:|---:|")
        for row in relay_summary:
            lines.append(
                f"| {row['relay_url']} | {row['aggregated_weight']:.2f} | {row['source_count']} |"
            )
    else:
        lines.append("No relay map provided, or no selected backlinks matched relay landing URLs.")
    lines.append("")

    lines.append("## Execution Notes")
    lines.append("")
    lines.append("- Acquire top dofollow and indexed opportunities first.")
    lines.append("- Keep exact-match anchors under 10% of total anchors.")
    lines.append("- Diversify landing URLs; do not concentrate on homepage only.")
    lines.append("- Recalculate weekly after live link checks.")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build weighted backlink plan for aisbti.com")
    parser.add_argument("--site-url", required=True, help="Canonical site URL, e.g. https://aisbti.com")
    parser.add_argument("--input-csv", required=True, help="Prospect CSV")
    parser.add_argument("--output-md", required=True, help="Output markdown path")
    parser.add_argument("--output-json", required=True, help="Output JSON path")
    parser.add_argument("--relay-map", default="", help="Optional relay map CSV")
    parser.add_argument("--min-score", type=float, default=35.0)
    parser.add_argument("--top-n", type=int, default=40)
    parser.add_argument("--money-keyword", action="append", default=[])

    args = parser.parse_args()

    site_domain = normalize_domain(args.site_url)
    if not site_domain:
        raise ValueError("Invalid --site-url")

    rows = read_csv_rows(args.input_csv)
    relay_map = load_relay_map(args.relay_map)
    selected: List[Dict[str, object]] = []
    rejected: List[Dict[str, object]] = []

    anchor_counter: Counter = Counter()
    alerts: List[str] = []

    for raw in rows:
        source_url = (raw.get("source_url") or "").strip()
        source_domain = (raw.get("source_domain") or "").strip()
        target_url = (raw.get("target_url") or "").strip()
        anchor_text = (raw.get("anchor_text") or "").strip()
        link_type = (raw.get("link_type") or "nofollow").strip().lower()
        placement = (raw.get("placement") or "directory").strip().lower()

        if not source_domain and source_url:
            source_domain = normalize_domain(source_url)

        if not target_url:
            rejected.append({"reason": "missing_target_url", "row": raw})
            continue

        target_domain = normalize_domain(target_url)
        if target_domain != site_domain:
            rejected.append({"reason": "target_domain_mismatch", "row": raw})
            continue

        if parse_float(raw.get("relevance"), 0.0) < 0.20:
            rejected.append({"reason": "very_low_relevance", "row": raw})
            continue

        metrics = score_row(raw)
        enriched = {
            "source_domain": source_domain,
            "source_url": source_url,
            "target_url": target_url,
            "anchor_text": anchor_text,
            "link_type": link_type,
            "placement": placement,
            **metrics,
        }

        if metrics["score"] < args.min_score:
            rejected.append({"reason": "below_min_score", "row": enriched})
            continue

        selected.append(enriched)
        bucket = anchor_category(anchor_text, site_domain, args.money_keyword)
        anchor_counter[bucket] += 1

    selected.sort(key=lambda item: (float(item["score"]), float(item["transfer_score"])), reverse=True)
    selected = selected[: max(args.top_n, 0)]

    anchor_total = sum(anchor_counter.values()) or 1
    anchor_mix = {k: anchor_counter.get(k, 0) / anchor_total for k in ["branded", "url", "partial", "exact", "generic"]}

    if anchor_mix.get("exact", 0.0) > 0.10:
        alerts.append("Exact-match anchors exceed 10%; rebalance before outreach.")
    if anchor_mix.get("branded", 0.0) < 0.40:
        alerts.append("Branded anchor share is low; add more branded anchors.")

    relay_totals: Dict[str, Dict[str, object]] = {}
    for item in selected:
        target_url = str(item["target_url"])
        transfer_score = float(item["transfer_score"])
        for relay in relay_map.get(target_url, []):
            relay_url = relay["relay_url"]
            relay_ratio = float(relay["relay_ratio"])
            transferred = round(transfer_score * relay_ratio * 0.85, 2)

            if relay_url not in relay_totals:
                relay_totals[relay_url] = {
                    "relay_url": relay_url,
                    "aggregated_weight": 0.0,
                    "source_count": 0,
                }
            relay_totals[relay_url]["aggregated_weight"] = round(
                float(relay_totals[relay_url]["aggregated_weight"]) + transferred, 2
            )
            relay_totals[relay_url]["source_count"] = int(relay_totals[relay_url]["source_count"]) + 1

    relay_summary = sorted(
        relay_totals.values(),
        key=lambda row: float(row["aggregated_weight"]),
        reverse=True,
    )

    markdown = build_markdown(
        site_url=args.site_url,
        min_score=args.min_score,
        top_n=args.top_n,
        rows_total=len(rows),
        selected=selected,
        rejected=rejected,
        anchor_mix=anchor_mix,
        relay_summary=relay_summary,
        alerts=alerts,
    )

    os.makedirs(os.path.dirname(args.output_md) or ".", exist_ok=True)
    os.makedirs(os.path.dirname(args.output_json) or ".", exist_ok=True)

    with open(args.output_md, "w", encoding="utf-8") as handle:
        handle.write(markdown)

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "site_url": args.site_url,
        "site_domain": site_domain,
        "candidates_total": len(rows),
        "selected_total": len(selected),
        "rejected_total": len(rejected),
        "min_score": args.min_score,
        "top_n": args.top_n,
        "anchor_mix": anchor_mix,
        "alerts": alerts,
        "selected_candidates": selected,
        "relay_summary": relay_summary,
        "rejected_candidates": rejected,
    }

    with open(args.output_json, "w", encoding="utf-8") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)

    print(f"Plan generated: {args.output_md}")
    print(f"JSON generated: {args.output_json}")
    print(f"Selected opportunities: {len(selected)} / {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
