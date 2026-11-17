#!/usr/bin/env python3
"""Build a deterministic, source-linked release archive for this Skill.

This helper is for maintainers and CI only. It never reads runtime state,
OAuth credentials, or environment secrets. The resulting ZIP contains the
reviewable Skill files plus a manifest of every included source file and its
SHA-256 digest.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
import sys
import zipfile
from pathlib import Path


SKILL_SLUG = "ecommerce-gmail-customer-service"
SKILL_ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIRECTORIES = ("agents", "assets", "references", "scripts", "tests")
SOURCE_FILES = ("README.md", "SKILL.md", "LICENSE", "NOTICE")
EXCLUDED_PARTS = {".git", "__pycache__"}
EXCLUDED_FILES = {"skill-card.md", ".ds_store"}
SENSITIVE_SUFFIXES = (".pem", ".key", ".p12", ".pfx")
SENSITIVE_NAME_PARTS = ("credential", "secret", "token")
SEMVER_RE = re.compile(r"^(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
COMMIT_RE = re.compile(r"^[0-9a-f]{7,64}$")
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def relative_posix(path: Path) -> str:
    return path.relative_to(SKILL_ROOT).as_posix()


def is_included_path(path: Path) -> bool:
    relative = path.relative_to(SKILL_ROOT)
    if relative.name in SOURCE_FILES:
        return True
    return bool(relative.parts) and relative.parts[0] in SOURCE_DIRECTORIES


def reject_sensitive_path(relative: str) -> None:
    lower_name = Path(relative).name.lower()
    if lower_name in EXCLUDED_FILES:
        raise ValueError(f"generated or platform-managed file must not be released: {relative}")
    if lower_name.endswith(SENSITIVE_SUFFIXES) or lower_name == ".env" or lower_name.startswith(".env."):
        raise ValueError(f"sensitive file must not be released: {relative}")
    if any(part in lower_name for part in SENSITIVE_NAME_PARTS):
        raise ValueError(f"sensitive-looking file must not be released: {relative}")


def collect_source_files() -> list[Path]:
    """Return only reviewable source files allowed in the distributable Skill."""
    files: list[Path] = []
    for path in sorted(SKILL_ROOT.rglob("*")):
        relative = path.relative_to(SKILL_ROOT)
        if any(part in EXCLUDED_PARTS for part in relative.parts):
            continue
        if path.is_symlink():
            raise ValueError(f"symbolic links are not allowed in release archives: {relative.as_posix()}")
        if not path.is_file() or not is_included_path(path):
            continue
        if path.suffix == ".pyc":
            continue
        relative_text = relative.as_posix()
        reject_sensitive_path(relative_text)
        files.append(path)

    if not any(relative_posix(path).lower() == "skill.md" for path in files):
        raise ValueError("SKILL.md is required in a release archive")
    return files


def build_manifest(args: argparse.Namespace, files: list[Path]) -> dict[str, object]:
    entries = []
    for path in files:
        content = path.read_bytes()
        entries.append(
            {
                "path": relative_posix(path),
                "size": len(content),
                "sha256": sha256_bytes(content),
            }
        )
    return {
        "schema_version": 1,
        "skill": {"slug": SKILL_SLUG, "version": args.version},
        "source": {
            "repository": args.source_repo,
            "commit": args.source_commit,
            "ref": args.source_ref,
            "path": args.source_path,
        },
        "files": entries,
    }


def write_zip(archive_path: Path, files: list[Path], manifest: dict[str, object]) -> None:
    manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            relative = relative_posix(path)
            info = zipfile.ZipInfo(relative, date_time=ZIP_TIMESTAMP)
            info.create_system = 3
            info.compress_type = zipfile.ZIP_DEFLATED
            mode = stat.S_IMODE(path.stat().st_mode) or 0o644
            info.external_attr = mode << 16
            archive.writestr(info, path.read_bytes())

        manifest_info = zipfile.ZipInfo("release-manifest.json", date_time=ZIP_TIMESTAMP)
        manifest_info.create_system = 3
        manifest_info.compress_type = zipfile.ZIP_DEFLATED
        manifest_info.external_attr = 0o644 << 16
        archive.writestr(manifest_info, manifest_bytes)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True, help="Skill release semver")
    parser.add_argument("--output-dir", required=True, type=Path, help="Directory for release artifacts")
    parser.add_argument("--source-repo", required=True, help="GitHub owner/repository")
    parser.add_argument("--source-commit", required=True, help="Immutable source commit SHA")
    parser.add_argument("--source-ref", required=True, help="Published tag or ref")
    parser.add_argument("--source-path", required=True, help="Skill path within the repository")
    args = parser.parse_args(argv)

    if not SEMVER_RE.fullmatch(args.version):
        parser.error("--version must be valid semver")
    if not COMMIT_RE.fullmatch(args.source_commit):
        parser.error("--source-commit must be a hexadecimal Git SHA")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", args.source_repo):
        parser.error("--source-repo must be GitHub owner/repository")
    if not args.source_ref.strip() or not args.source_path.strip():
        parser.error("--source-ref and --source-path must not be empty")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    output_dir = args.output_dir.resolve()
    try:
        output_dir.relative_to(SKILL_ROOT)
    except ValueError:
        pass
    else:
        raise ValueError("--output-dir must be outside the Skill directory")

    output_dir.mkdir(parents=True, exist_ok=True)
    files = collect_source_files()
    manifest = build_manifest(args, files)
    archive_name = f"{SKILL_SLUG}-{args.version}.zip"
    archive_path = output_dir / archive_name
    checksum_path = output_dir / f"{archive_name}.sha256"
    write_zip(archive_path, files, manifest)
    checksum_path.write_text(f"{sha256_bytes(archive_path.read_bytes())}  {archive_name}\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "archive": str(archive_path),
                "checksum": str(checksum_path),
                "file_count": len(files),
                "sha256": sha256_bytes(archive_path.read_bytes()),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        print(f"release artifact error: {error}", file=sys.stderr)
        raise SystemExit(2)
