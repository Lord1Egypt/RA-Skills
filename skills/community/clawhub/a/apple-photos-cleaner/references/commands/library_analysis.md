# Library Analysis — `library_analysis.py`

Get comprehensive library statistics: counts, storage, date ranges, people, quality scores.

```bash
python3 scripts/library_analysis.py [--human] [--output FILE]
```

**Options:**
- `--human` — Human-readable summary instead of JSON
- `--output FILE` — Write JSON to file
- `--db-path PATH` — Custom database path
- `--library PATH` — Custom Photos library path

**Example Output:**
```
📊 APPLE PHOTOS LIBRARY ANALYSIS
==================================================

Total Assets: 12,453
Total Storage: 48.3 GB
Average Size: 4.1 MB
Date Range: 2020-01-15 to 2025-03-03

By Type:
  Photo: 11,234
  Video: 891
  Screenshots: 328
  Favorites: 456
  Bursts: 1,234

By Year:
  2025: 1,203 items, 5.2 GB
  2024: 3,456 items, 15.1 GB
  2023: 2,987 items, 12.4 GB
  ...

Top People:
  Alex: 3,456 photos
  Sam: 3,234 photos
  ...
```

**Usage in Conversation:**

**User:** "How many photos do I have?"  
**AI:** *Runs library_analysis.py with --human flag, reports summary*

**User:** "Show me my Photos storage breakdown"  
**AI:** *Runs library_analysis.py, highlights key stats*

---

[← All commands](../../SKILL.md#commands)
