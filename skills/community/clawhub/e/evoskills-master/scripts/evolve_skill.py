#!/usr/bin/env python3
"""End-to-end EvoSkills-style orchestration for OpenClaw skill packages."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from repair_skill import repair_skill
from skill_audit import analyze_skill
from surrogate_verify import build_report


def ensure_quick_start(skill_md: Path) -> bool:
    text = skill_md.read_text(encoding="utf-8", errors="ignore")
    if "## Quick Start" in text or "## Workflow" in text:
        return False
    title_marker = "\n# "
    idx = text.find(title_marker)
    if idx == -1:
        return False
    after_title = text.find("\n", idx + 3)
    insert_at = after_title + 1
    section = (
        "\n## Quick Start\n\n"
        "1. Confirm the request matches this skill's trigger surface.\n"
        "2. Load the minimum bundled references or scripts needed for the task.\n"
        "3. Follow the workflow and verify the result before reporting completion.\n"
    )
    skill_md.write_text(text[:insert_at] + section + text[insert_at:], encoding="utf-8")
    return True


def ensure_verification(skill_md: Path) -> bool:
    text = skill_md.read_text(encoding="utf-8", errors="ignore")
    if "## Verification" in text or "## Verification Checklist" in text:
        return False
    section = (
        "\n## Verification Checklist\n\n"
        "- Verify the request matched this skill's intended trigger.\n"
        "- Verify any referenced scripts, tools, or APIs used the expected inputs.\n"
        "- Verify the output includes the key artifacts or summaries promised by the workflow.\n"
        "- Report what was verified and what remains unverified.\n"
    )
    skill_md.write_text(text + section, encoding="utf-8")
    return True


def ensure_resource_mentions(skill_md: Path, skill_root: Path) -> bool:
    text = skill_md.read_text(encoding="utf-8", errors="ignore")
    changed = False
    lines: list[str] = []
    if (skill_root / "references").exists() and "references/" not in text:
        lines.append("- Read files under `references/` when you need detailed guidance or domain context.")
    if (skill_root / "scripts").exists() and "scripts/" not in text:
        lines.append("- Prefer reusable helpers under `scripts/` when the workflow would otherwise reimplement deterministic logic.")
    if lines:
        section = "\n## Bundled Resources\n\n" + "\n".join(lines) + "\n"
        skill_md.write_text(text + section, encoding="utf-8")
        changed = True
    return changed


def strengthen_description(skill_md: Path) -> bool:
    text = skill_md.read_text(encoding="utf-8", errors="ignore")
    if not text.startswith("---\n"):
        return False
    end = text.find("\n---", 4)
    if end == -1:
        return False
    frontmatter = yaml.safe_load(text[4:end]) or {}
    if not isinstance(frontmatter, dict):
        return False
    description = str(frontmatter.get("description", "")).strip()
    if len(description) >= 80:
        return False
    extra = " Use when the task requires the packaged workflow, bundled references, or helper scripts instead of a generic response."
    frontmatter["description"] = (description + extra).strip()
    yaml_text = yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=False).strip()
    skill_md.write_text(f"---\n{yaml_text}\n---" + text[end + 4 :], encoding="utf-8")
    return True


def repair_openai_yaml(skill_root: Path) -> bool:
    yaml_path = skill_root / "agents" / "openai.yaml"
    if not yaml_path.exists():
        return False
    data = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        return False
    interface = data.setdefault("interface", {})
    changed = False
    short_description = str(interface.get("short_description", "")).strip()
    if short_description:
        if len(short_description) < 25:
            interface["short_description"] = (short_description + " for complex OpenClaw workflows").strip()[:64]
            changed = True
        elif len(short_description) > 64:
            interface["short_description"] = short_description[:64].rstrip()
            changed = True
    default_prompt = str(interface.get("default_prompt", "")).strip()
    if default_prompt and not default_prompt.startswith("Use $"):
        interface["default_prompt"] = f"Use ${skill_root.name} to follow this skill's workflow."
        changed = True
    if changed:
        yaml_path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return changed


def semantic_patch(skill_root: Path, audit_before: dict) -> list[str]:
    changes: list[str] = []
    issue_codes = {issue["code"] for issue in audit_before["issues"]}
    skill_md = skill_root / "SKILL.md"
    if "thin-body" in issue_codes:
        repaired = repair_skill(skill_root)
        if "expanded_thin_body" in repaired["changes"]:
            changes.append("expanded_thin_body")
    if "thin-description" in issue_codes and skill_md.exists() and strengthen_description(skill_md):
        changes.append("strengthened_description")
    if "no-entrypoint" in issue_codes and skill_md.exists() and ensure_quick_start(skill_md):
        changes.append("added_quick_start")
    if "no-verification" in issue_codes and skill_md.exists() and ensure_verification(skill_md):
        changes.append("added_verification")
    if {"unmentioned-references", "unmentioned-scripts"} & issue_codes and skill_md.exists() and ensure_resource_mentions(skill_md, skill_root):
        changes.append("mentioned_resources")
    if {"default-prompt", "short-description-length"} & issue_codes and repair_openai_yaml(skill_root):
        changes.append("repaired_openai_yaml")
    return changes


def run_single_round(skill_dir: Path, goal: str, round_index: int) -> dict:
    starting_audit = analyze_skill(skill_dir)
    repair_report = repair_skill(skill_dir)
    post_repair_audit = analyze_skill(skill_dir)
    semantic_changes = semantic_patch(skill_dir, post_repair_audit)
    final_audit = analyze_skill(skill_dir)
    verifier = build_report(skill_dir, goal)
    return {
        "round": round_index,
        "starting_audit": starting_audit,
        "repair_report": repair_report,
        "post_repair_audit": post_repair_audit,
        "semantic_changes": semantic_changes,
        "final_audit": final_audit,
        "verifier": verifier,
        "changed": bool(repair_report["changes"] or semantic_changes),
    }


def evolve_skill(skill_dir: Path, goal: str = "", rounds: int = 1) -> dict:
    skill_dir = Path(skill_dir)
    baseline = analyze_skill(skill_dir)
    round_reports: list[dict] = []
    stop_reason = "max_rounds_reached"
    previous_score = baseline["score"]

    for round_index in range(1, max(1, rounds) + 1):
        report = run_single_round(skill_dir, goal, round_index)
        round_reports.append(report)
        current_score = report["final_audit"]["score"]
        if not report["changed"] and current_score == previous_score:
            stop_reason = "no_further_changes"
            break
        if report["final_audit"]["ok"] and not report["verifier"]["blocking_issues"] and current_score >= previous_score:
            stop_reason = "audit_clean"
            if round_index >= rounds or not report["changed"]:
                break
        previous_score = current_score

    final_report = round_reports[-1] if round_reports else {
        "final_audit": baseline,
        "verifier": build_report(skill_dir, goal),
        "changed": False,
        "repair_report": {"changes": []},
        "semantic_changes": [],
    }

    return {
        "skill_dir": str(skill_dir),
        "goal": goal,
        "rounds_requested": rounds,
        "rounds_completed": len(round_reports),
        "stop_reason": stop_reason,
        "baseline_audit": baseline,
        "round_reports": round_reports,
        "repair_report": final_report["repair_report"],
        "post_repair_audit": final_report.get("post_repair_audit", baseline),
        "semantic_changes": final_report.get("semantic_changes", []),
        "final_audit": final_report["final_audit"],
        "verifier": final_report["verifier"],
        "changed": any(report["changed"] for report in round_reports),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run an EvoSkills-style evolution cycle on an OpenClaw-compatible skill.")
    parser.add_argument("skill_dir", help="Path to the skill directory")
    parser.add_argument("--goal", default="", help="Short statement of the improvement goal")
    parser.add_argument("--rounds", type=int, default=1, help="Maximum number of evolution rounds to run")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()

    report = evolve_skill(Path(args.skill_dir), args.goal, rounds=max(1, args.rounds))
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Evolved skill: {report['skill_dir']}")
        if report["goal"]:
            print(f"Goal: {report['goal']}")
        print(f"Rounds: {report['rounds_completed']}/{report['rounds_requested']} ({report['stop_reason']})")
        print(f"Baseline score: {report['baseline_audit']['score']}")
        print(f"Final score: {report['final_audit']['score']}")
        if report["repair_report"]["changes"] or report["semantic_changes"]:
            print("Changes:")
            for round_report in report["round_reports"]:
                round_changes = round_report["repair_report"]["changes"] + round_report["semantic_changes"]
                if not round_changes:
                    continue
                for change in round_changes:
                    print(f"- round {round_report['round']}: {change}")
        else:
            print("Changes:\n- none")
        print("Next upgrades:")
        for item in report["verifier"]["next_upgrades"]:
            print(f"- {item}")
    return 0 if report["final_audit"]["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
