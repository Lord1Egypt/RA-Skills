# Timeline Recap — `timeline_recap.py`

Generate narrative summaries of photo activity for any date range. Groups photos into events and includes context: people, locations, scenes.

```bash
python3 scripts/timeline_recap.py --start-date YYYY-MM-DD [--end-date YYYY-MM-DD] [--narrative]
```

**Options:**
- `--start-date` — Start date (required)
- `--end-date` — End date (optional, defaults to today)
- `--cluster-hours N` — Hours between photos to consider separate events (default: 4)
- `--narrative` — Output narrative text instead of JSON
- `--output FILE` — Write to file

**What It Generates:**
- Day-by-day photo activity
- Event clustering (groups photos taken close together)
- People detected in each event
- Scene classifications (beach, sunset, dog, etc.)
- Location data (if available)
- Favorites count

**Example Output:**
```
📅 PHOTO TIMELINE RECAP
==================================================

Period: 2025-03-01 to 2025-03-07
Total: 156 photos across 5 days
Events: 12

📆 2025-03-01 (Saturday) - 45 photos

  🕐 09:15 (2h 15m)
     32 photos, 2 videos ⭐ 5 favorites
     👥 Alex, Sam
     🏷️  swimming, pool, sports
     📍 41.5369, -90.5776

  🕐 18:30 (45m)
     13 photos
     👥 Alex, Sam
     🏷️  dinner, food, family
```

**Usage in Conversation:**

**User:** "What did I do last week?"  
**AI:** *Runs timeline_recap.py with last week's dates, narrates the timeline in story form*

**User:** "Show me my photo activity for February"  
**AI:** *Runs timeline_recap.py with Feb 1 - Feb 28, summarizes highlights*

**User:** "Tell me about our vacation photos from August"  
**AI:** *Runs timeline_recap.py with August dates, creates a narrative story*

**AI Tip:** When presenting timeline results, narrate them like a story! Don't just dump the JSON. Example:

> "You had a busy Saturday on March 1st! In the morning around 9:15, you spent about 2 hours at the pool — 32 photos with Alex and Sam, mostly swimming and sports shots. You marked 5 as favorites. Then in the evening around 6:30, you captured a family dinner with 13 photos. Looks like a great day!"

---

[← All commands](../../SKILL.md#commands)
