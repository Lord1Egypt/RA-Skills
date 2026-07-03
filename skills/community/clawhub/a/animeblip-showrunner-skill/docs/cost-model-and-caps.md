# Cost model and keeping spend bounded

## What costs money

`generate_motion` (scene video) is the **expensive** op. Scene images cost less;
screenplay/text is cheap. The whole approach exists to avoid re-paying for motion:

- **Never full-regen.** Every fix names the single failing scene so the agent
  regenerates only that shot (via `withReference` targets) and re-assembles the cut.
- **Review before you pay.** Drive the pipeline step-by-step (screenplay only → review via
  `get_project_state.py` → then images/video) when the brief is risky or expensive, so you
  approve the screenplay **before** any image/video spend.

## Spend ceiling (rule of thumb)

| Guard | Value | Meaning |
|---|---|---|
| retries per shot | ~**2** | Targeted regen attempts for any single scene/op |
| fix-sends per episode | ~**6** | Total fix-sends per episode |

These are not hard-enforced by any loop — YOU keep track while polling. When you hit them,
**STOP and surface to the human** instead of sending another fix: a stuck episode needs a
human, not more spend. Do not keep retrying to "just finish" an episode — that's how a retry
spiral burns credits.

## Targeted, never full-regen

- A failing shot is identified by its exact `op:scene` (from the structured `failures[]`),
  so you re-send only that shot — never re-run shots that already succeeded.
- Bound total fix-sends per episode regardless of which shots failed.

Combined with surfacing to the human at the ceiling, the worst case for a stuck episode
stays bounded and visible.
