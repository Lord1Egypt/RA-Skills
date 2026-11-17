# Storage Analyzer — `storage_analyzer.py`

Detailed storage breakdown: by year, type, source, growth trends, file types, storage hogs.

```bash
python3 scripts/storage_analyzer.py [--human] [--output FILE]
```

**Analyzes:**
- Total storage and breakdown by photo/video
- Storage by year and month
- Screenshots vs regular photos
- File types (JPEG, HEIC, MOV, etc.)
- Growth trends over time
- Top 20 largest files

**Example Output:**
```
💾 STORAGE ANALYSIS
==================================================

Total Storage: 48.3 GB

By Type:
  Photo: 32.1 GB (66.5%)
    11,234 items, avg 2.9 MB
  Video: 16.2 GB (33.5%)
    891 items, avg 18.7 MB

By Source:
  Photos & Videos: 46.1 GB (95.4%)
  Screenshots: 2.2 GB (4.6%)

By Year:
  2025: 5.2 GB (1,203 items)
  2024: 15.1 GB (3,456 items)
  2023: 12.4 GB (2,987 items)
  ...

Top 10 Largest Files:
  1. 📹 287 MB - VID_2024_vacation.mov
  2. 📹 245 MB - VID_2024_swim_meet.mov
  3. 📹 198 MB - VID_2023_birthday.mov
  ...

Recent Growth (last 12 months):
  Total added: 18.7 GB
  Average per month: 1.6 GB
```

**Usage in Conversation:**

**User:** "What's taking up space in my Photos?"  
**AI:** *Runs storage_analyzer.py, highlights biggest categories*

**User:** "Show me my largest videos"  
**AI:** *Runs storage_analyzer.py, focuses on storage_hogs section filtered by videos*

**User:** "How much storage am I adding per month?"  
**AI:** *Runs storage_analyzer.py, reports recent growth stats*

---

[← All commands](../../SKILL.md#commands)
