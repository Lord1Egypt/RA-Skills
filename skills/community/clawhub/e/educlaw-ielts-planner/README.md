# 📚 EduClaw — Personal IELTS Study Secretary

> An [OpenClaw](https://openclaw.dev) skill that transforms your AI agent into a dedicated IELTS study planner with Google Calendar integration, automated material discovery, and progress tracking.

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**[🇻🇳 Đọc bằng Tiếng Việt](README_VI.md)**

---

## Overview

EduClaw is a comprehensive IELTS study management skill for OpenClaw. It automates the entire study planning lifecycle — from creating personalized roadmaps to scheduling sessions on Google Calendar with detailed, unique lesson plans for each session.

### Key Features

- **Bilingual Support** — Auto-detects user language (English/Vietnamese), responds consistently
- **4-Step Workflow** — Ask schedule → Research & Plan → Calendar → Documentation
- **Google Calendar Integration** — Creates detailed study events via `gcalcli` with unique descriptions per session
- **Smart Scheduling** — Respects user's preferred time slots, handles conflicts interactively
- **Dynamic Timezone** — Detects system timezone at runtime (never hardcoded)
- **Cron Automation** — Daily prep briefs, weekly reports, material updates via Discord
- **SQLite Progress Database** — Local `educlaw.db` with sessions, vocabulary, materials, and weekly summary tables — queryable, ACID-compliant, zero external dependencies
- **Discord Notifications** — Calendar conflict alerts, study reminders, progress reports
- **4-Month Roadmap** — Band 6.0 → 7.5+ structured in 4 phases (Foundation → Skill Building → Advanced → Exam Simulation)

---

## Requirements

| Dependency | Purpose |
|-----------|---------|
| [OpenClaw](https://openclaw.dev) | Agent platform (v2026.3+ recommended) |
| [gcalcli](https://github.com/insanum/gcalcli) | Google Calendar CLI (must be authenticated) |
| Google Calendar account | For scheduling study sessions |
| Discord bot (optional) | For notifications and cron delivery |

### Optional

- Web search enabled in OpenClaw — for material discovery
> **📖 First time?** See the **[Complete Setup Guide (EN)](SETUP.md)** | **[Hướng dẫn cài đặt (VI)](SETUP_VI.md)** for step-by-step instructions covering all tools, API keys, bot creation, and more.
---

## Installation

### From OpenClaw Skills Registry

```bash
openclaw skill install educlaw-ielts-planner
```

### Manual Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/moclaw/educlaw-ielts-planner.git
   ```

2. Copy to your OpenClaw skills directory:
   ```bash
   cp -r educlaw-ielts-planner ~/.openclaw/skills/educlaw-ielts-planner-1.0.0/
   ```

3. Verify installation:
   ```bash
   openclaw skill list
   ```

### Prerequisites Setup

1. **Install & authenticate gcalcli:**
   ```bash
   pip install gcalcli
   gcalcli list   # Follow OAuth flow to authenticate
   ```

2. **Enable web search** in your OpenClaw config (`openclaw.json`):
   ```json
   {
     "agents": {
       "defaults": {
         "webSearch": true
       }
     }
   }
   ```

---

## Usage

### Discord

```
@Jaclyn Plan my IELTS study for band 7.5 in 4 months
```

Or use the slash command:
```
/educlaw_ielts_planner
```

### Terminal (TUI)

```bash
openclaw tui
# Then type: "Plan my IELTS study for band 7.5"
```

### CLI (One-shot)

```bash
openclaw agent --message "Plan my IELTS study for band 7.5 in 4 months"
openclaw agent --message "Schedule IELTS study for next 2 weeks"
openclaw agent --message "Show my IELTS progress"
```

### Supported Languages

The agent detects your language automatically:

| Language | Example Trigger |
|----------|----------------|
| English | "Plan my IELTS study for band 7.5" |
| Vietnamese | "Lên kế hoạch học IELTS 7.5 trong 4 tháng" |

---

## Workflow

EduClaw follows a strict 4-step workflow:

### Step 0: Schedule Preferences
The agent asks your preferred study hours, available days, and blocked times. **Never auto-selects time slots.**

### Step 1: Research & Planning
- Reviews study history from previous sessions
- Searches for fresh, specific materials (books, YouTube, websites)
- Builds a 2-week rolling schedule with vocabulary, exercises, and goals
- Presents the plan and **waits for your approval** before proceeding

### Step 2: Google Calendar Events
- Checks free slots within your preferred time window
- Handles conflicts interactively (never auto-resolves)
- Creates events with **100% unique descriptions** — each session has distinct vocabulary, materials, lesson plans, and exercises
- Sets 15-minute reminder per session

### Step 3: Documentation
- Creates/updates `IELTS_STUDY_PLAN.md` with roadmap, vocabulary, resources, and progress tracker
- Initializes SQLite progress database (`workspace/tracker/educlaw.db`) with 4 tables

---

## 4-Month Roadmap (Band 6.0 → 7.5+)

| Phase | Weeks | Goal |
|-------|-------|------|
| **Phase 1: Foundation** | 1–4 | Master exam format, vocabulary & grammar base |
| **Phase 2: Skill Building** | 5–8 | Advance techniques, target band 6.5 |
| **Phase 3: Advanced** | 9–12 | Consistent band 7.0, real exam conditions |
| **Phase 4: Exam Simulation** | 13–16 | Stabilize 7.0–7.5, exam readiness |

---

## Cron Jobs (Automated Study Support)

EduClaw supports automated cron jobs delivered to Discord:

| Job | Schedule | Purpose |
|-----|----------|---------|
| `ielts-calendar-watcher` | Every 2 hours | Detect calendar conflicts with study sessions |
| `ielts-daily-prep` | 23:00 Sun–Fri | Prep brief for next day's session (vocab, materials, review) |
| `ielts-meeting-conflict-check` | 08:00 Mon–Sat | Morning conflict check for today's session |
| `ielts-weekly-report` | Sunday 10:00 | Progress summary, completion rates, adjustments |
| `ielts-weekly-material-update` | Saturday 14:00 | Fresh materials for next week's topics |

### Setup Example

```bash
openclaw cron add \
  --name "ielts-daily-prep" \
  --cron "0 18 * * 1-6" \
  --tz "$(timedatectl show --property=Timezone --value)" \
  --channel discord \
  --announce \
  --message "You are EduClaw. Check today's IELTS session, search fresh materials, deliver prep brief." \
  --model "google/gemini-2.5-flash"
```

---

## Progress Tracker (SQLite Database)

EduClaw uses a SQLite database at `workspace/tracker/educlaw.db` as the single source of truth for progress:

| Table | Tracks |
|-------|--------|
| **sessions** | Date, phase, skill, topic, event_id, status, score, duration, weak areas |
| **vocabulary** | Word, IPA, meaning, collocations, example, review count, mastery status |
| **materials** | Title, type, URL, skill, phase, status, rating |
| **weekly_summaries** | Sessions planned vs completed, vocab count, mock scores, adjustments |

> **Why SQLite?** Supports complex queries (aggregations, joins, filters), is ACID-compliant, and works via `sqlite3` CLI or Python's built-in `sqlite3` module. No external API needed. Cron jobs query the DB directly for real-time reports.

---

## Calendar Event Format

### Title
```
IELTS Phase X | Session Y - <Skill>: <Topic>
```

### Description (each event is 100% unique)

Every calendar event contains a detailed, structured lesson plan:

- **Goals** — Specific, measurable targets for the session
- **Lesson Plan** — Timed activities with exact material references (book/page/URL)
- **Vocabulary** — 10 unique words with IPA, collocations, and example sentences
- **Materials** — Exact book pages, URLs, YouTube links for this specific session
- **Exercises** — Numbered tasks with time limits and target scores
- **Previous Session Review** — Carry-forward items from last session
- **Self-Check** — Post-session checklist

---

## Guardrails

| Rule | Details |
|------|---------|
| ❌ Never delete untracked events | Only delete events with event_id in SQLite database, after user confirmation |
| ❌ Never auto-select time slots | Always asks first (Step 0) |
| ❌ Never auto-resolve conflicts | Shows options, waits for user choice |
| ❌ Never hardcode timezone | Detects from system at runtime |
| ❌ Never create >14 events at once | Batches by 2 weeks |
| ❌ Never show internal reasoning | Clean output only |
| ❌ Never place unverified URLs | Every link in calendar events must be fetched & content-verified before inclusion |
| ✅ Always detect user language | Responds consistently |
| ✅ Always ask schedule preferences | Before any scheduling |
| ✅ Always wait for approval | Before creating events |
| ✅ Always unique descriptions | No duplicate vocab/materials across sessions |

---

## File Structure

```
educlaw-ielts-planner/
├── README.md           # English documentation (this file)
├── README_VI.md        # Vietnamese documentation
├── SETUP.md            # Complete setup & installation guide (EN)
├── SETUP_VI.md         # Hướng dẫn cài đặt đầy đủ (VI)
├── SKILL.md            # OpenClaw skill prompt (core logic)
├── WORKFLOW.md          # Step-by-step execution guide
├── schema.sql          # SQLite database schema
├── _meta.json          # Skill metadata
├── LICENSE             # MIT License
├── CHANGELOG.md        # Version history
└── examples/
    └── sample-events.md # Example calendar events
```

---

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## Author

**moclaw** — [GitHub](https://github.com/moclaw)

Built with [OpenClaw](https://openclaw.dev) 🦞
