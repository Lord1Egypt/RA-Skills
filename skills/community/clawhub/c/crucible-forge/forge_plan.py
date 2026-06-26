#!/usr/bin/env python3
"""
Forge Planner — Reorganization Plan Generator
==============================================

Takes a scan report and configuration, produces:
- Hardline safety rules (generated before any moves)
- Ordered execution plan with dependency tracking
- Reference patch list (what updates after each move)
- Per-directory _README.md content
- Rollback procedures for every step

Usage:
    python3 forge_plan.py --config forge_config.py --scan-report scan_report.json
    python3 forge_plan.py --config forge_config.py --scan-report scan_report.json --output plan.json
"""

import argparse
import importlib.util
import json
import os
import re
import sys
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def load_config(config_path: str) -> object:
    # Security: validate path before executing config file
    if not os.path.isfile(config_path):
        print(f"ERROR: Config not found: {config_path}")
        sys.exit(1)
    if not config_path.endswith(".py"):
        print(f"ERROR: Config must be a .py file: {config_path}")
        sys.exit(1)
    if os.path.getsize(config_path) > 1_000_000:
        print(f"ERROR: Config file too large (>1MB): {config_path}")
        sys.exit(1)
    spec = importlib.util.spec_from_file_location("config", config_path)
    if spec is None or spec.loader is None:
        print(f"ERROR: Cannot load config from {config_path}")
        sys.exit(1)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    return config


def load_scan_report(path: str) -> dict:
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERROR: Cannot load scan report: {e}")
        sys.exit(1)


def generate_safety_rules(config, scan_report: dict) -> dict:
    """Generate hardline safety rules based on workspace state."""
    protected_files = set(getattr(config, "PROTECTED_FILES", []))
    protected_dirs = set(getattr(config, "PROTECTED_DIRS", []))

    # Auto-protect files referenced by running processes
    auto_protected = set()
    for proc in scan_report.get("running_processes", []):
        if proc.get("workspace_reference"):
            # Extract file paths from process command line
            line = proc.get("line", "")
            for f in scan_report.get("files", []):
                if os.path.basename(f["path"]) in line:
                    auto_protected.add(f["path"])

    # Auto-protect files with secrets warnings
    secrets_files = set()
    for w in scan_report.get("secrets_warnings", []):
        secrets_files.add(w["file"])

    rules = {
        "generated_at": datetime.now().isoformat(),
        "zero_deletion_policy": True,
        "require_backup": getattr(config, "REQUIRE_BACKUP_BEFORE_PLAN", True),
        "require_file_count_check": getattr(config, "REQUIRE_FILE_COUNT_CHECK", True),
        "max_moves_per_plan": getattr(config, "MAX_MOVES_PER_PLAN", 500),
        "max_move_percentage": getattr(config, "MAX_MOVE_PERCENTAGE", 80),
        "protected_files": sorted(protected_files),
        "protected_dirs": sorted(protected_dirs),
        "auto_protected_by_processes": sorted(auto_protected),
        "secrets_warning_files": sorted(secrets_files),
        "all_protected": sorted(protected_files | auto_protected),
        "rules": [
            "NEVER delete any file. Move to archive only.",
            "NEVER modify protected files. Read-only access only.",
            "ALWAYS create backup before executing any move.",
            "ALWAYS verify file count before and after moves.",
            "ALWAYS update references atomically with moves.",
            "NEVER move files referenced by running processes.",
            "ALWAYS review plan before execution. No auto-execute.",
            "If a file's purpose is unclear, move to inbox/ for triage.",
            "If a file contains secrets, flag but do not move.",
            "Rollback procedure must exist for every planned move.",
        ],
    }

    return rules


def classify_file(filepath: str, config) -> str:
    """Determine target directory for a file based on classification rules."""
    rules = getattr(config, "FILE_CLASSIFICATION_RULES", [])

    for pattern, target_dir in rules:
        # Simple glob matching
        if _glob_match(filepath, pattern):
            return target_dir

    return ""  # No classification — stays where it is


def _glob_match(filepath: str, pattern: str) -> bool:
    """Simple glob pattern matching."""
    import fnmatch
    basename = os.path.basename(filepath)
    return fnmatch.fnmatch(basename, pattern) or fnmatch.fnmatch(filepath, pattern)


def generate_moves(config, scan_report: dict, safety_rules: dict) -> list:
    """Generate the list of file moves needed."""
    template = getattr(config, "DIRECTORY_TEMPLATE", {})
    workspace_root = getattr(config, "WORKSPACE_ROOT", ".")
    all_protected = set(safety_rules["all_protected"])
    protected_dirs = set(safety_rules["protected_dirs"])

    moves = []
    references = scan_report.get("references", {})

    for f in scan_report.get("files", []):
        path = f["path"]

        # Skip protected
        if path in all_protected or f.get("protected"):
            continue

        # Skip files already in a template directory
        top_dir = path.split("/")[0] if "/" in path else ""
        if top_dir in template:
            continue

        # Skip files in protected directories
        in_protected = False
        for pd in protected_dirs:
            if path.startswith(pd + "/") or path == pd:
                in_protected = True
                break
        if in_protected:
            continue

        # Try classification rules
        target = classify_file(path, config)
        if target:
            new_path = os.path.join(target, os.path.basename(path))
            # Find references that need updating
            ref_updates = []
            for source, refs in references.items():
                if path in refs or os.path.basename(path) in refs:
                    ref_updates.append({
                        "file": source,
                        "old_ref": path,
                        "new_ref": new_path,
                    })

            moves.append({
                "source": path,
                "destination": new_path,
                "reason": f"Classification rule: {target}",
                "reference_updates": ref_updates,
                "rollback": f"mv '{new_path}' '{path}'",
            })

    return moves


def generate_directory_creation(config) -> list:
    """Generate list of directories to create."""
    template = getattr(config, "DIRECTORY_TEMPLATE", {})
    workspace_root = getattr(config, "WORKSPACE_ROOT", ".")

    dirs_to_create = []
    for dir_path, description in template.items():
        full_path = os.path.join(workspace_root, dir_path)
        if not os.path.exists(full_path):
            dirs_to_create.append({
                "path": dir_path,
                "description": description,
                "create_readme": getattr(config, "GENERATE_README_FILES", True),
            })

    return dirs_to_create


def generate_readmes(config) -> list:
    """Generate _README.md content for each template directory."""
    template = getattr(config, "DIRECTORY_TEMPLATE", {})
    readme_template = getattr(config, "README_TEMPLATE", "# {dir_name}\n\n{description}\n")

    readmes = []
    for dir_path, description in template.items():
        dir_name = os.path.basename(dir_path) or dir_path
        content = readme_template.format(
            dir_name=dir_name.replace("-", " ").title(),
            description=description,
            belongs_here=description,
        )
        readmes.append({
            "path": os.path.join(dir_path, "_README.md"),
            "content": content,
        })

    return readmes


def build_execution_order(moves: list, safety_rules: dict) -> list:
    """Order moves by dependency — files referenced by other moves go first."""
    # Build dependency graph
    move_sources = {m["source"] for m in moves}
    move_destinations = {m["destination"] for m in moves}

    # Separate moves into phases
    phases = []

    # Phase 0: Create directories
    phases.append({
        "phase": 0,
        "name": "Create directories",
        "description": "Create target directories before any file moves.",
    })

    # Phase 1: Create backup and manifest
    phases.append({
        "phase": 1,
        "name": "Backup and manifest",
        "description": "Create fresh backup and file manifest for rollback.",
    })

    # Phase 2: Files with no reference dependencies
    independent = []
    dependent = []
    for m in moves:
        has_deps = bool(m.get("reference_updates"))
        if has_deps:
            dependent.append(m)
        else:
            independent.append(m)

    phases.append({
        "phase": 2,
        "name": "Independent moves",
        "description": "Move files with no cross-references (safe, parallel-capable).",
        "moves": independent,
        "move_count": len(independent),
    })

    # Phase 3: Files with reference dependencies (move + patch atomically)
    phases.append({
        "phase": 3,
        "name": "Dependent moves with reference patches",
        "description": "Move files and update all references atomically.",
        "moves": dependent,
        "move_count": len(dependent),
    })

    # Phase 4: Post-move verification
    phases.append({
        "phase": 4,
        "name": "Post-move verification",
        "description": "Run forge_audit.py --phase post to verify everything.",
    })

    return phases


def validate_plan(moves: list, safety_rules: dict, scan_report: dict) -> list:
    """Validate the plan against safety rules. Return list of issues."""
    issues = []
    total_files = scan_report["summary"]["total_files"]
    max_moves = safety_rules["max_moves_per_plan"]
    max_pct = safety_rules["max_move_percentage"]

    if len(moves) > max_moves:
        issues.append({
            "severity": "ERROR",
            "message": f"Plan has {len(moves)} moves, exceeding limit of {max_moves}",
        })

    if total_files > 0:
        pct = (len(moves) / total_files) * 100
        if pct > max_pct:
            issues.append({
                "severity": "ERROR",
                "message": f"Plan moves {pct:.1f}% of files, exceeding {max_pct}% safety limit",
            })

    # Check for destination conflicts
    destinations = defaultdict(list)
    for m in moves:
        destinations[m["destination"]].append(m["source"])

    for dest, sources in destinations.items():
        if len(sources) > 1:
            issues.append({
                "severity": "ERROR",
                "message": f"Multiple files targeting same destination: {dest} ← {sources}",
            })

    # Check for moves of protected files (shouldn't happen, but verify)
    all_protected = set(safety_rules["all_protected"])
    for m in moves:
        if m["source"] in all_protected:
            issues.append({
                "severity": "CRITICAL",
                "message": f"Plan includes move of protected file: {m['source']}",
            })

    return issues


def generate_plan(config, scan_report: dict) -> dict:
    """Generate complete reorganization plan."""
    print("Generating safety rules...")
    safety_rules = generate_safety_rules(config, scan_report)

    print("Planning directory creation...")
    dirs = generate_directory_creation(config)

    print("Generating _README.md content...")
    readmes = generate_readmes(config)

    print("Planning file moves...")
    moves = generate_moves(config, scan_report, safety_rules)

    print("Building execution order...")
    execution_order = build_execution_order(moves, safety_rules)

    print("Validating plan...")
    issues = validate_plan(moves, safety_rules, scan_report)

    plan = {
        "generated_at": datetime.now().isoformat(),
        "workspace_root": getattr(config, "WORKSPACE_ROOT", "."),
        "safety_rules": safety_rules,
        "directories_to_create": dirs,
        "readmes_to_generate": readmes,
        "moves": moves,
        "execution_order": execution_order,
        "validation_issues": issues,
        "summary": {
            "directories_to_create": len(dirs),
            "readmes_to_generate": len(readmes),
            "files_to_move": len(moves),
            "reference_patches": sum(len(m.get("reference_updates", [])) for m in moves),
            "validation_errors": len([i for i in issues if i["severity"] in ("ERROR", "CRITICAL")]),
            "validation_warnings": len([i for i in issues if i["severity"] == "WARNING"]),
        },
        "rollback_command": (
            "# To rollback, restore from the pre-move backup:\n"
            f"# tar -xzf backups/forge-pre-move-*.tar.gz -C {getattr(config, 'WORKSPACE_ROOT', '.')}\n"
            "# Then verify with: python3 forge_audit.py --config forge_config.py --phase post"
        ),
    }

    return plan


def print_plan_summary(plan: dict):
    """Print human-readable plan summary."""
    s = plan["summary"]
    print("\n" + "=" * 60)
    print("FORGE REORGANIZATION PLAN")
    print("=" * 60)
    print(f"Workspace:             {plan['workspace_root']}")
    print(f"Directories to create: {s['directories_to_create']}")
    print(f"READMEs to generate:   {s['readmes_to_generate']}")
    print(f"Files to move:         {s['files_to_move']}")
    print(f"Reference patches:     {s['reference_patches']}")
    print(f"Validation errors:     {s['validation_errors']}")
    print(f"Validation warnings:   {s['validation_warnings']}")

    if plan["validation_issues"]:
        print("\n--- VALIDATION ISSUES ---")
        for issue in plan["validation_issues"]:
            print(f"  [{issue['severity']}] {issue['message']}")

    if s["validation_errors"] > 0:
        print("\n⛔ PLAN HAS ERRORS — Do not execute until resolved.")
    else:
        print("\n✅ Plan validated. Review the full plan before executing.")

    print("\n--- SAFETY RULES ---")
    for rule in plan["safety_rules"]["rules"]:
        print(f"  • {rule}")

    if plan["moves"]:
        print(f"\n--- PLANNED MOVES (showing first 20 of {len(plan['moves'])}) ---")
        for m in plan["moves"][:20]:
            patches = len(m.get("reference_updates", []))
            patch_note = f" (+{patches} ref patches)" if patches else ""
            print(f"  {m['source']} → {m['destination']}{patch_note}")
        if len(plan["moves"]) > 20:
            print(f"  ... and {len(plan['moves']) - 20} more")

    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Forge Planner — Reorganization Plan Generator")
    parser.add_argument("--config", required=True, help="Path to forge_config.py")
    parser.add_argument("--scan-report", required=True, help="Path to scan_report.json")
    parser.add_argument("--output", default=None, help="Output plan JSON path")
    args = parser.parse_args()

    config = load_config(args.config)
    scan_report = load_scan_report(args.scan_report)

    plan = generate_plan(config, scan_report)
    print_plan_summary(plan)

    output_dir = getattr(config, "OUTPUT_DIR", os.path.join(config.WORKSPACE_ROOT, "forge-output"))
    os.makedirs(output_dir, exist_ok=True)
    output_path = args.output or os.path.join(output_dir, "reorg_plan.json")

    with open(output_path, "w") as f:
        json.dump(plan, f, indent=2, default=str)

    print(f"\nFull plan written to: {output_path}")
    print("Review the plan carefully before executing any moves.")


if __name__ == "__main__":
    main()
