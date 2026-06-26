#!/usr/bin/env python3

from __future__ import annotations

import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path


REPO_FILES_WITH_VERSION = ("README.md", "README_CN.md", "README_EN.md", "INSTALL.md")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_manifest(root: Path) -> dict:
    return tomllib.loads((root / "manifest.toml").read_text(encoding="utf-8"))


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def read_frontmatter(root: Path) -> dict[str, str]:
    skill_text = (root / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", skill_text, re.DOTALL)
    ensure(match is not None, "SKILL.md is missing frontmatter.")

    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


def check_versions(root: Path, manifest: dict) -> None:
    version = manifest["version"]
    for relative_path in REPO_FILES_WITH_VERSION:
        text = (root / relative_path).read_text(encoding="utf-8")
        ensure(
            f"`{version}`" in text,
            f"{relative_path} does not mention manifest version {version}.",
        )


def check_skill_frontmatter(root: Path) -> None:
    fields = read_frontmatter(root)
    ensure(fields.get("name") == "memory-system", "SKILL.md frontmatter name must be memory-system.")
    ensure("Use when" in fields.get("description", ""), "SKILL.md description should follow the OpenClaw skill format.")
    ensure(fields.get("homepage") == "https://github.com/cjke84/agent-memory-system-guide", "SKILL.md homepage is missing or incorrect.")
    ensure(fields.get("user-invocable") == "true", "SKILL.md should expose user-invocable: true.")
    ensure("metadata" in fields and '"openclaw"' in fields["metadata"], "SKILL.md metadata.openclaw is missing.")


def run_pytest(root: Path) -> None:
    command = [sys.executable, "-m", "pytest", "-q"]
    print(f"$ {' '.join(command[2:])}")
    env = dict(os.environ)
    env["AGENT_MEMORY_RELEASE_CHECK"] = "1"
    result = subprocess.run(
        command,
        cwd=root,
        text=True,
        capture_output=True,
        env=env,
        check=False,
    )
    if result.stdout:
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
    if result.stderr:
        print(result.stderr, file=sys.stderr, end="" if result.stderr.endswith("\n") else "\n")
    ensure(result.returncode == 0, "pytest -q failed.")


def main() -> int:
    root = repo_root()
    manifest = load_manifest(root)
    check_versions(root, manifest)
    check_skill_frontmatter(root)
    run_pytest(root)
    print(f"Version: {manifest['version']}")
    print("Release checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
