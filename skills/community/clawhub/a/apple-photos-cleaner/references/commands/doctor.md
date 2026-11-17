# Doctor — `doctor.py`

Diagnose why a command can't run. Each check reports pass/warn/fail plus a concrete fix.

```bash
python3 scripts/doctor.py [--library PATH] [--format human|json] [--check-automation]
python3 scripts/doctor.py --schema-dump > schema.sql
```

**Options:**
- `--library PATH` / `--db-path PATH` — Library bundle or database to check (default: the standard location)
- `--format human|json` — Output format (default: human). Agents should use `json`
- `--check-automation` — Also test AppleScript access to Photos.app. It can launch Photos and show a permission prompt, so it's opt-in
- `--schema-dump` — Print the database's table definitions (no rows, no metadata) for a bug report about a new macOS version

**Checks:** `python`, `library` (found where), `read_access` (Full Disk Access), `schema` (macOS version from Photos' model version, known-fingerprint match), `features` (which commands, sections and options this library's schema can't support, from every script's declared columns), `library_size`, `optimize_storage` (heuristic: are originals on this Mac?), `automation` (only with `--check-automation`).

**Exit codes:** 0 when nothing failed (warnings are fine), 3 library not found, 4 no read access, 1 for other failures (e.g. Automation denied).

**Usage in Conversation:**

**User:** "Why isn't this working?"
**AI:** *Runs doctor.py --format json, then relays each failing check's `fix`, e.g. how to grant Full Disk Access*

---

[← All commands](../../SKILL.md#commands)
