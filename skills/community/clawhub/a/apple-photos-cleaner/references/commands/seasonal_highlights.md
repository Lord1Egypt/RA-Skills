# Seasonal Highlights — `seasonal_highlights.py`

Curate the best photos from each season using quality scores, favorites, and scene context.

```bash
python3 scripts/seasonal_highlights.py [--year YYYY] [--top 20] [--southern] [--human]
```

**Options:**
- `--year YYYY` — Filter to specific year
- `--top N` — Top N photos per season (default: 20)
- `--southern` — Use Southern Hemisphere season definitions
- `--human` — Human-readable summary

**What it reports:**
- Best photos per season (spring, summer, fall, winter)
- Season-by-season quality scores and favorite counts
- Year-over-season distribution matrix
- Busiest season identification
- Best single photo per season

---

[← All commands](../../SKILL.md#commands)
