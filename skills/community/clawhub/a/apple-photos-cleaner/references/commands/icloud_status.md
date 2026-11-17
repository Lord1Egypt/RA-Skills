# iCloud Sync Status — `icloud_status.py`

Check iCloud sync coverage across the library: synced vs local-only, download status, large unsynced items.

```bash
python3 scripts/icloud_status.py [--human] [--output FILE]
```

**What it reports:**
- Sync coverage percentage (synced vs local-only)
- Storage breakdown by sync state
- Photo vs video sync comparison
- Year-over-year sync trends
- Large local-only items (>10 MB) that aren't synced
- My assets vs others' assets
- Downloadable (cloud-only) item count

---

[← All commands](../../SKILL.md#commands)
