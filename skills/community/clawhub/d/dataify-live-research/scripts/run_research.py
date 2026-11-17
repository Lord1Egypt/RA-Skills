#!/usr/bin/env python3
"""Collect a bounded, resumable evidence package for an open research question."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from html import unescape
import json
import os
from pathlib import Path
import re
import sys
from typing import Any
from urllib.parse import urlsplit
from urllib.parse import urlunsplit, parse_qsl, urlencode

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from dataify_client import content_from_response, search, unlock, token_from_environment, urls_from_search


MODES = {"quick": 6, "standard": 12, "deep": 20}

KNOWN_ENTITIES = {
    "dataify": {
        "identity_terms": ("dataify",),
        "official_domains": ("dataify.com", "doc.dataify.com", "github.com/dataify-server"),
        "seed_urls": ("https://www.dataify.com/", "https://doc.dataify.com/", "https://github.com/dataify-server"),
        "search_phrases": ("Dataify APIs products", "Dataify API MCP SDK documentation", "Dataify SDK CLI MCP"),
    },
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def slug(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]+", "-", value).strip("-").lower() or "research"


def entity_profile(question: str) -> dict[str, tuple[str, ...]] | None:
    lowered = question.lower()
    for name, profile in KNOWN_ENTITIES.items():
        if re.search(r"\b{}\b".format(re.escape(name)), lowered):
            return profile
    return None


def identity_terms(question: str) -> tuple[str, ...]:
    profile = entity_profile(question)
    if profile:
        return profile["identity_terms"]
    question_words = {"what", "which", "how", "why", "when", "where", "who", "does", "is", "are", "the", "an"}
    candidates = re.findall(r"\b[A-Z][A-Za-z0-9._-]{1,}\b", question)
    return tuple(dict.fromkeys(term.lower() for term in candidates if term.lower() not in question_words))


def build_plan(question: str, geography: str, freshness: str, limit: int) -> list[dict[str, Any]]:
    angles = (
        ("overview", "{} overview primary sources {} {}"),
        ("current", "{} latest developments evidence {} {}"),
        ("data", "{} statistics research report {} {}"),
        ("risks", "{} risks criticism limitations {} {}"),
        ("alternatives", "{} alternatives market landscape {} {}"),
        ("implementation", "{} implementation examples case studies {} {}"),
    )
    actions = []
    profile = entity_profile(question)
    official_domains = profile["official_domains"] if profile else ()
    for index, (angle, template) in enumerate(angles[:max(1, limit)], 1):
        query = template.format(question, geography, freshness)
        if index <= len(official_domains):
            query = "site:{} {}".format(official_domains[index - 1], question)
        actions.append({
            "id": "a{:02d}".format(index), "type": "search", "angle": angle,
            "query": query, "url": None,
            "status": "pending", "attempts": 0, "output": None, "error": None,
        })
    return actions


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_state(args: argparse.Namespace) -> tuple[Path, dict]:
    if args.resume:
        path = args.resume if args.resume.name == "state.json" else args.resume / "state.json"
        state = json.loads(path.read_text(encoding="utf-8"))
        if args.retry_failed_safe:
            for action in state["actions"]:
                if action["status"] == "failed" and action["type"] in {"search", "fetch"}:
                    action.update(status="pending", error=None)
        return path, state
    if not args.question:
        raise ValueError("--question is required unless --resume is used")
    limit = args.max_actions if args.max_actions is not None else MODES[args.mode]
    if not 1 <= limit <= 30:
        raise ValueError("--max-actions must be between 1 and 30")
    full_plan = build_plan(args.question, args.geography, args.freshness, min(6, limit))
    discovery_count = min(len(full_plan), max(1, limit // 2))
    actions = full_plan[:discovery_count]
    profile = entity_profile(args.question)
    if profile:
        if limit == 1:
            actions = []
            seed_count = 1
        else:
            # One focused discovery query plus two direct official seeds leaves
            # room for result expansion while surviving an empty search index.
            actions = full_plan[:1]
            seed_count = min(2, limit - len(actions))
        for url in profile["seed_urls"][:seed_count]:
            actions.append({
                "id": "a{:02d}".format(len(actions) + 1), "type": "fetch",
                "angle": "official", "query": None, "url": url,
                "status": "pending", "attempts": 0, "output": None, "error": None,
            })
    state = {
        "version": 1, "question": args.question, "geography": args.geography,
        "freshness": args.freshness, "audience": args.audience, "decision": args.decision,
        "mode": args.mode, "action_budget": limit, "created_at": now(), "updated_at": now(),
        "actions": actions,
    }
    path = args.output_dir / "state.json"
    write_json(path, state)
    return path, state


def domain_priority(value: str, domains: tuple[str, ...]) -> int:
    parsed = urlsplit(value if "://" in value else "//" + value)
    host = parsed.netloc.lower()
    path = parsed.path.rstrip("/")
    for index, domain in enumerate(domains):
        target_host, _, target_path = domain.partition("/")
        if host == target_host and (not target_path or path == '/' + target_path or path.startswith('/' + target_path + '/')):
            return index * 2
    for index, domain in enumerate(domains):
        target_host, _, target_path = domain.partition("/")
        if host.endswith("." + target_host) and (not target_path or path == '/' + target_path or path.startswith('/' + target_path + '/')):
            return index * 2 + 1
    return len(domains) * 2 + 1


def rank_urls(urls: list[str], question: str = "") -> list[str]:
    blocked = ("google.com/search", "accounts.google", "webcache.googleusercontent")
    candidates = [url for url in urls if not any(item in url.lower() for item in blocked)]
    profile = entity_profile(question)
    if not profile:
        return candidates
    return sorted(candidates, key=lambda url: domain_priority(url, profile["official_domains"]))


def normalize_source_url(url: str) -> str:
    parts = urlsplit(url)
    host = parts.netloc.lower()
    path = parts.path.rstrip("/") or "/"
    query = urlencode([(k,v) for k,v in parse_qsl(parts.query, keep_blank_values=True) if not k.lower().startswith('utm_') and k.lower() not in {'fbclid','gclid'}])
    return urlunsplit((parts.scheme.lower(), host, path, query, ""))


def quality_gate_sources(rows: list[dict], question: str, min_content: int = 200) -> tuple[list[dict], list[dict]]:
    """Deduplicate and score fetched pages; keep failure reasons auditable."""
    blocked = re.compile(r"just a moment|captcha|access denied|page not found|404 not found|sign in to continue|authwall|agree\s*(?:&|and)\s*join|join linkedin", re.I)
    query_terms = {word.lower() for word in re.findall(r"[A-Za-z0-9]{3,}|[\u4e00-\u9fff]{2}", question)} - {'what','which','does','offer','the','and','are','how','研究','最近','七天','产品','变化'}
    profile = entity_profile(question)
    required_identity = identity_terms(question)
    seen: set[str] = set()
    kept, rejected = [], []
    for row in rows:
        source = row.get("source", "")
        content = row.get("content", "").strip()
        try:
            normalized = normalize_source_url(source)
        except Exception:
            rejected.append({**row, "reason": "invalid_url"})
            continue
        if normalized in seen:
            rejected.append({**row, "reason": "duplicate_url", "normalized_url": normalized})
            continue
        seen.add(normalized)
        if len(content) < min_content:
            rejected.append({**row, "reason": "too_short", "normalized_url": normalized})
            continue
        if blocked.search(content[:2000]):
            rejected.append({**row, "reason": "blocked_or_error_page", "normalized_url": normalized})
            continue
        haystack = (source + " " + content[:5000]).lower()
        host = urlsplit(normalized).netloc
        if required_identity:
            entity_match = any(term in haystack for term in required_identity)
            official_match = bool(profile and domain_priority(normalized, profile["official_domains"]) <= len(profile["official_domains"]) * 2)
            if not entity_match and not official_match:
                rejected.append({**row, "reason": "entity_mismatch", "normalized_url": normalized})
                continue
        relevance = sum(term in haystack for term in query_terms) / max(1, len(query_terms))
        if relevance == 0:
            rejected.append({**row, 'reason': 'topic_mismatch'})
            continue
        is_official = bool(profile and domain_priority(normalized, profile["official_domains"]) <= len(profile["official_domains"]) * 2)
        authority = 1.0 if is_official or host.endswith((".gov", ".gov.uk", ".europa.eu", ".edu")) else 0.8 if any(x in host for x in ("docs.", "developer.", "github.com")) else 0.5
        scored = {**row, "normalized_url": normalized, "relevance_score": round(relevance, 3), "authority_score": authority, "quality_score": round(relevance * 0.7 + authority * 0.3, 3)}
        kept.append(scored)
    kept.sort(key=lambda item: item["quality_score"], reverse=True)
    return kept, rejected


def visible_text(value: str) -> str:
    value = re.sub(r"<(script|style|noscript)\b[^>]*>.*?</\1>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", unescape(value)).strip()


def build_brief(question: str, sources: list[dict], rejected: list[dict], collected_at: str) -> dict:
    primary_required = bool(re.search(r"\b(official|government|regulator|regulation|law)\b", question, re.I))
    has_primary = any(source.get("authority_score", 0) >= 0.8 for source in sources)
    status = "brief_ready" if len(sources) >= 2 and (not primary_required or has_primary) else "insufficient_evidence"
    lines = ["# Live research brief", "", "- Question: {}".format(question), "- Collected: {}".format(collected_at), "- Status: {}".format(status), "", "## Executive summary", ""]
    if status == "brief_ready":
        lines.append("The following findings are extractive leads from {} quality-gated live sources; verify the linked evidence before making a high-stakes decision.".format(len(sources)))
    else:
        lines.append("The run did not retain enough independent usable pages or required primary-source evidence to support a reliable conclusion.")
    lines.extend(["", "## Evidence-backed findings", ""])
    for index, source in enumerate(sources, 1):
        excerpt = visible_text(source["content"])[:500]
        lines.append("- [{}] {}".format(index, excerpt))
    lines.extend(["", "## Contradictions and uncertainty", "", "No contradiction is resolved automatically; compare sources with different claims, dates, or incentives before synthesis.", "", "## Evidence gaps", "", "- {} candidate pages were rejected by duplicate, length, or block-page quality gates.".format(len(rejected)), "", "## Recommended next actions", "", "1. Validate material claims against the numbered primary sources.", "2. Expand only the angles still listed as evidence gaps.", "", "## Sources", ""])
    for index, source in enumerate(sources, 1):
        lines.append("{}. [{}]({}) — score {:.3f}; angle `{}`".format(index, source["source"], source["source"], source["quality_score"], source.get("angle", "unknown")))
    return {"status": status, "question": question, "collected_at": collected_at, "sources": sources, "rejected": rejected, "markdown": "\n".join(lines) + "\n"}


def expand(state: dict, parent: dict, body: str) -> None:
    existing = {item.get("url") for item in state["actions"] if item.get("url")}
    budget = state.get("action_budget", state.get("max_actions", MODES["quick"]))
    remaining = budget - len(state["actions"])
    if budget >= 6 and not state.get('correction_used'):
        remaining = max(0, remaining - 2)
    searches = [item for item in state["actions"] if item["type"] == "search"]
    parent_index = next(index for index, item in enumerate(searches) if item["id"] == parent["id"])
    fetch_slots = max(0, budget - len(searches))
    base, extra = divmod(fetch_slots, len(searches))
    parent_quota = base + (1 if parent_index < extra else 0)
    already_added = sum(
        item["type"] == "fetch" and parent["id"] in item.get("depends_on", [])
        for item in state["actions"]
    )
    allowance = min(remaining, max(0, parent_quota - already_added))
    for url in rank_urls(urls_from_search(body), state.get("question", "")):
        if allowance <= 0:
            break
        if url in existing:
            continue
        state["actions"].append({
            "id": "a{:02d}".format(len(state["actions"]) + 1), "type": "fetch",
            "angle": parent["angle"], "query": None, "url": url, "status": "pending",
            "attempts": 0, "output": None, "error": None, "depends_on": [parent["id"]],
        })
        existing.add(url)
        allowance -= 1


def evidence(state_path: Path, state: dict) -> list[dict]:
    result = []
    for action in state["actions"]:
        if action["status"] != "success" or not action.get("output"):
            continue
        path = state_path.parent / action["output"]
        raw = path.read_text(encoding="utf-8", errors="replace")
        result.append({
            "evidence_id": "ev-{}".format(action["id"]), "angle": action["angle"],
            "source": action.get("url") or action.get("query"), "source_type": action["type"],
            "collected_at": state["updated_at"], "raw_path": action["output"],
            "sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
            "excerpt": raw[:1000],
        })
    write_json(state_path.parent / "evidence.json", result)
    return result


def reports(state_path: Path, state: dict, items: list[dict]) -> dict:
    failed = [item for item in state["actions"] if item["status"] == "failed"]
    rows = []
    for item in items:
        if item["source_type"] != "fetch":
            continue
        raw = (state_path.parent / item["raw_path"]).read_text(encoding="utf-8", errors="replace")
        rows.append({"source": item["source"], "content": raw, "angle": item["angle"], "evidence_id": item["evidence_id"]})
    kept, rejected = quality_gate_sources(rows, state["question"])
    report = build_brief(state["question"], kept, rejected, state["updated_at"])
    report.update({"research_date": state["updated_at"], "scope": {"geography": state["geography"], "freshness": state["freshness"]}, "evidence": items, "failures": failed})
    write_json(state_path.parent / "report.json", report)
    (state_path.parent / "report.md").write_text(report["markdown"], encoding="utf-8")
    return report


def execute(state_path: Path, state: dict, args: argparse.Namespace) -> int:
    token = token_from_environment()
    budget = state.get("action_budget", state.get("max_actions", MODES["quick"]))
    state["action_budget"] = budget
    raw_dir = state_path.parent / "evidence"
    raw_dir.mkdir(parents=True, exist_ok=True)
    successes = 0
    # Discovery can append fetch actions, but the explicit iteration cap keeps
    # execution bounded even if a future planner mutation is malformed.
    for _ in range(max(1, budget * 2)):
        successful = {item["id"] for item in state["actions"] if item["status"] == "success"}
        candidates = [item for item in state["actions"] if item["status"] == "pending" and all(dep in successful for dep in item.get("depends_on", []))]
        if not candidates:
            if len(state['actions']) + 2 <= budget and not state.get('correction_used'):
                preliminary = reports(state_path, state, evidence(state_path, state))
                if preliminary['status'] != 'brief_ready':
                    state['correction_used'] = True
                    state['actions'].append({'id':'a{:02d}'.format(len(state['actions'])+1),'type':'search','angle':'correction','query':state['question'],'url':None,'status':'pending','attempts':0,'output':None,'error':None})
                    write_json(state_path,state)
                    continue
            break
        action = candidates[0]
        action["attempts"] += 1
        result = search(action["query"], token, state["geography"]) if action["type"] == "search" else unlock(action["url"], token, state["geography"], clean_content=True)
        if result["ok"]:
            suffix = "json" if action["type"] == "search" else "txt"
            path = raw_dir / "{}-{}.{}".format(action["id"], action["angle"], suffix)
            material = result["body"] if action["type"] == "search" else content_from_response(result["body"])
            path.write_text(material, encoding="utf-8")
            action.update(status="success", output=str(path.relative_to(state_path.parent)), error=None)
            successes += 1
            if action["type"] == "search":
                expand(state, action, result["body"])
        else:
            action.update(status="failed", error=result["error"])
        state["updated_at"] = now()
        write_json(state_path, state)
        if args.checkpoint and not args.autopilot and successes:
            break
    else:
        state["run_warning"] = "execution_iteration_limit_reached"
        write_json(state_path, state)
    items = evidence(state_path, state)
    report = reports(state_path, state, items)
    print(json.dumps({"status": report["status"], "evidence": len(items), "usable_sources": len(report["sources"]), "state": str(state_path), "report": str(state_path.parent / "report.md")}, ensure_ascii=False))
    return 0 if report["status"] == "brief_ready" else 2


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--question")
    value.add_argument("--geography", default="US")
    value.add_argument("--freshness", default="12 months")
    value.add_argument("--audience", default="decision maker")
    value.add_argument("--decision", default="understand the evidence and decide next actions")
    value.add_argument("--mode", choices=tuple(MODES), default="quick")
    value.add_argument("--max-actions", type=int)
    value.add_argument("--output-dir", type=Path, default=Path("live-research-run"))
    value.add_argument("--resume", type=Path)
    value.add_argument("--retry-failed-safe", action="store_true")
    value.add_argument("--checkpoint", action="store_true")
    value.add_argument("--autopilot", action="store_true")
    value.add_argument("--dry-run", action="store_true")
    return value


def main() -> int:
    args = parser().parse_args()
    try:
        state_path, state = load_state(args)
        if args.dry_run:
            print(json.dumps({"state": str(state_path), "actions": state["actions"]}, ensure_ascii=False, indent=2))
            return 0
        return execute(state_path, state, args)
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
