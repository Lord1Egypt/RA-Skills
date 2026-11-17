#!/usr/bin/env python3
"""
photos-cleaner: one entry point for every command (ROADMAP T1.6).

    python3 photos_cleaner.py <command> [options]      # from the repo / skill bundle
    python3 -m photos_cleaner <command> [options]      # same, as a module
    photos-cleaner <command> [options]                 # after `pipx install .`

Commands are the scripts in scripts/ (underscores or hyphens both work:
`junk-finder` = `junk_finder`). Each command's own flags, output and exit codes
are unchanged, and `python3 scripts/<command>.py` keeps working.
"""

# Annotations below use 3.10 syntax; deferring them keeps this file runnable on older Pythons
# long enough for _bootstrap to print the upgrade instructions.
from __future__ import annotations

import difflib
import importlib
import importlib.util
import sys
from pathlib import Path

PROG = "photos-cleaner"
MUTATING = {"cleanup_executor", "smart_export"}
# One line per command, identical to SKILL.md's command table (a test keeps them in sync).
SUMMARIES = {
    "library_analysis": "Big picture: counts, storage, date range, top people, quality distribution",
    "junk_finder": "Screenshots (old and all), screen recordings, low-quality photos, burst leftovers, duplicates, with savings estimates",
    "duplicate_finder": "Duplicate groups (Apple's detection + timestamp/dimension match) with a keep recommendation",
    "storage_analyzer": "Storage by year, type and format; growth trends; largest items",
    "timeline_recap": "Narrative recap of a date range, clustered into events with people, places and scenes",
    "best_photos": "Highest-quality photos; `--hidden-gems` for great unfavorited ones",
    "people_analyzer": "Who appears, how often, together, over time; best photos per person",
    "location_mapper": "Location clusters, trips, offline place names",
    "scene_search": "Search by detected content (beach, dog…) or a content inventory",
    "photo_habits": "When you shoot: hour, weekday, streaks, seasons",
    "on_this_day": "This date in past years (`--window` widens it)",
    "album_auditor": "Orphan photos, empty albums, overlapping albums",
    "live_photo_analyzer": "Live Photos vs stills, storage impact, conversion candidates",
    "shared_library": "Shared Library vs personal: contributors, storage split",
    "icloud_status": "iCloud sync coverage, large local-only items",
    "similarity_finder": "Visually similar photos (Apple's computed feature scores)",
    "seasonal_highlights": "Best photos per season",
    "face_quality": "Best and worst portraits per person",
    "cleanup_executor": "**Mutating:** move a junk category to Recently Deleted",
    "smart_export": "**Mutating:** export copies organized by date, person, album or place",
    "doctor": "Diagnose setup and schema problems, with a fix per check",
}
USAGE_ERROR = 2  # ExitCode.USAGE; _common isn't importable until commands_dir() is on sys.path


def commands_dir() -> Path:
    """scripts/ next to this file (repo, skill bundle), else the installed photos_cleaner_commands package."""
    local = Path(__file__).resolve().parent / "scripts"
    # Require our own module, so an unrelated `scripts/` next to an installed copy is never used.
    if (local / "_common.py").is_file():
        return local
    spec = importlib.util.find_spec("photos_cleaner_commands")
    if spec is None or not spec.submodule_search_locations:
        raise SystemExit("photos-cleaner: can't find its commands (scripts/ or photos_cleaner_commands)")
    return Path(next(iter(spec.submodule_search_locations)))


def available_commands(directory: Path) -> dict[str, str]:
    """command module name -> one-line summary, for every script in *directory*."""
    return {path.stem: SUMMARIES.get(path.stem, "") for path in sorted(directory.glob("[a-z]*.py"))}


def usage(commands: dict[str, str]) -> str:
    width = max(len(name) for name in commands) + 2
    lines = [
        f"usage: {PROG} <command> [options]",
        f"       {PROG} <command> --help   (that command's options)",
        "",
        "Analyze and clean up an Apple Photos library. Every analysis command is read-only;",
        "mutating commands only act with the confirmation token from their own preview.",
        "",
        "commands:",
    ]
    for name, summary in commands.items():
        summary = summary.replace("**Mutating:** ", "")
        label = "(mutating) " if name in MUTATING else ""
        lines.append(f"  {name.replace('_', '-'):<{width}}{label}{summary}")
    lines += ["", f"If a command fails, run `{PROG} doctor` for the fix."]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    directory = commands_dir()
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))
    import _bootstrap  # noqa: F401  (on Python < 3.10 exits with the fix, before any command imports)

    commands = available_commands(directory)
    if not args or args[0] in ("-h", "--help", "help"):
        print(usage(commands))
        return 0 if args else USAGE_ERROR

    name = args[0].removesuffix(".py").replace("-", "_")
    if name not in commands:
        print(f"{PROG}: unknown command {args[0]!r}", file=sys.stderr)
        if close := difflib.get_close_matches(name, commands, n=3):
            print(f"Did you mean: {', '.join(c.replace('_', '-') for c in close)}?", file=sys.stderr)
        print(f"Run `{PROG} --help` for the list.", file=sys.stderr)
        return USAGE_ERROR

    # Each command parses sys.argv itself; present it as `photos-cleaner <command>` in its usage text.
    sys.argv = [f"{PROG} {name.replace('_', '-')}", *args[1:]]
    module = importlib.import_module(name)
    return int(module.main() or 0)


if __name__ == "__main__":
    sys.exit(main())
