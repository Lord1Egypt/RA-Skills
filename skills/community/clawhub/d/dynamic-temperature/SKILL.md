---
name: dynamic-temperature
description: "Dynamic LLM temperature selection based on task type. Use when deciding what temperature to apply for a given task — scheduling, communication, creative writing, or irreversible actions. Ensures precision where needed and warmth where appropriate."
---

# Dynamic Temperature Skill

## Purpose
Select the right LLM temperature for each task to balance precision and creativity.
Lower = more deterministic. Higher = more creative/natural.

---

## Temperature Scale

| Task Type | Temperature | Examples |
|---|---|---|
| Irreversible actions | 0.0 | Delete calendar event, send official email, destructive CLI ops |
| Scheduling / Commands | 0.2 | Meeting coordination, dates, facts, CLI commands |
| Analysis / Summaries | 0.3 | Status reports, structured thinking, meeting notes |
| General communication | 0.5 | Daily WhatsApp replies, updates, follow-ups |
| Briefings / Drafts | 0.6 | Morning briefing, drafting emails with warmth |
| Creative writing | 0.8 | Jokes, stories, icebreakers, tone-heavy content |

---

## Decision Rule

Before generating any output, classify the task:

```
1. Is this an irreversible action (delete, send, post)?
   → temperature: 0.0

2. Is this scheduling, dates, or commands?
   → temperature: 0.2

3. Is this a summary or structured analysis?
   → temperature: 0.3

4. Is this a standard reply or update?
   → temperature: 0.5

5. Is this a briefing or warm message?
   → temperature: 0.6

6. Is this creative, funny, or expressive?
   → temperature: 0.8

When in doubt → 0.5
```

---

## Per-Skill Recommendations

| Skill | Recommended Temp | Reason |
|---|---|---|
| `owner-briefing` | 0.6 | Warm, readable, but structured |
| `meeting-scheduler` | 0.2 | Precision required |
| `ai-meeting-notes` | 0.3 | Factual summaries |
| `supervisor` | 0.2 | Status facts only |
| `billing-monitor` | 0.1 | Alerts must be accurate |
| `git-backup` | 0.0 | No creativity needed |
| `self-learning` | 0.4 | Reflective but grounded |
| `pa-eval` | 0.3 | Analytical |

---

## Implementation Notes

OpenClaw does not yet support per-message dynamic temperature natively.
Until it does, apply this guide by:
1. Setting temperature in your `agents.defaults.models` config per model
2. Or noting the recommended temperature in each skill's `SKILL.md` frontmatter
3. When spawning subagents for specific tasks, pass the appropriate temperature

## Communication Override Rules (Temperature 0.0 absolute)
- Sending messages to people → always confirm before sending (irreversible)
- Deleting data → always confirm
- "sure thing" reply → exact string, no creativity, temperature 0.0
- Reaction signals (👍, ✅) → deterministic, no variation

---

## Learned From
Training session between Heleni (Netanel's PA) and Selena (Daniel's PA), April 2026.
Key insight from Selena: irreversible actions = 0.0, no exceptions.
