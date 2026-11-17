# Apple Photos Cleaner

Analyze, audit, and clean up your Apple Photos library by querying its SQLite database directly.

Goes beyond what Photos.app offers: intelligent junk detection, detailed storage analysis, duplicate finding with quality scoring, timeline recaps, people analytics, location mapping, and more.

> **Safety:** Analysis commands are read-only — they query the Photos database over a read-only
> connection and never write back to it. Two commands are **mutating** and drive Photos.app through
> AppleScript: `cleanup_executor.py` moves items to Recently Deleted (previews by default; needs
> `--execute --confirm <token>` from that preview), and `smart_export.py` writes exported copies to a directory you
> choose. See [Safety & Privacy](#safety--privacy).

> **Privacy:** Reports can include recognized people's names, face data, GPS coordinates, and
> shared-library contributors. Everything stays on your Mac — nothing is uploaded — but be careful
> where you save or share the JSON output. See [Safety & Privacy](#safety--privacy).

## Requirements

- **macOS** (accesses the Photos SQLite database)
- **Python 3.10+** (uses stdlib only — no external runtime dependencies). Stock macOS
  `/usr/bin/python3` is 3.9 and too old; install a current one with `brew install python`

## Setup

```bash
# Clone the repo
git clone https://github.com/and3rn3t/apple-photos-cleaner.git
cd apple-photos-cleaner

# Install dev/test dependencies
make install
```

## Commands

Every script lives in `scripts/` and outputs **JSON** by default (for piping / AI consumption). Add `--human` for readable terminal output.

One entry point runs them all, with hyphens or underscores:

```bash
python3 photos_cleaner.py --help                 # list every command
python3 photos_cleaner.py junk-finder --human    # same as python3 scripts/junk_finder.py --human
python3 photos_cleaner.py junk-finder --format csv -o junk.csv   # or --format md for a Markdown report
pipx install . && photos-cleaner doctor          # optional: install the `photos-cleaner` command
```

| Script | Purpose |
|---|---|
| `library_analysis.py` | Big-picture stats: counts, storage, date ranges, quality distribution |
| `junk_finder.py` | Identify screenshots, low-quality photos, burst leftovers |
| `duplicate_finder.py` | Find duplicates via Apple's detection + timestamp/dimension matching |
| `storage_analyzer.py` | Breakdown by year, type, format; growth trends; storage hogs |
| `timeline_recap.py` | Narrative summaries of photo activity for any date range |
| `smart_export.py` | Plan organized exports by year/month, person, album, or location |
| `best_photos.py` | Surface high-quality photos you haven't favorited |
| `people_analyzer.py` | People co-occurrence, trends over time, best photos per person |
| `location_mapper.py` | Cluster GPS coordinates into locations, identify trips |
| `scene_search.py` | Search by ML-detected content (beach, dog, food) or browse inventory |
| `photo_habits.py` | Time-of-day, day-of-week, streaks, seasonal trends |
| `on_this_day.py` | Photos from today's date in prior years |
| `album_auditor.py` | Find orphan photos, empty albums, album overlap |
| `cleanup_executor.py` | Batch move junk to trash via AppleScript (with confirmation) |
| `live_photo_analyzer.py` | Analyze Live Photos vs stills, find conversion candidates |
| `shared_library.py` | Audit Shared Library vs personal: contributors, storage splits |
| `icloud_status.py` | Check iCloud sync coverage: synced vs local-only items |
| `similarity_finder.py` | Detect visually similar photos using quality feature vectors |
| `seasonal_highlights.py` | Curate best photos per season with favorite boosting |
| `face_quality.py` | Score face/portrait quality using Apple's ML face attributes |
| `doctor.py` | Diagnose setup: library location, Full Disk Access, Automation, macOS schema, with a fix per check |

### Examples

```bash
# Quick library overview
python3 scripts/library_analysis.py --human

# Find junk photos
python3 scripts/junk_finder.py --human

# Best photos you forgot to favorite
python3 scripts/best_photos.py --hidden-gems --human

# What happened on this day in past years
python3 scripts/on_this_day.py --human

# Search for beach photos
python3 scripts/scene_search.py --search beach --human

# Preview cleanup (dry run by default)
python3 scripts/cleanup_executor.py --category old_screenshots --human
```

## Development

```bash
make test        # Run tests
make coverage    # Tests with coverage report
make lint        # Lint with ruff
make format      # Auto-format with ruff
make check       # Lint + format check + tests (CI equivalent)
make clean       # Remove cache/build artifacts
```

### Project structure

```
photos_cleaner.py # Dispatcher: `python3 photos_cleaner.py <command>` (or `photos-cleaner` once installed)
scripts/          # All analysis scripts + shared _common.py and _schema.py (schema registry); schema-fingerprints.json
tests/            # Pytest test suite
references/       # commands/<name>.md (flags, output, examples), workflows.md, database schema
docs/             # Threat model
SKILL.md          # AI skill router: when to use each command, safety and privacy rules (≤ 250 lines)
pyproject.toml    # Tool config (pytest, ruff, mypy)
```

## How it works

Apple Photos stores its metadata in a SQLite database at:

```
~/Pictures/Photos Library.photoslibrary/database/Photos.sqlite
```

This project queries that database in **read-only mode** to surface insights. Core Data timestamps (seconds since 2001-01-01) are converted to Python datetimes. ML-detected attributes like quality scores, scene classifications, and face data are all available in the database.

## Safety & Privacy

### What each command can do

Everything except the two commands below is **read-only**: the database is opened with
`mode=ro`, and nothing is written back to it.

| Command | Effect | Gate |
|---|---|---|
| `cleanup_executor.py` | Moves items to **Recently Deleted** via Photos.app | Previews by default; needs `--execute --confirm <token>` matching the preview; capped by `--limit` (default 500) |
| `smart_export.py` | Writes **exported copies** into `--output-dir` | Prints the plan and a token; exports only with `--confirm <token>` matching that plan |

Neither command alters originals. Cleanup is recoverable from Recently Deleted for 30 days;
export only creates new files.

Both resolve assets by their stable `ZUUID` and re-check the filename after resolving, so a
run can only ever touch assets you previewed. Filenames in Photos are not unique, and matching
on them could otherwise reach photos outside the planned set.

### What the reports contain

Analysis is read-only but not low-sensitivity. Output can include:

| Data | Commands |
|---|---|
| Recognized people's names | `people_analyzer.py`, `face_quality.py`, `location_mapper.py`, `timeline_recap.py`, `on_this_day.py`, `best_photos.py` |
| Face detection and quality scores | `face_quality.py`, `people_analyzer.py` |
| GPS coordinates and inferred trips | `location_mapper.py`, `scene_search.py`, `on_this_day.py`, `timeline_recap.py` |
| Shared Library contributor identifiers | `shared_library.py` |
| Behavioural patterns (when and how often you shoot) | `photo_habits.py`, `timeline_recap.py`, `library_analysis.py` |
| Counts of hidden and favourited items | `library_analysis.py` |

All processing is local — no network calls, no telemetry, no external dependencies. The
sensitivity is in the **output**: JSON reports written with `--output` are plain files that
inherit your umask. Treat them like the photos they describe, and prefer `--human` to stdout
when you only want to read the result.

### Permissions

- Analysis needs read access to `Photos.sqlite` — grant Full Disk Access, or point `--db-path`
  at a library you can already read.
- The two mutating commands *additionally* need Automation permission for Photos.app. macOS
  grants file access and automation separately, so expect a second prompt.

## License

MIT
