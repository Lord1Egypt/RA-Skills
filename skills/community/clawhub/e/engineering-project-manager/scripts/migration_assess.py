#!/usr/bin/env python3
"""Non-destructive V1.0 -> V1.1 migration assessment for a project directory."""

import argparse
import json
import re
import sys
from pathlib import Path

from pm_common import (
    HEADING_DEF_RE,
    TABLE_DEF_RE,
    V11_BLOCK_END_RE,
    V11_BLOCK_START_RE,
    VERSIONED_REQ_PATTERN,
    read_text,
    requirement_files,
)


CM_MARKER = Path("08-configuration") / "CONFIGURATION-MANAGEMENT.json"
EVIDENCE_MARKER = Path("05-verification") / "EVIDENCE-MANAGEMENT.json"
TASKS_FILE = Path("00-project") / "management" / "TASKS.json"
TRACEABILITY_FILE = Path("01-requirements") / "TRACEABILITY.md"

CM_INIT_COMMANDS = [
    "python3 scripts/change_manager.py --project PROJECT init",
    "python3 scripts/baseline_manager.py --project PROJECT init --actor \"Configuration Manager\"",
]

EVIDENCE_INIT_COMMAND = (
    "python3 scripts/verification_evidence.py --project PROJECT init "
    "--actor \"Verification Engineer\""
)

FRENCH_NORMATIVE_RE = re.compile(
    r"\b(doit|doivent|devra|devront|doit être|doivent être|devra être|devront être)\b",
    re.IGNORECASE,
)


def load_json_marker(path: Path):
    if not path.is_file():
        return None, "missing"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, f"unreadable: {exc}"
    if not isinstance(data, dict):
        return None, "invalid: not an object"
    if data.get("enabled") is not True:
        return data, "disabled"
    return data, "enabled"


def detect_format(path: Path, text: str):
    lines = text.splitlines()
    v11_blocks = 0
    legacy_headings = 0
    legacy_tables = 0
    legacy_french = 0

    in_block = False
    for line in lines:
        if V11_BLOCK_START_RE.match(line):
            v11_blocks += 1
            in_block = True
            continue
        if V11_BLOCK_END_RE.match(line):
            in_block = False
            continue
        if in_block:
            continue
        if HEADING_DEF_RE.match(line):
            legacy_headings += 1
        elif TABLE_DEF_RE.match(line):
            legacy_tables += 1

    if FRENCH_NORMATIVE_RE.search(text):
        legacy_french += 1

    if v11_blocks and (legacy_headings or legacy_tables):
        detected = "MIXED"
    elif v11_blocks:
        detected = "V1.1"
    elif legacy_headings or legacy_tables:
        detected = "LEGACY"
    else:
        detected = "NONE"

    return {
        "format": detected,
        "v11_blocks": v11_blocks,
        "legacy_headings": legacy_headings,
        "legacy_tables": legacy_tables,
        "legacy_french": bool(legacy_french),
    }


def assess_requirements(project: Path):
    files = requirement_files(project)
    if not files:
        return {
            "state": "NONE",
            "files": [],
            "init_command": None,
            "attention": ["No requirement files found under 01-requirements/."],
        }

    file_reports = []
    overall_formats = set()
    attention = []

    for path in files:
        text = read_text(path)
        report = detect_format(path, text)
        report["path"] = path.relative_to(project).as_posix()
        file_reports.append(report)
        overall_formats.add(report["format"])

        if report["format"] == "LEGACY":
            attention.append(
                f"{report['path']}: contains legacy unversioned requirement "
                "headings; migrate to V1.1 revisioned blocks."
            )
        elif report["format"] == "MIXED":
            attention.append(
                f"{report['path']}: contains both V1.1 blocks and legacy "
                "headings; complete the migration to V1.1 blocks."
            )

        if report["legacy_french"]:
            attention.append(
                f"{report['path']}: French normative wording detected; "
                "English is the canonical language for V1.1."
            )

    if overall_formats == {"V1.1"}:
        state = "V1.1"
    elif overall_formats == {"LEGACY"}:
        state = "LEGACY"
    elif "NONE" in overall_formats and len(overall_formats) == 1:
        state = "NONE"
    else:
        state = "MIXED"

    if state in {"LEGACY", "MIXED", "NONE"}:
        attention.append(
            "Requirement migration is manual: convert each requirement to a "
            "V1.1 revisioned block [PROJECT_PROCESS_REQ_SEQ@RREV] ... [END_REQ]."
        )

    return {
        "state": state,
        "files": file_reports,
        "init_command": None,
        "attention": attention,
    }


def assess_configuration_management(project: Path):
    marker_path = project / CM_MARKER
    data, status = load_json_marker(marker_path)

    if status == "enabled":
        model = data.get("model")
        version = data.get("model_version")
        if model != "PROJECT_MANAGER_CONFIGURATION_MANAGEMENT" or version != "1.1":
            return {
                "state": "INVALID",
                "init_command": "\n".join(CM_INIT_COMMANDS),
                "attention": [
                    f"{CM_MARKER.as_posix()}: enabled but unexpected model "
                    f"'{model}' or version '{version}'; expected "
                    "PROJECT_MANAGER_CONFIGURATION_MANAGEMENT/1.1."
                ],
            }
        return {
            "state": "ENABLED",
            "init_command": "\n".join(CM_INIT_COMMANDS),
            "attention": [],
        }

    if status == "disabled":
        return {
            "state": "DISABLED",
            "init_command": "\n".join(CM_INIT_COMMANDS),
            "attention": [
                f"{CM_MARKER.as_posix()}: exists but enabled=false; "
                "review and re-run init if migration is intended."
            ],
        }

    attention = [f"{CM_MARKER.as_posix()}: {status}."]
    if status == "missing":
        attention.append(
            "Configuration Management V1.1 is not enabled; legacy projects are "
            "skipped by the audit chain."
        )

    return {
        "state": "MISSING",
        "init_command": "\n".join(CM_INIT_COMMANDS),
        "attention": attention,
    }


def assess_verification_evidence(project: Path):
    marker_path = project / EVIDENCE_MARKER
    data, status = load_json_marker(marker_path)

    if status == "enabled":
        model = data.get("model")
        version = data.get("model_version")
        if model != "PROJECT_MANAGER_VERIFICATION_EVIDENCE_MANAGEMENT" or version != "1.0":
            return {
                "state": "INVALID",
                "init_command": EVIDENCE_INIT_COMMAND,
                "attention": [
                    f"{EVIDENCE_MARKER.as_posix()}: enabled but unexpected model "
                    f"'{model}' or version '{version}'; expected "
                    "PROJECT_MANAGER_VERIFICATION_EVIDENCE_MANAGEMENT/1.0."
                ],
            }
        return {
            "state": "ENABLED",
            "init_command": EVIDENCE_INIT_COMMAND,
            "attention": [],
        }

    if status == "disabled":
        return {
            "state": "DISABLED",
            "init_command": EVIDENCE_INIT_COMMAND,
            "attention": [
                f"{EVIDENCE_MARKER.as_posix()}: exists but enabled=false; "
                "review and re-run init if migration is intended."
            ],
        }

    attention = [f"{EVIDENCE_MARKER.as_posix()}: {status}."]
    if status == "missing":
        attention.append(
            "Verification Evidence Management is not enabled; legacy projects "
            "are skipped by the audit chain."
        )

    return {
        "state": "MISSING",
        "init_command": EVIDENCE_INIT_COMMAND,
        "attention": attention,
    }


def assess_tasks(project: Path):
    tasks_path = project / TASKS_FILE
    if not tasks_path.is_file():
        return {
            "present": False,
            "schema_version": None,
            "attention": [f"{TASKS_FILE.as_posix()}: missing."],
        }
    try:
        data = json.loads(tasks_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {
            "present": True,
            "schema_version": None,
            "attention": [f"{TASKS_FILE.as_posix()}: unreadable: {exc}"],
        }
    if not isinstance(data, dict):
        return {"present": True, "schema_version": None,
                "attention": [f"{TASKS_FILE.as_posix()}: expected a JSON object; restore valid task state."]}
    schema_version = data.get("schema_version")
    attention = []
    if schema_version != 1:
        attention.append(
            f"{TASKS_FILE.as_posix()}: unsupported schema_version {schema_version}; "
            "expected 1."
        )
    return {
        "present": True,
        "schema_version": schema_version,
        "attention": attention,
    }


def assess_traceability(project: Path):
    trace_path = project / TRACEABILITY_FILE
    if not trace_path.is_file():
        return {
            "state": "MISSING",
            "init_command": None,
            "revisioned_refs": [],
            "legacy_refs": [],
            "attention": [
                f"{TRACEABILITY_FILE.as_posix()}: missing; create it after "
                "requirements are stable."
            ],
        }

    text = read_text(trace_path)
    revisioned_refs = set(re.findall(VERSIONED_REQ_PATTERN, text))
    legacy_refs = set(re.findall(r"\b(?:STK|SYS|SWE|HWE|MLE|MEC|CYB)-REQ-\d+\b", text))
    # Remove matches that are also versioned (overlap is not possible by pattern,
    # but keep the logic explicit).
    legacy_refs -= revisioned_refs

    if revisioned_refs and legacy_refs:
        state = "MIXED"
    elif revisioned_refs:
        state = "V1.1"
    elif legacy_refs:
        state = "LEGACY"
    else:
        state = "EMPTY"

    attention = []
    if state == "MISSING":
        attention.append(
            f"{TRACEABILITY_FILE.as_posix()}: missing; legacy projects require it."
        )
    elif state == "LEGACY":
        attention.append(
            f"{TRACEABILITY_FILE.as_posix()}: references legacy unversioned IDs; "
            "update to exact V1.1 revisioned references."
        )
    elif state == "MIXED":
        attention.append(
            f"{TRACEABILITY_FILE.as_posix()}: contains both V1.1 and legacy "
            "references; complete the update to exact revisioned references."
        )
    elif state == "EMPTY":
        attention.append(
            f"{TRACEABILITY_FILE.as_posix()}: present but contains no requirement "
            "references."
        )

    return {
        "state": state,
        "revisioned_refs": sorted(revisioned_refs),
        "legacy_refs": sorted(legacy_refs),
        "init_command": None,
        "attention": attention,
    }


def assess_project(project: Path):
    from management_audit import summary
    management = summary(project)
    requirements = assess_requirements(project)
    configuration_management = assess_configuration_management(project)
    verification_evidence = assess_verification_evidence(project)
    tasks = assess_tasks(project)
    traceability = assess_traceability(project)

    attention = []
    attention.extend(requirements["attention"])
    attention.extend(configuration_management["attention"])
    attention.extend(verification_evidence["attention"])
    attention.extend(tasks["attention"])
    attention.extend(traceability["attention"])
    attention.extend(management["findings"])

    return {
        "project": project.resolve().as_posix(),
        "management_extensions": {
            **management,
            "init_command": 'python3 scripts/management_init.py PROJECT --actor "Project coordinator"',
            "migration_policy": "Explicit opt-in only; existing engineering records and legacy documents are not converted or replaced.",
        },
        "requirements": {
            "state": requirements["state"],
            "files": requirements["files"],
            "init_command": requirements["init_command"],
        },
        "configuration_management": {
            "state": configuration_management["state"],
            "marker": CM_MARKER.as_posix(),
            "init_command": configuration_management["init_command"],
        },
        "verification_evidence": {
            "state": verification_evidence["state"],
            "marker": EVIDENCE_MARKER.as_posix(),
            "init_command": verification_evidence["init_command"],
        },
        "tasks": {
            "present": tasks["present"],
            "schema_version": tasks["schema_version"],
        },
        "traceability": {
            "state": traceability["state"],
            "init_command": traceability["init_command"],
            "revisioned_refs": traceability["revisioned_refs"],
            "legacy_refs": traceability["legacy_refs"],
        },
        "attention": attention,
    }


def render_text(report):
    lines = []
    lines.append("=== MIGRATION ASSESSMENT ===")
    lines.append("")
    lines.append(f"Project: {report['project']}")
    lines.append("")

    lines.append("Requirements:")
    lines.append(f"  State: {report['requirements']['state']}")
    for file_report in report["requirements"]["files"]:
        lines.append(f"  File: {file_report['path']}")
        lines.append(f"    Format: {file_report['format']}")
        lines.append(f"    V1.1 blocks: {file_report['v11_blocks']}")
        lines.append(f"    Legacy headings: {file_report['legacy_headings']}")
        lines.append(f"    Legacy tables: {file_report['legacy_tables']}")
        lines.append(
            f"    French legacy wording: "
            f"{'yes' if file_report['legacy_french'] else 'no'}"
        )
    if report["requirements"]["init_command"]:
        lines.append(f"  Init command:\n    {report['requirements']['init_command']}")
    lines.append("")

    lines.append("Configuration Management:")
    lines.append(f"  State: {report['configuration_management']['state']}")
    lines.append(f"  Marker: {report['configuration_management']['marker']}")
    if report["configuration_management"]["init_command"]:
        lines.append("  Init commands:")
        for command in report["configuration_management"]["init_command"].splitlines():
            lines.append(f"    {command}")
    lines.append("")

    lines.append("Verification Evidence:")
    lines.append(f"  State: {report['verification_evidence']['state']}")
    lines.append(f"  Marker: {report['verification_evidence']['marker']}")
    if report["verification_evidence"]["init_command"]:
        lines.append(f"  Init command: {report['verification_evidence']['init_command']}")
    lines.append("")

    lines.append("Tasks:")
    lines.append(f"  Present: {'yes' if report['tasks']['present'] else 'no'}")
    lines.append(f"  Schema version: {report['tasks']['schema_version']}")
    lines.append("")

    lines.append("Management extensions (explicit opt-in):")
    for kind, value in report["management_extensions"]["registries"].items():
        lines.append(f"  {kind}: {'ENABLED' if value['enabled'] else 'NOT_ENABLED'}")
    lines.append("  " + report["management_extensions"]["migration_policy"])
    lines.append("  " + report["management_extensions"]["init_command"])
    lines.append("")

    lines.append("Traceability:")
    lines.append(f"  State: {report['traceability']['state']}")
    lines.append(
        f"  Revisioned references: {len(report['traceability']['revisioned_refs'])}"
    )
    lines.append(
        f"  Legacy references: {len(report['traceability']['legacy_refs'])}"
    )
    if report["traceability"]["init_command"]:
        lines.append(f"  Init command: {report['traceability']['init_command']}")
    lines.append("")

    if report["attention"]:
        lines.append("Items needing human attention:")
        for item in report["attention"]:
            lines.append(f"  - {item}")
    else:
        lines.append("Items needing human attention: none")

    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Non-destructive V1.0 -> V1.1 migration assessment."
    )
    parser.add_argument("project", help="Project directory to assess")
    parser.add_argument(
        "--json", action="store_true", help="Emit machine-readable JSON output"
    )
    args = parser.parse_args(argv)

    project = Path(args.project)
    if not project.is_dir():
        print(f"ERROR: not a directory: {project}", file=sys.stderr)
        return 2

    report = assess_project(project)

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(render_text(report))

    return 0


if __name__ == "__main__":
    sys.exit(main())
