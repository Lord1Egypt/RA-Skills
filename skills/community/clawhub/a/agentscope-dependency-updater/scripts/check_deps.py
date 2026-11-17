#!/usr/bin/env python3
"""Inspect AgentScope project dependencies and suggest safe updates."""

import argparse
import re
import sys
from pathlib import Path


def read_pyproject(project_root: Path) -> str:
    return (project_root / "pyproject.toml").read_text(encoding="utf-8")


def parse_dependencies(text: str):
    deps = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith('"agentscope') or line.startswith("'agentscope"):
            deps.append(("agentscope", line.strip('",')))
        elif line.startswith('"') and ">=" in line:
            name = line.split(">=")[0].strip('", ')
            deps.append((name, line.strip('",')))
    return deps


def validate(project_path: Path) -> int:
    project_root = project_path.resolve()
    if not (project_root / "pyproject.toml").exists():
        print("FAIL: pyproject.toml not found")
        return 1

    text = read_pyproject(project_root)
    deps = parse_dependencies(text)
    print("# AgentScope Dependency Updater\n")
    print(f"Project root: {project_root}\n")
    if not deps:
        print("No obvious dependencies detected.")
        return 0

    for name, raw in deps:
        print(f"- {raw}")
    print("\nAction: review PyPI or your internal index before bumping.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect AgentScope dependencies")
    parser.add_argument("--project", required=True, type=Path)
    args = parser.parse_args()
    if not args.project.exists():
        print(f"FAIL: {args.project} does not exist")
        return 1
    return validate(args.project)


if __name__ == "__main__":
    sys.exit(main())
