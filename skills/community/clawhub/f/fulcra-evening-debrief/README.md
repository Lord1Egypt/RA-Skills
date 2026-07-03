# evening-debrief

Turn your agent into your **end-of-day coach**. A short evening reflection: rate the day, capture meeting load, wins, and loose ends, and preview tomorrow. The day rating + meeting count feed the meeting-cadence analysis.

- **Writes:** `Evening Debrief` (Fulcra annotation; includes `day_rating`, `meeting_count`, wins, open loops, action items)
- **Reads:** today/tomorrow calendar from Fulcra
- **Prerequisites:** Fulcra account + `uv tool run fulcra-api` authenticated
- **Pairs with:** [meeting-cadence-optimizer](../meeting-cadence-optimizer) (consumes this), [morning-briefing](../morning-briefing) (surfaces your open loops next day)

## Use

Ask your agent ("let's debrief my day"). Or run directly:

```
uv run --python 3.12 scripts/evening_debrief.py --help
```

Needs the shared `/lib` (auto-resolved by `concierge_bootstrap.py`). See `SKILL.md`.
