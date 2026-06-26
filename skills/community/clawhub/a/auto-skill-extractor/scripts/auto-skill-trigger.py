#!/usr/bin/env python3
"""
Auto-Skill Trigger System v2.0
Called after subagent completion to determine if skill extraction is needed.

Changes from v1:
- Generates meaningful SKILL.md from transcript summary, not just placeholders
- Properly integrated with OpenClaw workspace paths
- Cleaner output format for main agent consumption
"""

import sys
import json
import hashlib
import re
import os
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(os.environ.get("AUTO_SKILL_WORKSPACE", "/home/wahaj/.openclaw/workspace")).resolve()
AUTO_DIR = WORKSPACE / "skills" / "auto"
DRAFT_DIR = WORKSPACE / "skills" / "auto-draft"
QUEUE_FILE = WORKSPACE / "scripts" / "skill-extraction-queue.json"
MAX_QUEUE_SIZE = 50
COMPLEXITY_THRESHOLD = 4


def sanitize_skill_name(name: str) -> str:
    """Prevent path traversal and invalid chars."""
    name = os.path.basename(name)
    name = re.sub(r'[^a-zA-Z0-9_-]', '-', name)
    return name[:64]


def calculate_complexity(tool_calls: int, has_error_recovery: bool = False, multi_domain: bool = False) -> int:
    score = min(10, int(tool_calls * 0.7))
    if has_error_recovery:
        score += 2
    if multi_domain:
        score += 2
    return min(10, score)


def generate_skill_name(transcript_summary: str, tags: list = None) -> str:
    """Generate a descriptive skill name from transcript summary."""
    if tags:
        key_tags = [t for t in tags if len(t) > 2][:3]
        if key_tags:
            name = "-".join(key_tags)
            hash_str = hashlib.md5(name.encode()).hexdigest()[:6]
            return f"{name}-{hash_str}"

    words = transcript_summary.lower().split()
    stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "is", "was", "are", "were", "be", "been", "have", "has", "had", "do", "does", "did", "will", "would", "could", "should", "may", "might", "can", "this", "that", "these", "those", "it", "its", "from", "into", "not", "no", "yes", "then", "than", "so", "if", "as", "up", "out", "about", "over", "after", "before", "using", "used", "which", "what", "when", "how", "why"}
    key_words = [w for w in words if w not in stop_words and len(w) > 2 and w.isalpha()]

    if len(key_words) >= 2:
        name = f"{key_words[0]}-{key_words[-1]}"
    elif key_words:
        name = key_words[0]
    else:
        name = "unknown-task"

    hash_str = hashlib.md5(name.encode()).hexdigest()[:6]
    return f"{name}-{hash_str}"


def generate_skill_md(skill_name: str, transcript_summary: str, tool_calls: int, complexity: int, tags: list = None) -> str:
    """Generate a meaningful SKILL.md from transcript data."""
    # Extract key actions from summary
    actions = []
    for line in transcript_summary.split('\n'):
        line = line.strip().strip('- •').strip()
        if line and len(line) > 10 and not line.startswith('#'):
            actions.append(line)

    # Build tags section
    tag_str = ""
    if tags:
        tag_str = "\n".join([f"  - {t}" for t in tags])

    # Title from name
    title = skill_name.replace('-', ' ').title()

    md = f"""# {title}

Auto-extracted skill from subagent work.

## Description

{transcript_summary[:500]}

## When to Use

{chr(10).join(['- ' + a[:100] for a in actions[:5]]) if actions else '- [Fill in conditions where this skill applies]'}

## Procedure

1. [Step 1 — fill in from transcript]
2. [Step 2]
3. [Step 3]

## Complexity

- Tool calls: {tool_calls}
- Complexity score: {complexity}/10
- Tags: {', '.join(tags) if tags else 'none'}

## Verification

- [ ] [Check 1]
- [ ] [Check 2]

## Status

DRAFT — needs 3 successful re-invocations before promotion to ACTIVE.
Created: {datetime.now().isoformat()}
"""
    return md


def should_extract_skill(completion_status: str, tool_calls: int, complexity: int, manual_trigger: bool = False) -> dict:
    result = {"should_extract": False, "reason": ""}

    if manual_trigger:
        result["should_extract"] = True
        result["reason"] = "Manual trigger"
        return result

    if completion_status != "success":
        result["reason"] = f"Status '{completion_status}' is not 'success'"
        return result

    if tool_calls < 3:
        result["reason"] = f"Only {tool_calls} tool calls (minimum 3)"
        return result

    if complexity < COMPLEXITY_THRESHOLD:
        result["reason"] = f"Complexity {complexity} below threshold ({COMPLEXITY_THRESHOLD})"
        return result

    result["should_extract"] = True
    result["reason"] = f"Qualifies: {tool_calls} tools, complexity {complexity}"
    return result


def create_draft(skill_name: str, tool_calls: int, complexity: int, transcript_summary: str, tags: list = None, session_id: str = ""):
    """Create a draft skill directory with SKILL.md and meta.json."""
    draft_dir = DRAFT_DIR / skill_name

    if draft_dir.exists():
        return {"action": "skip", "reason": f"Draft '{skill_name}' already exists"}

    draft_dir.mkdir(parents=True, exist_ok=True)

    # Generate SKILL.md
    skill_md = generate_skill_md(skill_name, transcript_summary, tool_calls, complexity, tags)
    (draft_dir / "SKILL.md").write_text(skill_md)

    # Create meta.json (sanitized)
    meta = {
        "created": datetime.now().isoformat(),
        "tool_calls": tool_calls,
        "complexity": complexity,
        "invocation_count": 0,
        "status": "DRAFT",
        "skill_name": skill_name,
        "tags": tags or [],
        "source_session_hash": hashlib.sha256(session_id.encode()).hexdigest()[:16]
    }
    (draft_dir / "meta.json").write_text(json.dumps(meta, indent=2))

    return {"action": "extract", "skill_name": skill_name}


def main():
    try:
        DRAFT_DIR.mkdir(parents=True, exist_ok=True)
        AUTO_DIR.mkdir(parents=True, exist_ok=True)
        (WORKSPACE / "scripts").mkdir(parents=True, exist_ok=True)

        if len(sys.argv) > 1 and sys.argv[1].endswith('.json'):
            with open(sys.argv[1], 'r') as f:
                data = json.load(f)
        else:
            data = json.load(sys.stdin)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(json.dumps({"error": f"Invalid input: {e}"}))
        sys.exit(1)

    completion_status = data.get("completion_status", "")
    tool_calls = data.get("tool_calls", 0)
    session_id = data.get("session_id", "")
    transcript_summary = data.get("transcript_summary", "")
    tags = data.get("tags", [])
    manual_trigger = data.get("manual_trigger", False)

    complexity = calculate_complexity(
        tool_calls,
        has_error_recovery=data.get("has_error_recovery", False),
        multi_domain=data.get("multi_domain", False)
    )

    qualification = should_extract_skill(completion_status, tool_calls, complexity, manual_trigger)

    if not qualification["should_extract"]:
        print(json.dumps({"action": "skip", "reason": qualification["reason"]}))
        return

    skill_name = sanitize_skill_name(
        data.get("skill_name") or generate_skill_name(transcript_summary, tags)
    )

    result = create_draft(skill_name, tool_calls, complexity, transcript_summary, tags, session_id)
    print(json.dumps(result))


if __name__ == "__main__":
    main()