#!/usr/bin/env python3

import argparse
import subprocess
import sys
from pathlib import Path

from pm_common import (
    git_capture,
    load_tasks,
    read_text,
)


def run_audit(script_dir, name, project, extra_args=None):
    extra_args = extra_args or []
    result = subprocess.run(
        [
            sys.executable,
            str(script_dir / name),
            str(project),
            "--strict",
            *extra_args,
        ]
    )

    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project")
    parser.add_argument("--baseline", help="Exact FROZEN baseline to authorize")

    args = parser.parse_args()

    project = Path(args.project)
    scripts = Path(__file__).parent

    errors = []

    checks = [
        "project_audit.py",
        "requirements_lint.py",
        "traceability_check.py",
        "domain_audit.py",
        "configuration_audit.py",
        "verification_evidence_audit.py",
        "management_audit.py",
    ]

    for check in checks:
        print()
        print("===", check, "===")

        extra_args = []
        if check == "management_audit.py":
            extra_args = ["--release"]
        if check == "configuration_audit.py":
            extra_args = ["--release-candidate"]
            if args.baseline:
                extra_args.append(args.baseline)

        if not run_audit(
            scripts,
            check,
            project,
            extra_args,
        ):
            errors.append(
                f"{check}: FAIL"
            )

    tasks_data = load_tasks(project)

    if tasks_data:
        for task in tasks_data.get(
            "tasks",
            [],
        ):
            if (
                task.get("priority")
                in {"P0", "P1"}
                and task.get("status")
                not in {"DONE", "CANCELLED"}
            ):
                errors.append(
                    f"{task['id']}: "
                    f"{task['priority']} "
                    f"still {task['status']}"
                )

    status = (
        project
        / "00-project"
        / "STATUS.md"
    )

    g3 = None

    if status.exists():
        for line in read_text(
            status
        ).splitlines():

            if line.strip().startswith(
                "| G3 "
            ):
                cols = [
                    c.strip()
                    for c in line.strip("|").split("|")
                ]

                if len(cols) >= 2:
                    g3 = cols[1]

    if g3 not in {
        "PASS",
        "PASS_WITH_ACTIONS",
    }:
        errors.append(
            f"G3 Release Readiness not PASS: {g3}"
        )

    dirty = git_capture(
        project,
        "status",
        "--porcelain",
    )

    if dirty:
        errors.append(
            "Git working tree not clean"
        )

    local = git_capture(
        project,
        "rev-parse",
        "HEAD",
    )

    import os

    ci_sha = (
        os.environ.get("CI_COMMIT_SHA")
        or os.environ.get("GITHUB_SHA")
    )

    if ci_sha:
        if local != ci_sha:
            errors.append(
                "Local HEAD differs from CI commit"
            )
    else:
        upstream = git_capture(
            project,
            "rev-parse",
            "@{u}",
        )

        if not upstream:
            errors.append(
                "Upstream branch missing"
            )
        elif local != upstream:
            errors.append(
                "Local HEAD differs from remote"
            )

    print()

    for error in errors:
        print("ERROR:", error)

    if errors:
        print(
            f"RELEASE CHECK: FAIL "
            f"({len(errors)} error(s))"
        )
        return 1

    print("RELEASE CHECK: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
