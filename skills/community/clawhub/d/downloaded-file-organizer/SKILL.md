---
name: organize
description: Organize files from the Downloads folder into appropriate local directories
---

Organize files from the Downloads folder into appropriate local directories.

## Steps

### 1. Check configuration

Run:
```bash
python3 ~/.claude/skills/organize/organizer.py --scan 2>&1
```

If the output contains `"error": "config_missing"`, first run setup interactively:
```bash
python3 ~/.claude/skills/organize/organizer.py --setup
```
Default target root is `~/Documents`, default downloads dir is `~/Downloads`.

Then re-run `--scan`.

---

### 2. Display dry-run plan

Parse the JSON array returned by `--scan` and display it as a table:

| Filename | Destination | Reason | Notes |
|----------|-------------|--------|-------|
| ...      | ...         | ...    | Renamed (if conflict) |

- `target_subdir` is the subdirectory relative to target root
- `renamed: true` means the file will be renamed to avoid conflict
- If the plan is empty, tell the user there are no files to organize

---

### 3. Ask for confirmation

Say: "The plan above covers N file(s). Reply **confirm** to proceed, or tell me what to adjust."

- If the user **confirms**: proceed to step 4
- If the user requests **changes**: adjust the plan (modify `target_subdir` and `final_target` fields accordingly), show the updated table, and ask again
- If the user **cancels**: stop

---

### 4. Execute

Pass the (possibly modified) plan JSON back to the script:

```bash
python3 ~/.claude/skills/organize/organizer.py --execute '<JSON>'
```

Display results:
- How many files were moved successfully
- Any errors
- Mention that the log is saved at `~/.claude/skills/organize/logs/` and the index is updated at `~/.claude/skills/organize/index.md`

---

### 5. Offer watch mode

Ask: "Would you like to enable **watch mode**? New files in your downloads folder will be organized automatically (stops when the terminal is closed)."

If yes:
```bash
python3 ~/.claude/skills/organize/organizer.py --watch
```

---

## Notes

- Script location: `~/.claude/skills/organize/organizer.py`
- Config: `~/.claude/skills/organize/config.json`
- Logs: `~/.claude/skills/organize/logs/YYYY-MM-DD.log`
- Index: `~/.claude/skills/organize/index.md`
- The script requires `watchdog` for watch mode: `pip install watchdog`

## Configurable fields in config.json

| Field | Description |
|-------|-------------|
| `target_root` | Root directory where files are moved into |
| `downloads_dir` | Directory to scan for new files |
| `rules` | Keyword-based classification rules (array of `{keywords, target, reason}`) |
| `extension_fallbacks` | Extension-based fallback rules (array of `{extensions, target, reason}`) |
| `ignored_filenames` | Filenames to skip (case-insensitive), e.g. `desktop.ini` |
| `ignored_prefixes` | Filename prefixes to skip, e.g. `.` and `$` |
| `skip_dirs` | Directories excluded from index generation |
