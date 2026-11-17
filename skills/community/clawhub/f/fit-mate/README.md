# Fitness Coach

An AI fitness coach skill for personalized training plans, fitness-focused meal guidance, recovery-aware logging, wearable analysis, and weekly progress reviews.

## What It Covers

- personalized workout plans for home or gym
- meal planning with macro awareness and city-aware food suggestions
- workout, body-weight, hydration, food, and sleep logging
- smartwatch and wearable data analysis
- weekly progress reports and plan adjustments

## Install

If your OpenClaw environment supports registry install:

```bash
openclaw skills install fitness-coach
```

For local/manual install:

```bash
cp -R ./fitness-coach ~/.openclaw/skills/fitness-coach
```

## Commands

| Command | Description |
|---------|-------------|
| `/fitness-coach` | Setup or show current status |
| `/fitness-coach setup` | Create or refresh the user profile |
| `/fitness-coach plan` | Generate or revise the active workout plan |
| `/fitness-coach diet` | Generate a full-day meal plan |
| `/fitness-coach meal <type>` | Generate one quick meal idea |
| `/fitness-coach eat` | Log food intake and estimate macros |
| `/fitness-coach water` | Log hydration and show daily progress |
| `/fitness-coach sleep` | Log sleep duration and quality |
| `/fitness-coach log` | Log workout completion and/or body weight |
| `/fitness-coach watch` | Analyze smartwatch or wearable data |
| `/fitness-coach checkin` | Run a daily coaching check-in |
| `/fitness-coach progress` | Review trends across recent windows |
| `/fitness-coach adjust` | Reassess calories, macros, or training |
| `/fitness-coach report` | Generate a weekly summary report |

## Runtime Data

Runtime files live in `data/` under the installed skill directory.

```text
data/
├── user_profile.json
├── current_plan.json
├── current_status.json
├── cache/
│   ├── progress_summary.json
│   └── personal_bests.json
├── logs/
│   ├── food/
│   │   └── YYYY-MM.json
│   ├── hydration/
│   │   └── YYYY-MM.json
│   ├── sleep/
│   │   └── YYYY-MM.json
│   ├── workout/
│   │   └── YYYY-MM.json
│   ├── weight/
│   │   └── YYYY-MM.json
│   ├── watch/
│   │   └── YYYY-MM.json
│   └── adjustments/
│       └── YYYY-MM.json
└── weekly_reports/
    └── week_YYYY-MM-DD.md
```

This layout keeps daily commands fast by reading hot files first and only opening narrow monthly log slices when needed.

It also keeps token and latency growth close to flat for normal use:

- daily commands read `current_status.json` and cache files before any raw logs
- raw logs are partitioned by month, so most reads touch one file, not the whole history
- only the most recent `12` full months are in the default active raw-log window; older months are cold archive unless the user explicitly asks for deep history
- cache files are refreshed after writes and then reused until genuinely stale
- `cache/progress_summary.json` is intended for section-level refreshes, not full rebuilds after every write
- weekly reports are archived outputs and should not be reread for normal coaching turns

The authoritative file shapes live in `references/data-schema.md`.

## Project Structure

```text
fitness-coach/
├── SKILL.md
├── references/
│   ├── data-schema.md
│   ├── nutrition-regions.md
│   ├── persona.md
│   ├── report-template.md
│   ├── training.md
│   └── watch-analysis.md
└── data/
    └── .gitkeep
```
