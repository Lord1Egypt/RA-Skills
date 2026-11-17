# Best Photos / Hidden Gems — `best_photos.py`

Surface your highest-quality photos using Apple's computed quality scores. Find hidden gems — great photos you never favorited.

```bash
python3 scripts/best_photos.py [--min-quality N] [--top N] [--hidden-gems] [--human]
```

**Options:**
- `--min-quality N` — Minimum quality score threshold (default: 0.7, range: 0.0-1.0)
- `--top N` — Number of top photos to return (default: 50)
- `--hidden-gems` — Only show photos that are NOT favorited
- `--year YYYY` — Filter to specific year
- `--human` — Human-readable summary
- `--output FILE` — Write JSON to file

**What It Shows:**
- Quality score distribution across your library (excellent/good/average/poor)
- Top N photos ranked by quality with detailed score breakdowns
- Hidden gems: high-quality photos you haven't favorited yet
- Per-photo scores for composition, lighting, symmetry, patterns, etc.

**Example Output:**
```
⭐ BEST PHOTOS / HIDDEN GEMS
==================================================

Photos with quality scores: 11,234
Above threshold (0.7): 2,456
Hidden gems (great but not favorited): 2,100
Already favorited high-quality: 356

Quality Distribution:
  🌟 Excellent (≥0.85): 456
  ✅ Good (≥0.70):      2,000
  📊 Average (≥0.50):   5,234
  📉 Below avg (≥0.30): 2,544
  ❌ Poor (<0.30):       1,000

Top 20 Photos:
    1. IMG_1234.jpg
       Q:0.952 | 4.2 MB | 4032x3024 💎
       📐 composition:0.95, lighting:0.92, symmetry:0.88
```

**Usage in Conversation:**

**User:** "Show me my best photos"  
**AI:** *Runs best_photos.py with --human flag, highlights top shots*

**User:** "Find hidden gems I haven't favorited"  
**AI:** *Runs best_photos.py with --hidden-gems, suggests which to favorite*

**User:** "What are my best photos from 2025?"  
**AI:** *Runs best_photos.py with --year 2025, shows quality distribution and top picks*

---

[← All commands](../../SKILL.md#commands)
