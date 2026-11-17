# Face Quality Scoring — `face_quality.py`

Score face quality per person using Apple Photos' face detection attributes: quality measure, blur, yaw angle, smile, face size, and center position.

```bash
python3 scripts/face_quality.py [--person NAME] [--top 10] [--human]
```

**Options:**
- `--person NAME` — Filter to specific person name
- `--top N` — Top N best/worst per person (default: 10)
- `--human` — Human-readable summary

**What it reports:**
- Per-person face quality rankings
- Best and worst portraits per person
- Composite face score (quality, blur, size, yaw, smile, center)
- Overall library face quality average
- Most photographed person, highest quality person

---

[← All commands](../../SKILL.md#commands)
