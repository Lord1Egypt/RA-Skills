#!/usr/bin/env python3
"""Rehydrate state.json from docs/cccc planning docs, reviews, and git history."""
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR", subprocess.getoutput("git rev-parse --show-toplevel 2>/dev/null || pwd")).strip())
WORKSPACE = ROOT / "docs/cccc"


def read_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def read_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def find_milestone_in_backlog() -> dict | None:
    text = read_file(WORKSPACE / "milestone-backlog.md")
    if not text:
        return None
    blocks = _split_by_headers(text)
    candidates = []
    for header, content in blocks:
        id_match = re.search(r'\b(M\d+[A-Z]?)\b', header, re.IGNORECASE)
        if not id_match:
            continue
        mid = id_match.group(1).upper()
        status = "unknown"
        lower = (header + "\n" + content).lower()
        if "in_progress" in lower or "in progress" in lower or "进行中" in lower:
            status = "in_progress"
        elif "pending" in lower or "待执行" in lower or "todo" in lower:
            status = "pending"
        elif "completed" in lower or "pass" in lower or "完成" in lower:
            status = "completed"
        candidates.append({"id": mid, "status": status, "source": "milestone-backlog.md"})

    # Priority: in_progress > pending > first not completed
    for s in ("in_progress", "pending"):
        for c in candidates:
            if c["status"] == s:
                return c
    for c in candidates:
        if c["status"] != "completed":
            return c
    return None


def find_milestone_in_roadmap() -> dict | None:
    text = read_file(WORKSPACE / "roadmap.md")
    if not text:
        return None
    blocks = _split_by_headers(text)
    for header, content in blocks:
        id_match = re.search(r'\b(M\d+[A-Z]?)\b', header, re.IGNORECASE)
        if not id_match:
            continue
        mid = id_match.group(1).upper()
        lower = (header + "\n" + content).lower()
        if "in_progress" in lower or "in progress" in lower or "current" in lower or "进行中" in lower:
            return {"id": mid, "status": "in_progress", "source": "roadmap.md"}
    return None


def find_milestone_in_current_state() -> dict | None:
    text = read_file(WORKSPACE / "current-state.md")
    if not text:
        return None
    m = re.search(r'\b(M\d+[A-Z]?)\b.*?(?:current|当前|active|active milestone)', text, re.IGNORECASE)
    if m:
        return {"id": m.group(1).upper(), "status": "in_progress", "source": "current-state.md"}
    return None


def find_last_reviewed_milestone() -> dict | None:
    """Find the last milestone that passed Codex review, return the next one."""
    reviews_dir = WORKSPACE / "reviews" / "milestones"
    if not reviews_dir.exists():
        return None
    passed = []
    for f in sorted(reviews_dir.glob("*.json")):
        data = read_json(f)
        if data and data.get("status") == "pass":
            mid = data.get("milestone_id", "")
            if mid:
                passed.append(mid)
    if not passed:
        return None
    last_passed = passed[-1]
    # Try to find the next milestone in backlog
    text = read_file(WORKSPACE / "milestone-backlog.md")
    if text:
        all_ids = re.findall(r'\b(M\d+[A-Z]?)\b', text, re.IGNORECASE)
        all_ids = list(dict.fromkeys(mid.upper() for mid in all_ids))
        if last_passed.upper() in all_ids:
            idx = all_ids.index(last_passed.upper())
            if idx + 1 < len(all_ids):
                return {"id": all_ids[idx + 1], "status": "pending",
                        "source": f"after reviewed milestone {last_passed}"}
    return None


def check_open_questions() -> bool:
    text = read_file(WORKSPACE / "open-questions.md")
    if not text:
        return False
    # Check for unresolved questions (not marked as resolved)
    lines = text.split("\n")
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- [ ]") or stripped.startswith("* [ ]"):
            return True
    return False


def has_planning_docs() -> bool:
    for name in ("roadmap.md", "milestone-backlog.md"):
        if (WORKSPACE / name).exists():
            return True
    return False


def get_completed_from_reviews() -> list[str]:
    reviews_dir = WORKSPACE / "reviews" / "milestones"
    if not reviews_dir.exists():
        return []
    completed = []
    for f in sorted(reviews_dir.glob("*.json")):
        data = read_json(f)
        if data and data.get("status") == "pass":
            mid = data.get("milestone_id", "")
            if mid:
                completed.append(mid.upper())
    return list(dict.fromkeys(completed))


def rehydrate(template_path: Path | None = None) -> dict:
    """Rehydrate state from available sources. Returns new state dict."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    sources = []
    confidence = "low"

    # Start from existing state first (preserves Codex gate statuses, task, etc.)
    # Then fill missing fields from template
    existing_state = read_json(WORKSPACE / "state.json") or {}
    template_state = read_json(template_path) if template_path and template_path.exists() else {}
    state = {**template_state, **existing_state}

    # Preserve runtime state that shouldn't be reset
    preserved_keys = {
        "skill_name", "skill_version", "workspace", "workspace_schema_version",
        "task", "user_language", "language_source",
        "project_context_status", "created_at",
        "codex_plan_review_status", "codex_final_review_status",
        "last_codex_plan_review_file", "last_codex_milestone_review_file",
        "last_codex_final_review_file", "codex_unavailable_reason",
    }
    preserved = {k: state[k] for k in preserved_keys if k in state}

    # Reset mutable fields
    state.update({
        "status": "SETUP_COMPLETE",
        "current_milestone_id": None,
        "pause_reason": None,
        "stop_hook_continuations": 0,
        "review_round_current": 0,
        "fix_attempts_current": 0,
        "completed_milestones": [],
        "blocked_milestones": [],
        "known_risks": state.get("known_risks", []),
        "last_context_update": None,
        "roadmap_status": state.get("roadmap_status", "not_reviewed"),
        "current_milestone_codex_review_status": "not_run",
        "current_milestone_codex_review_file": None,
        "previous_status": None,
        "resume_reason": None,
        "resume_strategy": None,
        "last_resumed_at": None,
        "last_human_decision": None,
    })

    # Restore preserved values
    state.update(preserved)

    # Rehydrate milestone detection
    milestone = None

    # 1. Check existing state (if it had a valid milestone)
    old_mid = state.get("current_milestone_id")
    if old_mid:
        milestone = {"id": old_mid, "status": "in_progress", "source": "state.json (previous)"}
        sources.append("state.json")
        confidence = "medium"

    # 2. Check planning docs
    if not milestone:
        milestone = find_milestone_in_backlog()
        if milestone:
            sources.append("milestone-backlog.md")
            confidence = "high"

    if not milestone:
        milestone = find_milestone_in_roadmap()
        if milestone:
            sources.append("roadmap.md")
            confidence = "medium"

    if not milestone:
        milestone = find_milestone_in_current_state()
        if milestone:
            sources.append("current-state.md")
            confidence = "medium"

    # 3. Check review history
    if not milestone:
        milestone = find_last_reviewed_milestone()
        if milestone:
            sources.append("reviews/milestones")
            confidence = "medium"

    # Set milestone
    if milestone:
        state["current_milestone_id"] = milestone["id"]
        state["status"] = "READY_TO_CONTINUE"
    else:
        # No milestone found
        if has_planning_docs():
            state["status"] = "NEEDS_HUMAN"
            state["pause_reason"] = "Planning docs exist but current milestone could not be determined. Run /cc-codex-collaborate resume to select a milestone."
            confidence = "low"
        else:
            state["status"] = "SETUP_COMPLETE"
            confidence = "low"

    # Check open questions
    if check_open_questions():
        if state["status"] not in ("NEEDS_HUMAN", "PAUSED_FOR_HUMAN"):
            state["status"] = "NEEDS_HUMAN"
            if not state["pause_reason"]:
                state["pause_reason"] = "Open questions exist in open-questions.md"

    # Restore completed milestones from review history (only if verified by Codex)
    completed = get_completed_from_reviews()
    if completed:
        state["completed_milestones"] = completed

    # Don't override Codex gate statuses
    if state.get("codex_plan_review_status") == "pass":
        state["roadmap_status"] = "codex_approved"

    # Rehydrate metadata
    state["last_state_rehydrated_at"] = now
    state["last_state_rehydrate_sources"] = sources
    state["last_state_rehydrate_reason"] = "reset state"
    state["rehydrate_confidence"] = confidence
    state["updated_at"] = now

    return state


def main():
    template_path = WORKSPACE.parent.parent / ".claude/skills/cc-codex-collaborate/templates/cccc/state.template.json"
    state = rehydrate(template_path)

    # Output as JSON to stdout
    print(json.dumps(state, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
