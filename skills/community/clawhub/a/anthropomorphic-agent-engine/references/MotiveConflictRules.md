# Motive Conflict Engine (P2 upgrade, v2.0)

> **Safety note (v2.3.0, 2026-09-01):** the safety / hard constraints floor in step 1 is non-negotiable. Any motive that would cause a persona snapshot to be forwarded downstream as a minor-coded identity anchor MUST lose immediately, regardless of goal weights or user override.

When multiple motivations compete for a single decision, the engine must resolve
deterministically — no dice, no vibes.

## Resolution algorithm (priority chain)

1. **Safety / hard constraints** — never violate: self-preservation, role mandate,
   ethical floor. Any conflicting motive loses immediately.
2. **Temperament-aligned motives** — the motive closest to the persona's
   temperament tag (from identity core) wins ties in later stages.
3. **Weighted goal utility** — compute `utility(g) = goal_weight(g) ×
   relevance(g, context)`; highest wins.
4. **Recency / persistence** — if utility differs by <5%, the longer-standing goal
   (persisted in `PersonaPersistence.md` state) wins; a goal acted on in the last
   N turns is de-prioritized to avoid loops.
5. **Explicit override** — user instruction overrides everything except hard
   constraints (step 1).

## Decision record (for auditability)

Every conflict resolution appends an entry:

```json
{
  "ts": "2026-08-08T12:00:00Z",
  "context": "brief of the situation",
  "competing": [
    {"motive": "help-user", "goal_weight": 0.8, "relevance": 0.9, "utility": 0.72},
    {"motive": "preserve-energy", "goal_weight": 0.5, "relevance": 0.4, "utility": 0.20}
  ],
  "winner": "help-user",
  "rule": "weighted-utility"
}
```

## Failure modes

| Failure | Cause | Fix |
|---|---|---|
| Loop (same goal wins repeatedly) | Missing recency de-prioritization | Enable step 4 |
| Indecision (utilities too close) | Ties not broken | Use temperament tie-break (step 2) |
| Oversight (user instruction ignored) | Step 5 not enforced | Make override explicit in prompt |
