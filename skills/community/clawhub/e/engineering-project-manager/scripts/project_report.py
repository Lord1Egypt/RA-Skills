#!/usr/bin/env python3
"""Read-only project status from existing authoritative records; no health score."""

import argparse
from collections import Counter
import json
from pathlib import Path
import subprocess
import sys

from pm_common import active_requirement_records, git_capture, requirement_definitions


def read_object(root, relative):
    path = root / relative
    if not path.is_file():
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{relative}: expected a JSON object")
    return value


def build_report(project):
    root = Path(project).resolve()
    if not root.is_dir():
        raise ValueError("Project directory does not exist")
    report = {
        "report_version": 1,
        "git": {"commit": git_capture(root, "rev-parse", "HEAD"),
                "branch": git_capture(root, "branch", "--show-current")},
        "tasks": None, "requirements": None, "changes": None,
        "baselines": None, "verification": None, "management": None, "findings": [],
        "release_readiness": "NOT_EVALUATED",
        "notice": "Operational status only; not a SPICE assessment or certification.",
    }
    status = git_capture(root, "status", "--porcelain")
    report["git"]["dirty"] = None if status is None else bool(status)
    if report["git"]["commit"] is None:
        report["findings"].append("Git commit unavailable")

    try:
        tasks = read_object(root, "00-project/management/TASKS.json")
        if tasks is not None:
            from project_state import normalize_state, validate_state
            problems = validate_state(normalize_state(tasks))
            if problems:
                raise ValueError("Invalid task state: " + "; ".join(problems))
            values = tasks["tasks"]
            report["tasks"] = {
                "counts": dict(sorted(Counter(t["status"] for t in values).items())),
                "total": len(values),
                "ready": [t["id"] for t in values if t["status"] == "READY"],
                "blocked": [{"id": t["id"], "reason": t.get("blocker")}
                            for t in values if t["status"] == "BLOCKED"],
            }
        else:
            report["findings"].append("TASKS.json is absent")
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        report["findings"].append(str(exc))

    try:
        active = active_requirement_records(root)
        all_requirements = requirement_definitions(root)
        report["requirements"] = {
            "active_revisioned": len(active),
            "legacy": sum(r.get("scheme") == "LEGACY" for r in all_requirements),
            "status_counts": dict(sorted(Counter(r.get("status") for r in active).items())),
            "note": "Counts are inventory; use requirements_lint.py and traceability_check.py for validation.",
        }
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        report["findings"].append(str(exc))

    try:
        changes = read_object(root, "08-configuration/CHANGE-REQUESTS.json")
        if changes is not None:
            from change_manager import validate_registry
            problems = validate_registry(root, changes)
            if problems:
                raise ValueError("Invalid change registry: " + "; ".join(problems))
            report["changes"] = dict(sorted(Counter(c["Status"] for c in changes["changes"]).items()))
        from configuration_audit import audit, current_baseline
        errors, warnings = audit(root)
        report["findings"].extend(errors)
        baseline_registry = read_object(root, "08-configuration/BASELINE-REGISTRY.json")
        report["baselines"] = {
            "enabled": (root / "08-configuration/CONFIGURATION-MANAGEMENT.json").is_file(),
            "current": current_baseline(root),
            "count": len(baseline_registry["baselines"]) if baseline_registry else 0,
            "warnings": warnings,
        }
    except (OSError, ValueError, TypeError, KeyError, AttributeError, RuntimeError) as exc:
        report["findings"].append(str(exc))

    try:
        from verification_evidence_audit import audit
        errors, warnings = audit(root)
        report["findings"].extend(errors)
        if (root / "05-verification/EVIDENCE-MANAGEMENT.json").is_file():
            from verification_evidence import coverage, load_registry, validate_registry
            registry = load_registry(root)
            problems, _ = validate_registry(root, registry)
            if problems:
                raise ValueError("Evidence registry invalid; coverage withheld")
            report["verification"] = {"enabled": True, "coverage": coverage(root, registry)}
        else:
            report["verification"] = {"enabled": False, "warnings": warnings}
    except (OSError, ValueError, TypeError, KeyError, AttributeError, RuntimeError) as exc:
        report["findings"].append(str(exc))
    from management_audit import summary
    report["management"] = summary(root)
    report["findings"].extend(report["management"]["findings"])
    report["findings"] = sorted(set(report["findings"]))
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--release-check", action="store_true", help="Also run the real release gate, read-only")
    args = parser.parse_args(argv)
    try:
        report = build_report(args.project)
        if args.release_check:
            result = subprocess.run(
                [sys.executable, str(Path(__file__).with_name("release_check.py")), args.project],
                capture_output=True, text=True, timeout=180,
            )
            report["release_readiness"] = "PASS" if result.returncode == 0 else "FAIL"
            report["release_check"] = {"exit_code": result.returncode,
                                       "output": result.stdout + result.stderr}
        if args.json:
            print(json.dumps(report, indent=2, sort_keys=True))
        else:
            print("PROJECT STATUS — " + report["notice"])
            for key in ("git", "tasks", "requirements", "changes", "baselines", "verification", "management"):
                print(f"\n{key.title()}:\n{json.dumps(report[key], indent=2)}")
            print("\nRelease readiness: " + report["release_readiness"])
            for finding in report["findings"]:
                print("ATTENTION: " + finding)
        return 1 if report["findings"] or report["release_readiness"] == "FAIL" else 0
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
