---
name: favorites-curator
description: Build and maintain a local favorites catalog from installed repositories, apps, skills, extensions, and hooks. Use when the user asks to create, refresh, curate, scan, or summarize a favorites collection, software inventory, skill inventory, or daily digest of useful local resources.
---

# Favorites Curator

Maintain a file-backed catalog of useful local resources.

## Do First

1. Run `scripts/scan_favorites.py` to refresh entries and the latest snapshot.
2. Run `scripts/daily_digest.py` to compare the latest snapshot with the previous one and produce a digest.
3. Run `scripts/notify_candidates.py` when the user wants short notification copy for notable items.

## Paths

- Entries: `favorites/entries/`
- Snapshots: `favorites/snapshots/`
- Reports: `favorites/reports/`
- Cache: `favorites/enrichment-cache.json`
- Skill code: `skills/favorites-curator/`
- Naming and schema notes: `references/naming-and-model.md`

## Covered Sources

- `~/ai` git repositories
- `brew` installed formulae and casks
- `/Applications` and `~/Applications`
- `~/.codex/skills`
- `~/.claude/skills`
- `~/.agents/skills`
- `~/.openclaw/workspace/skills`
- `~/.openclaw/extensions`
- `~/.openclaw/hooks`

## Expected Workflow

### Refresh catalog

```bash
python3 skills/favorites-curator/scripts/scan_favorites.py
```

Use `--limit-source` to iterate on one source:

```bash
python3 skills/favorites-curator/scripts/scan_favorites.py --limit-source brew
```

### Generate daily digest

```bash
python3 skills/favorites-curator/scripts/daily_digest.py
```

This produces a Markdown report with:
- new entries
- updated entries
- likely similar items worth deduping or cross-referencing
- notable items worth surfacing

### Emit notification copy

```bash
python3 skills/favorites-curator/scripts/notify_candidates.py
```

Use `--top N` to cap the number of lines.

## Data Rules

- Prefer local metadata over online enrichment.
- Leave missing fields empty or mark them as inferred in `field_sources`.
- Keep filenames ASCII, sortable, and machine-friendly.
- Store one entry per file.
- Update the same entry file on re-scan instead of creating duplicates.

## Output Contract

Each entry file must keep these fields in frontmatter:
- `name`
- `author`
- `data_type`
- `install_path`
- `install_time`
- `update_time`
- `summary`
- `simple_usage`
- `source_url`

Other helper fields are allowed when useful for automation.

## Notes

- The scripts are local-first and safe to run repeatedly.
- `brew info --json=v2 --installed` is used once per scan; avoid tight cron loops.
- Read `references/naming-and-model.md` before changing filename rules or schema.
