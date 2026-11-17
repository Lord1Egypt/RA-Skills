#!/usr/bin/env python3
"""Build a deterministic, audited public PPT Smith registry archive."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

if __package__:
    from .output_safety import OutputTransaction, check_source, checked_path
else:
    from output_safety import OutputTransaction, check_source, checked_path


ROOT = Path(__file__).resolve().parents[1]
GENERATED_AUDIT = {"references/BUNDLE-AUDIT.json", "references/BUNDLE-AUDIT.md"}


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def ignore_rules() -> list[str]:
    rules: list[str] = []
    for line in (ROOT / ".clawhubignore").read_text(encoding="utf-8").splitlines():
        value = line.strip()
        if value and not value.startswith("#"):
            rules.append(value)
    return rules


def ignored(relative: str, rules: list[str]) -> bool:
    for rule in rules:
        if rule.endswith("/"):
            prefix = rule.rstrip("/")
            if relative == prefix or relative.startswith(prefix + "/"):
                return True
        elif fnmatch.fnmatch(relative, rule) or fnmatch.fnmatch(Path(relative).name, rule):
            return True
    return False


def staged_files() -> list[str]:
    values = git("ls-files", "--cached").splitlines()
    rules = ignore_rules()
    return [value for value in values if value not in GENERATED_AUDIT and not ignored(value, rules)]


def copy_public_tree(destination: Path) -> list[str]:
    if subprocess.run(["git", "diff", "--quiet"], cwd=ROOT).returncode != 0:
        raise RuntimeError("unstaged changes exist; stage the exact release candidate before packaging")
    files = staged_files()
    for relative in files:
        source = check_source(ROOT / relative)
        if not source.is_file():
            raise RuntimeError(f"tracked release file is missing: {relative}")
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    return files


def audit_tree(destination: Path) -> None:
    command = [
        sys.executable,
        str(destination / "scripts" / "audit_bundle.py"),
        "--root",
        str(destination),
        "--mode",
        "archive",
        "--fail-on-finding",
    ]
    environment = dict(os.environ)
    environment["PPTSMITH_AUDIT_TIMESTAMP"] = git("show", "-s", "--format=%cI", "HEAD")
    subprocess.run(command, cwd=destination, env=environment, check=True)


def write_zip(source: Path, target: Path) -> tuple[int, str]:
    files = sorted(
        path for path in source.rglob("*")
        if path.is_file() and path.relative_to(source).as_posix() not in GENERATED_AUDIT
    )
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            relative = path.relative_to(source).as_posix()
            info = zipfile.ZipInfo(relative, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    return len(files), digest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / ".release-artifacts")
    parser.add_argument("--overwrite", action="store_true", help="Replace only owned output directories")
    args = parser.parse_args()

    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not version or version in {".", ".."} or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-" for c in version):
        raise ValueError("Unsafe VERSION for bundle path")
    output_dir = checked_path(args.output_dir)
    staging = output_dir / f"meowclaw-pptsmith-{version}"
    archive_path = output_dir / f"meowclaw-pptsmith-{version}.zip"
    manifest_path = output_dir / f"meowclaw-pptsmith-{version}.manifest.json"

    transaction = OutputTransaction(
        output_dir, tool="build_public_bundle", overwrite=args.overwrite,
        sources=[ROOT / name for name in staged_files()], source_roots=[ROOT],
    )
    with transaction.staging() as stage:
        staged_tree = stage / staging.name
        staged_tree.mkdir()
        staged_archive = stage / archive_path.name
        staged_manifest = stage / manifest_path.name
        copied = copy_public_tree(staged_tree)
        audit_tree(staged_tree)
        file_count, digest = write_zip(staged_tree, staged_archive)

        manifest = {
            "schema_version": "1.0",
            "version": version,
            "source_commit": git("rev-parse", "HEAD"),
            "archive": archive_path.name,
            "sha256": digest,
            "files_from_index": len(copied),
            "files_in_archive": file_count,
            "bytes": staged_archive.stat().st_size,
            "audit_status": json.loads((staged_tree / "references" / "BUNDLE-AUDIT.json").read_text(encoding="utf-8"))["status"],
        }
        staged_manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        transaction.commit(stage)
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
