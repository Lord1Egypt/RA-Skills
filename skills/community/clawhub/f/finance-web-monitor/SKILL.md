---
name: finance-web-monitor
description: "Monitor and summarize finance websites for fund-investing support. Use when user asks to fetch finance site text, track changes, or schedule periodic monitoring/briefings from a list of URLs (no login required)."
---

# Finance Web Monitor Skill

Use this skill to fetch text from finance sources and schedule periodic monitoring/briefings. No login flows.

## Core workflow

1) **Confirm scope**
   - Ask for URL list if not provided.
   - Ask for cadence/time window (e.g., daily 08:30, weekdays only).
   - Ask for output format (short brief vs. detailed) and risk preference.

2) **Fetch & extract**
   - Use `web_fetch` with `extractMode: "text"` and a reasonable `maxChars`.
   - If a site blocks raw fetch, report it and ask for an API/alternate source.

3) **Summarize**
   - Produce a concise market overview + key headlines + fund-related takeaways.
   - Emphasize risk controls for稳健偏好.

4) **Change monitoring**
   - Save a small rolling snapshot in workspace (e.g., `/home/claw/.openclaw/workspace/finance-monitor/state.json`).
   - On next run, compare new text with previous snapshot and report changes only.

5) **Scheduling**
   - Use `cron` to schedule daily briefings; include “reminder/briefing” wording in payload.
   - For one-off “check now”, run immediately without cron.

## Suggested source list

If the user wants a default list, read `references/sources.md` and confirm. Update it when the user adds/removes sources.
