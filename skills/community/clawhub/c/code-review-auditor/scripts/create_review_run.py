#!/usr/bin/env python3
"""Create a timestamped code-review output folder for code-review-auditor."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path


CATEGORY_FILES = [
    "findings.md",
    "security.md",
    "architecture.md",
    "bugs.md",
    "code-smells.md",
    "patterns.md",
    "performance.md",
    "testing.md",
    "observability.md",
    "hotspots.md",
    "refactoring-plan.md",
]


def git_value(root: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=root,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        return result.stdout.strip()
    except Exception:
        return ""


def unique_run_dir(project_root: Path, timestamp: str) -> Path:
    review_root = project_root / "review"
    base = review_root / timestamp
    if not base.exists():
        return base
    for index in range(1, 100):
        candidate = review_root / f"{timestamp}-{index:02d}"
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"Could not create unique review directory for {timestamp}")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", nargs="?", default=".", help="Project root to receive review/")
    parser.add_argument("--mode", default="complete", help="Review mode")
    parser.add_argument("--scope", default="", help="Short scope description")
    parser.add_argument("--stacks", default="", help="Comma-separated detected stacks")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    run_dir = unique_run_dir(project_root, timestamp)
    metrics_dir = run_dir / "metrics"
    metrics_dir.mkdir(parents=True, exist_ok=False)

    stacks = [item.strip() for item in args.stacks.split(",") if item.strip()]
    rel_run_dir = os.path.relpath(run_dir, project_root)

    summary = f"""# Code Review Summary

- Mode: {args.mode}
- Created: {now.isoformat(timespec="seconds")}
- Project: {project_root}
- Scope: {args.scope or "Not specified"}
- Stacks detected: {", ".join(stacks) if stacks else "Not specified"}

## Executive Summary

Pending review notes.

## Top Risks

Pending.

## Findings By Severity

| Severity | Count |
|---|---:|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 0 |
| Info | 0 |

## Findings By Category

| Category | Count |
|---|---:|
| Bugs | 0 |
| Security | 0 |
| Architecture | 0 |
| Code Smells | 0 |
| Patterns | 0 |
| Performance | 0 |
| Testing | 0 |
| Observability | 0 |

## Recommended Next Actions

Pending.

## Report Index

- [Findings](findings.md)
- [Security](security.md)
- [Architecture](architecture.md)
- [Bugs](bugs.md)
- [Code Smells](code-smells.md)
- [Patterns](patterns.md)
- [Performance](performance.md)
- [Testing](testing.md)
- [Observability](observability.md)
- [Hotspots](hotspots.md)
- [Score](metrics/score.md)
- [Metadata](metadata.json)
- [Refactoring Plan](refactoring-plan.md)
"""
    write_text(run_dir / "summary.md", summary)

    for filename in CATEGORY_FILES:
        title = filename.removesuffix(".md").replace("-", " ").title()
        if filename == "refactoring-plan.md":
            body = "# Refactoring Plan\n\nNo refactoring plan created for this run yet.\n"
        else:
            body = f"# {title}\n\nNo findings recorded yet.\n"
        write_text(run_dir / filename, body)

    score = """# Review Score

- Risk Score: Not assessed
- Maintainability Score: Not assessed
- Security Posture: Unknown
- Test Confidence: Unknown
- Refactorability: Not assessed

## Drivers

Pending.
"""
    write_text(metrics_dir / "score.md", score)

    score_json = {
        "risk_score": None,
        "maintainability_score": None,
        "security_posture": "Unknown",
        "test_confidence": "Unknown",
        "refactorability": None,
        "severity_counts": {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0},
        "category_counts": {
            "bugs": 0,
            "security": 0,
            "architecture": 0,
            "code_smells": 0,
            "patterns": 0,
            "performance": 0,
            "testing": 0,
            "observability": 0,
        },
    }
    write_text(metrics_dir / "score.json", json.dumps(score_json, indent=2) + "\n")

    status = git_value(project_root, "status", "--porcelain")
    metadata = {
        "skill": "code-review-auditor",
        "mode": args.mode,
        "created_at_local": now.isoformat(timespec="seconds"),
        "review_directory": rel_run_dir,
        "repository": {
            "root": str(project_root),
            "git_branch": git_value(project_root, "branch", "--show-current"),
            "git_commit": git_value(project_root, "rev-parse", "HEAD"),
            "dirty": bool(status) if (project_root / ".git").exists() else None,
        },
        "scope": {"included": [], "excluded": [], "reason": args.scope},
        "stacks_detected": stacks,
        "commands_used": [],
        "limitations": [],
    }
    write_text(run_dir / "metadata.json", json.dumps(metadata, indent=2) + "\n")

    print(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
