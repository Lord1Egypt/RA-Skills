# Brief Dimensions

Taxonomy for recording user preferences. Load when updating `~/Clawic/data/brief/preferences.md`.

Routing rule first: a preference the user **states outright** ("always one page", "no emoji") is declared, not learned — it goes straight to `config.yaml` (matching variable or preference area, SKILL.md Configuration) and skips the levels below. This file governs preferences **inferred from feedback** on delivered briefs.

## Signal → Dimension Mapping

How feedback phrases translate into preference lines:

| User says | Dimension | Record as |
|-----------|-----------|-----------|
| "Too long" / "just the highlights" | Depth | `default: summary (pattern)` |
| "Where are the numbers?" | Content/metrics | `metrics: always include (pattern)` |
| "I didn't need all that background" | Content/context | `context: minimal (pattern)` |
| "Send it before the meeting next time" | Timing | `trigger: pre-meeting (pattern)` |
| "Can you email this instead?" | Format/channel | `channel: email (pattern)` |
| "Perfect" / "love this format" | — | Promote each preference used in that brief one level |
| Ambiguous reaction ("hm, ok") | — | Not a signal. Record nothing; ask if it recurs |

One preference per line. Record the observable behavior, never an inference about personality ("prefers metrics up front", not "is a numbers person").

## Personalization Levels

```
[none]      → Default brief format
[pattern]   → 2+ consistent signals observed, not confirmed
[confirmed] → User explicitly approved
[locked]    → Confirmed, then reinforced across multiple briefs
```

Promotion and demotion:
- none → pattern: 2+ consistent signals. A single remark is noise; the same remark twice is a preference.
- pattern → confirmed: explicit user approval only ("yes, always do that"). Never promote silently.
- confirmed → locked: the confirmed preference survives reinforcement across multiple briefs and brief types.
- Demotion: one contradicting signal drops a `pattern` back to none. A contradicted `confirmed`/`locked` → ask which the user wants; never silently flip a preference the user approved.

## Scope

What the brief covers:
- `type` — Executive, project, meeting, handoff, decision
- `audience` — Self, boss, team, external stakeholder
- `purpose` — Inform, enable decision, prepare for meeting

## Content

What to include:
- `metrics` — Always include? Only if changed? Which ones?
- `context` — How much background
- `risks` — Highlight vs mention vs omit
- `history` — Include recent decisions/changes

What to exclude:
- `assumed` — Knowledge they already have
- `noise` — Details that don't affect the action

## Structure

How to organize:
- `order` — BLUF first? Chronological? By priority?
- `sections` — Which sections, in what order
- `hierarchy` — Flat list vs nested detail
- `emphasis` — What to bold/highlight

## Format

How to present:
- `channel` — Where to deliver (message, doc, email)
- `medium` — Text, PDF, slides, verbal
- `length` — One-pager, detailed, executive summary
- `visuals` — Status indicators, charts, tables
- `tone` — Formal, internal casual, direct (formal → strip emoji markers)

## Timing

When to deliver:
- `trigger` — Pre-meeting, start of week, on-demand
- `lead-time` — How far before the event
- `frequency` — One-time, recurring, as-needed

## Depth

How detailed:
- `default` — Summary, standard, comprehensive
- `per-type` — Different depth for different brief types
- `expandable` — Include "more detail available" sections
