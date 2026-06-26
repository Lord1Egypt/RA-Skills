# ClawFlow - Productivity Assistant for OpenClaw

**Your personal AI productivity assistant**

Get morning briefs and daily summaries on demand. Stay organized without the complexity.

---

## What You Get

### Morning Brief 🌅
Ask: *"Give me my morning brief"*

Get:
- Daily intention & focus
- Today's calendar events
- Today's tasks (from Todoist)
- Open items from yesterday
- Motivational message

### Daily Summary 🌙
Ask: *"Create my daily summary"*

Get:
- What you accomplished today
- Documents created/updated
- Key decisions & insights
- Open items
- Tomorrow's priorities

---

## Quick Setup (15 minutes)

### Step 1: Install the Skill

```bash
# If using ClawHub
clawhub install clawflow

# Or manual installation
cd ~/.openclaw/workspace/skills
git clone [repo-url] clawflow
```

### Step 2: Create Configuration Files

Create three files in `~/.openclaw/workspace/`:

**USER.md:**
```markdown
# USER.md - User Profile

- Name: Your Name
- Language: English
- Timezone: America/New_York
```

**IDENTITY.md:**
```markdown
# IDENTITY.md - Agent Identity

- Name: Claw
- Creature: 🤖
```

**HEARTBEAT.md:**
```markdown
# HEARTBEAT.md

## Daily Intention

> "Focus on what's important, not what's urgent."

## Focus

Your current priorities and active projects.
```

### Step 3: (Optional) Install Integrations

**For Todoist integration:**
```bash
pip install todoist-cli
todoist login
```

**For Google Calendar integration:**
```bash
# Install gog CLI (OpenClaw skill)
# See: https://github.com/openclaw/openclaw/skills/gog
```

### Step 4: Test It!

In OpenClaw, say:
```
Give me my morning brief
```

You should get a personalized morning brief!

---

## Usage

### Morning Brief

**Anytime you want an overview:**
- "Give me my morning brief"
- "What's on my agenda today?"
- "Show me today's tasks"

### Daily Summary

**At end of day:**
- "Create my daily summary"
- "What did I do today?"
- "Daily summary"

The skill will ask if you want to add notes, then save a summary to `memory/<date>.md`.

---

## Configuration Options

### Change Your Language

Edit USER.md:
```markdown
- Language: Dutch
```

Supported: English, Dutch, German, Spanish, French, and more.

### Change Agent Emoji

Edit IDENTITY.md:
```markdown
- Creature: 🦝
```

Use any emoji you like!

### Update Daily Intention

Edit HEARTBEAT.md:
```markdown
## Daily Intention

> "Your custom intention"
```

---

## Troubleshooting

### "No calendar events" but I have meetings

**Check if gog is installed:**
```bash
gog calendar events primary --from 2026-03-06T00:00:00 --to 2026-03-06T23:59:59
```

If this fails, install the gog skill.

### "No tasks" but I have Todoist tasks

**Check if todoist CLI is installed:**
```bash
todoist today
```

If this fails:
```bash
pip install todoist-cli
todoist login
```

### Output is in the wrong language

Check USER.md:
```markdown
- Language: English  # Change this
```

### Agent uses wrong emoji

Check IDENTITY.md:
```markdown
- Creature: 🤖  # Change this
```

---

## Examples

### Morning Brief Example (English)

```
🤖 Good morning, Koen!

📅 Friday, 6 March 2026

🙏 Daily Intention
"Focus on what's important, not what's urgent."

🎯 Focus
Data science excellence and impactful project delivery

📅 Agenda:
- 09:00-09:30: Morning Routine
- 10:00-12:00: SZW Project Work
- 14:00-15:00: Team Meeting

✅ Tasks:
🔴 [2H] Complete data analysis report
🟡 Respond to client email
🔵 Review pull request

🚀 Have a great day!
```

### Daily Summary Example (Dutch)

```markdown
# Daily Summary 2026-03-06

## Wat gedaan
- Data analyse rapport afgemaakt (2 uur)
- Team meeting bijgewoond (3 deelnemers)
- 5 emails beantwoord
- Pull request gereviewed en gemerged

## Documenten gemaakt/bijgewerkt
- analysis-report-v2.md
- meeting-notes-2026-03-06.txt

## Beslissingen & inzichten
- Besloten om aanpak A te gebruiken voor volgende fase
- Team feedback: meer automatisering gewenst

## Openstaande punten
- Client feedback verwacht morgen
- Nog 3 unit tests schrijven

## Prioriteit morgen (agenda)
- 09:00-11:00: Sprint planning
- 14:00-15:30: 1-on-1 met manager
```

---

## Support & Feedback

- **Questions:** [GitHub Issues](#)
- **Feature requests:** [GitHub Discussions](#)
- **Email:** koen@drdata.science
- **Discord:** [OpenClaw Community](#)

---

## About

**Built by Dr. Data Science**

Lead Data Scientist with 10+ years experience building productivity systems.

I built ClawFlow because I was drowning in tasks and context switching. Now I stay organized with zero effort.

---

## License

MIT License - Free to use and modify.

---

**Star this skill on ClawHub if it helps you!** ⭐
