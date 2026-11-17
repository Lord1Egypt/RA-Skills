# People Analyzer — `people_analyzer.py`

Deep analysis of people detected in your photos: who appears most, who's photographed together, trends over time, best photo of each person.

```bash
python3 scripts/people_analyzer.py [--min-photos N] [--top N] [--human]
```

**Options:**
- `--min-photos N` — Minimum photos to include a person (default: 5)
- `--top N` — Number of top people to analyze in detail (default: 20)
- `--human` — Human-readable summary
- `--output FILE` — Write JSON to file

**What It Shows:**
- All named people ranked by photo count
- Per-person yearly trends (are you photographing them more or less?)
- Co-occurrence analysis (who appears together most)
- Best quality photo for each person
- Favorites count per person
- Unnamed face count

**Example Output:**
```
👥 PEOPLE ANALYZER
==================================================

Named people (≥5 photos): 15
Photos with unnamed faces: 1,234

Top People:
  Alex: 3,456 photos (★ 89)
    📅 2023:890, 2024:1,200, 2025:1,366
  Sam: 3,234 photos (★ 76)
    📅 2023:845, 2024:1,100, 2025:1,289

Frequently Photographed Together:
  Alex + Sam: 2,100 photos
  Alex + Mom: 456 photos
```

**Usage in Conversation:**

**User:** "Who's in my photos the most?"  
**AI:** *Runs people_analyzer.py, reports top people with counts*

**User:** "Who do I photograph together?"  
**AI:** *Runs people_analyzer.py, focuses on co-occurrence analysis*

---

[← All commands](../../SKILL.md#commands)
