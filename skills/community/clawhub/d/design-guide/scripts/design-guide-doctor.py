#!/usr/bin/env python3
"""Diagnose design-guide versions, required files, and local AIDE synchronization."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import platform
import shutil
import sys
from dataclasses import asdict, dataclass

try:
    from i18n import add_locale_argument, t
except ModuleNotFoundError:  # Imported by the repository test suite.
    from scripts.i18n import add_locale_argument, t


EXCLUDED_PARTS = {".git", ".github", ".codex", "promo", "__pycache__"}
EXCLUDED_NAMES = {".DS_Store"}
EXCLUDED_SUFFIXES = {".pyc", ".tmp"}
AIDE_PATHS = {
    "codex": pathlib.Path(".codex/skills/design-guide"),
    "claude": pathlib.Path(".claude/skills/design-guide"),
    "cursor": pathlib.Path(".cursor/skills/design-guide"),
    "qwen": pathlib.Path(".qwen/skills/design-guide"),
}


@dataclass
class TargetResult:
    aide: str
    path: str
    installed: bool
    version: str | None
    synchronized: bool
    missing_required: list[str]
    digest: str | None


def load_manifest(root: pathlib.Path) -> dict:
    path = root / "design-guide.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"unable to read {path}: {exc}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("version"), str):
        raise ValueError(f"invalid manifest: {path}")
    return data


def load_version_file(root: pathlib.Path) -> str:
    path = root / "VERSION"
    try:
        version = path.read_text(encoding="utf-8").strip()
    except OSError as exc:
        raise ValueError(f"unable to read {path}: {exc}") from exc
    if not version:
        raise ValueError(f"empty version file: {path}")
    return version


def included_files(root: pathlib.Path) -> list[pathlib.Path]:
    result: list[pathlib.Path] = []
    if not root.exists():
        return result
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in EXCLUDED_PARTS for part in relative.parts):
            continue
        if relative.as_posix() == ".design-guide/profile.md":
            continue
        if path.name in EXCLUDED_NAMES or path.suffix in EXCLUDED_SUFFIXES:
            continue
        result.append(relative)
    return sorted(result)


def tree_digest(root: pathlib.Path) -> str | None:
    files = included_files(root)
    if not files:
        return None
    digest = hashlib.sha256()
    for relative in files:
        digest.update(relative.as_posix().encode())
        digest.update(b"\0")
        digest.update((root / relative).read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def inspect_target(aide: str, target: pathlib.Path, source_digest: str, required: list[str]) -> TargetResult:
    installed = (target / "SKILL.md").is_file()
    version: str | None = None
    digest = tree_digest(target) if installed else None
    if installed:
        try:
            version = load_manifest(target)["version"]
        except ValueError:
            version = None
    missing = [item for item in required if not (target / item).is_file()] if installed else list(required)
    return TargetResult(
        aide=aide,
        path=str(target),
        installed=installed,
        version=version,
        synchronized=bool(installed and digest == source_digest and not missing),
        missing_required=missing,
        digest=digest,
    )


def report(source: pathlib.Path, target_home: pathlib.Path) -> dict:
    manifest = load_manifest(source)
    version_file = load_version_file(source)
    version_consistent = version_file == manifest["version"]
    source_digest = tree_digest(source)
    if source_digest is None:
        raise ValueError(f"source has no public files: {source}")
    required = manifest.get("requiredFiles", [])
    if not isinstance(required, list) or not all(isinstance(item, str) for item in required):
        raise ValueError("manifest requiredFiles must be a string array")
    missing_source = [item for item in required if not (source / item).is_file()]
    targets = [
        inspect_target(aide, target_home / relative, source_digest, required)
        for aide, relative in AIDE_PATHS.items()
    ]
    return {
        "name": manifest["name"],
        "version": manifest["version"],
        "versionFile": version_file,
        "versionConsistent": version_consistent,
        "source": str(source),
        "sourceDigest": source_digest,
        "missingSourceRequired": missing_source,
        "python": platform.python_version(),
        "commands": {aide: shutil.which(aide) for aide in AIDE_PATHS},
        "targets": [asdict(item) for item in targets],
        "healthy": version_consistent and not missing_source and all(item.installed and item.synchronized for item in targets),
    }


def print_human(data: dict, locale: str) -> None:
    print(f"design-guide {data['version']}")
    print(f"{t('Source', locale)}: {data['source']}")
    consistency = t("consistent", locale) if data["versionConsistent"] else t("MISMATCH", locale)
    print(f"{t('Version file', locale)}: {data['versionFile']} ({consistency})")
    print(f"{t('Public digest', locale)}: {data['sourceDigest'][:12]}")
    if data["missingSourceRequired"]:
        print(t("Source manifest: FAIL", locale))
        for item in data["missingSourceRequired"]:
            print(f"  missing: {item}")
    else:
        print(t("Source manifest: OK", locale))
    for target in data["targets"]:
        if not target["installed"]:
            status = "MISSING"
        elif target["synchronized"]:
            status = "OK"
        else:
            status = "STALE"
        command = "available" if data["commands"].get(target["aide"]) else "CLI not found"
        version = target["version"] or "unknown"
        print(f"{target['aide']}: {status} ({t('version {version}; {command}', locale, version=version, command=command)}) -> {target['path']}")
        for item in target["missing_required"]:
            print(f"  missing: {item}")
    print(t("Overall: OK", locale) if data["healthy"] else t("Overall: ACTION REQUIRED", locale))


def main() -> int:
    parser = argparse.ArgumentParser(description=t("Check design-guide version and local AIDE synchronization."))
    add_locale_argument(parser)
    parser.add_argument("--source", default=str(pathlib.Path(__file__).resolve().parents[1]))
    parser.add_argument("--target-home", default=os.environ.get("F_DESIGN_TARGET_HOME", str(pathlib.Path.home())))
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true", help=t("Exit non-zero when any AIDE target is missing or stale"))
    args = parser.parse_args()
    try:
        data = report(pathlib.Path(args.source).resolve(), pathlib.Path(args.target_home).resolve())
    except ValueError as exc:
        print(t("Doctor error: {error}", args.locale, error=exc), file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print_human(data, args.locale)
    return 1 if args.strict and not data["healthy"] else 0


if __name__ == "__main__":
    sys.exit(main())
