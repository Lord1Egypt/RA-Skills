# Persona Persistence (P0 upgrade, v2.0)

Continuous-state persona simulation is only useful if the state survives across
sessions. This module defines the persistence contract — schema, lifecycle, and
integration points — so a persona behaves identically after a restart.

## State schema (persisted per persona)

```json
{
  "persona_id": "nanwang-v1.2",
  "schema_version": 1,
  "created_at": "2026-08-08T00:00:00Z",
  "updated_at": "2026-08-08T12:00:00Z",
  "core": {
    "identity_anchors": ["adult woman (18+)", "mole below left eye", "white daisy in hair"],
    "temperament_tag": "gentle-quiet-timid",
    "temperature": 0.0
  },
  "state": {
    "cognitive": { "working_memory": [], "beliefs": {}, "focus": "" },
    "emotional": { "current": "calm", "valence": 0.2, "arousal": -0.1, "decay_rate": 0.05 },
    "motivational": { "active_goals": [], "goal_weights": {} },
    "social": { "relationship_scores": {}, "social_context": "" }
  },
  "episodes": []
}
```

## Lifecycle rules

1. **Load** on session start: read the persona state file; hydrate cognitive /
   emotional / motivational / social blocks.
2. **Update** on every interaction: append to working memory (bounded, FIFO),
   shift emotional state (valence/arousal), decay inactive goals.
3. **Persist** at session end (or every N turns): write the full state atomically
   (write temp file → rename).
4. **Version** the schema: bump `schema_version` on breaking changes; migrate on
   load.

## Determinism guarantee

- `temperature = 0.0` for core identity decisions.
- Emotional decay is a pure function of time and `decay_rate` — reproducible.
- Randomness (if any) must be seeded from a stored seed so replays match.

## Storage contract

| Env | Storage |
|---|---|
| Local / self-hosted | `~/.openclaw/personas/<persona_id>.json` (or workspace-scoped) |
| Server | Any KV / file store; keep atomic writes |

## Integration

- Pair with `references/EmotionBehaviorMap.md` to project state → expression.
- Pair with `references/MotiveConflictRules.md` for multi-goal decisions.
