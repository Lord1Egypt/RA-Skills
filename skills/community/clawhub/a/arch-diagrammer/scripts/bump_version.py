#!/usr/bin/env python3
import argparse
import datetime
import pathlib
import re
import sys


VERSION_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


def parse_version(text: str) -> tuple[int, int, int]:
    match = VERSION_RE.match(text.strip())
    if not match:
        raise ValueError(f"invalid version: {text!r}")
    return tuple(int(part) for part in match.groups())


def format_version(version: tuple[int, int, int]) -> str:
    return ".".join(str(part) for part in version)


def bump(version: tuple[int, int, int], level: str) -> tuple[int, int, int]:
    major, minor, patch = version
    if level == "major":
        return major + 1, 0, 0
    if level == "minor":
        return major, minor + 1, 0
    if level == "patch":
        return major, minor, patch + 1
    raise ValueError(f"unsupported bump level: {level}")


def replace_or_fail(path: pathlib.Path, pattern: str, replacement: str) -> None:
    content = path.read_text(encoding="utf-8")
    updated, count = re.subn(pattern, replacement, content, flags=re.MULTILINE)
    if count == 0:
        raise RuntimeError(f"pattern not found in {path}")
    path.write_text(updated, encoding="utf-8")


def replace_if_present(path: pathlib.Path, pattern: str, replacement: str) -> bool:
    content = path.read_text(encoding="utf-8")
    updated, count = re.subn(pattern, replacement, content, flags=re.MULTILINE)
    if count == 0:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def ensure_changelog_entry(path: pathlib.Path, version: str) -> bool:
    content = path.read_text(encoding="utf-8")
    heading = f"## [{version}] - "
    if heading in content:
        return False

    date_text = datetime.date.today().isoformat()
    entry = f"## [{version}] - {date_text}\n\n- 待补充\n\n"

    marker = "本文件记录 `arch-diagrammer` skill 的版本变更，遵循语义化版本。\n\n"
    if marker in content:
        updated = content.replace(marker, marker + entry, 1)
    else:
        updated = entry + content
    path.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Bump arch-diagrammer skill version")
    parser.add_argument("level", nargs="?", choices=["major", "minor", "patch"])
    parser.add_argument("--set", dest="set_version", help="set explicit semantic version, e.g. 1.2.3")
    parser.add_argument("--dry-run", action="store_true", help="print target version without writing files")
    args = parser.parse_args()

    if not args.level and not args.set_version:
        parser.error("provide bump level or --set")
    if args.level and args.set_version:
        parser.error("use either bump level or --set")

    root = pathlib.Path(__file__).resolve().parent.parent
    version_file = root / "VERSION"
    skill_file = root / "SKILL.md"
    readme_file = root / "README.md"
    changelog_file = root / "CHANGELOG.md"

    current = parse_version(version_file.read_text(encoding="utf-8").strip())
    target = parse_version(args.set_version) if args.set_version else bump(current, args.level)

    old_version = format_version(current)
    new_version = format_version(target)

    if args.dry_run:
        print(f"{old_version} -> {new_version}")
        return 0

    version_file.write_text(new_version + "\n", encoding="utf-8")
    replace_or_fail(skill_file, r"^version:\s+.*$", f"version: {new_version}")
    replace_if_present(skill_file, r"^- 当前版本：`.*?`（见 `VERSION`）$", f"- 当前版本：`{new_version}`（见 `VERSION`）")
    replace_or_fail(readme_file, r"^- 当前版本：`.*?`$", f"- 当前版本：`{new_version}`")
    created = ensure_changelog_entry(changelog_file, new_version)

    print(f"Bumped version: {old_version} -> {new_version}")
    if created:
        print("Created CHANGELOG.md template entry")
    else:
        print("CHANGELOG.md entry already exists")
    return 0


if __name__ == "__main__":
    sys.exit(main())
