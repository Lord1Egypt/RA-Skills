---
name: crypto-exit-rule-drafter
description: A rule-drafting skill that helps users define exit conditions in advance for their crypto positions. Use when the user wants to set pre-defined exit rules. Prompt-only.
---

# crypto-exit-rule-drafter

A rule-drafting skill that helps users define exit conditions in advance for their crypto positions.

## Workflow

1. Ask about the current or planned position: asset, size, entry price, and thesis.
2. Ask what would make this investment wrong: price drop, fundamental change, or time horizon.
3. Draft two exit rules: a stop-loss level (downside exit) and a thesis-review level (fundamental exit).
4. Make the rules concrete and written, not vague intentions.
5. Set a review trigger and a consequence for when the rule is hit.

## Output Format

- Position summary
- Downside exit rule (price or percentage level)
- Fundamental exit rule (what must change)
- Review trigger and date
- Written commitment statement

## Quality Bar

- Rules are specific enough to actually trigger, not vague aspirational targets.
- Separates emotional stopping from rule-based stopping.
- Does not set stop-losses so tight that normal volatility triggers them.

## Edge Cases

- If the user has no clear thesis for the position, help them articulate one before drafting rules.
- If the position is long-term and the user has high conviction, focus more on fundamental exit than price stops.

## Compatibility

- Prompt-only, no exchange or portfolio integration.
- Works from user-provided position details.
