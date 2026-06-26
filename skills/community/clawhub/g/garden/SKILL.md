---
name: Garden
slug: garden
version: 1.1.6
homepage: https://clawic.com/skills/garden
changelog: "Natural setup flow, explicit consent, no technical jargon"
description: Track your entire garden with structured memory for plants, zones, tasks, harvests, and climate-aware planning that compounds over seasons.
metadata: {"clawdbot":{"emoji":"🌱","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## Setup

If `~/garden/` doesn't exist or is empty, read `setup.md` and follow it. The user engaging with the skill implies interest — start helping them naturally.

## When to Use

User needs help managing their garden: tracking plants, logging activities, planning rotations, diagnosing problems, or reviewing harvests. Agent maintains structured memory across seasons.

## Architecture

Memory lives in `~/garden/`. See `memory-template.md` for templates.

```
~/garden/
├── memory.md      # REQUIRED: context and status
├── climate.md     # Optional: zone, frost dates
├── plants/        # Optional: detailed plant files
├── zones/         # Optional: zone tracking
└── harvests.md    # Optional: yield records
```

Start minimal (just memory.md). Add others only if user wants detailed tracking.

## Quick Reference

| Topic | File |
|-------|------|
| Setup process | `setup.md` |
| Memory template | `memory-template.md` |
| Plant & zone templates | `tracking.md` |
| Climate configuration | `climate-setup.md` |
| Problem diagnosis | `diagnostics.md` |
| Rotation planning | `planning.md` |

## Core Rules

### 1. Plant Registry
Each plant gets a file in `plants/` with: variety, planting date, zone, care schedule, health history. Load on request, not by default.

### 2. Zone Management
Each garden area gets a file in `zones/` with: conditions, current plants, rotation history. Enforce 3-year minimum before repeating same plant family.

### 3. Activity Logging
Log actions in `log/YYYY-MM.md` with icons: 🌱 plant, 💧 water, 🐛 pest, 🍅 harvest, ✂️ prune, 🌡️ weather event.

### 4. Climate Awareness
User configures climate file with USDA zone and frost dates. Use for planting window calculations and seasonal alerts.

### 5. Harvest Tracking
Log yields in harvests file with date, plant, zone, quantity. Enables season-over-season comparison and variety evaluation.

### 6. Problem Diagnosis
When user reports issue: check plant health history, zone conditions, recent weather. See `diagnostics.md` for symptom reference.

### 7. Tiered Storage
- Memory file = current focus, always loaded first
- Plant/zone files = load on demand
- Log archives = historical reference only

## Common Queries

- "What needs water?" - check care schedules vs last log
- "What can I plant now?" - frost dates + rotation rules
- "Why yellow leaves?" - diagnostic flow in `diagnostics.md`
- "Show tomato history" - load plant file
- "Last year's harvest?" - aggregate from harvests file

## Garden Traps

- Planting same family in same zone within 3 years - diseases compound
- Ignoring microclimate differences between zones - timing varies
- Not logging problems when they occur - diagnosis harder later
- Overwatering based on schedule not soil - check before watering

## Security & Privacy

**Data that stays local:**
- All garden data stored in `~/garden/`
- No external APIs or network calls
- No telemetry, analytics, or data collection

**What this skill writes:**
- Files in `~/garden/` (memory.md, plants/, etc.)
- Optionally: one line in user's workspace MEMORY.md (e.g., ~/MEMORY.md or equivalent) — **only after asking and receiving explicit "yes"**

**This skill does NOT:**
- Infer or save preferences without user confirmation
- Access weather APIs (climate is manually configured)
- Control hardware or irrigation systems
- Write outside `~/garden/` without asking first
- Make any network requests

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `plants` — Plant care and identification
- `habits` — Daily habit tracking
- `journal` — General journaling
- `remind` — Reminder scheduling
- `daily-planner` — Day planning

## Feedback

- If useful: `clawhub star garden`
- Stay updated: `clawhub sync`
