# meeting-cadence-optimizer

Turn your agent into your **meeting diet coach**. Correlates how many meetings you have with how you rated those days, finds your "sweet spot," and reports a confidence level so it never invents a pattern from thin data.

- **Reads:** `Evening Debrief` annotations (`meeting_count` + `day_rating`)
- **Writes:** optional `Cadence Analysis` annotation
- **Confidence-gated:** insufficient (<7 days) / low (7–13) / medium (14–29) / high (30+) — it says so plainly
- **Prerequisites:** Fulcra account; some history from [evening-debrief](../evening-debrief)

## Use

Ask your agent ("am I overbooked? what's my meeting sweet spot?"). Or run directly:

```
uv run --python 3.12 scripts/cadence.py --help
```

Needs the shared `/lib` (auto-resolved by `concierge_bootstrap.py`). See `SKILL.md`.
