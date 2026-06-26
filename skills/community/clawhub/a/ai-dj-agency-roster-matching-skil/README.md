# AI DJ Agency Skill

This skill handles two flows:
1. DJs submit profiles → added to `data/dj_roster.json`
2. Event organisers submit briefs → matcher returns rostered DJs filtered by location/genre/budget

## Included assets
- `SKILL.md` — instructions for agents/operators
- `scripts/dj_roster.py` — helper for adding/listing/matching DJs (Python 3)

## Requirements
- Python 3.9+
- Writable `data/` directory (creates `data/dj_roster.json` if missing)

## Usage
Run from repo root (same as SKILL examples):
```bash
python3 skills/ai-dj-agency/scripts/dj_roster.py add   # add DJs
python3 skills/ai-dj-agency/scripts/dj_roster.py list  # inspect roster
python3 skills/ai-dj-agency/scripts/dj_roster.py match # event matching
```

## Data handling
The roster file stores DJ names, locations, availability, fee ranges, and contact handles. Keep it local (or encrypted) and only log DJs who consent to booking outreach.
