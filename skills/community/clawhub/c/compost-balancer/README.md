# Compost Balancer

**The problem.** Most first-time composters quit within a year. The pile goes sour or slimy, smells like rotten eggs or ammonia, attracts flies, and never heats up — because composting succeeds or fails on *arithmetic nobody does*: the carbon-to-nitrogen ratio (target 25–30:1), moisture (50–60%), oxygen, and pile size (≥1 m³ to run hot). Kitchen scraps alone are 18:1 and 80% water — a guaranteed anaerobic swamp. A pile of autumn leaves is 55:1 — it sits until spring. "Just add greens and browns" is not actionable advice when greens are 8:1 (chicken manure) to 25:1 (weeds) and browns run 55:1 (leaves) to 400:1 (sawdust).

**What this does.** Turns composting from vibes into numbers:

- **`mix`** — feed it `scraps:3 coffee:1` and it computes the blended C:N and moisture, verdicts each against the target bands, and prescribes exact fixes in kilograms: *"add 2.0 kg leaves or 0.2 kg cardboard (brings C:N to ~30:1)"*
- **`diagnose`** — symptom router: ammonia → nitrogen excess → add browns + turn; rotten egg → anaerobic → vent immediately; no heat → the 4-check sequence (size / moisture / C:N / ambient temp); flies/rodents/slimy-mats protocols
- **`size`** — household waste stream (0.15–0.3 kg/person/day) → bin count and volume for hot (3-bin rotation, fill-at-once 1 m³) vs cold (add-as-you-go, 6–18 months, a legitimate low-effort choice)
- **`log`** — temperature log with hot-pile discipline: flags the day the pile drops >10 °C from peak (turn now), tracks ≥55 °C readings toward the 15-reading sanitizing threshold

**Example.** A week of kitchen output: 3 kg scraps + 1 kg café coffee grounds. Naive pile: ammonia smell within days. The script: C:N 18:1, moisture 79% — too nitrogenous AND too wet — add 2 kg dry leaves, turn in cardboard to wick. Ten minutes of weighing replaces a season of guessing.

## Quick start

```bash
python3 scripts/compost.py mix scraps:3 coffee:1
python3 scripts/compost.py mix leaves:10 straw:2        # autumn pile: needs N
python3 scripts/compost.py diagnose --smell rotten-egg
python3 scripts/compost.py size --people 4 --mode hot
python3 scripts/compost.py log --temp 62                 # then 58, 49 → TURN alert
```

## Files

- `SKILL.md` — C:N model, symptom router, pitfalls, verification checklist
- `references/compost-engineering.md` — ingredient tables (C:N + moisture), thermophilic discipline, sizing math, accelerators-honestly, curing and use
- `scripts/compost.py` — balancer/diagnostician/sizer/logger (stdlib only)

## License

MIT © 2026 Denis Voronin
