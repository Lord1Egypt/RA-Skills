# Location / Travel Mapper — `location_mapper.py`

Analyze where your photos were taken. Clusters GPS coordinates into locations, identifies trips, and shows most-photographed places.

```bash
python3 scripts/location_mapper.py [--radius N] [--year YYYY] [--human]
```

**Options:**
- `--radius N` — Cluster radius in km (default: 1.0)
- `--year YYYY` — Filter to specific year
- `--min-photos N` — Minimum photos per location cluster (default: 3)
- `--human` — Human-readable summary
- `--output FILE` — Write JSON to file

**What It Shows:**
- GPS coverage percentage
- Location clusters with photo counts, date ranges, and people
- Identified trips (clusters with 5+ photos spanning 4+ hours)
- Per-location monthly breakdown

**Example Output:**
```
📍 LOCATION / TRAVEL MAPPER
==================================================

Photos with GPS: 8,456 (67.9%)
Without GPS: 3,997
Unique locations: 45
Possible trips: 12

Top Locations:
    1. (41.5369, -90.5776)
       1,234 photos ⭐12 🧳 | 5.2 GB
       📅 2020-01-15 → 2025-03-03
       👥 Alex, Sam
```

**Usage in Conversation:**

**User:** "Where have I taken the most photos?"  
**AI:** *Runs location_mapper.py, reports top locations*

**User:** "Show me my trips from 2025"  
**AI:** *Runs location_mapper.py with --year 2025, highlights identified trips*

---

[← All commands](../../SKILL.md#commands)
