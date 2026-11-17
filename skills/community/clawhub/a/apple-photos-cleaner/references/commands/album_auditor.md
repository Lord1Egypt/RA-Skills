# Album Auditor — `album_auditor.py`

Find orphan photos (not in any album), empty albums, tiny albums, and overlapping albums.

```bash
python3 scripts/album_auditor.py [--human]
```

**Options:**
- `--human` — Human-readable summary
- `--output FILE` — Write JSON to file

**What It Shows:**
- Orphan photos count (not in any album)
- Empty albums that can be deleted
- Tiny albums (≤3 photos) that might be incomplete
- Album overlap (shared photos between albums, with percentages)
- Album size ranking

**Example Output:**
```
📁 ALBUM AUDITOR
==================================================

Total albums: 45
Albums with photos: 38
Empty albums: 4
Tiny albums (≤3 photos): 7
Photos in albums: 8,234 / 12,453
Orphan photos (no album): 4,219

📭 Orphan Photos:
  4,219 photos not in any album
  Total size: 18.3 GB

🗑️  Empty Albums (4):
  • Old Vacation
  • Test Album

🔄 Album Overlaps:
  "Vacation 2024" ∩ "Summer 2024"
    45 shared (12.3% / 8.9%)
```

**Usage in Conversation:**

**User:** "Are my photos well organized?"  
**AI:** *Runs album_auditor.py, reports orphans, empty albums, and overlap*

**User:** "How many photos aren't in any album?"  
**AI:** *Runs album_auditor.py, reports orphan count and size*

---

[← All commands](../../SKILL.md#commands)
