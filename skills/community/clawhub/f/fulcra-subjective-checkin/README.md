# subjective-checkin

Turn your agent into your **wellness journal**. A 2-minute morning conversation that captures how you actually feel — overall feeling, energy, social battery, physical notes, and an intention for the day — and saves it to Fulcra as a structured annotation the other skills can read.

- **Writes:** `Morning Check-In` (Fulcra annotation)
- **Reads:** optional sleep/context from Fulcra
- **Prerequisites:** Fulcra account + `uv tool run fulcra-api` authenticated
- **Pairs with:** [morning-briefing](../morning-briefing) (consumes this), [evening-debrief](../evening-debrief)

## Use

Ask your agent in Claude Code ("do my morning check-in") — the `SKILL.md` tells it how to run the conversation and save. Or run the script directly:

```
uv run --python 3.12 scripts/fulcra_checkin.py --help
```

Self-contained (no shared lib needed). See `SKILL.md` for the full flow and payload shape.
