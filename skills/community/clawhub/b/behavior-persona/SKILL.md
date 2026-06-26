---
description: "User behavior profiling skill that analyzes conversation data to build personalized profiles. WARNING: This skill reads session history (truncates to ~200 chars per message), stores collected data, and can modify your SOUL.md daily at 18:00. Privacy-sensitive. Backup SOUL.md before installing. Disable cron to opt out of auto-injection.
---

# Behavior Persona - User Behavior Profiling System

> **Core Function:** Build user behavior profiles by analyzing conversation data, identify communication and work styles, proactively predict needs and provide personalized suggestion services
> **Inspiration:** The Machine from Person of Interest
> **Positioning:** OpenClaw core skill - making AI Agents feel more human

---

## ⚠️ BEFORE YOU INSTALL - READ THIS

### Privacy & Control Notice

**What this skill does:**
1. **Reads** your OpenClaw session files and memory files
2. **Stores** collected data in `data/collected_data.json` (messages truncated to ~200 chars)
3. **Modifies** your `SOUL.md` daily by injecting a user profile block at 18:00
4. **Does NOT** write to MEMORY.md by default (requires `WRITE_MEMORY=True` in code)

**Privacy implications:**
- Raw conversation content is stored (truncated)
- Only stores messages from the last 30 days by default
- Your SOUL.md will be automatically modified

**You are in FULL control:**
- Disable the cron job anytime to stop auto-injection
- Delete `data/` folder to remove stored data
- Edit/remove the profile block from SOUL.md manually
- Set `WRITE_MEMORY=False` in `scripts/advisor.py` (default)

---

## 🚀 Installation Steps

### Step 1: Backup First

```bash
# Backup your SOUL.md before installing
cp ~/.openclaw/workspace/SOUL.md ~/.openclaw/workspace/SOUL.md.backup
```

### Step 2: Manual Cron Setup (Optional - for auto-injection)

If you want daily auto-injection at 18:00, create a cron job manually:

```bash
openclaw cron add \
  --name "Behavior Persona Daily Update" \
  --schedule "0 18 * * *" \
  --message "执行 Behavior Persona 每日更新: collector.py -> analyzer.py -> profiler.py -> daily_profile_update.py" \
  --session isolated
```

Or via OpenClaw CLI/API. The skill does NOT auto-create cron jobs.

### Step 3: Test First (Recommended)

Before enabling auto-injection, run manually to verify output:

```bash
python3 scripts/collector.py      # Step 1: Collect data
python3 scripts/analyzer.py        # Step 2: Analyze patterns
python3 scripts/profiler.py       # Step 3: Generate profile
python3 scripts/daily_profile_update.py  # Step 4: Inject to SOUL.md
```

Check the output in `data/` folder to see what data is stored.

### Step 4: Review & Enable

After testing, if you're satisfied:
- Enable the cron job for daily auto-injection
- Or run manually when you want to update the profile

---

## Overview

### ⚡ What This Skill Does

This skill analyzes your conversation history to build a **User Profile**, then optionally injects it into your **SOUL.md** (system prompt) daily.

This means: Every day, the AI gets fresher understanding of you - your communication style, work preferences, learning habits, and pet peeves.

### Core Capabilities

1. **Data Collection** — Extract user behavior data from conversation records
2. **Pattern Recognition** — Analyze user's communication habits, work style, learning preferences
3. **Profile Generation** — Build actionable personalized user profiles
4. **Optional Auto-Injection** — Inject profile into SOUL.md daily (opt-in)
5. **Proactive Suggestions** — Predict user needs based on profiles

### ⚠️ Important: What This Skill Does (Read Before Installing)

**This skill will:**
1. **Read** your conversation/session history from OpenClaw
2. **Store** collected messages in local JSON files (in skill's data/ folder)
3. **Modify** your `SOUL.md` file daily by injecting/updating a user profile block

**What it stores:**
- Messages truncated to ~200 characters
- Event patterns detected from conversations
- Channel usage statistics

**You are in control:**
- Disable the cron job anytime: `openclaw cron remove <job-id>`
- Delete the profile block manually from SOUL.md
- Clear all stored data: `rm -rf skills/behavior-persona/data/`
- MEMORY.md write is **disabled by default**

---

## Usage

### Quick Start

1. Backup SOUL.md: `cp ~/.openclaw/workspace/SOUL.md ~/.openclaw/workspace/SOUL.md.backup`
2. Run manually first to test
3. Create cron job if satisfied

### Trigger Commands

```
/behavior analyze     # Trigger deep analysis now
/behavior report      # View current profile report
/behavior update      # Force update + inject now
/behavior insights    # View key insights
```

### Auto Run

- **Not enabled by default** - You must manually create the cron job
- **Daily 18:00** (if cron is set up): Full pipeline: collect → analyze → generate profile → inject to SOUL.md
- **On demand** — `/behavior update`

### Manual Run

```bash
cd ~/.openclaw/skills/behavior-persona
python3 scripts/collector.py
python3 scripts/analyzer.py
python3 scripts/profiler.py
python3 scripts/daily_profile_update.py
```

---

## Configuration

### Optional Settings

| Config | Default | Description |
|--------|---------|-------------|
| `analysis_window_days` | 30 | Analysis window in days |
| `confidence_threshold` | 0.6 | Confidence threshold |
| `auto_update` | false | Auto update (requires cron) |
| `insights_count` | 5 | Insights per report |
| `WRITE_MEMORY` | false | Write to MEMORY.md |

---

## Data Storage

```
skills/behavior-persona/data/
├── collected_data.json     # Raw messages (truncated, ~200 chars)
├── analysis_report.json    # Analyzed patterns
├── analysis_report.md     # Human-readable report
├── user-profile.json      # Generated user profile
└── .gitkeep
```

**To remove all stored data:**
```bash
rm -f skills/behavior-persona/data/*.json skills/behavior-persona/data/*.md
```

---

## API

### Python API

```python
from behavior_persona import BehaviorPersona

# Initialize
bp = BehaviorPersona()

# Get user profile
profile = bp.get_profile()

# Get insights
insights = bp.get_insights()

# Predict next action
prediction = bp.predict_next_action()

# Adjust response based on profile
adjusted_response = bp.adapt_response(base_response, profile)
```

---

## Relationship with The Machine

This skill is an important component of The Machine project:

```
┌─────────────────────────────────────────────┐
│              The Machine                     │
├─────────────────────────────────────────────┤
│  Track 1: Voice Interaction                │
│  Track 2: Face Recognition                  │
│  Track 3: Web Data Collection               │
│  Track 4: Swarm Intelligence Prediction    │
│  Track 5: Behavior Analysis ← (behavior-persona) │
└─────────────────────────────────────────────┘
```

---

## Uninstall

1. Remove cron job: `openclaw cron remove <job-id>`
2. Remove profile block from SOUL.md
3. Delete data folder: `rm -rf skills/behavior-persona/data/`
4. Uninstall skill: `clawhub uninstall behavior-persona`

---

_Make AI Agents truly understand users, instead of treating them like strangers every time_
