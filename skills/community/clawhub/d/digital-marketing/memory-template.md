# Memory Template — Digital Marketing

Create `~/digital-marketing/memory.md` only if the user wants continuity across sessions.

```markdown
# Digital Marketing Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending

## Context
- Company or product:
- Audience:
- Offer:
- Stage:
- Channels in play:
- Main metric:
- Constraints:

## Notes
- Winning hooks or claims:
- Losing angles:
- Active campaigns:
- Open experiments:
- Review boundaries:

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning context | Gather only what improves decisions |
| `complete` | Enough context exists | Work normally without re-asking basics |
| `paused` | User does not want more setup | Stop pushing for more detail |
| `never_ask` | User opted out of continuity | Work statelessly |

## Optional Support Files

If the user wants deeper continuity, create:

- `~/digital-marketing/campaigns.md` — current campaigns and asset bundles
- `~/digital-marketing/experiments.md` — hypotheses, thresholds, outcomes
- `~/digital-marketing/signals.md` — recurring metrics, anomalies, reusable lessons

## Key Principles

- Keep the memory short enough to scan fast
- Store decisions, not whole conversations
- Prefer context that changes execution quality: audience, message, channel mix, proof, constraints
- Update `last` whenever the local workspace changes
