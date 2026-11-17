# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses
[Semantic Versioning](https://semver.org/): a new JSON field is a minor release,
a removed or renamed one is a major. See [RELEASING.md](RELEASING.md) for how a
release is cut.

## [Unreleased]

## [1.4.0] - 2026-10-15

"One CLI": a single `photos-cleaner` entry point, the same flags on every
command, Markdown and CSV output, and a common envelope on every result. Also
`timeline_recap` on macOS 26 goes from 9.0 s to 0.5 s on a real 15.7k-photo
library.

### Fixed

- **`timeline_recap` on macOS 26 is fast again.** Each event reopened and
  queried Photos' search index for its scene labels, so a whole-library
  timeline took about 9 s on a real 15.7k-photo library. Labels are now
  loaded in one batch for exactly the photos the command shows
  (`IndexLabels.preload`), about 15x faster on a synthetic 2,000-event
  library. `on_this_day` reads only the photos it shows, not the whole
  library's labels.

### Added

- **Result envelope** (T1.7, first part). Every JSON, Markdown and CSV result
  now starts with `schema_version` (1), `command`, `generated_at` (UTC) and
  `warnings`, ahead of the command's own fields, which are unchanged. In
  Markdown it is the leading block. In CSV it is a first `section=envelope`
  row, present even when the result has no other rows, and any warnings follow
  as `warnings` rows. This is
  additive, so minor. `warnings` is where deprecations land, as the
  deprecation policy describes. Published JSON Schema files are the remaining
  part of T1.7.

- **Markdown and CSV output** (T2.23). Every command accepts
  `--format md|csv`, rendered generically from the JSON result so all
  commands support them.
  - `md`: a Markdown report. Summaries become bullet lists, nested objects
    become sections, and lists become tables.
  - `csv`: every list in the result, at any depth, as rows with a `section`
    column (e.g. `screenshots`, `folders.2024/03-March.items`); nested values
    become JSON cells.
  - Both honor `-o`. They contain the same data as JSON, so the privacy
    guidance applies.
  - CSV text that a spreadsheet would run as a formula (`=`, `+`, `-`, `@`,
    tab, CR) is prefixed with `'`, because album titles and filenames come from
    whoever shared the photo. A row's own `section` field is kept as
    `entry_section`, so `section` is always the row's source path.

- **Consistent flags** (T1.8). Every command now accepts `--db-path`,
  `--library`, `-o/--output`, `--format json|human`, `-q/--quiet` and
  `-v/--verbose`, with the same meaning everywhere.
  - `--human` (and `timeline_recap --narrative`) remain as shorthand for
    `--format human`.
  - `--quiet` leaves only the result on stdout and problems on stderr: no
    summary, progress or info logs.
  - `smart_export` gains `-o`.

- **One entry point: `photos-cleaner`** (T1.6). `python3 photos_cleaner.py <command>`
  or `python3 -m photos_cleaner <command>` runs any command (`junk-finder` and
  `junk_finder` both work), and `--help` lists them all, with the mutating ones
  marked. `pipx install .` provides a `photos-cleaner` command. The scripts
  install as a private `photos_cleaner_commands` package, so their module names
  stay out of `site-packages`. Running `python3 scripts/<command>.py` still
  works, and each command's flags, output and exit codes are unchanged.

### Changed

- The known schema fingerprints moved from `references/` to
  `scripts/schema-fingerprints.json`, so they ship with an installed copy and
  an installed `doctor` recognizes known libraries.

## [1.3.0] - 2026-10-15

Scene search works again on macOS 26. Its labels now come from Photos' own
search index, verified against a real macOS 26.7.2 library. Minor rather than
patch because results gain a `source` field.

### Fixed

- **Scene search works on macOS 26** (#35). Its `ZSCENECLASSIFICATION` keys
  scenes by number and stores no names, so `scene_search` and the scene
  sections of `on_this_day`/`timeline_recap` were unavailable. Labels are now
  read from Photos' own search index (`database/search/psi.sqlite`, opened
  read-only through the same write guard), including Apple's synonyms
  ("seaside" finds "Beach"). That index has no per-photo confidence, so results
  are newest-first with `confidence: null` and a `scene_confidence` entry in
  `degraded`. Older libraries keep using `ZSCENECLASSIFICATION` unchanged. The
  layout was confirmed on a real macOS 26.7.2 library.

### Added

- Scene results carry `source` (`database` or `search_index`). `doctor` no
  longer lists scene features as unavailable when the search index covers
  them.

## [1.2.0] - 2026-10-15

Fixes from checking 1.1.0 against a real macOS 26 library. Screenshot cleanup
no longer selects screen recordings, and previews show the filenames people
recognize. Minor rather than patch because both add JSON fields.

### Fixed

- **Screen recordings are no longer treated as screenshots** (#37). Photos flags
  screen recordings with the same `ZISDETECTEDSCREENSHOT` as screenshots, so
  `cleanup_executor --category old_screenshots/all_screenshots` selected screen
  recordings (videos) too, and junk, library and storage reports counted them
  as screenshots. Found on a real macOS 26 library, where an old-screenshots
  preview included a `.mov`. Screenshot categories and counts are now photos
  only. **This changes which items those cleanup categories select.**

### Added

- **Original filenames** (#38). Items in every report and preview now carry
  `original_filename` (from `ZADDITIONALASSETATTRIBUTES.ZORIGINALFILENAME`), and
  `--human` output shows it. On current macOS, `filename` (`ZASSET.ZFILENAME`)
  is Photos' internal storage name, a UUID, which made it hard to tell what a
  cleanup preview would delete. `filename` is unchanged and remains what the
  AppleScript cross-check compares against. A library without the column
  reports `original_filenames` in `degraded`, and previews fall back to
  `filename`.
- `screen_recordings` as its own `cleanup_executor` category and `junk_finder`
  section, plus `screen_recordings` counts in `library_analysis` (`by_type`) and
  `storage_analyzer` (`by_source`).

## [1.1.0] - 2026-10-15

"Solid ground": roadmap items T0.9, T0.16, T1.1, T1.2, T1.4, T1.9, T1.10, T1.19,
T1.20 and T1.23. Mutations now need a confirmation token, the database is guarded
against writes, schema differences between macOS versions degrade gracefully
instead of crashing, and a new `doctor` command diagnoses setup problems.

Known issue: scene search doesn't work on macOS 26, whose database no longer
stores scene names. `scene_search` exits 5 and the scene sections of
`on_this_day`/`timeline_recap` are reported as `degraded` (#35).

### Breaking (safety)

- **Mutations need a confirmation token** (T1.19). The old prompts could be
  bypassed by an agent: `cleanup_executor` read a typed `yes` from stdin, so a
  piped `yes` approved it, and `smart_export` skipped its prompt whenever stdin
  wasn't a terminal. Now each preview prints a `confirm_token` (also in its
  JSON, with a ready-to-run `next_command`). Executing requires
  `--confirm <token>`. The token is bound to the exact assets and options shown,
  so if anything changed, nothing runs and the exit code is 11.
  - `cleanup_executor --execute` → `--execute --confirm <token>`
  - `smart_export` without `--plan-only` no longer exports by itself; it needs
    `--confirm <token>`. `--yes` is removed (exit 2).

  - `next_command` uses the running interpreter and the script's absolute
    path, so an agent can run it verbatim from any directory.
  - `--limit` and `--batch-size` must be positive. SQLite reads `LIMIT -1` as
    "no limit", which bypassed the per-run bound.

  These ship without a deprecation period under the safety exception in
  CONTRIBUTING.md.

### Added

- **`doctor.py`** (T1.10). Checks Python, library location, Full Disk Access,
  the database schema, which commands/sections/options this library can't
  support (from every script's declared columns), library size, whether
  "Optimize Mac Storage" looks on, and, with `--check-automation`, AppleScript
  access to Photos.app. Each check prints pass/warn/fail and a concrete fix.
  `--format json` is for agents. SKILL.md tells agents to run it first when
  any command fails. On Python < 3.10 (stock macOS `python3` is 3.9) it prints
  the fix instead of crashing on import. With `--verbose`, the read-only guard
  logs anything it refuses (action, table, column).
- **Schema fingerprinting** (T1.2). The macOS release is read from Photos' own
  data-model version (Ventura through macOS 26 Tahoe), and an exact
  table/column fingerprint is matched against
  `references/schema-fingerprints.json`, seeded with a verified macOS 26
  fingerprint. An unknown schema is a warning that
  lists what will be degraded, never a crash. `doctor --schema-dump` prints
  table definitions only (no rows) so a new release's schema can be
  contributed.

- `smart_export --format json` prints the plan, or the export result, as JSON.

- `docs/threat-model.md`, linked from SECURITY.md (T0.9). It lists trust boundaries, what we
  protect, the mitigation for each threat with the code that enforces it, and the known gaps.
- A deprecation policy in CONTRIBUTING.md (T0.16). Flags and JSON fields get one minor release
  of warnings, and removal only in a major release. Safety fixes are the only exception.
- **Documented exit codes** (T1.9): 2 usage, 3 database not found, 4 permission
  denied (with a Full Disk Access hint), 5 schema unsupported, 10 cancelled,
  11 confirmation required. Previously every failure exited 1.
- **Read-only guard** (T1.20): on top of `mode=ro`, every connection installs a
  SQLite authorizer that refuses anything but reads, so a future bug cannot
  write to `Photos.sqlite` even through a misopened connection.

### Changed

- **SKILL.md is now a router** (T1.23): about 1,320 lines down to about 120. It
  keeps what each command is for, when to use it, the output contract, the
  mutation flow, permissions, privacy, limitations and exit codes. Each
  command's flags, example output and conversation examples moved verbatim to
  `references/commands/<command>.md`, and the recipes to
  `references/workflows.md`. A test caps SKILL.md at 250 lines and requires a
  linked reference file per command. The flag and default audits now read the
  reference files.

- **Graceful degradation** (T1.4). Each script declares `REQUIRED_COLUMNS` and
  `OPTIONAL_COLUMNS`. A missing required column is a clean exit 5 naming it,
  instead of a raw "no such column" crash. A missing optional column (computed
  quality scores, faces, scenes, bursts, Apple duplicate detection, iCloud /
  Live Photo / Shared Library fields, …) leaves that one section `null` or
  computed from what exists, and adds `{"section", "reason"}` to the new
  `degraded` list in every JSON result. `--human` output ends with the same
  note. `cleanup_executor` categories and `smart_export --person/--album`
  refuse with exit 5 rather than act on partial data. A test drops every
  fixture column in turn and runs every script against the result.
- **Central schema registry** (T1.1). `scripts/_schema.py` is now the only code
  that inspects `Photos.sqlite`'s schema. It reads the table list once per
  connection and maps logical names (`face.person_fk`, `asset.uuid`, …) to
  whichever physical column the library has. Supporting a column Apple renames
  is now a one-line change to `LOGICAL_COLUMNS`. Nine ad-hoc
  `PRAGMA table_info` / `sqlite_master` probes across seven files are gone, and
  a test keeps them out.

### Fixed

- `smart_export --album` hardcoded the album join table as `Z_27ASSETS` /
  `Z_3ASSETS`. Core Data renumbers it between macOS versions, so the filter
  failed on most libraries. It is now found by shape, as `album_auditor`
  already did.
- `face_quality` joined faces on the pre-Sequoia `ZPERSON` / `ZASSET` columns,
  which don't exist in the macOS 15 face schema (`ZPERSONFORFACE` /
  `ZASSETFORFACE`). It now resolves them through the schema registry.
- `--library <bundle>.photoslibrary` works. Every script handed the bundle
  directory to SQLite as if it were the database file, which failed with a
  "disk I/O error"; only `--db-path` worked.
- Library or database paths containing `?`, `#` or `%` open correctly. The
  path went into SQLite's `file:` URI unescaped, so those characters were read
  as URI syntax.
- `cleanup_executor`, `smart_export` and `timeline_recap` accept `-v/--verbose`
  like every other command. It's how you get a traceback for an unexpected error.
- A missing Full Disk Access grant is now reported as permission denied.
  macOS privacy denials are invisible to `os.access()`, so it used to surface as
  an opaque SQLite open error.

## [1.0.3] - 2026-10-13

Hygiene patch: roadmap items T0.1–T0.6, T0.8, T0.12 and T0.13.

### Changed

- **Python 3.10 is now the minimum** (T0.12). 3.9 is end-of-life. Stock macOS
  `/usr/bin/python3` (Command Line Tools) is 3.9 and no longer works; install a
  current Python with `brew install python`. CI tests 3.10, 3.14 and 3.15.
- `--year`, `--start-date` and `--end-date` are interpreted as local capture dates.

### Fixed

- **Dates use local capture time, not UTC** (T0.1). Peak hour, On This Day,
  streaks, seasons, timelines, export folders and every per-year/month/day
  bucket were shifted for anyone outside UTC. A photo taken at 23:30 on Dec 31
  in Chicago used to be counted as Jan 1. Each asset's recorded time zone
  offset is used, falling back to the Mac's current zone.
- `smart_export --end-date` now includes the end date. It stopped at midnight,
  which dropped that whole day.
- `smart_export` output-folder containment check: a symlinked subfolder
  pointing at a sibling directory sharing the same prefix (`/out-evil` next to
  `/out`) passed as "inside" the output directory (T0.8).
- `--year` rejected malformed input, except a year followed by a trailing
  newline (T0.8).

### Security

- Every GitHub Action and reusable workflow is pinned by commit SHA (Renovate, #2); a test keeps it that way (T0.6).
- Security regression suite for AppleScript escaping (including a round-trip
  through real `osascript`), path traversal, and SQL injection (T0.8).

### Removed

- Personal names and machine references in examples and fixtures (T0.2).
- The no-op Lighthouse workflow; this is a CLI with no website to audit (T0.3).
- The stale "Future Enhancements" list in SKILL.md, which now links to
  [ROADMAP.md](ROADMAP.md) (T0.4).

### Added

- Test that every flag documented in SKILL.md/README exists on its script (T0.5).
- `CHANGELOG.md`, `RELEASING.md` and a Python version policy in CONTRIBUTING.md (T0.13).

## [1.0.2] - 2026-10-12

### Fixed

- `cleanup_executor` and `smart_export` target assets by Photos UUID instead of
  filename. Filenames aren't unique, so a filename match could delete or
  export a photo the filters had excluded.

### Changed

- Full-library scans stream rows instead of loading everything with `fetchall()`.
- Dependency ranges have upper bounds.
- SKILL.md documents export safety accurately and adds a data-sensitivity section.

### Added

- ClawHub manifest fields in SKILL.md (`version`, OS restriction), a test that
  keeps them in step with `pyproject.toml`, and a publish-on-merge workflow.
- CI gates: mypy, 80% coverage floor, ruff formatting, Python 3.14.
- Repository baseline: security policy, pre-commit hooks, consistency guard,
  gitleaks, actionlint, stale, labeler and release-drafter workflows.

## [1.0.1]

Published to ClawHub without a matching version bump or tag in this
repository, so its exact contents aren't recorded. It sits between 1.0.0 and
1.0.2; everything that changed in that window is listed under 1.0.2.

## [1.0.0] - 2026-03-03

### Added

- First release as a Claude/OpenClaw skill: 20 stdlib-only scripts that read
  the Photos SQLite database read-only. They cover library analysis, storage,
  junk and duplicate detection, timeline recaps, people, places, scenes, photo
  habits, On This Day, album audit, Live Photos, iCloud status, Shared Library,
  similarity, seasonal highlights and face quality.
- Opt-in mutating commands: `cleanup_executor` (moves items to Recently Deleted
  via Photos.app) and `smart_export` (exports copies via AppleScript), both
  preview-first.
- Schema detection for the old and new (`ZPERSONFORFACE`/`ZASSETFORFACE`) face tables.

[Unreleased]: https://github.com/and3rn3t/apple-photos-cleaner/compare/v1.4.0...HEAD
[1.4.0]: https://github.com/and3rn3t/apple-photos-cleaner/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/and3rn3t/apple-photos-cleaner/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/and3rn3t/apple-photos-cleaner/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/and3rn3t/apple-photos-cleaner/compare/v1.0.3...v1.1.0
<!-- No tags existed before 1.0.3; versions are anchored on commits. -->
[1.0.3]: https://github.com/and3rn3t/apple-photos-cleaner/compare/05552f3...v1.0.3
[1.0.2]: https://github.com/and3rn3t/apple-photos-cleaner/compare/cf2f97e...05552f3
[1.0.0]: https://github.com/and3rn3t/apple-photos-cleaner/tree/cf2f97e
