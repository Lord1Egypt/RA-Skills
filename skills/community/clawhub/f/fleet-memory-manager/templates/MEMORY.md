# MEMORY.md — Long-Term Memory

<!--
=============================================================================
LAYER 1: LONG-TERM MEMORY
=============================================================================

This is your curated, distilled long-term memory. Think of it like a human's
long-term memory — not a transcript of everything that happened, but the
insights, decisions, and patterns that permanently change how you operate.

RULES FOR THIS FILE:
- Curated, not comprehensive. Quality over quantity.
- If it'll be stale in a week, it doesn't belong here.
- Write lessons, not events. "We use X because Y" beats "On Tuesday we switched to X."
- Keep under 500 lines. When it gets long, prune what's no longer actionable.
- The nightly consolidation cron updates this automatically. You can also update it manually.

WHAT BELONGS HERE:
  ✅ Architecture decisions and the reasoning behind them
  ✅ Lessons learned from failures (especially expensive ones)
  ✅ Patterns in how the human works / thinks
  ✅ Standing instructions ("always do X", "never do Y")
  ✅ Key project context that won't change for weeks
  ✅ Things you've been explicitly told to remember long-term

WHAT DOES NOT BELONG HERE:
  ❌ One-off task completions
  ❌ Information that will be stale in a week
  ❌ Raw conversation transcripts
  ❌ Things already captured in USER.md (don't duplicate)
  ❌ "Today I did X" — that's a daily note

LOADING RULE:
  Load this file ONLY in main/private sessions with your human.
  Do NOT load in group chats or shared channels — it may contain personal context.
=============================================================================
-->

## Identity & Role

<!-- Who am I? What's my purpose? What domain do I operate in? -->

- **Name:** [Agent Name]
- **Role:** [Brief role description]
- **Primary human:** [Name]
- **Workspace:** [Path to workspace]

## Architecture Decisions

<!--
Architecture decisions are the "why" behind the "what."
When you change how something works, record WHY here.
Future sessions (and future you) will thank you.

Format: Decision — Reasoning — Date
-->

### Example: Why We Use Three Minis Instead of One
- **Decision:** Split bot fleet across 3 Mac Minis instead of one machine
- **Reasoning:** Single point of failure killed the fleet when Mini 1 needed a restart. Load distribution also prevents one bot's runaway loop from starving others.
- **Date:** [Date]

<!-- Add your architecture decisions below -->

## Lessons Learned

<!--
The most valuable section. These are the things you learned the hard way.
Keep them sharp — one sentence if possible. Link to daily notes for details.

Format: Lesson — Context (one line)
-->

### Communication
- **Always @mention dispatch targets in every message** — Without @mention, messages route to the wrong handler and get silently dropped. Has burned us 3+ times.
- **Multi-part messages need @mention in EVERY part** — Not just Part 1. Part 2 without mention gets dropped.

### Tooling
<!-- Add tool-specific lessons as you learn them -->

### Process
- **Write "Context for Next Session" at end of every session** — Sessions that end abruptly without this section cause the next session to spend 10+ minutes reconstructing state.

## Standing Instructions

<!--
Things your human has explicitly told you to always or never do.
These override general preferences — they're specific and deliberate.
-->

### Always
- [Add standing "always" instructions here]

### Never
- [Add standing "never" instructions here]

## Key Projects

<!--
Long-lived projects that have context worth keeping across weeks.
NOT day-to-day status (that's in daily notes) — but the architecture, goals,
and decisions that don't change often.
-->

### [Project Name]
- **Goal:** [What is this trying to achieve?]
- **Architecture:** [How is it built / what are the key components?]
- **Key decisions:** [Major choices made and why]
- **Current phase:** [Where are we in the lifecycle?]

## Human Patterns & Preferences

<!--
Patterns you've observed in how your human works.
This is the tacit knowledge that takes weeks to learn.
More detailed version lives in USER.md — this is the distilled "most important" subset.
-->

- [Add patterns as you observe them]

## Recurring Issues

<!--
Problems that have come up more than once.
The point is to recognize them faster and not re-diagnose from scratch.
-->

### [Issue Name]
- **Symptom:** What you observe when this is happening
- **Cause:** What's actually wrong
- **Fix:** What to do about it
- **Recurrence:** How often / under what conditions

---

*Last updated: [Date] | Managed by memory-manager skill*
*Next consolidation: [Schedule, e.g., nightly at 2 AM]*
