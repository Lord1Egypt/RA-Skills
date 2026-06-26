# ClawFlow Installation Guide

Step-by-step setup for the ClawFlow free skill.

---

## Prerequisites

- OpenClaw installed and running
- Basic familiarity with terminal/command line

---

## Step 1: Install the Skill

### Option A: Via ClawHub (Recommended)

```bash
clawhub install clawflow
```

### Option B: Manual Installation

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/drdata/clawflow.git
```

---

## Step 2: Copy Configuration Templates

```bash
# Navigate to workspace root
cd ~/.openclaw/workspace

# Copy templates (only if files don't exist)
cp skills/clawflow/templates/USER.md USER.md
cp skills/clawflow/templates/IDENTITY.md IDENTITY.md
cp skills/clawflow/templates/HEARTBEAT.md HEARTBEAT.md
```

**⚠️ Warning:** If you already have these files, DON'T overwrite them! Edit manually instead.

---

## Step 3: Configure USER.md

Edit `~/.openclaw/workspace/USER.md`:

```markdown
# USER.md - User Profile

- Name: [Your Name]              # e.g., "Koen"
- Language: [Your Language]      # e.g., "English", "Dutch"
- Timezone: [Your Timezone]      # e.g., "America/New_York", "Europe/Amsterdam"
```

**Language support:**
- **Primary:** English, Dutch (Nederlands) — full coverage for greetings
  and success messages.
- **Best-effort:** any other language (German, Spanish, French, Italian,
  Portuguese, …) — the LLM translates at runtime from the `Language:`
  field in `USER.md`. Quality varies; internal section names stay in
  English for compatibility with ClawFlow Complete if you upgrade later.

---

## Step 4: Configure IDENTITY.md

Edit `~/.openclaw/workspace/IDENTITY.md`:

```markdown
# IDENTITY.md - Agent Identity

- Name: [Agent Name]     # e.g., "Claw", "Assistant", "Jarvis"
- Creature: [Emoji]      # e.g., 🤖, 🦝, 🐙, 🦊, 🦉
```

**Popular emoji choices:**
- 🤖 Robot (default)
- 🦝 Raccoon (curious, handy)
- 🐙 Octopus (multitasker)
- 🦊 Fox (clever)
- 🦉 Owl (wise)

---

## Step 5: Configure HEARTBEAT.md

Edit `~/.openclaw/workspace/HEARTBEAT.md`:

```markdown
# HEARTBEAT.md

## Daily Intention

> "Your personal mantra or intention"

## Focus

Your current priorities:
- Project A: [description]
- Project B: [description]
- Learning goal: [description]
```

**Example:**
```markdown
## Daily Intention

> "Ship fast, learn faster."

## Focus

- Launch ClawFlow by March 13
- Help 100 people get organized
- Build in public on Twitter
```

---

## Step 6: (Optional) Install Integrations

### Todoist Integration

**Why:** See your tasks in morning brief and daily summary.

**How:**
```bash
# Install Todoist CLI
pip install todoist-cli

# Login
todoist login
```

**Test:**
```bash
todoist today
```

If you see your tasks, it works!

### Google Calendar Integration

**Why:** See your meetings in morning brief and daily summary.

**How:**
Install the `gog` OpenClaw skill (Google Workspace CLI).

See: [gog skill documentation](#)

**Test:**
```bash
gog calendar events primary --from 2026-03-06T00:00:00 --to 2026-03-06T23:59:59
```

If you see your events, it works!

---

## Step 7: Test the Skill

Open OpenClaw and say:

```
Give me my morning brief
```

You should see:
- Your daily intention & focus
- Today's calendar events (if gog configured)
- Today's tasks (if todoist configured)
- Personalized greeting with your name and emoji

**Expected output:**
```
🤖 Good morning, [Your Name]!

📅 [Today's Date]

🙏 Daily Intention
[Your intention from HEARTBEAT.md]

🎯 Focus
[Your focus from HEARTBEAT.md]

📅 Agenda:
[Your calendar events, or "No events" if not configured]

✅ Tasks:
[Your Todoist tasks, or "No tasks" if not configured]

🚀 Have a great day!
```

---

## Step 8: Test Daily Summary

At the end of your day, say:

```
Create my daily summary
```

The skill will:
1. Ask if you want to add details
2. Wait for your input (or say "skip")
3. Create a summary file at `~/.openclaw/workspace/memory/YYYY-MM-DD.md`

---

## Troubleshooting

### Morning brief shows "No calendar events" but I have meetings

**Check gog:**
```bash
gog calendar events primary --from <TODAY>T00:00:00 --to <TODAY>T23:59:59
```

If this fails, install the gog skill.

### Morning brief shows "No tasks" but I have Todoist tasks

**Check todoist CLI:**
```bash
todoist today
```

If this fails:
```bash
pip install todoist-cli
todoist login
```

### Output is in wrong language

**Check USER.md:**
```markdown
- Language: English  # Change to your language
```

Then ask for morning brief again.

### Agent uses wrong emoji

**Check IDENTITY.md:**
```markdown
- Creature: 🤖  # Change to your emoji
```

### Skill doesn't activate

**Check if skill is loaded:**
In OpenClaw, the skill should automatically activate when you say keywords like "morning brief" or "daily summary".

If not working, check:
1. Skill is in `~/.openclaw/workspace/skills/clawflow/`
2. SKILL.md file exists and is readable
3. Restart OpenClaw

---

## Next Steps

### Daily Routine

**Morning:**
1. Start your day
2. Say: *"Give me my morning brief"*
3. Review agenda and tasks
4. Start work

**Evening:**
1. End your day
2. Say: *"Create my daily summary"*
3. Add notes if desired
4. Review summary in `memory/<date>.md`

## Support

- **Questions:** GitHub Issues
- **Feature requests:** GitHub Discussions
- **Email:** koen@drdata.science
- **Discord:** OpenClaw Community

---

**Enjoy your new productivity assistant!** 🚀
