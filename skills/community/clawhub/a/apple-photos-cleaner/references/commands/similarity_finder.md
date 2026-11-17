# Photo Similarity Detection — `similarity_finder.py`

Find visually similar photos beyond exact duplicates using computed quality feature vectors (composition, lighting, color, patterns, etc.).

```bash
python3 scripts/similarity_finder.py [--threshold 0.95] [--year YYYY] [--limit 500] [--human]
```

**Options:**
- `--threshold` — Cosine similarity threshold 0-1 (default: 0.95, very similar)
- `--year YYYY` — Filter to specific year
- `--limit N` — Max photos to compare (default: 500, controls runtime)
- `--human` — Human-readable summary

**What it reports:**
- Groups of visually similar photos
- Potential storage savings per group
- Keep candidate (largest/highest quality in each group)
- Total extra (removable) similar photos

**Runtime note:** O(n²) comparison; use `--limit` to control runtime for large libraries.

---

[← All commands](../../SKILL.md#commands)
