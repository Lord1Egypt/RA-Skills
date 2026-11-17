#!/usr/bin/env python3
"""Validate an AgentScope project configuration."""

import argparse
import os
import sys
from pathlib import Path
from typing import List


def find_project_root(start: Path) -> Path:
    current = start.resolve()
    while current != current.parent:
        if (current / "pyproject.toml").exists():
            return current
        current = current.parent
    return start.resolve()


def check_pyproject(project_root: Path) -> List[str]:
    findings = []
    pyproject = project_root / "pyproject.toml"
    if not pyproject.exists():
        findings.append("FAIL: pyproject.toml is missing")
        return findings
    text = pyproject.read_text(encoding="utf-8")
    if "agentscope" not in text:
        findings.append("FAIL: agentscope dependency not found in pyproject.toml")
    else:
        findings.append("PASS: agentscope dependency detected")
    return findings


def check_env(project_root: Path) -> List[str]:
    findings = []
    env = project_root / ".env"
    if not env.exists():
        findings.append("WARN: .env file is missing")
        return findings
    text = env.read_text(encoding="utf-8")
    if "OPENAI_API_KEY" not in text and "DASHSCOPE_API_KEY" not in text:
        findings.append("WARN: no obvious API key placeholder found in .env")
    else:
        findings.append("PASS: .env contains an API key placeholder")
    return findings


def check_imports(project_root: Path) -> List[str]:
    findings = []
    py_files = list(project_root.rglob("*.py"))
    if not py_files:
        findings.append("WARN: no Python files found")
        return findings
    for path in py_files[:10]:
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        if "from agentscope" in text or "import agentscope" in text:
            findings.append(f"PASS: found AgentScope usage in {path.relative_to(project_root)}")
            break
    else:
        findings.append("WARN: no obvious AgentScope imports found in first 10 Python files")
    return findings


def validate(project_path: Path) -> int:
    project_root = find_project_root(project_path)
    findings = []
    findings.extend(check_pyproject(project_root))
    findings.extend(check_env(project_root))
    findings.extend(check_imports(project_root))

    print(f"# AgentScope Config Validator\n")
    print(f"Project root: {project_root}\n")
    for item in findings:
        print(f"- {item}")
    return 0 if all("FAIL" not in item for item in findings) else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate AgentScope project config")
    parser.add_argument("--project", required=True, type=Path)
    args = parser.parse_args()
    if not args.project.exists():
        print(f"FAIL: {args.project} does not exist")
        return 1
    return validate(args.project)


if __name__ == "__main__":
    sys.exit(main())
