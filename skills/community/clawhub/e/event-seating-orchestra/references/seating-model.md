# Event Seating Orchestra — Reference

## 1. Why seating charts are hard

n guests into k tables is an assignment problem; the social constraints make it combinatorial. 100 guests × 12 tables has more configurations than atoms in the observable universe. Hand-built charts fail in predictable ways: they cluster the hosts' favorite people, dump leftovers together, and violate exactly one keep-apart pair discovered at the venue.

The right tool is **constraint-aware optimization**: hard constraints (keep-apart, party integrity, capacity) enforced, soft preferences (mixing, balance) optimized.

## 2. Constraint classes

| Class | Examples | Handling |
|---|---|---|
| Hard | capacity, keep-apart pairs, must-together parties | violation = huge penalty + final audit |
| Semi-hard | mobility/aisle seats, kids with adults | flagged in report; heavy penalty |
| Soft | talker balance, mixing, prefer-near, language | weighted score terms |

## 3. Scoring model in detail

```
score = 1_000_000 × keep-apart pairs at same table
      + 100_000 × seats over capacity
      + 40 × (split parties × party size)
      + 25 × Σ max(0, talkers_per_table − 1)²
      + 60 × (number of kid tables − 1)        # kids belong together
      + 120 × kid tables with no adult
      + 6 × know-well pairs seated together     # we want NEW connections
      − 30 × prefer-near pairs seated together  # reward wishes
```

Talker balance uses a quadratic term: 1 talker per table is free, 2 costs 25, 3 costs 100 — matching the real-world phenomenon that conversation dies at 2+ dominators.

The `know_well` term is the mixing engine: guests who already know each other provide each other no new value at a wedding; the optimizer gently splits them (unless party/must-together overrides).

## 4. Simulated annealing parameters

- Blocks = parties (never split a couple mid-move).
- Moves: relocate block (50%) or swap two blocks' tables (50%).
- Temperature: linear cooling 8.0 → 0.2 over 30k iterations; accept worse moves with p = exp(Δs/T) early, nearly never late.
- Deterministic via `--seed` — same input, same chart, which makes "change one guest, re-run, diff" sane.

## 5. Running your own event

1. Export the guest list (name, party/group, flags: talker/quiet/kid/needs-aisle/language).
2. Add edges: keep_apart, prefer_near, know_well (optional but powers mixing).
3. Set tables to the venue's capacities, e.g. `"tables": [10, 10, 8, 8]`.
4. Run; read the audit lines. Then iterate seeds if you dislike an aesthetic outcome.
5. Print rosters per table (caterers want name lists), keep one master copy with reasons.

## 6. Special cases

- **Sweetheart/head table:** model the couple + wedding party as pre-assigned (add a "fixed table" by giving them a dedicated table in `tables` and a must-together party, then exclude them from the run list).
- **Late RSVPs:** re-run with same seed and edited list; diff rosters.
- **Families of 5+ at round tables of 10:** one family + one couple is often the happiest table; the party-block model produces exactly this.
- **Single guests:** leave `party` empty; the optimizer seats them where mixing scores best — never "at the back with the other singles" unless you build that by hand.
- **Language tables:** add a `language` flag and a soft term grouping non-shared-language guests near a translator (extend the script if needed).

## 7. Human review pass (non-negotiable)

The optimizer doesn't know that Table 3 is next to the speakers, or that Uncle X shouldn't face the door. After the run, do a 10-minute venue-map review with a second host: physical realities (drafts, exits, service lanes) are not in the graph.

## 8. Sources

- Classic assignment/graph partitioning formulation; simulated annealing (Kirkpatrick et al.).
- Wedding-planner practice literature for constraint classes (keep-apart, party integrity, talker balance) and caterer output formats.
