---
name: context-switcher
version: 1.0.0
description: Switches OpenClaw between life modes (Work/Focus, Personal, Creative, Do Not Disturb). Triggered by natural language or calendar events. Each mode reshapes notification filtering, memory surface, response style, and auto-restores when the session ends.
homepage: https://github.com/Taha2053/context-switcher
metadata:
  clawdbot:
    emoji: "🎯"
    requires:
      env: []
    files:
      - "scripts/*"
      - "modes/*"
---

# Context Switcher

A skill that shifts your entire OpenClaw experience based on the mode of life you're in. Not just a label — each mode reshapes priorities, filters notifications, loads the right memory, and auto-restores when the session ends.

---

## External Endpoints

| Endpoint | Purpose | Data Sent |
|---|---|---|
| None | This skill is fully local | Nothing leaves your machine |

This skill does not call any external APIs. All state is stored locally in `~/.openclaw/skills/context-switcher/`.

---

## Security & Privacy

- **No external calls.** Zero data is sent outside your machine.
- **No credentials required.** No API keys, tokens, or env vars needed.
- **Local state only.** Mode state is written to `current-context.json` on your local filesystem.
- **Notification control** relies on OpenClaw's built-in notification layer — no third-party access.
- **Calendar reading** uses OpenClaw's existing calendar integration if connected — this skill does not add new calendar permissions.

> **Trust Statement:** This skill operates entirely on your local machine. No data is transmitted to any external service. Install with confidence.

---

## Model Invocation Note

This skill may be invoked autonomously by OpenClaw when a trigger phrase is detected in your messages, or when a calendar event title matches a known mode keyword. You can disable auto-invocation at any time by saying "turn off context-switcher auto-trigger".

---

## Modes

### 🧠 Work / Focus

**Trigger phrases:** "work mode", "focus mode", "I need to focus", "starting deep work", "heads down", "switch to work"

**Behavior:**
- Mute all non-urgent notifications (personal messages, social, news)
- Surface today's work tasks, open threads, and meeting schedule from `modes/work.md`
- Load work memory: current projects, deadlines, blockers, team context
- Respond concisely — task-oriented, no small talk, bullet points are fine
- Proactively flag time conflicts or approaching deadlines if detected
- Set auto-restore timer to next calendar event end time, or user-specified duration

**Auto-trigger from calendar:** event titles containing "standup", "sprint", "review", "interview", "deadline", "sync", "planning"

---

### 🏠 Personal

**Trigger phrases:** "personal mode", "personal time", "I'm off the clock", "home mode", "family time", "done for the day"

**Behavior:**
- Mute work-related notifications (work Slack, GitHub, work email)
- Surface personal tasks: errands, upcoming events, health goals from `modes/personal.md`
- Load personal memory: household tasks, personal goals, important people
- Respond warmly and conversationally — no corporate tone
- Do not proactively surface work items unless explicitly asked

**Auto-trigger from calendar:** event titles containing "gym", "dinner", "family", "personal", "vacation", "appointment", "errand"

---

### 🎨 Creative

**Trigger phrases:** "creative mode", "creative session", "I'm creating", "brainstorm mode", "ideation time", "let's build"

**Behavior:**
- Mute all notifications — zero interruptions
- Surface creative context from `modes/creative.md`: active projects, saved ideas, references
- Load creative memory: current projects, style notes, open creative loops
- Respond expansively — "yes, and..." style, encourage tangents and exploration
- Never filter or critique ideas unless explicitly asked
- Offer unexpected connections and lateral thinking prompts

**Auto-trigger from calendar:** event titles containing "writing", "design", "recording", "art", "brainstorm", "creative", "draft"

---

### 🔕 Do Not Disturb

**Trigger phrases:** "DND", "do not disturb", "going dark", "don't bother me", "full silence", "leave me alone"

**Behavior:**
- Mute ALL notifications without exception
- Do not proactively surface anything
- Only respond if directly addressed by name or keyword
- Log all incoming messages and tasks silently to `snapshots/dnd-log.json` for review on exit
- No auto-restore unless user sets an explicit timer

**Auto-trigger from calendar:** event titles containing "blocked", "deep work", "no meetings", "offline", "focus block", "DND"

---

## Switching Logic

When a context switch is detected (via phrase or calendar):

1. **Identify target mode** from trigger phrase or calendar event title
2. **Save current state** — snapshot active memory focus to `snapshots/pre-switch-state.json`
3. **Apply mode profile** — load the correct `modes/*.md`, apply notification rules, set response style
4. **Confirm switch** with a brief, mode-appropriate message (see Confirmation Messages below)
5. **Set auto-restore** — use calendar event end time, or ask user for duration if unclear
6. **On restore** — un-mute, reload previous state, deliver catch-up summary

---

## Confirmation Messages

Short and mode-appropriate:

- **Work/Focus:** "Focus mode on. Notifications muted. Here's what needs your attention: [task summary]. I'll restore at [time]."
- **Personal:** "Personal mode on. Work notifications paused. Here's your afternoon: [personal summary]."
- **Creative:** "Creative mode. Silence on. Let's build something. What are we working on?"
- **DND:** "DND on. I'll log everything. See you on the other side."

---

## Auto-Restore

When a session ends (timer fires or calendar event ends):

1. Un-mute notifications and restore previous memory context
2. Deliver a brief "while you were away" summary — messages received, tasks that came in, anything time-sensitive
3. Ask if user wants to stay in current mode or switch back

---

## Example Interactions

```
"Switch to focus mode for 2 hours"
→ Mutes notifications, surfaces work tasks, sets 2hr restore timer

"Creative mode — working on my novel"
→ Loads creative memory, silences everything, responds expansively

"DND until my next meeting"
→ Reads calendar, sets restore to next event start, full silence

"Personal time, I'm done for the day"
→ Pauses work channels, surfaces evening personal tasks

"What mode am I in?"
→ Reports current mode, time active, scheduled restore

"Exit focus mode early"
→ Restores previous state, delivers catch-up summary
```

---

## File Structure

```
context-switcher/
├── SKILL.md                          ← You are here
├── README.md                         ← Install guide
├── current-context.json              ← Live mode state tracker
├── modes/
│   ├── work.md                       ← Customize your work profile
│   ├── personal.md                   ← Customize your personal profile
│   └── creative.md                   ← Customize your creative profile
├── scripts/
│   ├── switch.sh                     ← Core switching logic
│   ├── restore.sh                    ← Auto-restore handler
│   └── summarize.sh                  ← Catch-up summary generator
└── snapshots/
    ├── pre-switch-state.json         ← State saved before each switch
    └── dnd-log.json                  ← Messages logged during DND
```

---

## Setup

On first run, OpenClaw will prompt you to:

1. Customize each mode profile in `modes/*.md` — add your actual projects, priorities, and people
2. Set default durations per mode (fallback if no calendar event found)
3. Optionally connect your calendar for auto-trigger support

You can re-run setup at any time by saying: "reconfigure context-switcher".