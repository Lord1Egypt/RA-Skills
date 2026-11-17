---
name: apple-photos-cleaner
description: Analyze, clean up, and organize Apple Photos libraries. Find and report junk photos (screenshots, low-quality, burst leftovers, duplicates), analyze storage usage, generate photo timeline recaps, plan smart exports, analyze Live Photos, check iCloud sync, audit shared libraries, detect similar photos, curate seasonal highlights, and score face quality. All analysis operations are READ-ONLY on the database (safe); the separate cleanup and export commands drive Photos.app via AppleScript and require explicit opt-in. macOS only. PRIVACY — reports can include recognized people's names, face data, GPS coordinates, and shared-library contributor identifiers; all processing is local with no network access, but written reports carry that data. Requires Python 3.10+ (stdlib only) and access to the Apple Photos SQLite database. Trigger on: Photos cleanup, photo storage, duplicate photos, junk photos, screenshot cleanup, Photos analysis, photo timeline, photo export, Photos library stats, burst cleanup, storage hogs, photo organization, Live Photos, iCloud sync, shared library, similar photos, seasonal highlights, face quality, portraits.
version: 1.4.0
metadata: {"openclaw": {"os": ["macos"], "emoji": "📸", "homepage": "https://github.com/and3rn3t/apple-photos-cleaner", "requires": {"bins": ["python3", "osascript"]}}}
---

# Apple Photos Cleaner

Analyze, audit and clean up an Apple Photos library by reading its SQLite database: junk, duplicates, storage, people, places, timelines, best shots. Each command's flags, example output and conversation examples are in `references/commands/<command>.md`. Load that file before running a command you haven't used yet.

**Safety:** every analysis command is read-only. Connections open `mode=ro` behind an authorizer that refuses any write, so nothing is ever written to `Photos.sqlite`. Two commands are **mutating** and drive Photos.app through AppleScript: `cleanup_executor.py` (moves items to Recently Deleted) and `smart_export.py` (writes copies to a folder). Both only preview unless given the preview's confirmation token; see [Mutations](#mutations).

**Privacy:** read-only is not low-sensitivity. Reports can contain people's names, face data, GPS coordinates and Shared Library contributors. Everything runs locally with no network access, but `--output` files carry that data; see [Privacy](#privacy).

## When to Use This Skill

Photos cleanup or freeing storage; duplicates, screenshots, bursts, low-quality shots; storage hogs and growth; "what did I do last week/this year"; best photos and hidden gems; who appears in photos and with whom; where photos were taken and trips; searching by content; photo habits and streaks; "on this day" memories; album organization; actually deleting junk; Live Photos; Shared Library; iCloud sync coverage; similar photos; seasonal highlights; portrait quality; organized exports; anything failing (run `doctor`).

## Quick Start

The library is found automatically at `~/Pictures/Photos Library.photoslibrary`; pass `--library PATH` (or `--db-path PATH` for a `Photos.sqlite`) for another one.

**If any command fails** (nonzero exit), run `python3 scripts/doctor.py --format json` before retrying. It says what's wrong (library not found, missing Full Disk Access, a command your macOS version can't support) and gives the exact fix to relay to the user.

Typical first pass: `library_analysis.py` for the overview → `junk_finder.py` and `duplicate_finder.py` for cleanup candidates → `storage_analyzer.py` if space is the concern.

## Commands

All are `python3 scripts/<command>.py`, or equivalently `python3 photos_cleaner.py <command>` (`photos-cleaner <command>` when installed with `pipx install .`; `--help` lists them). Sensitivity of the output: 🔴 high, 🟠 medium, 🟡 low (see [Privacy](#privacy)).

| Command | Use it for | Output | Reference |
| --- | --- | --- | --- |
| `library_analysis` | Big picture: counts, storage, date range, top people, quality distribution | 🟡 | [library_analysis.md](references/commands/library_analysis.md) |
| `junk_finder` | Screenshots (old and all), screen recordings, low-quality photos, burst leftovers, duplicates, with savings estimates | 🟡 | [junk_finder.md](references/commands/junk_finder.md) |
| `duplicate_finder` | Duplicate groups (Apple's detection + timestamp/dimension match) with a keep recommendation | 🟡 | [duplicate_finder.md](references/commands/duplicate_finder.md) |
| `storage_analyzer` | Storage by year, type and format; growth trends; largest items | 🟡 | [storage_analyzer.md](references/commands/storage_analyzer.md) |
| `timeline_recap` | Narrative recap of a date range, clustered into events with people, places and scenes | 🟠 | [timeline_recap.md](references/commands/timeline_recap.md) |
| `best_photos` | Highest-quality photos; `--hidden-gems` for great unfavorited ones | 🟠 | [best_photos.md](references/commands/best_photos.md) |
| `people_analyzer` | Who appears, how often, together, over time; best photos per person | 🔴 | [people_analyzer.md](references/commands/people_analyzer.md) |
| `location_mapper` | Location clusters, trips, offline place names | 🔴 | [location_mapper.md](references/commands/location_mapper.md) |
| `scene_search` | Search by detected content (beach, dog…) or a content inventory | 🟠 | [scene_search.md](references/commands/scene_search.md) |
| `photo_habits` | When you shoot: hour, weekday, streaks, seasons | 🟠 | [photo_habits.md](references/commands/photo_habits.md) |
| `on_this_day` | This date in past years (`--window` widens it) | 🟠 | [on_this_day.md](references/commands/on_this_day.md) |
| `album_auditor` | Orphan photos, empty albums, overlapping albums | 🟡 | [album_auditor.md](references/commands/album_auditor.md) |
| `live_photo_analyzer` | Live Photos vs stills, storage impact, conversion candidates | 🟡 | [live_photo_analyzer.md](references/commands/live_photo_analyzer.md) |
| `shared_library` | Shared Library vs personal: contributors, storage split | 🔴 | [shared_library.md](references/commands/shared_library.md) |
| `icloud_status` | iCloud sync coverage, large local-only items | 🟡 | [icloud_status.md](references/commands/icloud_status.md) |
| `similarity_finder` | Visually similar photos (Apple's computed feature scores) | 🟡 | [similarity_finder.md](references/commands/similarity_finder.md) |
| `seasonal_highlights` | Best photos per season | 🟠 | [seasonal_highlights.md](references/commands/seasonal_highlights.md) |
| `face_quality` | Best and worst portraits per person | 🔴 | [face_quality.md](references/commands/face_quality.md) |
| `cleanup_executor` ⚠️ | **Mutating:** move a junk category to Recently Deleted | 🟡 | [cleanup_executor.md](references/commands/cleanup_executor.md) |
| `smart_export` ⚠️ | **Mutating:** export copies organized by date, person, album or place | 🟠 | [smart_export.md](references/commands/smart_export.md) |
| `doctor` | Diagnose setup and schema problems, with a fix per check | 🟡 | [doctor.md](references/commands/doctor.md) |

Multi-command recipes (cleanup assessment, freeing storage, year in review, people deep dive…): [references/workflows.md](references/workflows.md). Database tables: [references/database-schema.md](references/database-schema.md).

## Output

- **Shared flags (every command):** `--db-path`/`--library`, `--format json|human|md|csv` (`--human` is shorthand; `md` is a Markdown report and `csv` has every list in the result as rows, with a `section` column), `-o FILE` (write the JSON there), `-q/--quiet` (only the result on stdout and problems on stderr, which is best for agents), and `-v/--verbose`. Output is JSON by default; `doctor` and `smart_export` default to human. `--top N` is how many results to show, and `--limit N` caps how much is processed.
- **Every structured result starts with** `schema_version`, `command`, `generated_at` (UTC) and `warnings` (e.g. a deprecated flag you used, with its replacement). Check `warnings` and pass anything relevant on to the user.
- **Partial results (`degraded`):** Apple adds and renames database columns between macOS versions. Every JSON result has a `degraded` list, normally empty. An entry such as `{"section": "burst_leftovers", "reason": "missing column(s): ZASSET.ZAVALANCHEKIND"}` means that section is `null` or was computed from the data that exists. Tell the user that part isn't available on their macOS version, and never present a `null` as zero.
- **Names:** show people `original_filename` (e.g. `IMG_1234.HEIC`). `filename` is Photos' internal storage name, a UUID on current macOS; it's only an identifier.
- **In conversation, synthesize; don't dump.** Be specific ("287 screenshots older than 30 days, 2.1 GB"), mention savings, turn timelines and memories into a short story, and aggregate rather than echo raw GPS coordinates or long name lists.

## Mutations

Analysis only identifies candidates. Deleting or exporting is a separate step the user must approve:

1. **Preview.** Run `cleanup_executor.py --category CATEGORY` (or `smart_export.py --output-dir DIR --plan-only --format json`). The JSON includes `confirm_token` and `next_command`.
2. **Show the user** what would happen: counts, sizes, examples. For cleanup, items go to Recently Deleted and are recoverable for 30 days. Ask for a yes.
3. **Only after a yes, run `next_command` verbatim.** It ends in `--execute --confirm <token>` for cleanup or `--confirm <token>` for export.
4. **Exit code 11** means the candidates or options changed since the preview, so nothing was done. Show the new preview and ask again. Never reuse a token, never execute just to get one, and never pass `--confirm` without the user's yes. There is no interactive prompt, and piping `yes` does nothing.

Cleanup is capped by `--limit` (default 500). A cleanup category or an export filter (`--person`, `--album`) whose columns this macOS version lacks refuses with exit 5 rather than act on partial data.

## Requirements & Permissions

- **macOS** with Photos, and **Python 3.10+** using the stdlib only. Stock `/usr/bin/python3` is 3.9 and too old (`brew install python`); `doctor.py` says so instead of crashing.
- **Read access** to the library: grant Full Disk Access to the app running the commands (Terminal, editor, agent app).
- **Automation** permission for Photos.app, needed only by the two mutating commands. macOS asks for it separately (`doctor.py --check-automation` tests it).

## Privacy

Reports describe identifiable people (the subjects of the photos), not just the user. Treat report files like the photos themselves.

- 🔴 **High:** `people_analyzer`, `face_quality` (names, face attributes, portrait rankings), `location_mapper` (GPS, home/work clusters, trips), `shared_library` (other people's contributions).
- 🟠 **Medium:** dated narratives, scene labels, behavioural patterns, filenames with people or places.
- 🟡 **Low:** counts, sizes, filenames, album titles.
- Nothing leaves the Mac: no network calls, no telemetry. The only files written are the `--output` report and, for `smart_export`, the exported copies.
- Prefer `--human` when the user just wants to read a result; write `--output` files only when needed. Be careful sharing Shared Library reports, since they describe other people.

## Limitations

- **Dates are local capture time.** Years, days and hours, plus `--year`/`--start-date`/`--end-date`, use each photo's recorded time zone, falling back to this Mac's.
- **Schema varies by macOS version.** Missing columns degrade sections (`degraded`) or, for a command's core columns, exit 5. On macOS 26, scene labels come from Photos' search index, which has no per-photo confidence. `doctor.py` lists what a library supports.
- **Offline place names** cover about 100 major cities; elsewhere coordinates are shown.
- **Similarity** compares Apple's computed scores, not pixels, and is O(n²), so it is bounded by `--limit`.
- **Shared Library** needs a macOS 13+ library. **Exports** need Photos.app; with "Optimize Mac Storage", iCloud-only originals must be downloaded first.

## Exit Codes

Branch on the code rather than parsing stderr.

| Code | Meaning | What to do |
| --- | --- | --- |
| 0 | Success | |
| 1 | Unexpected error | Re-run with `--verbose`; run `doctor.py`; report it |
| 2 | Usage error (bad flag or value) | Fix the arguments |
| 3 | Photos database not found | Pass `--library` or `--db-path` |
| 4 | Permission denied | Grant Full Disk Access to the app running the command |
| 5 | Schema unsupported | This library lacks a column the command can't run without; stderr names it. Mutating commands and filters refuse rather than act on partial data |
| 10 | Cancelled by the user | |
| 11 | Confirmation required | Nothing was changed. Show the fresh preview (on stdout) and ask again |

## Troubleshooting

- **Anything failing:** run `python3 scripts/doctor.py` first. It checks each prerequisite and prints the fix.
- **Counts differ from Photos.app:** trashed items are excluded, and Photos.app views may filter differently.
- **No quality scores:** not every photo has Apple's computed scores. Those photos are skipped, and the result's `degraded` list says when a score column is missing entirely.

Roadmap, priorities and non-goals: [ROADMAP.md](ROADMAP.md).
