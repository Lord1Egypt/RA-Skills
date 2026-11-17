# Live Photo Analyzer — `live_photo_analyzer.py`

Analyze Live Photos vs still photos: identify Live Photos, compare storage impact, find Live Photos that could be converted to stills to save space.

```bash
python3 scripts/live_photo_analyzer.py [--human] [--year YYYY] [--output FILE]
```

**Options:**
- `--year YYYY` — Filter to specific year
- `--human` — Human-readable summary
- `--output FILE` — Write JSON to file

**What it reports:**
- Total Live Photos vs stills (count and storage)
- Playback style breakdown (live, loop, bounce, long exposure)
- Year-over-year Live Photo trends
- Estimated savings if Live Photos were converted to stills (~50% of video component)
- Unfavorited Live Photos as conversion candidates
- Largest Live Photos (biggest savings first)

---

[← All commands](../../SKILL.md#commands)
