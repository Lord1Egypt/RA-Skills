#!/usr/bin/env python3
"""
Autoresearch Pro — Evaluation Helper

Provides utilities for:
- Reading a target skill's SKILL.md
- Generating checklist questions
- Running mutation scoring
- Managing version snapshots for revert

Usage:
    python run_eval.py --skill-path ~/.openclaw/skills/merge-drafts \
                       --list-rounds

This script is OPTIONAL — the core logic lives in SKILL.md.
It exists to handle file I/O and state management reliably.
"""

import argparse
import json
import subprocess
from pathlib import Path

SKILLS_DIR = Path.home() / ".openclaw" / "skills"


def read_skill(skill_path: str) -> str:
    """Read the SKILL.md of a target skill."""
    skill_path = Path(skill_path)
    sk_path = skill_path / "SKILL.md"
    if not sk_path.exists():
        raise FileNotFoundError(f"SKILL.md not found at {sk_path}")
    return sk_path.read_text()


def write_skill(skill_path: str, content: str) -> None:
    """Write updated content to a target skill's SKILL.md."""
    skill_path = Path(skill_path)
    sk_path = skill_path / "SKILL.md"
    sk_path.write_text(content)


def snapshot(skill_path: str, round_num: int) -> Path:
    """Save a timestamped snapshot of SKILL.md before a mutation."""
    skill_path = Path(skill_path)
    snap_dir = skill_path / ".snapshots"
    snap_dir.mkdir(exist_ok=True)
    snap_path = snap_dir / f"round_{round_num:04d}.md"
    snap_path.write_text(read_skill(skill_path))
    return snap_path


def revert_to_snapshot(skill_path: str, round_num: int) -> None:
    """Revert SKILL.md to a saved snapshot."""
    skill_path = Path(skill_path)
    snap_path = skill_path / ".snapshots" / f"round_{round_num:04d}.md"
    if not snap_path.exists():
        raise FileNotFoundError(f"Snapshot not found: {snap_path}")
    content = snap_path.read_text()
    write_skill(skill_path, content)


def list_snapshots(skill_path: str) -> list:
    """List all available snapshots."""
    skill_path = Path(skill_path)
    snap_dir = skill_path / ".snapshots"
    if not snap_dir.exists():
        return []
    return sorted(snap_dir.glob("round_*.md"))


def generate_checklist_questions(skill_content: str) -> list[dict]:
    """
    Generate 10 checklist questions based on SKILL.md content.
    Returns a list of dicts with: {id, dimension, question, weight}.
    """
    import re

    # Simple heuristic: look at frontmatter, headers, content length
    has_description = bool(re.search(r"description:\s*", skill_content))
    frontmatter_match = re.search(r"^---\n(.*?)\n---", skill_content, re.DOTALL)
    frontmatter = frontmatter_match.group(1) if frontmatter_match else ""
    body = skill_content[frontmatter_match.end() :] if frontmatter_match else skill_content

    lines = [l.strip() for l in body.split("\n") if l.strip()]
    headers = [l for l in lines if l.startswith("#")]
    code_blocks = len(re.findall(r"```", body))
    word_count = len(body.split())

    questions = [
        {
            "id": 1,
            "dimension": "Description clarity",
            "question": "Is the `description` in frontmatter precise, specific, and does it clearly explain when to use this skill?",
            "weight": 1.0,
        },
        {
            "id": 2,
            "dimension": "Trigger coverage",
            "question": "Does the description cover the main real-world use cases this skill addresses?",
            "weight": 1.0,
        },
        {
            "id": 3,
            "dimension": "Workflow structure",
            "question": "Are workflow steps clearly sequenced, unambiguous, and actionable?",
            "weight": 1.0,
        },
        {
            "id": 4,
            "dimension": "Error guidance",
            "question": "Does the skill handle error states, edge cases, and failure modes clearly?",
            "weight": 1.0,
        },
        {
            "id": 5,
            "dimension": "Tool usage accuracy",
            "question": "Are tool names, parameters, and API references correct for OpenClaw?",
            "weight": 1.0,
        },
        {
            "id": 6,
            "dimension": "Example quality",
            "question": "Do examples reflect real usage patterns and cover important edge cases?",
            "weight": 1.0,
        },
        {
            "id": 7,
            "dimension": "Conciseness",
            "question": "Is the content free of redundant, repetitive, or unnecessary filler?",
            "weight": 1.0,
        },
        {
            "id": 8,
            "dimension": "Freedom calibration",
            "question": "Is the degree of instruction specificity (constraint vs. flexibility) appropriate for the task?",
            "weight": 1.0,
        },
        {
            "id": 9,
            "dimension": "Reference quality",
            "question": "Are references, links, or external resources mentioned accurately and helpfully?",
            "weight": 1.0,
        },
        {
            "id": 10,
            "dimension": "Completeness",
            "question": "Are all necessary sections present, filled in with real content (not TODO placeholders)?",
            "weight": 1.0,
        },
    ]

    return questions


def score_output(skill_content: str, test_input: str, active_question_ids: list[int]) -> dict:
    """
    Score a skill's output against active checklist questions.
    
    Since we can't run the skill in a sub-agent here, this performs
    a heuristic static analysis of the SKILL.md content.
    
    Returns dict with per-question results and total score 0-100.
    """
    questions = generate_checklist_questions(skill_content)
    active = [q for q in questions if q["id"] in active_question_ids]

    results = []
    passed = 0

    for q in active:
        score_val = heuristic_check(skill_content, test_input, q)
        results.append({"question_id": q["id"], "dimension": q["dimension"], "passed": score_val})
        passed += score_val

    total = int((passed / len(active)) * 100) if active else 0
    return {"total": total, "details": results}


def heuristic_check(skill_content: str, test_input: str, question: dict) -> int:
    """
    Heuristic yes/no check for a checklist question against SKILL.md content.
    Returns 1 (pass) or 0 (fail).
    
    This is a rough proxy — the actual scoring is done by reading the
    SKILL.md and reasoning about whether the question is satisfied.
    """
    import re

    qid = question["id"]
    body = skill_content.lower()

    if qid == 1:
        # Description clarity: has non-trivial description (>50 chars, not just TODO)
        desc_match = re.search(r'description:\s*(.+)', skill_content)
        if desc_match:
            desc = desc_match.group(1).strip()
            return 1 if len(desc) > 50 and "todo" not in desc.lower() else 0
        return 0

    elif qid == 2:
        # Trigger coverage: has actionable description with trigger words
        trigger_words = ["use when", "triggers", "when the user", "applicable", "scenario"]
        return 1 if any(w in body for w in trigger_words) else 0

    elif qid == 3:
        # Workflow structure: has numbered or clearly sequenced steps
        has_steps = bool(re.search(r"^\d+\.|^-\s+\w+|step\s+\d+", body, re.MULTILINE))
        return 1 if has_steps else 0

    elif qid == 4:
        # Error guidance: mentions error, warning, or edge case handling
        error_words = ["error", "warning", "edge case", "fail", "exception", "troubleshoot"]
        return 1 if any(w in body for w in error_words) else 0

    elif qid == 5:
        # Tool accuracy: mentions real OpenClaw tool names or APIs
        # Just check it has some specificity (not overly generic)
        return 1 if len(skill_content) > 500 else 0

    elif qid == 6:
        # Example quality: has code blocks or concrete examples
        return 1 if "```" in skill_content and skill_content.count("```") >= 2 else 0

    elif qid == 7:
        # Conciseness: content is substantive relative to length
        lines = [l.strip() for l in skill_content.split("\n") if l.strip()]
        return 1 if len(lines) > 20 else 0

    elif qid == 8:
        # Freedom calibration: has some constraint language
        constraint_words = ["must", "always", "never", "require", "do not", "禁止", "强制"]
        has_constraints = any(w in body for w in constraint_words)
        has_flexibility = any(w in body for w in ["may", "can", "optionally", "if needed"])
        return 1 if (has_constraints or has_flexibility) else 0

    elif qid == 9:
        # Reference quality: has links or external references
        has_links = bool(re.search(r"\[.+\]\(.+\)", body))
        return 1 if has_links else 0

    elif qid == 10:
        # Completeness: no TODO/FIXME placeholders dominating
        todo_count = len(re.findall(r"\[?TODO\]?|FIXME|XXX", body))
        return 0 if todo_count > 3 else 1

    return 1


def main():
    parser = argparse.ArgumentParser(description="Autoresearch Pro — Evaluation Helper")
    parser.add_argument("--skill-path", required=True, help="Path to target skill directory")
    parser.add_argument("--list-snapshots", action="store_true", help="List all snapshots")
    parser.add_argument("--snap-round", type=int, help="Snapshot round number to inspect")
    args = parser.parse_args()

    skill_path = Path(args.skill_path)

    if args.list_snapshots:
        snaps = list_snapshots(str(skill_path))
        print(f"Snapshots in {skill_path}:")
        for s in snaps:
            print(f"  {s.name}")
        return

    print("autoresearch-pro helper ready. Use --list-snapshots to inspect state.")


if __name__ == "__main__":
    main()
