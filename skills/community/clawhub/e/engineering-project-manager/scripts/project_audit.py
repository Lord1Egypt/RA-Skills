#!/usr/bin/env python3

import argparse
import json
import sys
from pathlib import Path

from pm_common import (
    VALID_TASK_STATUS,
    git_capture,
    load_tasks,
)


CORE_FILES = [
    "00-project/PROJECT.md",
    "00-project/PROCESS-SCOPE.md",
    "00-project/STANDARDS.md",
    "00-project/STATUS.md",
    "00-project/DECISIONS.md",
    "00-project/management/TASKS.json",
    "00-project/management/TASKS.md",
    "01-requirements/TRACEABILITY.md",
    "07-quality/QA-PLAN.md",
    "08-configuration/CONFIGURATION-PLAN.md",
    "08-configuration/CONFIGURATION-ITEMS.md",
    "08-configuration/BASELINES.md",
    "09-risks/RISK-REGISTER.md",
]


DOMAIN_MAP = {
    "SYS": ("system", "SYS"),
    "SWE": ("software", "SWE"),
    "HWE": ("hardware", "HWE"),
    "MLE": ("machine-learning", "MLE"),
    "MECH": ("mechanical", "MEC"),
    "CYBER": ("cybersecurity", "CYB"),
}


def cycles(tasks):
    table = {
        t["id"]: t
        for t in tasks
    }

    visiting = set()
    visited = set()
    found = []

    def visit(tid, path):
        if tid in visiting:
            found.append(
                path + [tid]
            )
            return

        if tid in visited:
            return

        visiting.add(tid)

        for dep in table.get(
            tid,
            {},
        ).get("depends_on", []):
            if dep in table:
                visit(
                    dep,
                    path + [tid],
                )

        visiting.remove(tid)
        visited.add(tid)

    for tid in table:
        visit(tid, [])

    return found


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project")
    parser.add_argument(
        "--strict",
        action="store_true",
    )

    args = parser.parse_args()
    root = Path(args.project)

    errors = []
    warnings = []

    for rel in CORE_FILES:
        if not (root / rel).exists():
            errors.append(
                f"Mandatory file missing: {rel}"
            )

    if (root / "01-planning").exists():
        errors.append(
            "Legacy structure forbidden: "
            "01-planning"
        )

    bootstrap = (
        root
        / "00-project"
        / "BOOTSTRAP.json"
    )

    if bootstrap.exists():
        try:
            metadata = json.loads(
                bootstrap.read_text(
                    encoding="utf-8"
                )
            )

            for domain in metadata.get(
                "domains",
                [],
            ):
                if domain not in DOMAIN_MAP:
                    continue

                directory, prefix = (
                    DOMAIN_MAP[domain]
                )

                req = (
                    root
                    / "01-requirements"
                    / directory
                    / f"{prefix}-REQUIREMENTS.md"
                )

                if not req.exists():
                    errors.append(
                        f"{domain}: requirements missing"
                    )

                if domain in {
                    "SYS",
                    "SWE",
                    "HWE",
                    "MLE",
                }:
                    arch = (
                        root
                        / "02-architecture"
                        / directory
                        / f"{prefix}-ARCHITECTURE.md"
                    )

                    if not arch.exists():
                        errors.append(
                            f"{domain}: architecture missing"
                        )

        except Exception as exc:
            errors.append(
                f"Invalid BOOTSTRAP.json: {exc}"
            )

    if not (root / ".git").exists():
        errors.append(
            "Local Git repository missing"
        )
    else:
        origin = git_capture(
            root,
            "remote",
            "get-url",
            "origin",
        )

        if not origin:
            errors.append(
                "Remote origin missing"
            )
        else:
            print("Git origin:", origin)

    tasks_data = load_tasks(root)

    if tasks_data is None:
        errors.append(
            "TASKS.json missing"
        )
    else:
        tasks = tasks_data.get(
            "tasks",
            [],
        )

        ids = [
            task.get("id")
            for task in tasks
        ]

        if len(ids) != len(set(ids)):
            errors.append(
                "Duplicate task IDs"
            )

        known = set(ids)

        for task in tasks:
            tid = task.get(
                "id",
                "<unknown>",
            )

            status = task.get("status")

            if status not in VALID_TASK_STATUS:
                errors.append(
                    f"{tid}: invalid state {status}"
                )

            for dep in task.get(
                "depends_on",
                [],
            ):
                if dep not in known:
                    errors.append(
                        f"{tid}: unknown dependency {dep}"
                    )

        for cycle in cycles(tasks):
            errors.append(
                "Dependency cycle: "
                + " -> ".join(cycle)
            )

    status_file = (
        root
        / "00-project"
        / "BOOTSTRAP-STATUS.json"
    )

    if not status_file.exists():
        warnings.append(
            "BOOTSTRAP-STATUS.json missing"
        )
    else:
        try:
            status = json.loads(
                status_file.read_text(
                    encoding="utf-8"
                )
            )

            if not status.get("complete"):
                errors.append(
                    "Bootstrap not COMPLETE"
                )

        except Exception as exc:
            errors.append(
                f"Invalid BOOTSTRAP-STATUS.json: {exc}"
            )

    for warning in warnings:
        print("WARNING:", warning)

    for error in errors:
        print("ERROR:", error)

    print(
        f"PROJECT AUDIT: "
        f"{len(errors)} error(s), "
        f"{len(warnings)} warning(s)"
    )

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
