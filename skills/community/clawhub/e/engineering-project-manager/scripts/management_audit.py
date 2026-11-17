#!/usr/bin/env python3
"""Read-only audit of the optional, versioned project management registries."""

import argparse
from collections import Counter
import importlib
import json
from pathlib import Path
import sys

from management_common import RecordError, Store, previously_managed, project_file, read_json

MARKER = "00-project/management/MANAGEMENT.json"
MODELS = (
    ("risks", "09-risks/RISKS.json", "RISK", "risk_manager"),
    ("problems", "07-quality/PROBLEMS.json", "PRB", "problem_manager"),
    ("milestones", "00-project/management/MILESTONES.json", "MS", "milestone_manager"),
    ("sources", "01-requirements/intake/SOURCES.json", "SRC", "intake_manager"),
    ("compliance", "01-requirements/intake/COMPLIANCE.json", "CMP", "compliance_manager"),
)


def marker_errors(project):
    marker = project_file(project, MARKER, must_exist=False)
    if not marker.exists():
        if previously_managed(project, MARKER):
            return ["Management activation record was deleted; restore it from Git"], False
        return [], False
    try:
        value = read_json(marker)
        if (not isinstance(value, dict) or value.get("enabled") is not True
                or type(value.get("schema_version")) is not int or value["schema_version"] != 1
                or value.get("registries") != [model[0] for model in MODELS]):
            return ["Invalid management activation record"], True
    except RecordError as exc:
        return [str(exc)], True
    return [], True


def audit(project, release=False):
    errors, warnings = [], []
    try:
        problems, all_enabled = marker_errors(project)
        errors.extend(problems)
        for kind, relative, prefix, module_name in MODELS:
            store = Store(project, relative, kind, prefix)
            if not store.exists():
                if all_enabled or previously_managed(project, relative):
                    errors.append(f"{kind}: previously enabled registry is missing; restore it")
                continue
            try:
                store.read()
                module = importlib.import_module(module_name)
                model_errors, model_warnings = module.audit(Path(project), release=release)
                errors.extend(f"{kind}: {item}" for item in model_errors)
                warnings.extend(f"{kind}: {item}" for item in model_warnings)
            except (RecordError, OSError, ValueError, TypeError, KeyError, AttributeError, RuntimeError) as exc:
                errors.append(f"{kind}: registry audit failed: {exc}")
        source_path = project_file(project, MODELS[3][1], must_exist=False)
        coverage_path = project_file(project, MODELS[4][1], must_exist=False)
        if source_path.exists() and not coverage_path.exists() and release:
            source_data = Store(project, MODELS[3][1], "sources", "SRC").read()
            if source_data["records"]:
                errors.append("Sources exist but the compliance matrix is not initialized")
    except (RecordError, OSError, ValueError) as exc:
        errors.append(str(exc))
    return sorted(set(errors)), sorted(set(warnings))


def summary(project):
    result = {"registries": {}, "findings": [], "warnings": []}
    for kind, relative, prefix, _ in MODELS:
        try:
            store = Store(project, relative, kind, prefix)
            if not store.exists():
                result["registries"][kind] = {"enabled": False}
                continue
            data = store.read()
            result["registries"][kind] = {"enabled": True, "total": len(data["records"]),
                                           "status_counts": dict(sorted(Counter(r["status"] for r in data["records"]).items()))}
        except (RecordError, OSError, ValueError) as exc:
            result["registries"][kind] = {"enabled": True, "invalid": True}
            result["findings"].append(f"{kind}: {exc}")
    errors, warnings = audit(project)
    result["findings"] = sorted(set(result["findings"] + errors))
    result["warnings"] = warnings
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project")
    parser.add_argument("--strict", action="store_true", help="Compatibility flag; integrity errors always fail")
    parser.add_argument("--release", action="store_true", help="Also enforce release-blocking dispositions and coverage")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    errors, warnings = audit(Path(args.project), release=args.release)
    if args.json:
        print(json.dumps({"errors": errors, "warnings": warnings, "release": args.release}, indent=2))
    else:
        for error in errors:
            print("ERROR:", error)
        for warning in warnings:
            print("WARN:", warning)
        print("MANAGEMENT AUDIT:", "FAIL" if errors else "PASS")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
