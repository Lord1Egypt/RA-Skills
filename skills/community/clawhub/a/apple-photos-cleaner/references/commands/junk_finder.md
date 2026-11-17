# Junk Finder — `junk_finder.py`

Identify cleanup candidates: screenshots, screen recordings, low-quality photos, burst leftovers, duplicates.

```bash
python3 scripts/junk_finder.py [--screenshot-age DAYS] [--quality-threshold N] [--human]
```

**Options:**
- `--screenshot-age DAYS` — Consider screenshots older than N days as junk (default: 30)
- `--quality-threshold N` — Quality score threshold for low-quality (default: 0.3, range: 0.0-1.0)
- `--no-duplicates` — Skip duplicate detection
- `--human` — Human-readable summary
- `--output FILE` — Write JSON to file

**Example Output:**
```
🗑️  JUNK FINDER RESULTS
==================================================

Found:
  📸 Screenshots: 328
     └─ Old (>30 days): 287
  🎥 Screen Recordings: 12
  📉 Low Quality: 156
  📸 Burst Leftovers: 1,089
  👥 Possible Duplicates: 45

Estimated Savings:
  Conservative: 2.3 GB
    (Old screenshots + burst leftovers)
  Aggressive: 5.7 GB
    (All screenshots + screen recordings + low quality + bursts + ~50% of duplicates)
```

**What It Finds:**
- **Screenshots** — Photos with the `ZISDETECTEDSCREENSHOT` flag
- **Screen recordings** — Videos with the same flag, listed separately and never counted as screenshots
- **Old screenshots** — Screenshots older than specified age (safe to delete)
- **Low quality** — Photos with low quality scores (high failure/noise, low composition/lighting)
- **Burst leftovers** — Unpicked photos from burst sequences
- **Possible duplicates** — Using Apple's built-in detection

**Usage in Conversation:**

**User:** "Find junk in my Photos"  
**AI:** *Runs junk_finder.py, reports totals and estimated savings*

**User:** "How many old screenshots do I have?"  
**AI:** *Runs junk_finder.py, focuses on screenshot stats*

**User:** "What can I delete to free up 5GB?"  
**AI:** *Runs junk_finder.py, shows conservative/aggressive estimates, suggests next steps*

---

[← All commands](../../SKILL.md#commands)
