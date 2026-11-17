"""Normalize action outputs, build traceable reports, and compare evidence snapshots."""

from __future__ import annotations

from datetime import datetime, timezone
import csv
import hashlib
import json
from pathlib import Path
import re
from typing import Any


URL_PATTERN = re.compile(r"https?://[^\s\"'<>]+")


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def first_url(text: str) -> str | None:
    match = URL_PATTERN.search(text)
    return match.group(0).rstrip(".,);]") if match else None


def normalize(state_path: Path) -> list[dict[str, Any]]:
    state = json.loads(state_path.read_text(encoding="utf-8"))
    evidence = []
    for action in state["actions"]:
        output = action.get("output")
        if action.get("status") != "success" or not output:
            continue
        raw_path = state_path.parent / output
        if not raw_path.exists():
            continue
        raw = raw_path.read_text(encoding="utf-8", errors="replace")
        action_type = action.get("type", "discover")
        url = action.get("url") or first_url(raw)
        source_type = "search_discovery"
        if action_type == "scrape":
            source_type = "structured_platform"
        elif action_type == "fetch":
            official_domain = (state.get("domains") or {}).get(action["entity"], "").lower()
            source_type = "first_party" if official_domain and url and official_domain in url.lower() else "external_page"
        evidence.append({
            "evidence_id": f'ev-{len(evidence) + 1:04d}',
            "action_id": action["id"],
            "entity": action["entity"],
            "module": action["module"],
            "source": {
                "url": url,
                "query": action.get("query"),
                "source_type": source_type,
                "observed_at": now(),
            },
            "content": {
                "raw_path": output,
                "sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
                "excerpt": re.sub(r"\s+", " ", raw)[:500],
            },
            "quality": {
                "authority": "high" if source_type == "first_party" else "medium",
                "directness": "low" if source_type == "search_discovery" else "high",
            },
            "status": "verified" if source_type != "search_discovery" else "unverified",
        })
    target = state_path.parent / "evidence.json"
    target.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return evidence


def load_findings(path: Path | None, evidence_ids: set[str]) -> list[dict[str, Any]]:
    if not path:
        return []
    findings = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(findings, list):
        raise ValueError("findings must be a JSON array")
    for finding in findings:
        missing = set(finding.get("evidence_ids", [])) - evidence_ids
        if missing:
            raise ValueError(f'dangling evidence IDs in {finding.get("finding_id", "finding")}: {sorted(missing)}')
    return findings


def build_report(state_path: Path, findings_path: Path | None = None) -> tuple[Path, Path]:
    state = json.loads(state_path.read_text(encoding="utf-8"))
    evidence_path = state_path.parent / "evidence.json"
    evidence = json.loads(evidence_path.read_text(encoding="utf-8")) if evidence_path.exists() else normalize(state_path)
    findings = load_findings(findings_path, {item["evidence_id"] for item in evidence})
    failures = [
        {"action_id": action["id"], "capability": action.get("capability"), "error": action.get("error")}
        for action in state["actions"] if action.get("status") == "failed"
    ]
    report = {
        "research_date": now()[:10],
        "scope": {key: state.get(key) for key in ("company", "competitors", "decision", "audience", "modules", "geography", "freshness", "mode")},
        "evidence": evidence,
        "findings": findings,
        "failures": failures,
        "recommendations": [finding["recommendation"] for finding in findings if finding.get("recommendation")],
        "status": "complete" if findings else "evidence_ready_analysis_required",
    }
    json_path = state_path.parent / "report.json"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    csv_path = state_path.parent / "evidence.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["evidence_id", "entity", "module", "source_type", "source", "observed_at", "raw_path", "sha256"])
        writer.writeheader()
        for item in evidence:
            writer.writerow({
                "evidence_id": item["evidence_id"],
                "entity": item["entity"],
                "module": item["module"],
                "source_type": item["source"]["source_type"],
                "source": item["source"].get("url") or item["source"].get("query"),
                "observed_at": item["source"]["observed_at"],
                "raw_path": item["content"]["raw_path"],
                "sha256": item["content"]["sha256"],
            })
    lines = [
        f'# Competitive intelligence report — {report["research_date"]}', "",
        "## Scope and assumptions", "",
        f'- Company: {state["company"]}',
        f'- Competitors: {", ".join(state["competitors"])}',
        f'- Decision: {state.get("decision", "")}',
        f'- Audience: {state.get("audience", "")}',
        f'- Modules: {", ".join(state["modules"])}',
        f'- Geography: {state.get("geography", "")}',
        f'- Freshness: {state.get("freshness", "")}', "",
        "## Evidence", "",
        "| ID | Entity | Module | Type | Source | Confidence |", "|---|---|---|---|---|---|",
    ]
    for item in evidence:
        source = item["source"].get("url") or item["source"].get("query") or "—"
        if str(source).startswith("http"):
            source = f'[source]({source})'
        confidence = "high" if item["quality"]["directness"] == "high" else "low"
        lines.append(f'| {item["evidence_id"]} | {item["entity"]} | {item["module"]} | {item["source"]["source_type"]} | {source} | {confidence} |')
    lines.extend(["", "## Findings", ""])
    if findings:
        for finding in findings:
            lines.extend([
                f'### {finding["title"]}', "",
                f'- Fact: {finding["fact"]}',
                f'- Inference: {finding["inference"]}',
                f'- Confidence: {finding["confidence"]}',
                f'- Evidence: {", ".join(finding["evidence_ids"])}',
                f'- Priority: {finding["priority"]}',
                f'- Recommendation: {finding["recommendation"]}', "",
            ])
    else:
        lines.extend(["Analysis required: inspect raw evidence and provide findings with valid evidence IDs.", ""])
    lines.extend(["## Limitations and failures", ""])
    lines.extend([f'- {item["action_id"]}: {item["error"]}' for item in failures] or ["- No collection failure recorded."])
    lines.extend(["", "## Recommendations", ""])
    lines.extend([f'- {item}' for item in report["recommendations"]] or ["- Pending evidence-grounded analysis."])
    markdown_path = state_path.parent / "report.md"
    markdown_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return markdown_path, json_path


def compare(old_path: Path, new_path: Path) -> list[dict[str, Any]]:
    old = {item["action_id"]: item for item in json.loads(old_path.read_text(encoding="utf-8"))}
    new = {item["action_id"]: item for item in json.loads(new_path.read_text(encoding="utf-8"))}
    changes = []
    for action_id in sorted(set(old) | set(new)):
        before, after = old.get(action_id), new.get(action_id)
        if before is None or after is None or before["content"]["sha256"] != after["content"]["sha256"]:
            changes.append({
                "action_id": action_id,
                "change_type": "added" if before is None else "removed" if after is None else "content_changed",
                "before_sha256": before and before["content"]["sha256"],
                "after_sha256": after and after["content"]["sha256"],
                "detected_at": now(),
            })
    return changes
