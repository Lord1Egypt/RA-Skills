# Memory Template — CMO

Create `~/Clawic/data/cmo/memory.md` with this structure:

```markdown
# CMO Memory

## Status
status: ongoing
last: YYYY-MM-DD

## Company
<!-- What they sell, to whom, stage, team size -->

## Funnel Numbers (as stated by the user)
<!-- ACV, win rate, lead→opp rate, sales cycle, current lead volume, CAC, payback -->
<!-- Date each figure; funnel rates go stale in a quarter -->

## Positioning In Use
<!-- The current statement or headline, and whether it has been tested -->

## Channels
<!-- Working, tested and killed (with the reason), never tried -->

## Constraints
<!-- Budget ceiling, vetoed channels, compliance regime, approval chain -->

## Open Threads
<!-- Live tests with their kill lines and read dates -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning |
|-------|---------|
| `ongoing` | Still learning their business and numbers |
| `complete` | Funnel, positioning, and constraints are known |

Declared preferences (motion, stage, currency, margin, approval ceiling) belong in `config.yaml`, not here. This file holds what was observed and reported; `config.yaml` holds what the user chose.
