#!/usr/bin/env python3

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_ROOT_NAME = "fitness-coach"
DEFAULT_OUTPUT = ROOT_DIR / "dist" / f"{DEFAULT_ROOT_NAME}.zip"

TOP_LEVEL_FILES = [
    Path("SKILL.md"),
    Path("README.md"),
    Path(".gitignore"),
]

TOP_LEVEL_DIRS = [
    Path("agents"),
    Path("references"),
    Path("scripts"),
    Path("data"),
]

SKIP_NAMES = {
    ".DS_Store",
    "__pycache__",
}

SKIP_PREFIXES = (
    ".venv",
    ".pdfgen-venv",
    "dist",
)

SKIP_SUFFIXES = (
    ".pyc",
    ".pyo",
)


def should_skip(relative_path: Path) -> bool:
    if relative_path.parts[:1] == ("data",) and relative_path != Path("data/.gitkeep"):
        return True

    for part in relative_path.parts:
        if part in SKIP_NAMES:
            return True
        if any(part.startswith(prefix) for prefix in SKIP_PREFIXES):
            return True

    if relative_path.name.endswith(SKIP_SUFFIXES):
        return True
    return False


def iter_release_files() -> list[Path]:
    files: list[Path] = []

    for relative_path in TOP_LEVEL_FILES:
        absolute_path = ROOT_DIR / relative_path
        if absolute_path.exists():
            files.append(relative_path)

    for relative_dir in TOP_LEVEL_DIRS:
        absolute_dir = ROOT_DIR / relative_dir
        if not absolute_dir.exists():
            continue
        for absolute_path in sorted(absolute_dir.rglob("*")):
            if not absolute_path.is_file():
                continue
            relative_path = absolute_path.relative_to(ROOT_DIR)
            if should_skip(relative_path):
                continue
            files.append(relative_path)

    return sorted(set(files))


def build_release_bundle(output_path: Path, root_name: str) -> Path:
    release_files = iter_release_files()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for relative_path in release_files:
            archive.write(ROOT_DIR / relative_path, arcname=Path(root_name) / relative_path)

    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a clean release zip for the fitness-coach skill.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Output zip path.")
    parser.add_argument("--root-name", default=DEFAULT_ROOT_NAME, help="Top-level folder name inside the zip archive.")
    args = parser.parse_args()

    bundle_path = build_release_bundle(args.output.resolve(), args.root_name)
    print(bundle_path)


if __name__ == "__main__":
    main()
