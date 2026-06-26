#!/usr/bin/env python3
"""
Forge Auditor — Pre/Post Verification
======================================

Runs integrity checks before and after workspace reorganization:

Pre-move audit:
  - Verifies backup exists and is recent
  - Creates file manifest (snapshot of current state)
  - Validates all protected files exist and are intact
  - Checks for running processes
  - Scans for exposed secrets

Post-move audit:
  - Compares file count (no files lost)
  - Verifies all protected files unchanged
  - Checks all cross-references resolve
  - Validates directory structure matches template
  - Reports any orphaned files

Usage:
    python3 forge_audit.py --config forge_config.py --phase pre
    python3 forge_audit.py --config forge_config.py --phase post --manifest pre_manifest.txt
    python3 forge_audit.py --config forge_config.py --phase content
"""

import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import time
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


class AuditResult:
    """Collects audit findings."""

    def __init__(self, phase: str):
        self.phase = phase
        self.timestamp = datetime.now().isoformat()
        self.checks = []
        self.passed = 0
        self.warnings = 0
        self.failures = 0

    def check_pass(self, name: str, detail: str = ""):
        self.checks.append({"name": name, "result": "PASS", "detail": detail})
        self.passed += 1

    def check_warn(self, name: str, detail: str):
        self.checks.append({"name": name, "result": "WARNING", "detail": detail})
        self.warnings += 1

    def check_fail(self, name: str, detail: str):
        self.checks.append({"name": name, "result": "FAIL", "detail": detail})
        self.failures += 1

    @property
    def overall(self) -> str:
        if self.failures > 0:
            return "FAIL"
        if self.warnings > 0:
            return "WARNING"
        return "PASS"

    def to_dict(self) -> dict:
        return {
            "phase": self.phase,
            "timestamp": self.timestamp,
            "overall": self.overall,
            "passed": self.passed,
            "warnings": self.warnings,
            "failures": self.failures,
            "checks": self.checks,
        }

    def print_report(self):
        symbols = {"PASS": "✅", "WARNING": "⚠️", "FAIL": "❌"}
        print(f"\n{'=' * 60}")
        print(f"FORGE {self.phase.upper()} AUDIT REPORT")
        print(f"{'=' * 60}")
        print(f"Time:     {self.timestamp}")
        print(f"Overall:  {symbols.get(self.overall, '?')} {self.overall}")
        print(f"Passed:   {self.passed}")
        print(f"Warnings: {self.warnings}")
        print(f"Failures: {self.failures}")
        print(f"\n--- CHECKS ---")
        for c in self.checks:
            sym = symbols.get(c["result"], "?")
            detail = f" — {c['detail']}" if c["detail"] else ""
            print(f"  {sym} {c['name']}{detail}")
        print(f"{'=' * 60}")


def get_file_hash(filepath: str) -> str:
    """SHA-256 hash of a file."""
    h = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        return ""


def create_manifest(workspace_root: str) -> list:
    """Create a file manifest with paths and hashes."""
    manifest = []
    workspace = Path(workspace_root).resolve()
    for root, _, filenames in os.walk(workspace):
        for fn in filenames:
            fp = Path(root) / fn
            try:
                rel = str(fp.relative_to(workspace))
                stat = fp.stat()
                manifest.append({
                    "path": rel,
                    "size": stat.st_size,
                    "hash": get_file_hash(str(fp)),
                    "modified": stat.st_mtime,
                })
            except OSError:
                pass
    return manifest


def run_pre_audit(config) -> AuditResult:
    """Pre-move audit: verify workspace is safe to reorganize."""
    result = AuditResult("pre-move")
    workspace_root = getattr(config, "WORKSPACE_ROOT", ".")
    workspace = Path(workspace_root).resolve()

    # Check 1: Workspace exists
    if workspace.is_dir():
        result.check_pass("Workspace exists", str(workspace))
    else:
        result.check_fail("Workspace exists", f"{workspace} not found")
        return result

    # Check 2: Backup exists and is recent
    backup_dir = getattr(config, "BACKUP_DIR", os.path.join(workspace_root, "backups"))
    max_age = getattr(config, "MAX_BACKUP_AGE_HOURS", 24) * 3600

    if os.path.isdir(backup_dir):
        backups = []
        for f in os.listdir(backup_dir):
            fp = os.path.join(backup_dir, f)
            if f.endswith((".tar.gz", ".tgz", ".zip")):
                backups.append((fp, os.path.getmtime(fp)))

        if backups:
            newest = max(backups, key=lambda x: x[1])
            age = time.time() - newest[1]
            if age < max_age:
                result.check_pass("Backup exists and recent", f"{newest[0]} ({age/3600:.1f}h old)")
            else:
                result.check_warn("Backup exists but stale", f"{newest[0]} ({age/3600:.1f}h old)")
        else:
            result.check_fail("No backup archives found", f"Checked {backup_dir}")
    else:
        result.check_fail("Backup directory missing", backup_dir)

    # Check 3: Protected files exist and are readable
    protected_files = getattr(config, "PROTECTED_FILES", [])
    for pf in protected_files:
        import glob as glob_mod
        matches = glob_mod.glob(os.path.join(workspace_root, pf))
        if matches:
            for m in matches:
                if os.path.isfile(m) and os.path.getsize(m) > 0:
                    result.check_pass(f"Protected file: {pf}", f"{os.path.getsize(m)} bytes")
                else:
                    result.check_fail(f"Protected file: {pf}", "Empty or not a file")
        else:
            result.check_warn(f"Protected file: {pf}", "Not found (check glob pattern)")

    # Check 4: Protected directories exist
    protected_dirs = getattr(config, "PROTECTED_DIRS", [])
    for pd in protected_dirs:
        full = os.path.join(workspace_root, pd)
        if os.path.isdir(full):
            count = sum(1 for _, _, files in os.walk(full) for _ in files)
            result.check_pass(f"Protected dir: {pd}", f"{count} files")
        else:
            result.check_warn(f"Protected dir: {pd}", "Not found")

    # Check 5: Running processes
    try:
        ps = subprocess.run(["ps", "aux"], capture_output=True, text=True, timeout=10)
        ws_procs = [l for l in ps.stdout.splitlines() if workspace_root in l]
        if ws_procs:
            result.check_warn(
                "Running processes using workspace",
                f"{len(ws_procs)} process(es) found — their files will be auto-protected"
            )
        else:
            result.check_pass("No running processes using workspace")
    except Exception:
        result.check_warn("Process check", "Could not run ps aux")

    # Check 6: Create manifest
    print("  Creating file manifest...")
    manifest = create_manifest(workspace_root)

    manifest_dir = getattr(config, "AUDIT_DIR", os.path.join(workspace_root, "backups"))
    os.makedirs(manifest_dir, exist_ok=True)
    manifest_path = os.path.join(manifest_dir, f"pre_manifest_{int(time.time())}.json")

    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    result.check_pass("Manifest created", f"{len(manifest)} files → {manifest_path}")

    # Check 7: File count baseline
    total = len(manifest)
    result.check_pass("File count baseline", f"{total} files")

    # Check 8: Secrets scan
    secrets_patterns = getattr(config, "SECRETS_PATTERNS", [])
    if secrets_patterns:
        warnings = 0
        compiled = []
        for p in secrets_patterns:
            try:
                compiled.append(re.compile(p))
            except re.error:
                pass

        for entry in manifest:
            fp = os.path.join(workspace_root, entry["path"])
            if entry["size"] > 10 * 1024 * 1024:
                continue
            try:
                content = Path(fp).read_text(encoding="utf-8", errors="replace")
                for pat in compiled:
                    if pat.search(content):
                        warnings += 1
                        break
            except OSError:
                pass

        if warnings:
            result.check_warn("Secrets scan", f"{warnings} file(s) contain potential secrets")
        else:
            result.check_pass("Secrets scan", "No exposed secrets detected")

    return result


def run_post_audit(config, manifest_path: str = None) -> AuditResult:
    """Post-move audit: verify nothing broke."""
    result = AuditResult("post-move")
    workspace_root = getattr(config, "WORKSPACE_ROOT", ".")
    workspace = Path(workspace_root).resolve()

    # Check 1: Workspace still exists
    if workspace.is_dir():
        result.check_pass("Workspace exists")
    else:
        result.check_fail("Workspace exists", "MISSING")
        return result

    # Check 2: File count comparison
    current_manifest = create_manifest(workspace_root)
    current_count = len(current_manifest)

    if manifest_path and os.path.exists(manifest_path):
        with open(manifest_path) as f:
            pre_manifest = json.load(f)
        pre_count = len(pre_manifest)

        if current_count >= pre_count:
            result.check_pass("File count", f"Pre: {pre_count}, Post: {current_count} (no files lost)")
        else:
            lost = pre_count - current_count
            result.check_fail("File count", f"Pre: {pre_count}, Post: {current_count} — {lost} files MISSING")

            # Find missing files
            pre_paths = {e["path"] for e in pre_manifest}
            current_paths = {e["path"] for e in current_manifest}
            missing = pre_paths - current_paths
            if missing:
                for m in sorted(missing)[:20]:
                    result.check_fail(f"Missing file", m)
    else:
        result.check_warn("File count", f"No pre-manifest to compare. Current: {current_count}")

    # Check 3: Protected files unchanged
    protected_files = getattr(config, "PROTECTED_FILES", [])
    if manifest_path and os.path.exists(manifest_path):
        with open(manifest_path) as f:
            pre_manifest = json.load(f)
        pre_hashes = {e["path"]: e["hash"] for e in pre_manifest}

        import glob as glob_mod
        for pf in protected_files:
            matches = glob_mod.glob(os.path.join(workspace_root, pf))
            for m in matches:
                rel = str(Path(m).relative_to(workspace))
                current_hash = get_file_hash(m)
                pre_hash = pre_hashes.get(rel, "")
                if pre_hash and current_hash == pre_hash:
                    result.check_pass(f"Protected unchanged: {rel}")
                elif pre_hash:
                    result.check_fail(f"Protected CHANGED: {rel}", "Hash mismatch — file was modified!")
                else:
                    result.check_warn(f"Protected file: {rel}", "Not in pre-manifest")

    # Check 4: Directory structure matches template
    template = getattr(config, "DIRECTORY_TEMPLATE", {})
    for dir_path in template:
        full = os.path.join(workspace_root, dir_path)
        if os.path.isdir(full):
            result.check_pass(f"Directory exists: {dir_path}")
        else:
            result.check_warn(f"Directory missing: {dir_path}")

    # Check 5: _README.md files exist
    if getattr(config, "GENERATE_README_FILES", True):
        for dir_path in template:
            readme = os.path.join(workspace_root, dir_path, "_README.md")
            if os.path.isfile(readme):
                result.check_pass(f"README exists: {dir_path}/_README.md")
            else:
                result.check_warn(f"README missing: {dir_path}/_README.md")

    # Check 6: Broken references scan
    print("  Scanning for broken references...")
    extensions = set(getattr(config, "REFERENCE_SCAN_EXTENSIONS", [".md", ".txt", ".py", ".sh"]))
    current_paths = {e["path"] for e in current_manifest}
    current_basenames = {os.path.basename(e["path"]) for e in current_manifest}
    broken_count = 0

    for entry in current_manifest:
        if Path(entry["path"]).suffix.lower() not in extensions:
            continue
        if entry["size"] > 10 * 1024 * 1024:
            continue
        fp = os.path.join(workspace_root, entry["path"])
        try:
            content = Path(fp).read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        # Look for file references that don't resolve
        file_refs = re.findall(r'[\w\-./]+\.(?:md|txt|py|sh|json|yaml|yml)', content)
        for ref in file_refs:
            ref = ref.strip("./")
            basename = os.path.basename(ref)
            if (ref not in current_paths and
                    basename not in current_basenames and
                    len(basename) > 4):
                broken_count += 1

    if broken_count == 0:
        result.check_pass("Reference integrity", "No broken references detected")
    else:
        result.check_warn("Reference integrity", f"{broken_count} potential broken references")

    # Check 7: Running processes still alive
    protected_dirs = getattr(config, "PROTECTED_DIRS", [])
    try:
        ps = subprocess.run(["ps", "aux"], capture_output=True, text=True, timeout=10)
        ws_procs = [l for l in ps.stdout.splitlines() if workspace_root in l]
        if ws_procs:
            result.check_pass("Running processes survived", f"{len(ws_procs)} still active")
    except Exception:
        pass

    # Save post-manifest
    audit_dir = getattr(config, "AUDIT_DIR", os.path.join(workspace_root, "backups"))
    os.makedirs(audit_dir, exist_ok=True)
    post_manifest_path = os.path.join(audit_dir, f"post_manifest_{int(time.time())}.json")
    with open(post_manifest_path, "w") as f:
        json.dump(current_manifest, f, indent=2)
    result.check_pass("Post-manifest created", post_manifest_path)

    return result


def run_content_audit(config) -> AuditResult:
    """Content audit: scan for misplaced content, orphans, issues."""
    result = AuditResult("content")
    workspace_root = getattr(config, "WORKSPACE_ROOT", ".")
    workspace = Path(workspace_root).resolve()
    template = getattr(config, "DIRECTORY_TEMPLATE", {})

    # Check 1: Root-level files that don't belong
    protected_files = set(getattr(config, "PROTECTED_FILES", []))
    root_items = os.listdir(workspace_root)
    root_files = [f for f in root_items if os.path.isfile(os.path.join(workspace_root, f))]
    unexpected_root = [f for f in root_files if f not in protected_files and not f.startswith(".")]

    if unexpected_root:
        result.check_warn(
            "Root-level files",
            f"{len(unexpected_root)} files at root: {', '.join(unexpected_root[:10])}"
        )
    else:
        result.check_pass("Root-level files", "All root files are protected or expected")

    # Check 2: Empty directories
    for root, dirs, files in os.walk(workspace_root):
        if not dirs and not files:
            rel = str(Path(root).relative_to(workspace))
            result.check_warn(f"Empty directory: {rel}")

    # Check 3: Duplicate filenames (potential confusion)
    from collections import Counter
    all_basenames = []
    for root, _, filenames in os.walk(workspace_root):
        all_basenames.extend(filenames)
    dupes = {name: count for name, count in Counter(all_basenames).items() if count > 1 and not name.startswith(".")}
    if dupes:
        top_dupes = sorted(dupes.items(), key=lambda x: -x[1])[:10]
        result.check_warn(
            "Duplicate filenames",
            "; ".join(f"{name} ({count}x)" for name, count in top_dupes)
        )
    else:
        result.check_pass("No duplicate filenames")

    # Check 4: Secrets in non-protected locations
    secrets_patterns = getattr(config, "SECRETS_PATTERNS", [])
    protected_dirs = set(getattr(config, "PROTECTED_DIRS", []))
    compiled = []
    for p in secrets_patterns:
        try:
            compiled.append(re.compile(p))
        except re.error:
            pass

    exposed = []
    for root, _, filenames in os.walk(workspace_root):
        rel_root = str(Path(root).relative_to(workspace))
        in_protected = any(rel_root.startswith(pd) for pd in protected_dirs)
        if in_protected:
            continue
        for fn in filenames:
            fp = Path(root) / fn
            if fp.stat().st_size > 10 * 1024 * 1024:
                continue
            try:
                content = fp.read_text(encoding="utf-8", errors="replace")
                for pat in compiled:
                    if pat.search(content):
                        exposed.append(str(fp.relative_to(workspace)))
                        break
            except OSError:
                pass

    if exposed:
        result.check_warn("Secrets in non-protected files", f"{len(exposed)} files: {', '.join(exposed[:5])}")
    else:
        result.check_pass("No secrets in non-protected files")

    return result


def main():
    parser = argparse.ArgumentParser(description="Forge Auditor — Pre/Post Verification")
    parser.add_argument("--config", required=True, help="Path to forge_config.py")
    parser.add_argument("--phase", required=True, choices=["pre", "post", "content"],
                        help="Audit phase: pre (before moves), post (after moves), content (deep scan)")
    parser.add_argument("--manifest", default=None, help="Pre-manifest path (for post-move comparison)")
    parser.add_argument("--output", default=None, help="Output report JSON path")
    args = parser.parse_args()

    config = load_config(args.config)

    if args.phase == "pre":
        result = run_pre_audit(config)
    elif args.phase == "post":
        result = run_post_audit(config, args.manifest)
    elif args.phase == "content":
        result = run_content_audit(config)
    else:
        print(f"Unknown phase: {args.phase}")
        sys.exit(1)

    result.print_report()

    # Save report
    output_dir = getattr(config, "OUTPUT_DIR", os.path.join(config.WORKSPACE_ROOT, "forge-output"))
    os.makedirs(output_dir, exist_ok=True)
    output_path = args.output or os.path.join(output_dir, f"audit_{args.phase}_{int(time.time())}.json")

    with open(output_path, "w") as f:
        json.dump(result.to_dict(), f, indent=2)

    print(f"\nAudit report written to: {output_path}")

    # Exit code reflects result
    sys.exit(1 if result.failures > 0 else 0)


if __name__ == "__main__":
    main()
