#!/usr/bin/env python3
import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

VALID_TYPES = {"mistake", "correction", "discovery", "decision", "regression"}
HIGH_REUSE_HINTS = {
    "repeat", "repeated", "again", "preference", "workflow", "regression", "break", "failure",
    "always", "default", "policy", "rule", "remember", "must", "should", "durable", "stable"
}
HIGH_CONFIDENCE_HINTS = {
    "user said", "explicit", "explicitly", "verified", "confirmed", "command output", "fixed",
    "reproduced", "observed", "measured", "file shows", "log shows"
}
WORKSPACE_HINTS = {"workspace", "environment", "tooling", "agent", "openclaw"}
PROJECT_HINTS = {"project", "repo", "repository", "skill"}
CROSS_SESSION_HINTS = {"cross-session", "always", "default", "long-term", "remember", "future"}
TARGET_RULES = [
    ("SOUL.md", {"voice", "tone", "style", "concise", "brief", "persona", "vibe", "humor"}),
    ("AGENTS.md", {"workflow", "process", "guardrail", "safety", "heartbeat", "regression", "procedure"}),
    ("TOOLS.md", {"path", "command", "python", "uv", "model", "tool", "search", "env", "environment"}),
    ("MEMORY.md", {"user", "project", "preference", "decision", "history", "milestone", "remember"}),
]


def parse_jsonl(path: Path):
    items = []
    if not path.exists():
        return items
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            obj.setdefault("_line", i)
            items.append(obj)
        except json.JSONDecodeError as e:
            items.append({
                "id": f"invalid-{i}",
                "type": "discovery",
                "summary": f"Invalid JSON at line {i}",
                "details": str(e),
                "status": "captured",
                "confidence": "low",
                "reuse_value": "low",
                "impact_scope": "single-task",
                "promotion_target_candidates": [],
                "_line": i,
            })
    return items


def count_hints(text: str, hints: set[str]) -> int:
    lower = text.lower()
    return sum(1 for h in hints if h in lower)


def infer_target(item):
    text = " ".join(str(item.get(k, "")) for k in ["type", "summary", "details", "source", "evidence"]).lower()
    targets = []
    for target, hints in TARGET_RULES:
        if any(h in text for h in hints):
            targets.append(target)
    return targets or ["daily-memory"]


def infer_scope(text: str) -> str:
    lower = text.lower()
    if any(k in lower for k in CROSS_SESSION_HINTS):
        return "cross-session"
    if any(k in lower for k in WORKSPACE_HINTS):
        return "workspace"
    if any(k in lower for k in PROJECT_HINTS):
        return "project"
    return "single-task"


def promotion_worthy(item, text: str) -> bool:
    lower = text.lower()
    if item.get("type") in {"correction", "decision", "regression"}:
        return True
    if any(k in lower for k in ["remember this", "should remember", "important", "breakage", "wasted effort"]):
        return True
    return False


def score_item(item):
    text = " ".join(str(item.get(k, "")) for k in ["summary", "details", "evidence", "source"])
    typ = item.get("type", "discovery")
    if typ not in VALID_TYPES:
        typ = "discovery"

    reuse_points = count_hints(text, HIGH_REUSE_HINTS)
    confidence_points = count_hints(text, HIGH_CONFIDENCE_HINTS)

    if typ in {"correction", "regression", "decision"}:
        reuse_points += 2
    if typ in {"correction", "decision"}:
        confidence_points += 1
    if promotion_worthy(item, text):
        reuse_points += 1

    scope = infer_scope(text)
    if scope == "workspace":
        reuse_points += 1
    elif scope == "cross-session":
        reuse_points += 2
        confidence_points += 1

    reuse_value = "high" if reuse_points >= 4 else "medium" if reuse_points >= 2 else "low"
    confidence = "high" if confidence_points >= 3 else "medium" if confidence_points >= 1 else "low"

    item["type"] = typ
    item["reuse_value"] = item.get("reuse_value") or reuse_value
    item["confidence"] = item.get("confidence") or confidence
    item["impact_scope"] = item.get("impact_scope") or scope
    item["promotion_target_candidates"] = item.get("promotion_target_candidates") or infer_target(item)
    item["promotion_worthiness"] = item.get("promotion_worthiness") or (
        "high" if promotion_worthy(item, text) and reuse_value in {"medium", "high"} and confidence in {"medium", "high"}
        else "medium" if promotion_worthy(item, text) or reuse_value == "high"
        else "low"
    )
    item["status"] = "scored"
    item.setdefault("timestamp", datetime.now(timezone.utc).isoformat())
    item.setdefault("id", re.sub(r"[^a-z0-9]+", "-", item.get("summary", "learning").lower()).strip("-")[:48] or "learning")
    return item


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="Input JSONL")
    ap.add_argument("-o", "--output", help="Output JSONL; default stdout")
    args = ap.parse_args()

    items = [score_item(x) for x in parse_jsonl(Path(args.input))]
    lines = [json.dumps(x, ensure_ascii=False) for x in items]
    if args.output:
        Path(args.output).write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    else:
        print("\n".join(lines))


if __name__ == "__main__":
    main()
