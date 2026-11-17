#!/usr/bin/env python3
"""Static auditor for OpenClaw-compatible skill packages."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import yaml


RELATIVE_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


@dataclass
class Issue:
    severity: str
    code: str
    message: str
    path: str


def _load_frontmatter(skill_md: Path) -> tuple[dict, str]:
    content = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", content, re.DOTALL)
    if not match:
        raise ValueError("SKILL.md must start with YAML frontmatter delimited by ---")
    frontmatter = yaml.safe_load(match.group(1)) or {}
    if not isinstance(frontmatter, dict):
        raise ValueError("Frontmatter must parse to a mapping")
    return frontmatter, match.group(2)


def _issue(severity: str, code: str, message: str, path: Path) -> Issue:
    return Issue(severity=severity, code=code, message=message, path=str(path))


def _check_relative_links(body: str, skill_dir: Path) -> Iterable[Issue]:
    for raw_target in RELATIVE_LINK_RE.findall(body):
        target = raw_target.strip()
        if "://" in target or target.startswith("#"):
            continue
        resolved = (skill_dir / target).resolve()
        if not resolved.exists():
            yield _issue("error", "broken-link", f"Referenced file does not exist: {target}", skill_dir / "SKILL.md")


def _find_nested_skill_packages(skill_dir: Path) -> list[Path]:
    nested: list[Path] = []
    seen: set[Path] = set()
    for parent in [skill_dir, skill_dir / "skills"]:
        if not parent.exists() or not parent.is_dir():
            continue
        for child in sorted(parent.iterdir()):
            candidate = child / "SKILL.md"
            if child.is_dir() and candidate.exists():
                resolved = child.resolve()
                if resolved not in seen and resolved != skill_dir.resolve():
                    seen.add(resolved)
                    nested.append(child)
    return nested


def analyze_skill(skill_dir: Path) -> dict:
    skill_dir = Path(skill_dir)
    issues: list[Issue] = []
    score = 100

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        nested_skills = _find_nested_skill_packages(skill_dir)
        if nested_skills:
            return {
                "ok": False,
                "score": 0,
                "issues": [
                    asdict(
                        _issue(
                            "error",
                            "multi-skill-repo",
                            f"Root SKILL.md not found, but detected {len(nested_skills)} child skill package(s). Create a repository entrypoint instead of a standalone root skill.",
                            skill_md,
                        )
                    )
                ],
                "summary": "Repository looks like a multi-skill package without a root entrypoint.",
                "skill": {
                    "name": normalize_name(skill_dir.name),
                    "nested_skill_count": len(nested_skills),
                    "nested_skill_dirs": [str(path) for path in nested_skills[:12]],
                },
            }
        return {
            "ok": False,
            "score": 0,
            "issues": [asdict(_issue("error", "missing-skill", "SKILL.md not found", skill_md))],
            "summary": "Skill package is missing SKILL.md.",
        }

    try:
        frontmatter, body = _load_frontmatter(skill_md)
    except Exception as exc:  # noqa: BLE001
        return {
            "ok": False,
            "score": 0,
            "issues": [asdict(_issue("error", "frontmatter", str(exc), skill_md))],
            "summary": "Skill package has invalid frontmatter.",
        }

    name = str(frontmatter.get("name", "")).strip()
    description = str(frontmatter.get("description", "")).strip()
    body_word_count = len(body.split())

    if not name:
        issues.append(_issue("error", "missing-name", "Frontmatter is missing name.", skill_md))
    elif not re.fullmatch(r"[a-z0-9-]+", name):
        issues.append(_issue("error", "bad-name", "Skill name should be lowercase hyphen-case.", skill_md))

    if not description:
        issues.append(_issue("error", "missing-description", "Frontmatter is missing description.", skill_md))
    elif len(description) < 80:
        issues.append(_issue("warning", "thin-description", "Description is too short to act as a strong trigger surface.", skill_md))

    if "TODO" in body or "TODO" in description:
        issues.append(_issue("error", "todo", "Skill still contains TODO placeholders.", skill_md))

    if body_word_count < 120:
        issues.append(_issue("warning", "thin-body", "SKILL.md body is very short; workflow may be underspecified.", skill_md))
    if body_word_count > 2200:
        issues.append(_issue("warning", "long-body", "SKILL.md body is long; consider moving details into references.", skill_md))

    if "## Quick Start" not in body and "## Workflow" not in body:
        issues.append(_issue("warning", "no-entrypoint", "Skill lacks an obvious quick-start or workflow section.", skill_md))

    if "verify" not in body.lower():
        issues.append(_issue("warning", "no-verification", "Skill does not explicitly describe verification.", skill_md))

    issues.extend(_check_relative_links(body, skill_dir))

    references_dir = skill_dir / "references"
    scripts_dir = skill_dir / "scripts"
    agents_yaml = skill_dir / "agents" / "openai.yaml"

    if references_dir.exists() and "references/" not in body:
        issues.append(_issue("warning", "unmentioned-references", "references/ exists but SKILL.md does not mention it.", skill_md))

    if scripts_dir.exists() and "scripts/" not in body:
        issues.append(_issue("warning", "unmentioned-scripts", "scripts/ exists but SKILL.md does not mention it.", skill_md))

    if agents_yaml.exists():
        try:
            agents = yaml.safe_load(agents_yaml.read_text(encoding="utf-8")) or {}
        except Exception as exc:  # noqa: BLE001
            issues.append(_issue("error", "bad-openai-yaml", f"agents/openai.yaml is invalid YAML: {exc}", agents_yaml))
        else:
            interface = agents.get("interface", {})
            default_prompt = str(interface.get("default_prompt", ""))
            short_description = str(interface.get("short_description", ""))
            if not default_prompt.startswith("Use $"):
                issues.append(_issue("warning", "default-prompt", "agents/openai.yaml default_prompt should explicitly mention the skill as $skill-name.", agents_yaml))
            if short_description and not (25 <= len(short_description) <= 64):
                issues.append(_issue("warning", "short-description-length", "agents/openai.yaml short_description should be 25-64 characters.", agents_yaml))

    for script in sorted(scripts_dir.glob("*.py")) if scripts_dir.exists() else []:
        try:
            source = script.read_text(encoding="utf-8")
            compile(source, str(script), "exec")
        except Exception as exc:  # noqa: BLE001
            issues.append(_issue("error", "script-compile", f"Python script does not compile: {exc}", script))

    severity_penalty = {"error": 18, "warning": 6, "info": 2}
    for issue in issues:
        score -= severity_penalty.get(issue.severity, 0)
    score = max(score, 0)

    summary = f"Found {sum(i.severity == 'error' for i in issues)} error(s) and {sum(i.severity == 'warning' for i in issues)} warning(s)."
    return {
        "ok": all(issue.severity != "error" for issue in issues),
        "score": score,
        "issues": [asdict(issue) for issue in issues],
        "summary": summary,
        "skill": {
            "name": name,
            "description_length": len(description),
            "body_word_count": body_word_count,
            "has_agents_yaml": agents_yaml.exists(),
            "script_count": len(list(scripts_dir.glob("*.py"))) if scripts_dir.exists() else 0,
            "reference_count": len(list(references_dir.glob("*"))) if references_dir.exists() else 0,
        },
    }


def normalize_name(value: str) -> str:
    return re.sub(r"-{2,}", "-", re.sub(r"[^a-z0-9]+", "-", value.strip().lower())).strip("-") or "unnamed-skill"


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit an OpenClaw-compatible skill package.")
    parser.add_argument("skill_dir", help="Path to the skill directory")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()

    report = analyze_skill(Path(args.skill_dir))
    if args.json:
        print(json.dumps(report, indent=2))
        return 0 if report["ok"] else 1

    print(f"Skill audit for: {args.skill_dir}")
    print(f"Score: {report['score']}")
    print(report["summary"])
    for issue in report["issues"]:
        print(f"[{issue['severity'].upper()}] {issue['code']}: {issue['message']} ({issue['path']})")
    if not report["issues"]:
        print("No issues found.")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
