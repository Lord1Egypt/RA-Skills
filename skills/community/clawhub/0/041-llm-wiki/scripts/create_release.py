"""Create a portable llm-wiki release zip package."""

from __future__ import annotations

import argparse
import datetime as _dt
import os
import re
import shutil
import stat
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RELEASE_DIR = ROOT / "release"


def read_version() -> str:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    match = re.search(r'^version:\s*"?([^"\n]+)"?\s*$', text, re.MULTILINE)
    return match.group(1).strip() if match else "1.0.0"


def remove_tree(path: Path) -> None:
    def on_error(function, value, _exc_info):
        os.chmod(value, stat.S_IWRITE)
        function(value)

    shutil.rmtree(path, onerror=on_error)


def copy_tree(name: str, package_dir: Path) -> None:
    src = ROOT / name
    if src.exists():
        ignore = shutil.ignore_patterns("__pycache__", "*.pyc", "superpowers")
        shutil.copytree(src, package_dir / name, dirs_exist_ok=True, ignore=ignore)


def copy_file(name: str, package_dir: Path) -> None:
    src = ROOT / name
    if src.exists():
        shutil.copy2(src, package_dir / name)


def clean_python_cache(package_dir: Path) -> None:
    for cache_dir in package_dir.rglob("__pycache__"):
        shutil.rmtree(cache_dir, ignore_errors=True)
    for pyc in package_dir.rglob("*.pyc"):
        pyc.unlink(missing_ok=True)


def write_wiki_index(package_dir: Path) -> None:
    wiki = package_dir / "wiki"
    wiki.mkdir(parents=True, exist_ok=True)
    today = _dt.date.today().isoformat()
    (wiki / "index.md").write_text(
        "\n".join(
            [
                "# Wiki Index",
                "",
                "> Knowledge base entry point. Start here to explore or add new content.",
                "",
                "## Recent Activity",
                "",
                "See [log.md](../log.md) for full history.",
                "",
                "## Quick Start",
                "",
                "1. Add source materials to `sources/`.",
                '2. Ask your agent: "Ingest sources/[filename] into wiki".',
                "3. Explore and query the generated knowledge.",
                "",
                "## Status",
                "",
                "- Empty: waiting for first ingest.",
                "",
                "---",
                "",
                f"*Last updated: {today}*",
                "",
            ]
        ),
        encoding="utf-8",
    )


def create_zip(package_dir: Path, zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(package_dir.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(RELEASE_DIR))


def build_release(version: str) -> tuple[Path, Path]:
    package_name = f"llm-wiki-v{version}"
    package_dir = RELEASE_DIR / package_name
    zip_path = RELEASE_DIR / f"{package_name}.zip"

    if package_dir.exists():
        remove_tree(package_dir)
    zip_path.unlink(missing_ok=True)

    package_dir.mkdir(parents=True)

    for name in ["assets", "docs", "examples", "hooks", "scripts", "src"]:
        copy_tree(name, package_dir)

    sources_dir = package_dir / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)
    sources_readme = ROOT / "sources" / "README.md"
    if sources_readme.exists():
        shutil.copy2(sources_readme, sources_dir / "README.md")

    for name in ["SKILL.md", "CLAUDE.md", "AGENTS.md", "README.md", "ROADMAP.md", ".gitignore"]:
        copy_file(name, package_dir)

    if (ROOT / "log.md").exists():
        copy_file("log.md", package_dir)
    else:
        (package_dir / "log.md").write_text("# Log\n\nNo activity yet.\n", encoding="utf-8")

    write_wiki_index(package_dir)
    clean_python_cache(package_dir)
    create_zip(package_dir, zip_path)
    return package_dir, zip_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Create an llm-wiki release zip package.")
    parser.add_argument("--print-version", action="store_true", help="Print the version from SKILL.md and exit.")
    parser.add_argument("version", nargs="?", default=read_version())
    args = parser.parse_args()

    if args.print_version:
        print(read_version())
        return

    package_dir, zip_path = build_release(args.version)
    print(f"Release {args.version} created successfully.")
    print(f"Location: {package_dir.relative_to(ROOT)}")
    print(f"Archive: {zip_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
