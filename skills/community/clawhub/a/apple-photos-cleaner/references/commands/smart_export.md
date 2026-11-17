# Smart Export — `smart_export.py`

Plan organized exports by year/month, person, album, or location. It shows what will be exported and only exports when given the plan's confirmation token.

```bash
python3 scripts/smart_export.py --output-dir PATH [--organize-by MODE] [--plan-only | --confirm TOKEN] [--format json]
```

**Options:**
- `--output-dir PATH` — Where to export (required)
- `--organize-by MODE` — How to organize: `year_month`, `person`, `album`, `location` (default: year_month)
- `--favorites` — Export only favorites
- `--start-date YYYY-MM-DD` — Filter by start date
- `--end-date YYYY-MM-DD` — Filter by end date
- `--person NAME` — Export only photos with this person
- `--album NAME` — Export only from this album
- `--plan-only` — Show plan without exporting (recommended first step)
- `--confirm TOKEN` — Run the export; must match the token the plan printed
- `--format human|json` — Plan/result format (default: human). JSON includes `confirm_token` and `next_command`

**Example Output:**
```
📤 EXPORT PLAN
==================================================
Organization: year_month
Total photos: 3,456
Total size: 15.2 GB
Folders: 36

Folders:
  2025/01-January/
    123 items, 542 MB
  2025/02-February/
    156 items, 687 MB
  2025/03-March/
    89 items, 398 MB
  ...

Confirmation token: <token>
To export exactly this plan, run:
    /usr/bin/python3 /path/to/scripts/smart_export.py --output-dir ~/Export --organize-by year_month --confirm <token>
```

**Mutating:** with a matching `--confirm` token this command exports. Without one it prints the plan and its token and exits with code 11. A token is bound to the exact assets, filters and `--output-dir`; if any of them changed, nothing is written and a fresh token is printed. The export drives Photos.app via AppleScript to write copies into `--output-dir`. It creates new files only — the library is never altered. Each asset is resolved by its `ZUUID`, and the resolved item's filename is re-checked before export, so the run cannot reach photos outside the plan. The final line reports `exported` and `skipped` counts; items are skipped when their id no longer resolves in Photos or the filename no longer matches.

**Usage in Conversation:**

**User:** "I want to export all my 2024 photos organized by month"  
**AI:** *Runs smart_export.py with year filter and --plan-only, shows the plan*

**User:** "Export all photos with Alex"  
**AI:** *Runs smart_export.py with --person "Alex" and --plan-only, shows what would be exported*

---

[← All commands](../../SKILL.md#commands)
