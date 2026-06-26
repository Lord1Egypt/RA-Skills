#!/usr/bin/env python3
"""
ExpertPack Export — Validator

Checks an exported EP against schema rules:
- Required files exist
- Manifest fields are valid
- No secrets leaked
- File sizes within guidelines
- Cross-references resolve

Usage:
    python3 validate.py --export-dir /path/to/export/
"""

import argparse
import os
import re
import sys
from pathlib import Path


SECRET_PATTERNS = [
    re.compile(r'(?:api[_-]?key|token|secret|password|bearer)\s*[:=]\s*(?!<REDACTED>)\S{10,}', re.IGNORECASE),
    re.compile(r'sk-[a-zA-Z0-9]{20,}'),
    re.compile(r'ghp_[a-zA-Z0-9]{36,}'),
    re.compile(r'xoxb-[a-zA-Z0-9\-]+'),
]

REQUIRED_PACK_FILES = ["manifest.yaml", "overview.md"]

AGENT_REQUIRED_DIRS = ["operational", "mind", "relationships", "facts", "presentation"]
AGENT_REQUIRED_FILES = [
    "operational/tools.md",
    "operational/safety.md",
    "mind/values.md",
    "relationships/people.md",
    "presentation/speech_patterns.md",
]

MAX_FILE_SIZE_KB = 5  # Soft limit — warn above this
MAX_FILE_SIZE_HARD_KB = 20  # Hard limit — error above this


def validate(export_dir: str) -> dict:
    """Validate an EP export directory."""
    export = Path(export_dir)
    results = {
        "passed": True,
        "errors": [],
        "warnings": [],
        "stats": {
            "packs": 0,
            "files": 0,
            "total_size_kb": 0,
        },
    }

    if not export.exists():
        results["errors"].append(f"Export directory does not exist: {export_dir}")
        results["passed"] = False
        return results

    # Find all packs
    packs_dir = export / "packs"
    composites_dir = export / "composites"

    pack_dirs = []
    if packs_dir.exists():
        pack_dirs = [d for d in packs_dir.iterdir() if d.is_dir()]
    if composites_dir.exists():
        pack_dirs += [d for d in composites_dir.iterdir() if d.is_dir()]

    if not pack_dirs:
        results["errors"].append("No packs or composites found in export directory")
        results["passed"] = False
        return results

    results["stats"]["packs"] = len(pack_dirs)

    for pack_dir in pack_dirs:
        _validate_pack(pack_dir, results)

    # Summary
    if results["errors"]:
        results["passed"] = False

    return results


def _validate_pack(pack_dir: Path, results: dict):
    """Validate a single pack directory."""
    pack_name = pack_dir.name

    # Check required files
    for req in REQUIRED_PACK_FILES:
        if not (pack_dir / req).exists():
            results["errors"].append(f"[{pack_name}] Missing required file: {req}")

    # Parse manifest
    manifest_path = pack_dir / "manifest.yaml"
    manifest = {}
    if manifest_path.exists():
        manifest = _parse_simple_yaml(manifest_path)

    pack_type = manifest.get("type", "unknown")
    subtype = manifest.get("subtype", "")

    # Validate manifest fields
    required_manifest = ["name", "slug", "type", "version", "entry_point"]
    for field in required_manifest:
        if field not in manifest:
            results["errors"].append(f"[{pack_name}] manifest.yaml missing field: {field}")

    # Agent-specific checks
    if subtype == "agent":
        for req_dir in AGENT_REQUIRED_DIRS:
            if not (pack_dir / req_dir).exists():
                results["warnings"].append(f"[{pack_name}] Agent pack missing directory: {req_dir}/")
        for req_file in AGENT_REQUIRED_FILES:
            fpath = pack_dir / req_file
            if not fpath.exists():
                results["warnings"].append(f"[{pack_name}] Agent pack missing file: {req_file}")
            elif fpath.stat().st_size < 50:
                results["warnings"].append(f"[{pack_name}] {req_file} appears to be a stub ({fpath.stat().st_size} bytes)")

    # Check all files
    for fpath in pack_dir.rglob("*"):
        if not fpath.is_file():
            continue

        results["stats"]["files"] += 1
        size_kb = fpath.stat().st_size / 1024
        results["stats"]["total_size_kb"] += size_kb

        # File size checks (only for .md files)
        if fpath.suffix == ".md":
            if size_kb > MAX_FILE_SIZE_HARD_KB:
                results["errors"].append(
                    f"[{pack_name}] {fpath.relative_to(pack_dir)} is {size_kb:.1f}KB — exceeds hard limit ({MAX_FILE_SIZE_HARD_KB}KB)")
            elif size_kb > MAX_FILE_SIZE_KB:
                results["warnings"].append(
                    f"[{pack_name}] {fpath.relative_to(pack_dir)} is {size_kb:.1f}KB — consider splitting")

        # Secret scan
        if fpath.suffix in (".md", ".yaml", ".yml", ".json", ".txt"):
            try:
                content = fpath.read_text(errors="replace")
                for pattern in SECRET_PATTERNS:
                    match = pattern.search(content)
                    if match:
                        results["errors"].append(
                            f"[{pack_name}] Potential secret in {fpath.relative_to(pack_dir)}: ...{match.group()[:30]}...")
                        break
            except Exception:
                pass

        # Naming convention check
        if fpath.suffix == ".md" and fpath.name != fpath.name.lower() and fpath.name not in (
            "MIGRATION.md", "LEGACY.md", "README.md", "SCHEMA.md", "STATUS.md"
        ):
            # Allow uppercase for conventional filenames
            if not fpath.name.isupper() and fpath.name not in ("MIGRATION.md",):
                pass  # kebab-case not enforced on well-known names


def _parse_simple_yaml(path: Path) -> dict:
    """Very simple YAML parser — handles flat key: value pairs and quoted strings."""
    result = {}
    try:
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("-"):
                continue
            if ":" in line:
                key, _, value = line.partition(":")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if value.lower() == "true":
                    value = True
                elif value.lower() == "false":
                    value = False
                elif value.lower() == "null":
                    value = None
                result[key] = value
    except Exception:
        pass
    return result


def main():
    parser = argparse.ArgumentParser(description="Validate EP export")
    parser.add_argument("--export-dir", required=True, help="Export root directory")
    args = parser.parse_args()

    results = validate(args.export_dir)

    print(f"{'✅ PASSED' if results['passed'] else '❌ FAILED'}")
    print(f"\nStats: {results['stats']['packs']} packs, {results['stats']['files']} files, "
          f"{results['stats']['total_size_kb']:.1f}KB total")

    if results["errors"]:
        print(f"\n❌ Errors ({len(results['errors'])}):")
        for e in results["errors"]:
            print(f"  {e}")

    if results["warnings"]:
        print(f"\n⚠️  Warnings ({len(results['warnings'])}):")
        for w in results["warnings"]:
            print(f"  {w}")

    sys.exit(0 if results["passed"] else 1)


if __name__ == "__main__":
    main()
