# 🌅 Daily Reflection

**Turn each day of agent work into durable memory, better behavior, and a useful morning briefing.**

Daily Reflection is an end-of-day OpenClaw routine. It reviews what happened, extracts real learnings, updates solution memory, detects recurring patterns, and prepares a concise briefing for the next session.

## What It Does

- Summarizes completed, started, blocked, and failed work
- Extracts up to 5 concrete learnings with “tomorrow better” actions
- Writes solved bugs into `solution_memory/*.json`
- Detects recurring patterns across the last 7 days
- Updates `memory/patterns.md` when behavior should change
- Creates `memory/morning-briefing.md` and archives daily briefings
- Keeps chat quiet: routine results go to memory; critical blockers can be summarized briefly

## Recommended Use

Recommended cadence: once per day in an isolated OpenClaw cron job, after explicit setup by the user/operator.

```text
Schedule: 59 23 * * *
Session: isolated
Delivery: none
Prompt: Read the daily-reflection skill and execute all steps for today.
```

## Output Files

```text
memory/YYYY-MM-DD.md
memory/morning-briefing.md
memory/briefings/YYYY-MM-DD.md
memory/patterns.md
memory/session-quality-log.md
solution_memory/[id].json
```

## Good Reflection Criteria

A good reflection is not a diary dump. It should answer:

- What actually changed today?
- What did we learn that prevents future mistakes?
- Which bugs now have reusable solution memory?
- Which pattern repeated enough to deserve a rule?
- What should tomorrow’s agent know before speaking?

## Not For

- Real-time progress updates
- Motivational journaling
- Replacing project source-of-truth notes
- Storing credentials, auth tokens, private chat dumps, raw transcripts, or production data

---

*by brasco05 · nightly memory consolidation for OpenClaw agents*
