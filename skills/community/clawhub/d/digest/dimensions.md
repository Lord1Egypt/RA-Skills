# Digest Dimensions

Reference for categorizing user preferences. Load when updating `preferences.md`. Each dimension lists its cold-start default; anything in `preferences.md` overrides it.

## Content

What they want:
- `industries` — Sectors to cover (tech, finance, health...)
- `competitors` — Specific companies. Track actions (launches, pricing, hires, filings), not mere mentions.
- `topics` — Cross-industry themes (AI, climate, markets...)
- `people` — Thought leaders, executives, creators. Track statements and moves, not coverage about them.
- `regions` — Geographic focus

What to exclude:
- `noise` — Topics that waste their time. Binary filter (SKILL.md rule 3).
- `saturated` — Covered by sources they already read. If they read a major daily, skip its front page; add second-order analysis instead of repeating it.

## Sources

- `trusted` — Sources they explicitly trust; their items skip the corroboration hold.
- `blocked` — Never use, even as corroboration.
- `weight` — Default when unset: primary (announcements, filings, papers) > original reporting > aggregators > social commentary.
- `recency` — Canonical windows when unset: breaking news ≤48h; analysis and opinion ≤7 days; evergreen pieces ≤30 days and only when they hit a [confirmed] or [locked] topic. User-set recency overrides all three.

## Format

- `channel` — Telegram group, DM, email, Slack. Default: wherever the user first asked for a digest.
- `medium` — Text, PDF, audio, video summary. Default: text.
- `structure` — Bullets, prose, headers, cards. Default: bullets.
- `length` — Headlines only, summaries, full analysis. Default budget: SKILL.md rule 5.
- `visuals` — Images/charts or text-only. Default: text-only until asked.
- `tone` — Formal, casual, direct. Default: mirror the register of the user's own messages.

## Timing

- `schedule` — Morning, evening, both, custom times. Default: on-demand only; propose a slot after the second requested digest, schedule nothing until confirmed.
- `frequency` — Daily, weekday-only, weekly.
- `timezone` — User's timezone; derive from context, confirm before first scheduled send.
- `context-aware` — Different digests for work vs personal time (→ Context Profiles in `preferences.md`).

## Prioritization (Weighting)

- `hierarchy` — What leads. Default: highest interest-match first, not newest (SKILL.md rule 1).
- `highlight` — What earns emphasis. Max 3 Highlights (SKILL.md rule 5).
- `bury` — What compresses into Worth Noting. Bury, don't delete.
- `urgent-signal` — Conditions that justify breaking schedule. Must reach [confirmed] before any interrupt (SKILL.md → Deliver).

## Depth

- `default-depth` — Default: 1-line summary + why-it-matters line per item.
- `per-topic` — Overrides; follow-up questions on a topic are the raise-depth signal.
- `expandable` — Default: end deep items with "more on this?" instead of including everything.

## Personalization Levels

```
[none]      → Generic digest, defaults above
[pattern]   → 2+ signals observed, not confirmed
[confirmed] → User explicitly approved when asked
[locked]    → Confirmed + 3 deliveries without contradiction
```

Promotion/demotion mechanics and signal counting: `preferences.md`.
