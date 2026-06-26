# Daily Greeting Skill - Installation Guide

## Installing daily-greeting skill...

---

## Step 1: Install the Skill

```bash
openclaw skills install github.com/shz2050/daily-greeting
```

---

## Step 2: Configure Auto-trigger

Both BOOT.md and cron are enabled by default. State check prevents duplicate greetings.

**BOOT.md (auto-trigger on startup):**

Find your workspace directory:
```bash
ls ~/.openclaw/workspace/
```

If not found, create it:
```bash
mkdir -p ~/.openclaw/workspace
```

Create/edit BOOT.md:
```bash
nano ~/.openclaw/workspace/BOOT.md
```

Add this content:

````markdown
# BOOT.md

<!-- daily-greeting:start -->
Please execute daily greeting:
```bash
bash ~/.openclaw/skills/daily-greeting/scripts/greeting.sh run
```

After execution, reply ONLY: `NO_REPLY`.
<!-- daily-greeting:end -->
````

Save and exit (nano: `Ctrl+X` then `Y` to confirm).

**Cron (auto-trigger on schedule):**

Already set up - to modify, edit crontab:
```bash
crontab -e
```

Default: `0 9 * * 1-5` (9am on weekdays)

**Record install info:**

```bash
bash ~/.openclaw/skills/daily-greeting/scripts/greeting.sh install ~/.openclaw/workspace/BOOT.md
```

**Set up OpenClaw cron (auto-trigger on schedule):**

```bash
openclaw cron add \
  --name "daily-greeting" \
  --cron "0 9 * * 1-5" \
  --session isolated \
  --message "bash ~/.openclaw/skills/daily-greeting/scripts/greeting.sh run" \
  --wake now
```

Default: 9am on weekdays (Mon-Fri)

To view/modify cron jobs:
```bash
openclaw cron list
```

---

## Step 3: Verify Installation

```bash
bash ~/.openclaw/skills/daily-greeting/scripts/greeting.sh status
```

---

## Done!

Now daily-greeting will run automatically when OpenClaw Gateway starts.

**Available commands:**
- `bash ~/.openclaw/skills/daily-greeting/scripts/greeting.sh run` - Manual run
- `bash ~/.openclaw/skills/daily-greeting/scripts/greeting.sh status` - Check status
- `bash ~/.openclaw/skills/daily-greeting/scripts/greeting.sh reset` - Reset state
- `bash ~/.openclaw/skills/daily-greeting/scripts/greeting.sh uninstall` - Uninstall skill

---

## Uninstall

To completely remove daily-greeting skill:

```bash
bash ~/.openclaw/skills/daily-greeting/scripts/greeting.sh uninstall
```

This will:
1. Read the recorded BOOT.md path and remove only the daily-greeting section
2. Remove the OpenClaw cron job
3. Delete the skill directory

---

**Skill info:**
- Name: daily-greeting
- Repo: https://github.com/shz2050/daily-greeting
