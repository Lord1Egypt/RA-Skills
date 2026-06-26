#!/usr/bin/env python3
"""Session feedback analyzer for the auto-improvement pipeline.

Parses Claude Code session JSONL files, detects skill invocations,
classifies user responses (correction/acceptance/partial) within a
3-turn influence window, and outputs feedback.jsonl for the generator.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Iterator

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from lib.common import utc_now_iso, write_json  # noqa: E402

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

CORRECTION_KEYWORDS_ZH = ("不对", "错了", "不是这样", "重新来", "换个方案", "不行", "有问题")
CORRECTION_KEYWORDS_EN = ("wrong", "incorrect", "no,", "no ", "redo", "try again", "that's not")
REDO_KEYWORDS = ("重新来", "redo", "try again", "换个方案", "再来一次", "重做")
ACCEPTANCE_KEYWORDS_ZH = ("好", "可以", "对的", "继续", "没问题", "行", "好的")
ACCEPTANCE_KEYWORDS_EN = ("looks good", "lgtm", "perfect", "correct", "yes", "great", "thanks")
REVERT_COMMANDS = ("git checkout", "git restore", "git reset")

DIMENSION_KEYWORDS = {
    "accuracy": ("naming", "format", "style", "命名", "格式", "风格", "拼写", "typo"),
    "coverage": ("missing", "forgot", "没考虑", "缺少", "漏了", "incomplete"),
    "reliability": ("again", "又", "重复", "inconsistent", "不稳定"),
    "efficiency": ("slow", "verbose", "太慢", "太多", "太长", "冗余"),
    "security": ("security", "secret", "安全", "密钥", "token", "credential"),
    "trigger_quality": ("wrong skill", "不该触发", "shouldn't trigger", "错误的skill"),
}

INFLUENCE_WINDOW = 3  # max user turns to scan after skill invocation


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class SkillInvocation:
    invocation_id: str
    skill_id: str
    timestamp: str
    message_index: int


@dataclass
class FeedbackEvent:
    event_id: str
    timestamp: str
    session_id: str
    skill_id: str
    invocation_uuid: str
    outcome: str  # "correction" | "acceptance" | "partial"
    confidence: float
    correction_type: str | None  # "rejection" | "revert" | "redo" | "partial" | None
    user_message_snippet: str
    turns_to_feedback: int
    ai_tools_used: list[str]
    dimension_hint: str | None


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze Claude Code sessions for skill feedback signals",
    )
    parser.add_argument(
        "--session-dir",
        default=str(Path.home() / ".claude" / "projects"),
        help="Root directory for session JSONL files",
    )
    parser.add_argument(
        "--output",
        default="feedback-store/feedback.jsonl",
        help="Output path for feedback JSONL",
    )
    parser.add_argument(
        "--no-snippets",
        action="store_true",
        help="Omit user message snippets from output",
    )
    parser.add_argument(
        "--skill-filter",
        help="Only analyze invocations of this skill",
    )
    parser.add_argument(
        "--min-invocations",
        type=int,
        default=5,
        help="Minimum invocations before computing metrics",
    )
    return parser.parse_args(argv)


def iter_session_files(session_dir: Path) -> Iterator[Path]:
    """Yield session JSONL files, skipping test/tmp directories."""
    for path in session_dir.rglob("*.jsonl"):
        path_str = str(path)
        if "pytest" in path_str or "/tmp/" in path_str:
            continue
        if "/subagents/" in path_str:
            continue
        yield path


def parse_session(path: Path) -> list[dict[str, Any]]:
    """Parse a session JSONL file into a list of message dicts."""
    messages: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                messages.append(json.loads(line))
            except json.JSONDecodeError:
                continue  # skip malformed lines
    return messages


def extract_session_id(path: Path) -> str:
    """Extract session ID from the JSONL filename."""
    return path.stem


def extract_project(path: Path) -> str:
    """Extract project name from the directory structure."""
    return path.parent.name


# ---------------------------------------------------------------------------
# Skill invocation detection
# ---------------------------------------------------------------------------


def detect_skill_invocations(messages: list[dict[str, Any]]) -> list[SkillInvocation]:
    """Detect skill invocations via tool_use or slash commands."""
    invocations: list[SkillInvocation] = []

    for idx, entry in enumerate(messages):
        msg_type = entry.get("type")
        uuid = entry.get("uuid", "")
        timestamp = entry.get("timestamp", "")

        # Path A: assistant tool_use with name=="Skill"
        if msg_type == "assistant":
            content = entry.get("message", {}).get("content", [])
            if isinstance(content, list):
                for block in content:
                    if (isinstance(block, dict)
                            and block.get("type") == "tool_use"
                            and block.get("name") == "Skill"):
                        skill_id = block.get("input", {}).get("skill", "")
                        if skill_id:
                            invocations.append(SkillInvocation(
                                invocation_id=uuid,
                                skill_id=skill_id,
                                timestamp=timestamp,
                                message_index=idx,
                            ))

        # Path B: system local_command with <command-name>
        if msg_type == "system" and entry.get("subtype") == "local_command":
            content_str = str(entry.get("content", ""))
            match = re.search(r"<command-name>/?([\w-]+)</command-name>", content_str)
            if match:
                skill_id = match.group(1)
                # Skip built-in commands
                if skill_id not in ("help", "clear", "resume", "compact", "config"):
                    invocations.append(SkillInvocation(
                        invocation_id=uuid,
                        skill_id=skill_id,
                        timestamp=timestamp,
                        message_index=idx,
                    ))

    return invocations


# ---------------------------------------------------------------------------
# Outcome classification
# ---------------------------------------------------------------------------


def _extract_user_text(entry: dict[str, Any]) -> str:
    """Extract text content from a user message entry."""
    msg = entry.get("message", {})
    content = msg.get("content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
            elif isinstance(block, str):
                parts.append(block)
        return " ".join(parts)
    return ""


def _detect_revert(messages: list[dict[str, Any]], start_idx: int, end_idx: int) -> bool:
    """Check if a git revert command appears in the window."""
    for entry in messages[start_idx:end_idx]:
        if entry.get("type") != "assistant":
            continue
        content = entry.get("message", {}).get("content", [])
        if not isinstance(content, list):
            continue
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "tool_use" and block.get("name") == "Bash":
                cmd = block.get("input", {}).get("command", "")
                if any(rc in cmd for rc in REVERT_COMMANDS):
                    return True
    return False


def _collect_ai_tools(messages: list[dict[str, Any]], start_idx: int, end_idx: int) -> list[str]:
    """Collect tool names used by the assistant in the window."""
    tools: set[str] = set()
    for entry in messages[start_idx:end_idx]:
        if entry.get("type") != "assistant":
            continue
        content = entry.get("message", {}).get("content", [])
        if not isinstance(content, list):
            continue
        for block in content:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                name = block.get("name", "")
                if name:
                    tools.add(name)
    return sorted(tools)


def classify_outcome(
    messages: list[dict[str, Any]],
    invocation: SkillInvocation,
    next_invocation_idx: int | None = None,
) -> FeedbackEvent | None:
    """Classify user response after a skill invocation.

    Returns None for ambiguous outcomes (excluded from metrics).
    """
    start_idx = invocation.message_index + 1
    window_end = next_invocation_idx or len(messages)

    # Collect user messages within the influence window
    # Skip system-injected skill loading messages (contain "Base directory for this skill")
    SYSTEM_INJECT_MARKERS = ("Base directory for this skill", "<command-name>", "SKILL.md", "---\nname:")
    user_turns: list[tuple[int, dict[str, Any]]] = []
    for idx in range(start_idx, window_end):
        entry = messages[idx]
        if entry.get("type") == "user":
            text = _extract_user_text(entry)
            # Skip if this is a system-injected skill prompt, not real user input
            if any(marker in text for marker in SYSTEM_INJECT_MARKERS):
                continue
            user_turns.append((idx, entry))
            if len(user_turns) >= INFLUENCE_WINDOW:
                break

    if not user_turns:
        return None  # session ended, ambiguous

    # Check AI tool usage (if no tools used after skill load, exclude)
    ai_tools = _collect_ai_tools(messages, start_idx, window_end)

    # Classify based on first user response
    first_turn_idx, first_turn = user_turns[0]
    user_text = _extract_user_text(first_turn)
    lowered = user_text.lower()
    turns_to_feedback = 1

    # Check for revert in the window
    if _detect_revert(messages, start_idx, min(window_end, start_idx + 20)):
        return _build_event(
            invocation, "correction", 0.9, "revert", user_text,
            turns_to_feedback, ai_tools,
        )

    # Check correction signals across all user turns in window
    QUALIFIER_WORDS = ("但是", "不过", "但", "but", "however", "except", "though")
    for turn_num, (_, turn) in enumerate(user_turns, 1):
        text = _extract_user_text(turn)
        text_lower = text.lower()

        has_correction_kw = any(kw in text_lower for kw in CORRECTION_KEYWORDS_ZH + CORRECTION_KEYWORDS_EN)
        has_acceptance_kw = any(kw in text_lower for kw in ACCEPTANCE_KEYWORDS_ZH + ACCEPTANCE_KEYWORDS_EN)
        has_qualifier = any(q in text_lower for q in QUALIFIER_WORDS)

        # Partial: acceptance + qualifier ("可以，但是X要改") or correction + qualifier
        if has_qualifier and (has_acceptance_kw or has_correction_kw):
            return _build_event(
                invocation, "partial", 0.7, "partial", text,
                turn_num, ai_tools,
            )

        # Explicit rejection
        if has_correction_kw:
            return _build_event(
                invocation, "correction", 0.9, "rejection", text,
                turn_num, ai_tools,
            )

        # Redo request
        if any(kw in text_lower for kw in REDO_KEYWORDS):
            return _build_event(
                invocation, "correction", 0.9, "redo", text,
                turn_num, ai_tools,
            )

    # Check acceptance signals on first turn
    if any(kw in lowered for kw in ACCEPTANCE_KEYWORDS_ZH + ACCEPTANCE_KEYWORDS_EN):
        return _build_event(
            invocation, "acceptance", 0.8, None, user_text,
            turns_to_feedback, ai_tools,
        )

    # Silent continuation: user gives a new instruction (no correction of prior)
    # Heuristic: if the user message is long and doesn't reference the skill's output
    if len(user_text) > 20 and not any(kw in lowered for kw in ("?", "？")):
        return _build_event(
            invocation, "acceptance", 0.6, None, user_text,
            turns_to_feedback, ai_tools,
        )

    return None  # ambiguous


def _build_event(
    invocation: SkillInvocation,
    outcome: str,
    confidence: float,
    correction_type: str | None,
    user_text: str,
    turns_to_feedback: int,
    ai_tools: list[str],
) -> FeedbackEvent:
    event_id = hashlib.sha256(
        f"{invocation.invocation_id}:{invocation.skill_id}".encode()
    ).hexdigest()[:16]
    snippet = " ".join(user_text.split())[:200]
    dimension = attribute_dimension(snippet)
    return FeedbackEvent(
        event_id=event_id,
        timestamp=invocation.timestamp,
        session_id="",  # filled by caller
        skill_id=invocation.skill_id,
        invocation_uuid=invocation.invocation_id,
        outcome=outcome,
        confidence=confidence,
        correction_type=correction_type,
        user_message_snippet=snippet,
        turns_to_feedback=turns_to_feedback,
        ai_tools_used=ai_tools,
        dimension_hint=dimension,
    )


# ---------------------------------------------------------------------------
# Dimension attribution
# ---------------------------------------------------------------------------


def attribute_dimension(snippet: str) -> str | None:
    """Heuristic mapping of correction text to evaluator dimensions."""
    lowered = snippet.lower()
    for dimension, keywords in DIMENSION_KEYWORDS.items():
        if any(kw in lowered for kw in keywords):
            return dimension
    return None


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------


def write_feedback_jsonl(
    events: list[FeedbackEvent],
    output_path: Path,
    no_snippets: bool = False,
) -> Path:
    """Append feedback events to a JSONL file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Read existing event IDs to avoid duplicates
    existing_ids: set[str] = set()
    if output_path.exists():
        with output_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        existing_ids.add(json.loads(line).get("event_id", ""))
                    except json.JSONDecodeError:
                        continue

    new_count = 0
    with output_path.open("a", encoding="utf-8") as f:
        for event in events:
            if event.event_id in existing_ids:
                continue
            d = asdict(event)
            if no_snippets:
                d["user_message_snippet"] = ""
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
            new_count += 1

    return output_path


def archive_old_events(feedback_path: Path, archive_dir: Path, days: int = 90) -> int:
    """Move events older than `days` to archive. Returns count archived."""
    if not feedback_path.exists():
        return 0

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    keep: list[str] = []
    archive: list[str] = []

    with feedback_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                ts = entry.get("timestamp", "")
                if ts:
                    entry_time = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                    if entry_time < cutoff:
                        archive.append(line)
                        continue
            except (json.JSONDecodeError, ValueError):
                pass
            keep.append(line)

    if not archive:
        return 0

    archive_dir.mkdir(parents=True, exist_ok=True)
    archive_path = archive_dir / f"feedback-{cutoff.strftime('%Y%m%d')}.jsonl"
    with archive_path.open("a", encoding="utf-8") as f:
        for line in archive:
            f.write(line + "\n")

    with feedback_path.open("w", encoding="utf-8") as f:
        for line in keep:
            f.write(line + "\n")

    return len(archive)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def analyze_sessions(
    session_dir: Path,
    skill_filter: str | None = None,
) -> list[FeedbackEvent]:
    """Analyze all sessions and return feedback events."""
    all_events: list[FeedbackEvent] = []

    for session_path in iter_session_files(session_dir):
        session_id = extract_session_id(session_path)
        project = extract_project(session_path)
        messages = parse_session(session_path)

        if not messages:
            continue

        invocations = detect_skill_invocations(messages)

        if skill_filter:
            invocations = [inv for inv in invocations if inv.skill_id == skill_filter]

        for i, invocation in enumerate(invocations):
            next_idx = invocations[i + 1].message_index if i + 1 < len(invocations) else None
            event = classify_outcome(messages, invocation, next_idx)
            if event:
                event.session_id = session_id
                all_events.append(event)

    return all_events


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    session_dir = Path(args.session_dir).expanduser()

    # Check opt-out
    opt_out = Path.home() / ".claude" / "feedback-config.json"
    if opt_out.exists():
        try:
            config = json.loads(opt_out.read_text())
            if not config.get("enabled", True):
                print("Feedback collection disabled via feedback-config.json")
                return 0
        except (json.JSONDecodeError, OSError):
            pass

    if not session_dir.exists():
        print(f"Session directory not found: {session_dir}", file=sys.stderr)
        return 1

    events = analyze_sessions(session_dir, skill_filter=args.skill_filter)

    output_path = Path(args.output)
    write_feedback_jsonl(events, output_path, no_snippets=args.no_snippets)

    # Archive old events
    archive_dir = output_path.parent / "archive"
    archived = archive_old_events(output_path, archive_dir)

    # Print summary
    from collections import Counter
    outcomes = Counter(e.outcome for e in events)
    skills = Counter(e.skill_id for e in events)
    print(f"Analyzed {len(events)} feedback events")
    print(f"  Outcomes: {dict(outcomes)}")
    print(f"  Top skills: {skills.most_common(5)}")
    if archived:
        print(f"  Archived {archived} old events")
    print(str(output_path))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
