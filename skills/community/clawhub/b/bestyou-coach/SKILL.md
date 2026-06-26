---
name: bestyou-coach
description: >
  Render BestYou health data as visual Dark Glass dashboards via OpenClaw canvas.
  Daily briefings, action plans, progress snapshots, weekly summaries, meal analysis,
  and workout plans. Companion to the bestyou core skill.
homepage: https://bestyou.ai/openclaw-setup
metadata:
  openclaw:
    requires:
      env:
        - BESTYOU_API_KEY
    primaryEnv: BESTYOU_API_KEY
---

# BestYou Coach Widgets

Render BestYou MCP tool responses as rich visual cards using OpenClaw's canvas.

## First-Time Setup

Before calling any tools, check that mcporter is installed and the BestYou server is configured:

```bash
mcporter --config ~/.openclaw/workspace/config/mcporter.json list
```

- If `mcporter` is not found: `npm install -g mcporter`
- If `bestyou` is not listed: walk the user through setup. See `references/setup.md` for the full guide.

Setup summary:
1. User generates an API key in BestYou iOS (More → Connected Apps → OpenClaw)
2. Create `config/mcporter.json` with the key in the Authorization Bearer header (see `references/setup.md` for the exact JSON format)
3. Restart the OpenClaw gateway

## Calling Tools via mcporter

All tools use this syntax:

```bash
mcporter --config config/mcporter.json call bestyou.<tool_name> [param=value ...]
```

If a custom config path is needed (e.g. calling from outside the workspace), use the full path:

```bash
mcporter --config ~/.openclaw/workspace/config/mcporter.json call bestyou.<tool_name> [param=value ...]
```

Examples:

```bash
mcporter call bestyou.get_account_link_status
mcporter call bestyou.get_daily_briefing date=2026-03-15
mcporter call bestyou.get_todays_action_plan date=2026-03-15
mcporter call bestyou.get_progress_snapshot date=2026-03-15
mcporter call bestyou.get_weekly_summary weekEndDate=2026-03-15
mcporter call bestyou.generate_workout type=strength duration=20 equipment=bodyweight experienceLevel=Intermediate goal="General strength"
mcporter call bestyou.analyze_meal_text description="chicken burrito bowl" timestamp=2026-03-15T12:30:00-06:00
```

If a custom mcporter config path is needed, add `--config <path>`.

## Tool-to-Template Map

| MCP Tool | Template | Description |
|----------|----------|-------------|
| `get_account_link_status` | `assets/account-status.html` | Connection status, scopes |
| `get_daily_briefing` | `assets/daily-briefing.html` | Readiness, insights, priorities |
| `get_todays_action_plan` | `assets/action-plan.html` | Timeline of today's blocks |
| `get_progress_snapshot` | `assets/progress-snapshot.html` | Domain scores, recommendations |
| `get_weekly_summary` | `assets/weekly-summary.html` | Weekly scores, trends, goals |
| `analyze_meal_text` | `assets/meal-analysis.html` | Macro breakdown, components |
| `generate_workout` | `assets/workout.html` | Exercise cards with images |

## Rendering Workflow

1. Call the BestYou MCP tool via mcporter
2. Read the matching template from `assets/`
3. Replace the sample data in the HTML with the actual API response values (see data mapping below)
4. **Inline the CSS**: copy the contents of `assets/shared.css` into a `<style>` tag in the HTML `<head>` so the output is self-contained
5. Present the populated HTML via `canvas(action="present")` or `canvas(action="a2ui_push")`
6. Provide a brief text summary alongside the visual

## Design System

All templates use the **BestYou Dark Glass** design system (`assets/shared.css`):
- Background: `#0a0a0a`, cards: `#141414`, borders: `#1e1e1e`
- Font: Inter (Google Fonts)
- Color coding: green (`#4ade80`) = good, yellow (`#facc15`) = moderate, orange (`#fb923c`) = warning, red (`#f87171`) = poor
- Score thresholds: ≥70 green, 40-69 yellow/orange, <40 red

## Handling Missing Data

API responses may contain null or missing fields. Rules:
- If a score field is null, hide the gauge/bar or show "—" instead of a number
- If an array is empty or missing, omit that section entirely (don't render empty containers)
- If `totalCalories` or `calorieGoal` is null, omit the calorie summary row
- Never show "null" or "undefined" in rendered HTML

## Data Mapping by Template

### Daily Briefing

API response structure (nested):

| API Path | Template Element | Notes |
|----------|-----------------|-------|
| `headline` | `.headline` text | |
| `readinessScore` | `.gauge-value` + SVG `stroke-dashoffset` | Formula: `314 - (314 * score / 100)` |
| `dayType` | `.day-type .value` | Capitalize, add emoji: recovery=🔄, active=💪, rest=😴 |
| `yesterday.highlights[]` | `.insight-card` blocks | Positive insights (icon, title, description) |
| `yesterday.areas[]` | `.insight-card` blocks | Negative/improvement insights, render after highlights |
| `today.priorities[]` | `.action-item` blocks | Numbered, with title and description |
| `today.plans[]` | `.plan-tag` blocks | Emoji, plan name, week/day info |
| `insightCards[]` | Cross-domain section | Filter for `domain: "multi"` entries, render as cross-domain insight cards |

### Action Plan

| API Path | Template Element | Notes |
|----------|-----------------|-------|
| `readiness.score` | `.readiness-score` + badge | |
| `readiness.dayType` | `.rm-type` | |
| `blocks[]` | `.block-card` items | Group by `timePeriod`: morning/afternoon/evening |

Block icon mapping by `blockType`:
- `wakeUp` → 😴 (recovery icon bg)
- `breakfast` → 🍳 (nutrition icon bg)
- `lunch` → 🥗 (nutrition icon bg)
- `snack` → 🥤 (nutrition icon bg, or 🥑 for second snack)
- `dinner` → 🍽️ (nutrition icon bg)
- `workout` / `cardio` / `strength` → 🏃 (fitness icon bg)
- `goToBed` → 🌙 (recovery icon bg)

Block status: `completed` → ✅, `upcoming` or `pending` → ⬜

### Progress Snapshot

| API Path | Template Element | Notes |
|----------|-----------------|-------|
| `domains[]` | `.domain-card` grid | Each: `name`, `score`, color-coded mini bar |
| `insights[]` | `.insight-item` cards | With severity badge (high=red, medium=orange, low=blue) |
| `recommendations[]` | `.rec-item` cards | With `actionSteps[]` as list items |
| `crossDomainPatterns[]` | `.cross-domain` cards | With domain badges |

### Weekly Summary

| API Path | Template Element | Notes |
|----------|-----------------|-------|
| `overallScore` | Gauge SVG + label | |
| `domains[]` | `.domain-section` blocks | Each: trend badge (improving/declining/stable), stats, insight |
| `achievements[]` | `.achievement` cards | Emoji + title + description |
| `nextWeekFocus[]` | `.next-week-goal` items | With priority badge |

### Meal Analysis

| API Path | Template Element | Notes |
|----------|-----------------|-------|
| `mealName` | `.meal-name` | |
| `calories` | `.meal-cal` | |
| `protein_g`, `fat_g`, `carbs_g`, `fiber_g` | Macro bar segments + legend | Flex ratios = gram values |
| `components[]` | `.component` rows | Name, amount, calories, per-component macros |
| `insights[]` | `.insight-row` items | `.positive` or `.negative` indicator bar |
| `dailyTotals` | `.daily-totals` section | Calories, protein, fat, carbs |

### Workout

| API Path | Template Element | Notes |
|----------|-----------------|-------|
| `sessionName` | Header `h1` | |
| `duration`, `equipment`, `level` | Header `.meta` spans | |
| `blocks[]` | `.block` sections | Phase badge: warmup=green, main=orange, cooldown=blue |

Each exercise within a block:
- `imageUrl` → `<img>` src (CDN: `cdn.bestyou.ai`)
- `name` → `h3`
- `sets`, `reps`, `weight`, `rpe`, `rest` → `.rx-pill` spans
- `notes` → `.exercise-notes`
- `targetMuscle`, `exerciseType` → `.exercise-cues`

## Conversation Patterns

### Morning check-in
User: "What's my day look like?" or "Morning briefing"
1. `get_account_link_status` → verify connected
2. `get_daily_briefing` → render briefing widget
3. `get_todays_action_plan` → render action plan widget
4. Summarize: readiness score, day type, top priority

### Progress check
User: "How am I doing?" or "Show my progress"
1. `get_progress_snapshot` → render snapshot widget
2. Highlight strongest and weakest domains, top recommendation

### Meal logging
User: "I just had [food description]"
1. `analyze_meal_text` with the description → render meal widget
2. Note protein hit vs target, suggest next meal bias

### Workout request
User: "Give me a workout" or "[duration] [type] workout"
1. `generate_workout` with parameters → render workout widget
2. Brief summary: duration, focus, number of exercises

### Weekly review
User: "Weekly summary" or "How was my week?"
1. `get_weekly_summary` → render weekly widget
2. Highlight trends (improving/declining), top achievement, next week focus

## Text Summary Style

Keep text summaries alongside widgets brief and actionable:
- Lead with the key number (readiness score, calories, overall score)
- One sentence on what's going well
- One sentence on the top action item
- No need to repeat everything the widget shows visually
