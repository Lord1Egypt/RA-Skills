#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

PRIORITY = {"low": 0, "medium": 1, "high": 2}
ANCHOR_CHOICES = {
    "SOUL.md": ["## Core Truths", "## Vibe", "## Continuity"],
    "AGENTS.md": ["## Every Session", "## Safety", "## Tools", "## Heartbeats"],
    "TOOLS.md": ["## Search Policy", "## 🐍 Python & UV Policy", "## What Goes Here"],
    "MEMORY.md": ["## 📅 最近提炼记录", "## Learned Records"],
}


def load_jsonl(path: Path):
    out = []
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def should_promote(item):
    return (
        PRIORITY.get(item.get("reuse_value", "low"), 0) >= 1
        and PRIORITY.get(item.get("confidence", "low"), 0) >= 1
        and item.get("promotion_worthiness", "medium") != "low"
    )


def pick_target(item):
    targets = item.get("promotion_target_candidates") or ["daily-memory"]
    return targets[0]


def choose_anchor(target_file: str, item: dict):
    summary = (item.get("summary") or "").lower()
    details = (item.get("details") or "").lower()
    blob = f"{summary} {details}"

    if target_file == "SOUL.md":
        return "## Core Truths" if any(k in blob for k in ["voice", "tone", "style", "brief", "concise", "persona"]) else "## Vibe"
    if target_file == "AGENTS.md":
        if any(k in blob for k in ["heartbeat", "periodic", "check"]):
            return "## Heartbeats"
        if any(k in blob for k in ["safety", "guardrail", "destructive"]):
            return "## Safety"
        return "## Every Session"
    if target_file == "TOOLS.md":
        if any(k in blob for k in ["python", "venv", "pip", "uv"]):
            return "## 🐍 Python & UV Policy"
        if any(k in blob for k in ["search", "model", "tool", "command", "path"]):
            return "## Search Policy"
        return "## What Goes Here"
    if target_file == "MEMORY.md":
        return "## 📅 最近提炼记录"
    return None


def make_entry(item: dict):
    summary = item.get("summary", "").strip()
    details = item.get("details", "").strip()
    evidence = item.get("evidence", "").strip()
    base = f"- {summary}"
    if details:
        base += f" - {details}"
    if evidence:
        base += f" | evidence: {evidence}"
    return base


def draft_patch(item):
    target = pick_target(item)
    rationale = (
        f"{item.get('type', 'learning')} | reuse={item.get('reuse_value', 'low')} | "
        f"confidence={item.get('confidence', 'low')} | scope={item.get('impact_scope', 'single-task')}"
    )
    anchor = choose_anchor(target, item)
    patch = {
        "id": item.get("id"),
        "target_file": target,
        "rationale": rationale,
        "confidence_note": item.get("confidence", "low"),
        "approval_required": True,
        "approved": False,
        "review_status": "pending",
        "suggested_entry": make_entry(item),
        "old_text": None,
        "new_text": None,
        "anchor": anchor,
        "insert_mode": "after-anchor" if anchor else "append",
        "source_summary": item.get("summary", ""),
    }

    if target == "MEMORY.md":
        entry = item.get("summary", "").strip()
        details = item.get("details", "").strip()
        patch["suggested_entry"] = f"| {item.get('timestamp', '')[:10]} | {item.get('source', 'unknown')} | {entry}" + (f" - {details} |" if details else " |")
    return patch


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="Scored JSONL")
    ap.add_argument("-o", "--output", help="Output JSON")
    args = ap.parse_args()

    items = load_jsonl(Path(args.input))
    patches = [draft_patch(x) for x in items if should_promote(x)]
    result = {
        "new_candidates": len(items),
        "high_priority": sum(
            1 for x in items
            if x.get("reuse_value") == "high" and x.get("confidence") in {"medium", "high"}
        ),
        "merge_groups": 0,
        "patch_candidates": patches,
        "needs_human_review": True,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
