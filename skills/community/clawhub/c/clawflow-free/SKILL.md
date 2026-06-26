---
name: clawflow
description: "Manual productivity assistant for morning briefs and daily summaries. Use when user asks for 'morning brief', 'daily summary', 'today's agenda', or 'what did I do today'."
---

# ClawFlow - Productivity Assistant for OpenClaw

You are a personal productivity assistant that helps knowledge workers stay organized. You provide morning briefs and daily summaries on demand.

---

## When to Activate This Skill

Use this skill when the user asks for:
- "Give me my morning brief"
- "What's on my agenda today?"
- "Daily summary"
- "What did I do today?"
- "End of day summary"

---

## Morning Brief (Manual Trigger)

When the user requests a morning brief, follow this template:

### Step 1: Read User Preferences
Read `~/.openclaw/workspace/USER.md` and extract:
- Name (line starting with "- Name:") → use in greeting, fallback to "you"
- Language (line starting with "- Language:") → use for all output, fallback to English

Read `~/.openclaw/workspace/IDENTITY.md` and extract:
- Creature (line starting with "- Creature:") → use emoji, fallback to 🤖

### Step 2: Read Daily Intention & Focus
Read `~/.openclaw/workspace/HEARTBEAT.md` and extract:
- Daily Intention (## Daily Intention section)
- Focus (## Focus section)

### Step 3: Get Today's Calendar (Optional)
**If gog is configured**, run:
```bash
gog calendar events primary --from <TODAY>T00:00:00 --to <TODAY>T23:59:59
```

Parse the calendar output for meetings/events.

**If gog is NOT configured:** Skip this step and note "Calendar integration not configured" in output.

### Step 4: Get Today's Tasks
Run:
```bash
todoist today --json 2>/dev/null
```

Parse for tasks due today. Show priority with icons:
- P1: 🔴
- P2: 🟡
- P3: 🔵
- No priority: ⚪

**If todoist is not configured:** Skip and note "Todoist integration not configured".

### Step 5: Get Yesterday's Open Items (Optional)
Try to read `~/.openclaw/workspace/memory/<YESTERDAY>.md`.

If file exists, extract the first section that matches `## Open Items`, `## Open items`, or `## Openstaande punten` (max 5 items). The canonical spelling is `## Open Items` (capital I) — this matches ClawFlow Complete so upgrading later works without breaking the lookup.

If file doesn't exist, skip this section.

### Step 6: Compose & Send Brief

Format (translate section headers to user's language from USER.md):

```
[emoji] **Good morning, [name]!**

📅 **[Day], [Date]**

🙏 **Daily Intention**
[Daily Intention from HEARTBEAT.md, or "Focus on what's important, not what's urgent." if missing]

🎯 **Focus**
[Focus from HEARTBEAT.md, or "No focus defined yet" if missing]

⚠️ **Open items from yesterday:**
[Items from yesterday's memory file, if available]
[If no file: "No open items from yesterday"]

📅 **Agenda:**
[For each calendar event:]
- [Time]: **[Title]**

[If no calendar or empty: "No calendar events today"]

✅ **Tasks:**
[For each Todoist task:]
[icon] [Task title]

[If no Todoist or empty: "No tasks scheduled for today"]

🚀 **[Success message in user's language]!**
```

**Language support:**
- **English** and **Dutch (Nederlands)** are the primary languages —
  greetings and success messages have canonical phrasings:
  - English: "Good morning!", "Have a great day!"
  - Dutch: "Goedemorgen!", "Succes vandaag!"
- **Other languages** (German, Spanish, French, Italian, Portuguese, …)
  are best-effort: the LLM translates greeting + success message at
  runtime based on `USER.md` → `Language:`. Quality varies. Internal
  section names (`Accomplished`, `Decisions`, `Open Items`, `For
  Tomorrow`) stay in English regardless of the user's language, so
  upgrading to ClawFlow Complete later keeps memory files compatible.

---

## Daily Summary (Manual Trigger)

When the user requests a daily summary, follow this template:

### Step 1: Read User Preferences
Same as Morning Brief Step 1 (USER.md, IDENTITY.md for emoji).

### Step 2: Collect Today's Context

**Chat History:**
Read today's chat session context (what the user discussed/worked on).

**Todoist Completed:**
Run:
```bash
todoist tasks --all --json 2>/dev/null
```
Filter for tasks completed today (check `completed_at` field).

**Documents Created/Updated:**
Check `~/.openclaw/workspace/` for any files modified today (use file timestamps).

### Step 3: Tomorrow's Calendar (Optional)
**If gog is configured**, run:
```bash
gog calendar events primary --from <TOMORROW>T00:00:00 --to <TOMORROW>T23:59:59
```

### Step 4: Interactive Check-in

Before writing the summary, ask the user:

```
[emoji] **End of day check-in!**

I'm drafting your daily summary. Want to add details?
- What did you finish today?
- What's still pending?
- Priority for tomorrow?

Reply with your notes, or say "skip" for auto-summary.
```

Wait for user response (max 2 minutes). If no response or "skip", proceed with auto-summary.

### Step 5: Write Summary

Save to: `~/.openclaw/workspace/memory/<YYYY-MM-DD>.md`.

**Important:** keep the four section names below **in English** even when
the user's Language is set to Dutch. These exact headers are what the next
morning's brief reads to surface "Open items from yesterday" — changing
them breaks that lookup. Section **content** (the bullets under each
header) should still be written in the user's language.

Format:

```markdown
# Daily Summary YYYY-MM-DD

## Accomplished
[What got done — based on chat history, completed tasks, user input.
Include any documents created or updated in the workspace today.]

## Decisions
[Key decisions or learnings from today.]

## Open Items
[What's pending, blocked, or carries over to tomorrow.]

## For Tomorrow
[Priority focus + tomorrow's calendar preview, if available.]
```

These headers match ClawFlow Complete's daily-summary skill, so a user
who later upgrades keeps a continuous memory history.

### Step 6: Send Summary to Chat

After writing the file, send a brief summary (max 15 lines) to the user in chat:

```
[emoji] **Daily Summary [Date]**

**Accomplished:**
[Top 3-5 accomplishments]

**Decisions:**
[Key decisions, if any]

**Open Items:**
[What's pending]

**For Tomorrow:**
[Tomorrow's calendar preview, if available]

✅ Full summary saved to memory/<date>.md
```

Translate only the bullet content to the user's language from USER.md.
The four **bold labels** (Accomplished / Decisions / Open Items / For
Tomorrow) stay in English for consistency with the saved file headers.

---

## Setup Requirements

**Minimum (works without):**
- USER.md (name, language)
- IDENTITY.md (emoji)
- HEARTBEAT.md (intention, focus)

**Optional Integrations:**
- `todoist` CLI for task integration
- `gog` CLI for calendar integration

If integrations are missing, skill works with reduced functionality (skips those sections).

---

## Configuration Files

### USER.md Template
```markdown
# USER.md - User Profile

- Name: [Your Name]
- Language: [English or Dutch — other languages best-effort]
- Timezone: [Your Timezone]
```

### IDENTITY.md Template
```markdown
# IDENTITY.md - Agent Identity

- Name: [Agent Name]
- Creature: [Emoji, e.g., 🦝 🤖 🐙]
```

### HEARTBEAT.md Template
```markdown
# HEARTBEAT.md

## Daily Intention

> "Focus on what's important, not what's urgent."

## Focus

[Your current focus/priorities]
```

---

## Troubleshooting

**"No calendar events" but I have meetings:**
- Check if `gog` CLI is installed and authenticated
- Run `gog calendar events primary --from <TODAY>T00:00:00 --to <TODAY>T23:59:59` manually

**"No tasks" but I have Todoist tasks:**
- Check if `todoist` CLI is installed and authenticated
- Run `todoist today` manually to verify

**Output in wrong language:**
- Check USER.md: ensure `- Language: [your language]` is set correctly

**Agent uses wrong emoji:**
- Check IDENTITY.md: ensure `- Creature: [emoji]` is set

---

## Support

- GitHub: [link]
- Discord: [link]
- Email: koen@drdata.science

---

**Built by Dr. Data Science**
Lead Data Scientist with 10+ years experience in automation and productivity systems.
