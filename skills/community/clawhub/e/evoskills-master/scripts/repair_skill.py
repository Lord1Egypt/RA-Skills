#!/usr/bin/env python3
"""Automatic repair helpers for OpenClaw-compatible skill packages."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml


LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^##\s+.+$", re.MULTILINE)


def normalize_skill_name(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", value.strip().lower())
    normalized = re.sub(r"-{2,}", "-", normalized).strip("-")
    return normalized or "unnamed-skill"


def load_skill_text(skill_md: Path) -> str:
    return skill_md.read_text(encoding="utf-8", errors="ignore")


def find_nested_skill_packages(skill_dir: Path) -> list[Path]:
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


def find_existing_skill_markdown(skill_dir: Path) -> Path | None:
    candidates = []
    for path in skill_dir.glob("*.md"):
        if path.name == "SKILL.md":
            return path
        lower = path.name.lower()
        if lower in {"skill.md", "skill-template.md"} or "skill" in lower:
            candidates.append(path)
    return candidates[0] if candidates else None


def parse_frontmatter(text: str) -> tuple[dict | None, str]:
    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not match:
        return None, text
    try:
        frontmatter = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return None, match.group(2)
    if not isinstance(frontmatter, dict):
        return None, match.group(2)
    return frontmatter, match.group(2)


def synthesize_frontmatter(skill_dir: Path, body: str) -> dict:
    title_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    raw_name = title_match.group(1) if title_match else skill_dir.name
    name = normalize_skill_name(raw_name)
    description = (
        f"Use when working with the {name} skill workflow, its bundled references, "
        "or its helper scripts in an OpenClaw-compatible skill package."
    )
    return {"name": name, "description": description}


def synthesize_body(skill_dir: Path) -> str:
    title = " ".join(part.capitalize() for part in normalize_skill_name(skill_dir.name).split("-"))
    lines = [
        f"# {title}",
        "",
        "## Purpose",
        "",
        f"Use this skill when the request matches the {normalize_skill_name(skill_dir.name)} workflow and you need a repeatable OpenClaw-compatible procedure instead of an improvised answer.",
        "",
        "## When To Use",
        "",
        "- Use it when the task clearly maps to this skill's packaged domain or operating procedure.",
        "- Use it when bundled references, scripts, or prompt scaffolding will make the result more reliable.",
        "- Avoid it when a simpler built-in workflow already solves the request with less overhead.",
        "",
        "## Quick Start",
        "",
        "1. Confirm the request matches this skill's intended workflow.",
        "2. Load the minimum bundled references or scripts needed for the task.",
        "3. Execute the workflow and verify the result before reporting completion.",
        "",
        "## Workflow",
        "",
        "1. Restate the user's goal in the skill's domain language so the working plan is explicit.",
        "2. Inspect the minimum local references, helpers, and configuration files needed for the task.",
        "3. Execute the main workflow in small checkpoints and keep intermediate outputs reviewable.",
        "4. If a step fails, adjust the plan using the closest bundled guidance before retrying.",
    ]
    resource_lines = []
    if (skill_dir / "references").exists():
        resource_lines.append("- Read files under `references/` for detailed guidance.")
    if (skill_dir / "scripts").exists():
        resource_lines.append("- Prefer helpers under `scripts/` over rewriting deterministic logic.")
    if resource_lines:
        lines.extend(["", "## Bundled Resources", ""] + resource_lines)
    lines.extend(
        [
            "",
            "## Failure Recovery",
            "",
            "- If inputs are missing, stop and identify the smallest missing artifact before continuing.",
            "- If a script or command fails, capture the error, inspect the nearest bundled guidance, and retry with a narrower change.",
            "- If the workflow remains ambiguous, report the blocker and preserve any partial artifacts that may help the next step.",
            "",
            "## Verification Checklist",
            "",
            "- Verify the output matches the task intent.",
            "- Verify any bundled scripts or APIs used the expected inputs.",
            "- Report what was verified and what remains unverified.",
        ]
    )
    return "\n".join(lines) + "\n"


def summarize_child_skill(skill_dir: Path, child_dir: Path) -> dict[str, str]:
    skill_md = child_dir / "SKILL.md"
    text = load_skill_text(skill_md)
    frontmatter, body = parse_frontmatter(text)
    if frontmatter is None:
        frontmatter = {}
    name = normalize_skill_name(str(frontmatter.get("name") or child_dir.name))
    title_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else child_dir.name
    description = " ".join(str(frontmatter.get("description", "")).split())
    description = description or f"Use this child skill for work routed to {name}."
    cleaned_description = description.rstrip(".")
    route_hint = cleaned_description
    route_hint = re.sub(r"^Use this skill when\s*", "", route_hint, flags=re.IGNORECASE).strip()
    route_hint = re.sub(r"^Use when\s*", "", route_hint, flags=re.IGNORECASE).strip()
    route_hint = re.sub(r"^Use this skill for\s*", "", route_hint, flags=re.IGNORECASE).strip()
    route_hint = re.sub(r"^when\s*", "", route_hint, flags=re.IGNORECASE).strip()
    route_hint = route_hint.rstrip(".")
    route_hint = route_hint[:140].rstrip()
    rel = child_dir.relative_to(skill_dir).as_posix()
    return {
        "name": name,
        "title": title,
        "description": cleaned_description[:180].rstrip(),
        "route_hint": route_hint or f"tasks that map to {name}",
        "path": f"{rel}/SKILL.md",
    }


def categorize_child_skill(summary: dict[str, str]) -> str:
    haystack = " ".join(
        [
            summary["name"],
            summary["title"],
            summary["description"],
            summary["route_hint"],
        ]
    ).lower()
    categories = [
        ("Payments & Finance", ["payment", "settlement", "invoice", "billing", "finance", "transaction", "checkout", "treasury"]),
        ("Bridging & Cross-Chain", ["bridge", "bridging", "cross-chain", "interchain", "relay"]),
        ("Wallets & Assets", ["wallet", "token", "asset", "custody", "balance", "stablecoin"]),
        ("Contracts & Protocols", ["contract", "rpc", "protocol", "defi", "composer", "verification", "abi"]),
        ("Infrastructure & DevTools", ["infra", "tool", "sdk", "cli", "foundry", "hardhat", "viem", "wagmi", "x402", "thirdweb"]),
        ("Identity & Access", ["identity", "auth", "authentication", "account", "user", "login", "permission", "access"]),
    ]
    for label, keywords in categories:
        if any(keyword in haystack for keyword in keywords):
            return label
    return "General Routing"


def synthesize_collection_body(skill_dir: Path, nested_skills: list[Path]) -> str:
    title = " ".join(part.capitalize() for part in normalize_skill_name(skill_dir.name).split("-"))
    child_summaries = [summarize_child_skill(skill_dir, child) for child in nested_skills[:12]]
    grouped_children: dict[str, list[dict[str, str]]] = {}
    for child in child_summaries:
        grouped_children.setdefault(categorize_child_skill(child), []).append(child)

    lines = [
        f"# {title}",
        "",
        "## Purpose",
        "",
        f"Use this repository entrypoint when the request maps to one of the bundled child skills inside `{normalize_skill_name(skill_dir.name)}` and you need help selecting the right sub-skill before execution.",
        "Treat this root skill as a router for a multi-skill repository rather than as the place where the domain workflow itself is executed.",
        "",
        "## When To Use",
        "",
        "- Use it when the repository packages multiple related skills under a shared domain.",
        "- Use it when you need to identify which child skill should own the request.",
        "- Avoid it when the user already named a specific child skill and you can jump there directly.",
        "",
        "## Quick Start",
        "",
        "1. Inspect the request and decide which bundled child skill best matches the task.",
        "2. Open that child skill's `SKILL.md` and follow its workflow instead of improvising at the repository root.",
        "3. If more than one child skill could apply, pick the narrowest one that fully covers the task.",
        "",
        "## Skill Groups",
        "",
    ]
    for group_name in sorted(grouped_children):
        member_names = ", ".join(f"`{child['name']}`" for child in grouped_children[group_name])
        lines.append(f"- **{group_name}**: {member_names}")

    lines.extend(["", "## Child Skills", ""])
    for group_name in sorted(grouped_children):
        lines.extend([f"### {group_name}", ""])
        for child in grouped_children[group_name]:
            lines.append(f"- `{child['name']}` -> [{child['path']}]({child['path']})")
            lines.append(f"  Route here for: {child['route_hint']}.")
            lines.append(f"  Summary: {child['title']} - {child['description']}.")
        lines.append("")

    if len(nested_skills) > 12:
        lines.append(f"- Additional child skills exist beyond the first 12; inspect the `skills/` directory before routing complex requests.")

    lines.extend(
        [
            "",
            "## Workflow",
            "",
            "1. Classify the request by capability, protocol, or product area.",
            "2. Route to the closest child skill and load only that skill's local references and scripts.",
            "3. If the first candidate is too broad, move to a narrower sibling skill instead of staying at the root entrypoint.",
            "4. After the child skill finishes, summarize which route was chosen and why.",
            "",
            "## Failure Recovery",
            "",
            "- If no child skill clearly matches, report the routing ambiguity and list the nearest candidates.",
            "- If a child skill is missing or broken, preserve the routing decision and report the gap instead of inventing a root-level workflow.",
            "- If multiple child skills are needed, sequence them explicitly and keep handoff points visible.",
            "",
            "## Verification Checklist",
            "",
            "- Verify the selected child skill actually matches the user request.",
            "- Verify the final answer names the child skill or subdirectory that was used.",
            "- Report any remaining ambiguity, missing child skills, or unverified routing assumptions.",
            "",
            "## Bundled Resources",
            "",
            "- Inspect child skill folders under `skills/` before treating the repository root as a standalone skill.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_skill(skill_md: Path, frontmatter: dict, body: str) -> None:
    yaml_text = yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=False).strip()
    skill_md.write_text(f"---\n{yaml_text}\n---\n\n{body.lstrip()}", encoding="utf-8")


def repair_missing_skill(skill_dir: Path) -> tuple[bool, list[str]]:
    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists():
        return False, []

    nested_skills = find_nested_skill_packages(skill_dir)
    if nested_skills:
        frontmatter = {
            "name": normalize_skill_name(skill_dir.name),
            "description": (
                f"Route requests across the bundled child skills in {normalize_skill_name(skill_dir.name)}. "
                "Use when a repository contains multiple related OpenClaw skills and the agent needs a root entrypoint that selects the right sub-skill before execution."
            ),
        }
        body = synthesize_collection_body(skill_dir, nested_skills)
        write_skill(skill_md, frontmatter, body)
        return True, [f"created_collection_entrypoint:{len(nested_skills)}"]

    existing = find_existing_skill_markdown(skill_dir)
    if existing is not None:
        text = load_skill_text(existing)
        frontmatter, body = parse_frontmatter(text)
        if frontmatter is None:
            frontmatter = synthesize_frontmatter(skill_dir, body or text)
            body = body or text
        write_skill(skill_md, frontmatter, body)
        return True, [f"recreated_skill_from:{existing.name}"]

    frontmatter = synthesize_frontmatter(skill_dir, "")
    body = synthesize_body(skill_dir)
    write_skill(skill_md, frontmatter, body)
    return True, ["created_skill_skeleton"]


def repair_frontmatter(skill_dir: Path) -> tuple[bool, list[str]]:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return False, []
    text = load_skill_text(skill_md)
    frontmatter, body = parse_frontmatter(text)
    changes: list[str] = []
    if frontmatter is None:
        frontmatter = synthesize_frontmatter(skill_dir, body)
        write_skill(skill_md, frontmatter, body)
        return True, ["repaired_frontmatter"]

    changed = False
    if not frontmatter.get("name"):
        frontmatter["name"] = normalize_skill_name(skill_dir.name)
        changes.append("added_name")
        changed = True
    if not frontmatter.get("description"):
        frontmatter["description"] = synthesize_frontmatter(skill_dir, body)["description"]
        changes.append("added_description")
        changed = True
    normalized = normalize_skill_name(str(frontmatter.get("name", "")))
    if normalized != frontmatter.get("name"):
        frontmatter["name"] = normalized
        changes.append("normalized_name")
        changed = True
    if changed:
        write_skill(skill_md, frontmatter, body)
    return changed, changes


def repair_broken_links(skill_dir: Path) -> tuple[bool, list[str]]:
    skill_md = skill_dir / "SKILL.md"
    text = load_skill_text(skill_md)
    changed = False
    fixes = 0

    all_files = [p for p in skill_dir.rglob("*") if p.is_file() and p.name != "SKILL.md"]

    def rank_candidates(label: str, target: str) -> list[Path]:
        basename = Path(target).name
        exact = [p for p in all_files if p.name == basename]
        if exact:
            return exact

        target_tokens = set(re.findall(r"[a-z0-9]+", f"{label} {Path(target).stem}".lower()))
        scored: list[tuple[int, str, Path]] = []
        for path in all_files:
            hay = " ".join(path.parts).lower()
            tokens = set(re.findall(r"[a-z0-9]+", hay))
            overlap = len(target_tokens & tokens)
            if overlap:
                scored.append((overlap, hay, path))
        scored.sort(key=lambda item: (-item[0], item[1]))
        if len(scored) == 1:
            return [scored[0][2]]
        if len(scored) >= 2 and scored[0][0] > scored[1][0]:
            return [scored[0][2]]
        return []

    def replace(match: re.Match[str]) -> str:
        nonlocal changed, fixes
        label, target = match.groups()
        target = target.strip()
        if "://" in target or target.startswith("#"):
            return match.group(0)
        resolved = (skill_dir / target).resolve()
        if resolved.exists():
            return match.group(0)
        candidates = rank_candidates(label, target)
        if len(candidates) == 1:
            rel = candidates[0].relative_to(skill_dir).as_posix()
            changed = True
            fixes += 1
            return f"[{label}]({rel})"
        changed = True
        fixes += 1
        return f"`{label}`"

    updated = LINK_RE.sub(replace, text)
    if changed:
        skill_md.write_text(updated, encoding="utf-8")
    return changed, [f"fixed_broken_links:{fixes}"] if changed else []


def split_long_body(skill_dir: Path, max_words: int = 2200) -> tuple[bool, list[str]]:
    skill_md = skill_dir / "SKILL.md"
    text = load_skill_text(skill_md)
    frontmatter, body = parse_frontmatter(text)
    if frontmatter is None:
        return False, []
    words = body.split()
    if len(words) <= max_words:
        return False, []

    matches = list(HEADING_RE.finditer(body))
    word_matches = list(re.finditer(r"\S+", body))
    if not word_matches:
        return False, []

    target_word_index = min(max_words - 200, len(word_matches) - 1)
    target_char = word_matches[target_word_index].start()
    candidate_headings = [match.start() for match in matches if 300 <= match.start() <= target_char]
    split_at = candidate_headings[-1] if candidate_headings else target_char

    head = body[:split_at].rstrip()
    tail = body[split_at:].lstrip()
    references_dir = skill_dir / "references"
    references_dir.mkdir(parents=True, exist_ok=True)
    detail_path = references_dir / "generated-long-body.md"
    detail_path.write_text("# Additional Skill Details\n\n" + tail, encoding="utf-8")
    head += (
        "\n\n## Additional Details\n\n"
        "See [generated-long-body.md](references/generated-long-body.md) for the extended material moved out of the main skill body.\n"
    )
    write_skill(skill_md, frontmatter, head)
    return True, ["split_long_body"]


def expand_thin_body(skill_dir: Path, min_words: int = 140) -> tuple[bool, list[str]]:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return False, []

    text = load_skill_text(skill_md)
    frontmatter, body = parse_frontmatter(text)
    if frontmatter is None:
        return False, []

    if len(body.split()) >= min_words:
        return False, []

    title_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else "Skill"
    normalized_name = normalize_skill_name(str(frontmatter.get("name") or skill_dir.name))
    references = sorted(path.relative_to(skill_dir).as_posix() for path in (skill_dir / "references").rglob("*") if path.is_file()) if (skill_dir / "references").exists() else []
    scripts = sorted(path.relative_to(skill_dir).as_posix() for path in (skill_dir / "scripts").glob("*.py")) if (skill_dir / "scripts").exists() else []

    sections: list[str] = []
    body_lower = body.lower()

    if "## Purpose" not in body:
        sections.extend(
            [
                "## Purpose",
                "",
                f"Use `{normalized_name}` when the request matches the {title} workflow and a repeatable OpenClaw-compatible procedure is more reliable than an improvised answer.",
                f"This skill should guide the operator through a scoped execution path, keep the working context small, and leave enough breadcrumbs for later retries or verification.",
                "",
            ]
        )

    if "## When To Use" not in body:
        sections.extend(
            [
                "## When To Use",
                "",
                "- Use it when the request clearly falls inside this skill's domain or packaged operating procedure.",
                "- Use it when bundled references, configuration, or helper scripts are likely to produce a more reliable result than a generic response.",
                "- Avoid it when the task does not match the skill trigger surface or when a lighter workflow would be safer.",
                "",
            ]
        )

    if "## Workflow" not in body:
        sections.extend(
            [
                "## Workflow",
                "",
                "1. Restate the goal in the language of this skill so the intended outcome is explicit.",
                "2. Inspect the smallest relevant bundled references, scripts, or config before acting.",
                "3. Execute the workflow in checkpoints and keep intermediate results easy to inspect.",
                "4. If a step fails, tighten the scope, apply the closest bundled guidance, and retry deliberately.",
                "",
            ]
        )

    if "## Failure Recovery" not in body:
        sections.extend(
            [
                "## Failure Recovery",
                "",
                "- If required inputs or credentials are missing, stop and name the missing dependency before continuing.",
                "- If a helper command fails, capture the error and compare it against the nearest reference or script expectations.",
                "- If the workflow remains uncertain after one retry, preserve partial output and report the blocker instead of guessing.",
                "",
            ]
        )

    if "verify" not in body_lower:
        sections.extend(
            [
                "## Verification Checklist",
                "",
                "- Verify the final output matches the user's requested outcome and format.",
                "- Verify any helper scripts, APIs, or references were used with the intended inputs.",
                "- Report what was verified directly and what remains assumed or unverified.",
                "",
            ]
        )

    resource_lines: list[str] = []
    if references and "references/" not in body:
        preview = ", ".join(f"`{item}`" for item in references[:3])
        resource_lines.append(f"- Read bundled references such as {preview} before improvising domain-specific steps.")
    if scripts and "scripts/" not in body:
        preview = ", ".join(f"`{item}`" for item in scripts[:3])
        resource_lines.append(f"- Prefer deterministic helpers such as {preview} when they already encode part of the workflow.")
    if resource_lines:
        sections.extend(["## Bundled Resources", ""] + resource_lines + [""])

    if not sections:
        return False, []

    expanded_body = body.rstrip() + "\n\n" + "\n".join(sections).rstrip() + "\n"
    write_skill(skill_md, frontmatter, expanded_body)
    return True, ["expanded_thin_body"]


def repair_skill(skill_dir: Path) -> dict:
    skill_dir = Path(skill_dir)
    changes: list[str] = []
    changed = False

    for fn in (repair_missing_skill, repair_frontmatter, repair_broken_links, expand_thin_body, split_long_body):
        local_changed, local_changes = fn(skill_dir)
        changed = changed or local_changed
        changes.extend(local_changes)

    return {"changed": changed, "changes": changes, "skill_dir": str(skill_dir)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Repair common OpenClaw skill package issues.")
    parser.add_argument("skill_dir", help="Path to the skill directory")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    report = repair_skill(Path(args.skill_dir))
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Repair run for: {report['skill_dir']}")
        if report["changes"]:
            for change in report["changes"]:
                print(f"- {change}")
        else:
            print("No repairs applied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
