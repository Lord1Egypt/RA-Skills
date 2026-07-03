# morning-briefing

Turn your agent into your **morning show host**. A daily kickoff that pulls last night's sleep, today's calendar, weather, and any open loops from yesterday's debrief, then delivers it in your agent's voice — tone-calibrated to how you slept and how you said you feel.

- **Reads:** Fulcra sleep + calendar; `Morning Check-In` and `Evening Debrief` annotations
- **Writes:** nothing required (a briefing log is optional)
- **Prerequisites:** Fulcra account + `uv tool run fulcra-api` authenticated
- **Pairs with:** [subjective-checkin](../subjective-checkin), [evening-debrief](../evening-debrief), [relationship-crm](../relationship-crm) (optional meeting prep)

## Use

Ask your agent ("give me my morning briefing"). Or gather the raw context directly:

```
uv run --python 3.12 scripts/collect.py --help
```

Needs the shared `/lib` on the path (handled automatically by `concierge_bootstrap.py`). See `SKILL.md`.
