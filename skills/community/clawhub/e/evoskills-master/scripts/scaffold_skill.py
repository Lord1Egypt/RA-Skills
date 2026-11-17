#!/usr/bin/env python3
"""Scaffold a new OpenClaw skill from repeated workflow evidence."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml

from evolve_skill import evolve_skill


STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "from",
    "that",
    "this",
    "into",
    "your",
    "their",
    "about",
    "when",
    "after",
    "before",
    "user",
    "task",
    "workflow",
    "repeat",
    "repeated",
    "repetitive",
}


def slugify(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.strip().lower())
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "auto-derived-skill"


def title_case_slug(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.split("-"))


def infer_name(goal: str, evidence: list[str]) -> str:
    if goal.strip():
        return slugify(goal)
    tokens = re.findall(r"[a-z0-9]+", " ".join(evidence).lower())
    ranked: list[str] = []
    for token in tokens:
        if len(token) < 4 or token in STOPWORDS:
            continue
        if token not in ranked:
            ranked.append(token)
    return slugify("-".join(ranked[:4])) if ranked else "auto-derived-skill"


def infer_trigger_description(skill_name: str, goal: str, evidence: list[str]) -> str:
    snippets = [item.strip().rstrip(".") for item in evidence if item.strip()]
    snippet_text = "; ".join(snippets[:3])
    base = (
        f"Use when repeated user requests match the {skill_name} workflow and the agent should stop improvising the same steps manually."
    )
    if goal.strip():
        base += f" Primary goal: {goal.strip().rstrip('.')}."
    if snippet_text:
        base += f" Common repeated evidence: {snippet_text}."
    return base


def infer_steps(goal: str, evidence: list[str]) -> list[str]:
    steps = []
    for item in evidence:
        text = item.strip().lstrip("-*0123456789. ").strip()
        if not text:
            continue
        if len(text.split()) < 3:
            continue
        steps.append(text.rstrip("."))
        if len(steps) >= 4:
            break
    if steps:
        return steps
    fallback = goal.strip().rstrip(".") or "deliver the repeated workflow outcome"
    return [
        f"Confirm the request matches the repeated {fallback} pattern.",
        "Load the minimum references, scripts, and prior examples needed for a reliable run.",
        "Execute the workflow in checkpoints and keep intermediate outputs easy to review.",
        "Verify the final result before reporting completion.",
    ]


def build_skill_body(skill_name: str, goal: str, evidence: list[str]) -> str:
    title = title_case_slug(skill_name)
    steps = infer_steps(goal, evidence)
    evidence_note = "\n".join(f"- {item.strip()}" for item in evidence[:5] if item.strip())
    lines = [
        f"# {title}",
        "",
        "## Purpose",
        "",
        f"Use `{skill_name}` when the user keeps asking for the same workflow and the agent should execute a repeatable OpenClaw skill instead of restating the process from scratch.",
        "",
        "## When To Use",
        "",
        "- Use it when the same task shape, deliverable, or tool sequence has shown up multiple times.",
        "- Use it when the workflow benefits from stable trigger language, predictable verification, and reusable references or scripts.",
        "- Avoid it when the current request is clearly one-off or does not match the repeated pattern captured below.",
        "",
        "## Quick Start",
        "",
        "1. Confirm the request matches the repeated workflow this skill was created to handle.",
        "2. Load the smallest relevant references or scripts before acting.",
        "3. Follow the workflow checklist and verify the result before reporting completion.",
        "",
        "## Workflow",
        "",
    ]
    for idx, step in enumerate(steps, start=1):
        lines.append(f"{idx}. {step}.")
    lines.extend(
        [
            "",
            "## Failure Recovery",
            "",
            "- If the request only partially matches the repeated workflow, state the mismatch before reusing the skill blindly.",
            "- If inputs are missing, ask only for the minimum missing artifact and keep the rest of the workflow intact.",
            "- If the workflow keeps drifting, update this skill with a narrower trigger surface instead of improvising around the mismatch.",
            "",
            "## Verification Checklist",
            "",
            "- Verify the output matches the repeated deliverable shape the user expects.",
            "- Verify any references, APIs, or scripts were used with the intended inputs.",
            "- Report what was verified directly and what still remains assumed.",
            "",
            "## Repetition Evidence",
            "",
            "This skill was auto-scaffolded from repeated task signals:",
            evidence_note or "- Repeated workflow evidence was not captured verbatim.",
            "",
            "## Bundled Resources",
            "",
            "- Read [repetition-evidence.md](references/repetition-evidence.md) before widening this workflow.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_skill_package(output_dir: Path, skill_name: str, goal: str, evidence: list[str]) -> list[str]:
    changes: list[str] = []
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "references").mkdir(parents=True, exist_ok=True)
    (output_dir / "agents").mkdir(parents=True, exist_ok=True)

    frontmatter = {
        "name": skill_name,
        "description": infer_trigger_description(skill_name, goal, evidence),
    }
    yaml_text = yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=False).strip()
    body = build_skill_body(skill_name, goal, evidence)
    (output_dir / "SKILL.md").write_text(f"---\n{yaml_text}\n---\n\n{body}", encoding="utf-8")
    changes.append("wrote_skill_md")

    evidence_text = "# Repetition Evidence\n\n"
    if evidence:
        evidence_text += "\n".join(f"- {item.strip()}" for item in evidence if item.strip()) + "\n"
    else:
        evidence_text += "- No explicit evidence strings were supplied.\n"
    (output_dir / "references" / "repetition-evidence.md").write_text(evidence_text, encoding="utf-8")
    changes.append("wrote_repetition_evidence")

    openai_yaml = {
        "interface": {
            "display_name": title_case_slug(skill_name),
            "short_description": "Auto-derived skill for repeated workflows.",
            "default_prompt": f"Use ${skill_name} to handle this repeated workflow consistently.",
        },
        "policy": {"allow_implicit_invocation": True},
    }
    (output_dir / "agents" / "openai.yaml").write_text(
        yaml.safe_dump(openai_yaml, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    changes.append("wrote_openai_yaml")
    return changes


def scaffold_skill(output_root: Path, goal: str, evidence: list[str], name: str = "", evolve_rounds: int = 1) -> dict:
    skill_name = slugify(name) if name.strip() else infer_name(goal, evidence)
    skill_dir = output_root / skill_name
    changes = write_skill_package(skill_dir, skill_name, goal, evidence)
    evolve_report = evolve_skill(skill_dir, goal or f"stabilize the {skill_name} repeated workflow skill", rounds=max(1, evolve_rounds))
    return {
        "skill_name": skill_name,
        "skill_dir": str(skill_dir),
        "changes": changes,
        "goal": goal,
        "evidence_count": len([item for item in evidence if item.strip()]),
        "evolve_report": evolve_report,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold and evolve a new OpenClaw skill from repeated workflow evidence.")
    parser.add_argument("output_root", help="Directory where the new skill should be created")
    parser.add_argument("--goal", default="", help="Short statement of the repeated workflow goal")
    parser.add_argument("--name", default="", help="Optional explicit skill name")
    parser.add_argument("--evidence", action="append", default=[], help="Repeated task evidence line; pass multiple times")
    parser.add_argument("--evidence-file", action="append", default=[], help="File containing repeated task evidence, one block per file")
    parser.add_argument("--rounds", type=int, default=1, help="How many evolve rounds to run after scaffolding")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    evidence = list(args.evidence)
    for file_path in args.evidence_file:
        evidence.append(Path(file_path).read_text(encoding="utf-8", errors="ignore"))

    report = scaffold_skill(Path(args.output_root), args.goal, evidence, name=args.name, evolve_rounds=args.rounds)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Created skill: {report['skill_name']}")
        print(f"Location: {report['skill_dir']}")
        print(f"Evidence count: {report['evidence_count']}")
        print(f"Final score: {report['evolve_report']['final_audit']['score']}")
    return 0 if report["evolve_report"]["final_audit"]["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
