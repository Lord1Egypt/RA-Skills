# Photo Habits & Insights — `photo_habits.py`

Behavioral analytics: when you shoot most, busiest days, seasonal patterns, streaks, photo vs video ratio trends.

```bash
python3 scripts/photo_habits.py [--year YYYY] [--human]
```

**Options:**
- `--year YYYY` — Filter to specific year
- `--human` — Human-readable summary
- `--output FILE` — Write JSON to file

**What It Shows:**
- Time-of-day breakdown (morning/afternoon/evening/night)
- Peak hour, peak day of week, peak month
- Day-of-week distribution with visual bars
- Longest photo streak (consecutive days with photos)
- Busiest single day
- Year-over-year trends with video ratio
- Monthly trend with photos/videos/screenshots breakdown

**Example Output:**
```
📊 PHOTO HABITS & INSIGHTS
==================================================

Total: 11,234 photos, 891 videos, 328 screenshots
Average per active day: 8.3

⏰ When You Shoot:
  Peak hour: 14:00
  Peak day: Saturday
  Peak month: Jul

  Time of Day:
    Morning (6am-12pm):   3,456 (28.1%) █████████
    Afternoon (12pm-6pm): 5,123 (41.6%) █████████████
    Evening (6pm-12am):   2,987 (24.3%) ████████
    Night (12am-6am):       737 (6.0%)  ██

🔥 Streaks:
  Longest streak: 45 consecutive days
    (2024-06-15 → 2024-07-29)
```

**Usage in Conversation:**

**User:** "What are my photo-taking patterns?"  
**AI:** *Runs photo_habits.py, narrates key insights*

**User:** "When do I take the most photos?"  
**AI:** *Runs photo_habits.py, highlights peak times and days*

---

[← All commands](../../SKILL.md#commands)
