# On This Day / Memory Lane — `on_this_day.py`

See what you photographed on today's date in previous years. Includes people, scenes, and quality context.

```bash
python3 scripts/on_this_day.py [--date YYYY-MM-DD] [--window N] [--human]
```

**Options:**
- `--date YYYY-MM-DD` — Target date (defaults to today)
- `--window N` — Include photos ±N days around target (default: 0)
- `--human` — Human-readable summary
- `--output FILE` — Write JSON to file

**What It Shows:**
- Photos from each previous year on the same date
- People, scenes, and best photo for each year
- Favorites count per year
- How many years ago each set of photos was taken

**Example Output:**
```
📅 ON THIS DAY
==================================================

Date: March 3
Photos found: 45 across 4 years

📆 2025 (1 year ago)
   12 photos, ⭐ 3
   👥 Alex, Sam
   🏷️  swimming, pool
   📸 Best: IMG_1234.jpg Q:0.89

📆 2024 (2 years ago)
   8 photos
   👥 Alex
   🏷️  park, outdoor
```

**Usage in Conversation:**

**User:** "What did I do on this day in past years?"  
**AI:** *Runs on_this_day.py, narrates memories year by year*

**User:** "Show me memories from March 3"  
**AI:** *Runs on_this_day.py --date 2026-03-03, tells the story*

**AI Tip:** Narrate memories warmly! "2 years ago today, you were at the pool with Alex and Sam — you took 12 photos and favorited 3 of them. The best shot has a quality score of 0.89!"

---

[← All commands](../../SKILL.md#commands)
