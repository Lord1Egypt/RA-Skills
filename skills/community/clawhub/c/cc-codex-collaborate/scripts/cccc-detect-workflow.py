#!/usr/bin/env python3
"""Detect active workflow from planning docs when state.json is incomplete."""
import json
import re
import sys
from pathlib import Path

WORKSPACE = Path("docs/cccc")


def read_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def _split_by_headers(text: str) -> list[tuple[str, str]]:
    """Split text into (header_line, block_content) pairs by ## headers."""
    parts = re.split(r'^(#{1,4}\s+.+)$', text, flags=re.MULTILINE)
    # parts alternates: [before_first_header, header1, content1, header2, content2, ...]
    blocks = []
    i = 1  # skip text before first header
    while i + 1 < len(parts):
        header = parts[i].strip()
        content = parts[i + 1]
        blocks.append((header, content))
        i += 2
    return blocks


def find_milestone_in_backlog() -> dict | None:
    """Find in_progress or first pending milestone in milestone-backlog.md."""
    text = read_file(WORKSPACE / "milestone-backlog.md")
    if not text:
        return None

    # Parse into blocks by markdown headers
    blocks = _split_by_headers(text)

    milestones = []
    for header, content in blocks:
        id_match = re.search(r'\b(M\d+)\b', header, re.IGNORECASE)
        if not id_match:
            continue
        mid = id_match.group(1).upper()
        title = re.sub(r'#{1,4}\s+', '', header)
        title = re.sub(r'\b' + mid + r'\b', '', title).strip().lstrip('—:：- ')
        milestones.append({"id": mid, "title": title, "context": header + "\n" + content})

    if not milestones:
        # Fallback: find bold or plain Mxxx patterns
        for m in re.finditer(r'(?:^|\n)\s*\*{0,2}(M\d+)\*{0,2}[\s:：—\-]*(.*?)(?:\n|$)', text):
            mid = m.group(1).upper()
            title = m.group(2).strip()
            # Get block until next line starting with M or #
            start = m.start()
            next_match = re.search(r'\n\s*(?:#{1,4}\s|M\d+)', text[start + 10:])
            end = start + 10 + next_match.start() if next_match else len(text)
            block = text[start:end]
            milestones.append({"id": mid, "title": title, "context": block})

    if not milestones:
        return None

    # Priority 1: in_progress / 进行中
    for ms in milestones:
        ctx_lower = ms["context"].lower()
        if any(re.search(kw, ctx_lower) for kw in [r'in[\s_.-]?progress', r'进行中', r'活跃', r'active', r'当前']):
            ms["status"] = "in_progress"
            return ms

    # Priority 2: pending / 待执行
    for ms in milestones:
        ctx_lower = ms["context"].lower()
        if any(re.search(kw, ctx_lower) for kw in [r'\bpending\b', r'待执行', r'待办', r'todo', r'not[\s_]?started', r'未开始']):
            ms["status"] = "pending"
            return ms

    # Priority 3: has unchecked task list items
    for ms in milestones:
        if re.search(r'-\s*\[\s*\]', ms["context"]):
            ms["status"] = "pending"
            return ms

    # Priority 4: first not completed
    completed_kw = [r'\bdone\b', r'\bcompleted\b', r'\bpassed\b', r'完成', r'已通过', r'✅']
    for ms in milestones:
        ctx_lower = ms["context"].lower()
        if not any(re.search(kw, ctx_lower) for kw in completed_kw):
            ms["status"] = "pending"
            return ms

    return None


def find_milestone_in_roadmap() -> dict | None:
    """Find current/next milestone in roadmap.md."""
    text = read_file(WORKSPACE / "roadmap.md")
    if not text:
        return None

    current_match = re.search(
        r'(?:current|next|active|当前|下一个|进行中)\s*(?:milestone|phase|里程碑)[:\s]*(M\d+)',
        text, re.IGNORECASE
    )
    if current_match:
        return {"id": current_match.group(1).upper(), "title": "", "status": "in_progress"}

    for match in re.finditer(r'-\s*\[\s*\]\s*(M\d+)', text):
        return {"id": match.group(1).upper(), "title": "", "status": "pending"}

    for match in re.finditer(r'\b(M\d{1,4})\b', text):
        mid = match.group(1).upper()
        context = text[match.start():match.start() + 200].lower()
        if not any(kw in context for kw in ['done', 'completed', 'passed', '完成', '已通过', '✅']):
            return {"id": mid, "title": "", "status": "pending"}

    return None


def find_milestone_in_current_state() -> dict | None:
    """Find current milestone mentioned in current-state.md."""
    text = read_file(WORKSPACE / "current-state.md")
    if not text:
        return None

    for match in re.finditer(
        r'(?:current\s*milestone|当前\s*里程碑|active\s*milestone)[:\s]*(M\d+)',
        text, re.IGNORECASE
    ):
        return {"id": match.group(1).upper(), "title": "", "status": "in_progress"}

    for match in re.finditer(r'\b(M\d{1,4})\b', text):
        mid = match.group(1).upper()
        context = text[match.start():match.start() + 100].lower()
        if any(kw in context for kw in ['current', 'active', 'in_progress', '当前', '进行中']):
            return {"id": mid, "title": "", "status": "in_progress"}

    return None


def has_open_questions() -> bool:
    """Check if open-questions.md has unresolved items."""
    text = read_file(WORKSPACE / "open-questions.md")
    if not text:
        return False
    if re.search(r'-\s*\[\s*\]', text):
        return True
    if text.count('?') > 2 or text.count('？') > 2:
        return True
    return False


def has_planning_docs() -> bool:
    """Check if non-trivial planning docs exist."""
    for f in ["roadmap.md", "milestone-backlog.md", "current-state.md"]:
        content = read_file(WORKSPACE / f)
        if content and len(content.strip()) > 50:
            if not content.strip().startswith("# ") or len(content.strip()) > 100:
                return True
    return False


def detect_workflow() -> dict:
    """Main detection logic. Returns action dict."""
    result = {
        "action": "needs_task",
        "reason": "No task, roadmap, or milestone backlog found.",
        "milestone_id": None,
        "milestone_source": None,
        "state_repaired": False,
    }

    state_path = WORKSPACE / "state.json"
    state = {}
    if state_path.exists():
        try:
            state = json.loads(state_path.read_text())
        except Exception:
            pass

    status = state.get("status", "")
    pause_reason = state.get("pause_reason")
    current_milestone_id = state.get("current_milestone_id")

    # ── Check A: Terminal states ──
    if status in ("DONE", "COMPLETED", "FAILED"):
        result["action"] = "done"
        result["reason"] = f"Current workflow status is {status}."
        return result

    # ── Check B: Paused states ──
    paused_statuses = {
        "PAUSED_FOR_HUMAN", "NEEDS_HUMAN", "PAUSED_FOR_CODEX",
        "PAUSED_FOR_SYSTEM", "NEEDS_SECRET", "SENSITIVE_OPERATION",
        "UNSAFE", "FAIL_UNCLEAR", "REVIEW_THRESHOLD_EXCEEDED",
    }
    if status in paused_statuses:
        result["action"] = "needs_resume"
        result["reason"] = f"Workflow is paused at {status}."
        return result

    # ── Check C: Active state with current milestone ──
    if current_milestone_id and str(current_milestone_id).lower() not in ("null", "none", ""):
        result["action"] = "continue_now"
        result["reason"] = f"Active milestone {current_milestone_id} found in state.json."
        result["milestone_id"] = current_milestone_id
        return result

    # ── Check D: Has pause_reason ──
    if pause_reason and str(pause_reason).lower() not in ("null", "none", ""):
        result["action"] = "needs_resume"
        result["reason"] = "Workflow has a pause_reason set."
        return result

    # ── Check E: Has open questions ──
    if has_open_questions():
        result["action"] = "needs_resume"
        result["reason"] = "Open questions exist. Run /cc-codex-collaborate resume."
        return result

    # ── Check F: Try to recover milestone from docs ──
    ms = find_milestone_in_backlog()
    if ms:
        result["action"] = "continue_now"
        result["reason"] = f"Recovered active milestone {ms['id']} from docs/cccc/milestone-backlog.md."
        result["milestone_id"] = ms["id"]
        result["milestone_source"] = "milestone-backlog.md"
        result["state_repaired"] = True
        return result

    ms = find_milestone_in_current_state()
    if ms:
        result["action"] = "continue_now"
        result["reason"] = f"Recovered active milestone {ms['id']} from docs/cccc/current-state.md."
        result["milestone_id"] = ms["id"]
        result["milestone_source"] = "current-state.md"
        result["state_repaired"] = True
        return result

    ms = find_milestone_in_roadmap()
    if ms:
        result["action"] = "continue_now"
        result["reason"] = f"Recovered milestone {ms['id']} from docs/cccc/roadmap.md."
        result["milestone_id"] = ms["id"]
        result["milestone_source"] = "roadmap.md"
        result["state_repaired"] = True
        return result

    # ── Check G: Planning docs exist but no milestone found ──
    if has_planning_docs():
        result["action"] = "needs_resume"
        result["reason"] = "Planning docs exist, but current milestone is missing from state.json. Run /cc-codex-collaborate resume."
        return result

    # ── Check H: Nothing found ──
    return result


def repair_state(milestone_id: str, source: str) -> None:
    """Repair state.json with recovered milestone."""
    from datetime import datetime, timezone

    state_path = WORKSPACE / "state.json"
    if not state_path.exists():
        return

    state = json.loads(state_path.read_text())
    now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

    state["current_milestone_id"] = milestone_id
    state["stop_hook_continuations"] = 0
    state["pause_reason"] = None

    if state.get("status") in ("SETUP_COMPLETE", "NOT_INITIALIZED", None, ""):
        state["status"] = "READY_TO_CONTINUE"

    state["last_state_repaired_at"] = now
    state["last_state_repair_reason"] = f"Recovered current milestone from docs/cccc/{source}"

    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "detect"

    if action == "detect":
        result = detect_workflow()
        if result["state_repaired"] and result["milestone_id"]:
            repair_state(result["milestone_id"], result["milestone_source"] or "unknown")
        print(json.dumps(result, ensure_ascii=False))

    elif action == "find-milestone":
        ms = find_milestone_in_backlog()
        if not ms:
            ms = find_milestone_in_current_state()
        if not ms:
            ms = find_milestone_in_roadmap()
        if ms:
            print(json.dumps(ms, ensure_ascii=False))
        else:
            print("null")

    elif action == "has-planning-docs":
        print("true" if has_planning_docs() else "false")

    else:
        print(f"Unknown action: {action}", file=sys.stderr)
        sys.exit(1)
