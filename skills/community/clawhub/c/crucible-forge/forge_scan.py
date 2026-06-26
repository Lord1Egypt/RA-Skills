#!/usr/bin/env python3
"""
Forge Scanner — Workspace Analysis Tool
========================================

Scans an AI agent workspace and produces a comprehensive report:
- File inventory (paths, sizes, types, modification times)
- Directory structure map
- Cross-reference graph (which files mention which)
- Broken references (mentioned files that don't exist)
- Running process dependencies
- Hardcoded path detection
- Secrets exposure warnings

Usage:
    python3 forge_scan.py --config forge_config.py
    python3 forge_scan.py --config forge_config.py --output scan_report.json
"""

import argparse
import importlib.util
import json
import os
import re
import shlex
import subprocess
import sys
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def load_config(config_path: str) -> object:
    """Load configuration from a Python file."""
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


def scan_files(workspace_root: str, protected_dirs: list) -> list:
    """Walk workspace and collect file metadata."""
    files = []
    workspace = Path(workspace_root).resolve()

    protected_resolved = set()
    for pd in protected_dirs:
        p = (workspace / pd).resolve()
        protected_resolved.add(p)

    for root, dirs, filenames in os.walk(workspace):
        root_path = Path(root).resolve()

        # Skip protected directories
        skip = False
        for pd in protected_resolved:
            if root_path == pd or pd in root_path.parents:
                skip = True
                break
        if skip:
            # Still record the directory exists, but mark as protected
            for fn in filenames:
                fp = root_path / fn
                try:
                    stat = fp.stat()
                    files.append({
                        "path": str(fp.relative_to(workspace)),
                        "size": stat.st_size,
                        "modified": stat.st_mtime,
                        "extension": fp.suffix.lower(),
                        "protected": True,
                    })
                except OSError:
                    pass
            continue

        for fn in filenames:
            fp = root_path / fn
            try:
                stat = fp.stat()
                files.append({
                    "path": str(fp.relative_to(workspace)),
                    "size": stat.st_size,
                    "modified": stat.st_mtime,
                    "extension": fp.suffix.lower(),
                    "protected": False,
                })
            except OSError:
                pass

    return files


def scan_directories(workspace_root: str) -> list:
    """Map directory structure."""
    dirs = []
    workspace = Path(workspace_root).resolve()

    for root, dirnames, filenames in os.walk(workspace):
        root_path = Path(root).resolve()
        rel = str(root_path.relative_to(workspace))
        if rel == ".":
            rel = ""
        dirs.append({
            "path": rel,
            "file_count": len(filenames),
            "subdir_count": len(dirnames),
            "has_readme": "_README.md" in filenames or "README.md" in filenames,
        })

    return dirs


def find_references(workspace_root: str, files: list, config) -> dict:
    """Scan files for cross-references to other files."""
    workspace = Path(workspace_root).resolve()
    extensions = set(getattr(config, "REFERENCE_SCAN_EXTENSIONS", [".md", ".txt", ".py", ".sh", ".json"]))
    patterns = getattr(config, "REFERENCE_PATTERNS", [])
    max_size = getattr(config, "MAX_SCAN_FILE_SIZE_MB", 10) * 1024 * 1024

    # Build a set of known file basenames and paths for matching
    known_files = set()
    known_basenames = defaultdict(list)
    for f in files:
        known_files.add(f["path"])
        basename = os.path.basename(f["path"])
        known_basenames[basename].append(f["path"])

    compiled_patterns = []
    for p in patterns:
        try:
            compiled_patterns.append(re.compile(p))
        except re.error as e:
            print(f"WARNING: Invalid regex pattern '{p}': {e}")

    references = defaultdict(set)  # source_file -> set of referenced files
    broken_refs = defaultdict(set)  # source_file -> set of unresolved references

    for f in files:
        if f["protected"]:
            continue
        if f["extension"] not in extensions:
            continue
        if f["size"] > max_size:
            continue

        filepath = workspace / f["path"]
        try:
            content = filepath.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        found_refs = set()

        # Pattern-based reference detection
        for pat in compiled_patterns:
            for match in pat.finditer(content):
                ref = match.group(1) if match.lastindex else match.group(0)
                ref = ref.strip("\"'`()[] ")
                if ref:
                    found_refs.add(ref)

        # Simple basename detection — look for known filenames in content
        for basename, paths in known_basenames.items():
            if len(basename) > 4 and basename in content:  # Skip very short names
                for p in paths:
                    if p != f["path"]:
                        found_refs.add(basename)

        # Resolve references
        source_dir = os.path.dirname(f["path"])
        for ref in found_refs:
            resolved = False

            # Try as-is (relative to workspace root)
            if ref in known_files:
                references[f["path"]].add(ref)
                resolved = True

            # Try relative to source file's directory
            if not resolved:
                rel_path = os.path.normpath(os.path.join(source_dir, ref))
                if rel_path in known_files:
                    references[f["path"]].add(rel_path)
                    resolved = True

            # Try basename match
            if not resolved:
                basename = os.path.basename(ref)
                if basename in known_basenames:
                    for p in known_basenames[basename]:
                        references[f["path"]].add(p)
                    resolved = True

            # If it looks like a file path but doesn't resolve, it's broken
            if not resolved and re.search(r'\.\w{1,5}$', ref):
                broken_refs[f["path"]].add(ref)

    # Convert sets to lists for JSON serialization
    return {
        "references": {k: sorted(v) for k, v in references.items()},
        "broken_references": {k: sorted(v) for k, v in broken_refs.items()},
    }


def detect_secrets(workspace_root: str, files: list, config) -> list:
    """Scan for potential secrets exposure."""
    workspace = Path(workspace_root).resolve()
    patterns = getattr(config, "SECRETS_PATTERNS", [])
    max_size = getattr(config, "MAX_SCAN_FILE_SIZE_MB", 10) * 1024 * 1024

    compiled = []
    for p in patterns:
        try:
            compiled.append((p, re.compile(p)))
        except re.error:
            pass

    warnings = []
    for f in files:
        if f["size"] > max_size:
            continue
        filepath = workspace / f["path"]
        try:
            content = filepath.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        for pattern_str, pat in compiled:
            matches = pat.findall(content)
            if matches:
                warnings.append({
                    "file": f["path"],
                    "pattern": pattern_str,
                    "match_count": len(matches),
                    "protected": f["protected"],
                })
                break  # One warning per file is enough

    return warnings


def detect_processes(config) -> list:
    """Check for running processes that might depend on workspace files."""
    if not getattr(config, "DETECT_RUNNING_PROCESSES", True):
        return []

    commands = getattr(config, "PROCESS_CHECK_COMMANDS", ["ps aux"])
    workspace_root = getattr(config, "WORKSPACE_ROOT", "")

    processes = []
    for cmd in commands:
        try:
            cmd_list = shlex.split(cmd) if isinstance(cmd, str) else list(cmd)
            result = subprocess.run(
                cmd_list, capture_output=True, text=True, timeout=10
            )
            for line in result.stdout.splitlines():
                if workspace_root and workspace_root in line:
                    processes.append({
                        "command": cmd,
                        "line": line.strip(),
                        "workspace_reference": True,
                    })
        except (subprocess.TimeoutExpired, OSError) as e:
            processes.append({
                "command": cmd,
                "error": str(e),
            })

    return processes


def generate_report(config) -> dict:
    """Generate complete workspace scan report."""
    workspace_root = getattr(config, "WORKSPACE_ROOT", ".")
    protected_dirs = getattr(config, "PROTECTED_DIRS", [])

    print(f"Scanning workspace: {workspace_root}")

    print("  Collecting files...")
    files = scan_files(workspace_root, protected_dirs)

    print("  Mapping directories...")
    directories = scan_directories(workspace_root)

    print("  Finding cross-references...")
    ref_data = find_references(workspace_root, files, config)

    print("  Checking for secrets...")
    secrets = detect_secrets(workspace_root, files, config)

    print("  Detecting running processes...")
    processes = detect_processes(config)

    # Summary statistics
    total_files = len(files)
    protected_count = sum(1 for f in files if f["protected"])
    total_size = sum(f["size"] for f in files)
    extensions = defaultdict(int)
    for f in files:
        extensions[f["extension"]] += 1

    root_files = [f for f in files if os.sep not in f["path"] and "/" not in f["path"]]

    report = {
        "generated_at": datetime.now().isoformat(),
        "workspace_root": workspace_root,
        "summary": {
            "total_files": total_files,
            "protected_files": protected_count,
            "movable_files": total_files - protected_count,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "total_directories": len(directories),
            "root_level_files": len(root_files),
            "file_types": dict(sorted(extensions.items(), key=lambda x: -x[1])),
            "broken_reference_count": sum(len(v) for v in ref_data["broken_references"].values()),
            "secrets_warnings": len(secrets),
            "active_processes": len([p for p in processes if p.get("workspace_reference")]),
        },
        "files": files,
        "directories": directories,
        "references": ref_data["references"],
        "broken_references": ref_data["broken_references"],
        "secrets_warnings": secrets,
        "running_processes": processes,
        "root_files": [f["path"] for f in root_files],
    }

    return report


def print_summary(report: dict):
    """Print human-readable summary to stdout."""
    s = report["summary"]
    print("\n" + "=" * 60)
    print("FORGE SCAN REPORT")
    print("=" * 60)
    print(f"Workspace:          {report['workspace_root']}")
    print(f"Total files:        {s['total_files']}")
    print(f"Protected files:    {s['protected_files']}")
    print(f"Movable files:      {s['movable_files']}")
    print(f"Total size:         {s['total_size_mb']} MB")
    print(f"Directories:        {s['total_directories']}")
    print(f"Root-level files:   {s['root_level_files']}")
    print(f"Broken references:  {s['broken_reference_count']}")
    print(f"Secrets warnings:   {s['secrets_warnings']}")
    print(f"Active processes:   {s['active_processes']}")

    if report["broken_references"]:
        print("\n--- BROKEN REFERENCES ---")
        for source, refs in report["broken_references"].items():
            for ref in refs:
                print(f"  {source} → {ref} (NOT FOUND)")

    if report["secrets_warnings"]:
        print("\n--- SECRETS WARNINGS ---")
        for w in report["secrets_warnings"]:
            prot = " [PROTECTED]" if w["protected"] else ""
            print(f"  {w['file']}: {w['pattern']} ({w['match_count']} matches){prot}")

    if report["running_processes"]:
        procs = [p for p in report["running_processes"] if p.get("workspace_reference")]
        if procs:
            print("\n--- ACTIVE PROCESSES USING WORKSPACE ---")
            for p in procs:
                print(f"  {p['line']}")

    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Forge Scanner — Workspace Analysis")
    parser.add_argument("--config", required=True, help="Path to forge_config.py")
    parser.add_argument("--output", default=None, help="Output JSON report path (default: forge-output/scan_report.json)")
    args = parser.parse_args()

    config = load_config(args.config)
    report = generate_report(config)
    print_summary(report)

    # Write JSON report
    output_dir = getattr(config, "OUTPUT_DIR", os.path.join(config.WORKSPACE_ROOT, "forge-output"))
    os.makedirs(output_dir, exist_ok=True)
    output_path = args.output or os.path.join(output_dir, "scan_report.json")

    with open(output_path, "w") as f:
        json.dump(report, f, indent=2, default=str)

    print(f"\nFull report written to: {output_path}")


if __name__ == "__main__":
    main()
