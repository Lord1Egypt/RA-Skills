---
name: changelog-watcher
description: Monitor GitHub repos and npm packages for new releases and version updates. Summarizes changelogs and highlights breaking changes. Use when the user asks to check for updates, find new releases, review changelogs, track version updates, or asks "what's new in X". Also use when asked to run or schedule a changelog check, set up release monitoring, or report on recent releases for any software package or GitHub repo.
---

# Changelog Watcher

Maintains a watchlist of GitHub repos and npm packages, detects new releases, and produces markdown reports with breaking changes highlighted.

## Files

- `watchlist.json` — user config (create from `assets/watchlist.example.json`)
- `state.json` — auto-managed last-seen versions (do not edit)
- `scripts/compare_versions.py` — main entry point; calls the others
- `scripts/check_github.py` — GitHub releases API
- `scripts/check_npm.py` — npm registry
- `scripts/format_report.py` — markdown report generator

For setup, watchlist format, cron scheduling, and rate limit guidance → read `references/setup-guide.md`.

## Skill Directory

```
~/.openclaw/workspace/skills/changelog-watcher/
```

All script paths below are relative to this directory.

## Usage

### Check for new releases and print report

```bash
python3 scripts/compare_versions.py --update-state | python3 scripts/format_report.py
```

### Dry-run (check without advancing state)

```bash
python3 scripts/compare_versions.py | python3 scripts/format_report.py
```

### First-time setup (set baseline, no output)

```bash
cp assets/watchlist.example.json watchlist.json
# edit watchlist.json to your packages
python3 scripts/compare_versions.py --update-state
```

## Workflow

1. Confirm `watchlist.json` exists. If not, guide user to copy from `assets/watchlist.example.json` and fill it in.
2. Run `compare_versions.py` (with `--update-state` unless doing a dry-run).
3. Pipe output to `format_report.py`.
4. Present the markdown report to the user.
5. If the user wants to schedule this: provide the cron line from `references/setup-guide.md`.

## Adding Entries

To add a GitHub repo:
```json
{"source": "github", "owner": "OWNER", "repo": "REPO", "name": "Display Name"}
```

To add an npm package:
```json
{"source": "npm", "package": "package-name", "name": "Display Name"}
```

Append to the `watch` array in `watchlist.json`, then run the full pipeline.

## Error Handling

- **Rate limited (exit 2):** Wait for the retry window; check how many GitHub entries are in the watchlist vs the 60/hr limit.
- **Not found (exit 3):** Verify the owner/repo or package name in the watchlist.
- **Network error:** Check connectivity; retry.
- **First-run shows zero releases:** Expected — first run sets the baseline only.
