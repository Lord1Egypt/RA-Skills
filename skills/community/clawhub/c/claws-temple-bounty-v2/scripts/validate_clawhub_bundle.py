#!/usr/bin/env python3
"""Validate the committed ClawHub bundle for claws-temple-bounty."""

from __future__ import annotations

import json
import re
import sys
import hashlib
from pathlib import Path


THIS_FILE = Path(__file__).resolve()


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def parse_version_from_skill(skill_path: Path) -> str:
    text = skill_path.read_text(encoding="utf-8")
    match = re.search(r"^version:\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$", text, re.MULTILINE)
    if not match:
        fail(f"could not resolve version from {skill_path}")
    return match.group(1)


def parse_simple_yaml_map(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            fail(f"unsupported manifest.yaml line in {path}: {raw_line!r}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def resolve_bundle_root(argv: list[str]) -> tuple[Path, Path | None]:
    if len(argv) > 1:
        bundle_root = Path(argv[1]).resolve()
        repo_candidate = THIS_FILE.parents[1]
        repo_root = None if (repo_candidate / "SKILL.md").exists() else repo_candidate
        return bundle_root, repo_root

    implicit_bundle_root = THIS_FILE.parents[1]
    if (implicit_bundle_root / "SKILL.md").exists():
        return implicit_bundle_root, None

    repo_root = THIS_FILE.parents[1]
    return repo_root / "dist" / "clawhub" / "claws-temple-bounty", repo_root


def main(argv: list[str]) -> None:
    bundle_root, repo_root = resolve_bundle_root(argv)

    if not bundle_root.exists():
        fail(f"missing ClawHub bundle directory: {bundle_root}")

    required_files = [
        bundle_root / "SKILL.md",
        bundle_root / "agents" / "openai.yaml",
        bundle_root / "clawhub-bundle-manifest.json",
        bundle_root / "manifest.yaml",
        bundle_root / "config" / "dependency-sources.json",
        bundle_root / "config" / "faction-proposals.json",
        bundle_root / "references" / "brand-lexicon.zh.md",
        bundle_root / "references" / "brand-lexicon.en.md",
        bundle_root / "references" / "output-contract.md",
        bundle_root / "references" / "task-flows" / "task-roadmap.md",
        bundle_root / "references" / "task-flows" / "task-1-coordinate-card.md",
        bundle_root / "references" / "task-flows" / "task-2-resonance-partner.md",
        bundle_root / "references" / "task-flows" / "task-3-faction-oath.md",
        bundle_root / "references" / "task-flows" / "task-4-curio-board.md",
        bundle_root / "references" / "task-flows" / "task-5-social-signal.md",
        bundle_root / "scripts" / "smoke-check.sh",
        bundle_root / "scripts" / "release-gate.sh",
        bundle_root / "scripts" / "self-heal-local-dependency.sh",
        bundle_root / "scripts" / "task4-live-skill-probe.sh",
        bundle_root / "scripts" / "test-rollout-gate.sh",
        bundle_root / "scripts" / "validate_clawhub_bundle.py",
    ]
    for path in required_files:
        if not path.exists():
            fail(f"missing required bundle file: {path}")

    for forbidden in (".claude", ".opencode", ".cursor", "AGENTS.md"):
        if (bundle_root / forbidden).exists():
            fail(f"forbidden repository-only artifact leaked into bundle: {bundle_root / forbidden}")

    text_files = [
        path
        for path in bundle_root.rglob("*")
        if path.is_file() and path.suffix in {".md", ".sh", ".json", ".yaml", ".yml", ".txt"}
    ]
    repo_root_marker = "skills" + "/claws-temple-bounty/"
    for path in text_files:
        text = path.read_text(encoding="utf-8")
        if repo_root_marker in text:
            fail(f"bundle still contains repository-root path reference in {path}")

    bundle_skill_path = bundle_root / "SKILL.md"
    manifest = json.loads((bundle_root / "clawhub-bundle-manifest.json").read_text(encoding="utf-8"))
    clawhub_manifest = parse_simple_yaml_map(bundle_root / "manifest.yaml")
    bundle_skill_text = bundle_skill_path.read_text(encoding="utf-8")
    for marker in (
        "## ClawHub Runtime Notes",
        "orchestrator skill",
        "agent-spectrum",
        "resonance-contract",
        "tomorrowdao-agent-skills",
        "portkey-ca-agent-skills",
        "CA keystore password",
        "https://www.shitskills.net/skill.md",
        "No hidden private-key fallback",
        "intended publish target on ClawHub",
    ):
        if marker not in bundle_skill_text:
            fail(f"missing ClawHub runtime-note marker {marker!r} in bundle SKILL.md")

    bundle_version = parse_version_from_skill(bundle_skill_path)
    dependency_version = json.loads((bundle_root / "config" / "dependency-sources.json").read_text(encoding="utf-8")).get("version")
    faction_version = json.loads((bundle_root / "config" / "faction-proposals.json").read_text(encoding="utf-8")).get("version")
    if manifest.get("skill_version") != bundle_version:
        fail(
            "bundle manifest version must match bundle SKILL.md version: "
            f"{manifest.get('skill_version')!r} != {bundle_version!r}"
        )
    expected_manifest_fields = {
        "slug": "claws-temple-bounty-v2",
        "display_name": "Claws Temple Bounty 2.0",
        "version": bundle_version,
        "license": "MIT-0",
    }
    for key, expected_value in expected_manifest_fields.items():
        actual_value = clawhub_manifest.get(key)
        if actual_value != expected_value:
            fail(
                f"manifest.yaml field {key!r} must be {expected_value!r}, "
                f"got {actual_value!r}"
            )
    for key in ("description", "author", "homepage"):
        if not clawhub_manifest.get(key):
            fail(f"manifest.yaml is missing required non-empty field: {key}")

    if dependency_version != bundle_version:
        fail(
            "bundle dependency source catalog version must match bundle SKILL.md version: "
            f"{dependency_version!r} != {bundle_version!r}"
        )
    if faction_version != bundle_version:
        fail(
            "bundle faction proposal config version must match bundle SKILL.md version: "
            f"{faction_version!r} != {bundle_version!r}"
        )

    if repo_root is not None:
        canonical_skill_path = repo_root / "skills" / "claws-temple-bounty" / "SKILL.md"
        if canonical_skill_path.exists():
            canonical_version = parse_version_from_skill(canonical_skill_path)
            if canonical_version != bundle_version:
                fail(
                    "canonical SKILL.md version must match ClawHub bundle version: "
                    f"{canonical_version!r} != {bundle_version!r}"
                )
        source_dir = repo_root / "skills" / "claws-temple-bounty"
        for rel_path, expected_hash in manifest.get("source_files", {}).items():
            bundle_equivalent = bundle_root / rel_path
            if not bundle_equivalent.exists():
                fail(f"bundle is missing a file declared in the manifest: {bundle_equivalent}")
            source_path = source_dir / rel_path
            if not source_path.exists():
                fail(f"bundle manifest references a missing canonical source file: {source_path}")
            actual_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
            if actual_hash != expected_hash:
                fail(
                    "ClawHub bundle is stale for canonical source file "
                    f"{source_path}: {actual_hash!r} != {expected_hash!r}; run scripts/build-clawhub.sh"
                )
        for name, expected_hash in manifest.get("generator_files", {}).items():
            source_path = repo_root / "scripts" / name
            if not source_path.exists():
                fail(f"bundle manifest references a missing generator file: {source_path}")
            actual_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
            if actual_hash != expected_hash:
                fail(
                    "ClawHub bundle is stale for generator file "
                    f"{source_path}: {actual_hash!r} != {expected_hash!r}; run scripts/build-clawhub.sh"
                )

    print(f"OK: ClawHub bundle validated at {bundle_root}")


if __name__ == "__main__":
    main(sys.argv)
