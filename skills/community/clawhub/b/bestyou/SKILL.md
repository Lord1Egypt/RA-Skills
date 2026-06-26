---
name: bestyou
description: >
  Connect your AI agent to BestYou health intelligence via MCP. 19 on-device
  AI agents coordinate fitness, nutrition, sleep, and recovery into an adaptive
  daily Action Plan. Query readiness, generate workouts, analyze meals, and
  manage your plan. Integrates Apple Watch, Oura Ring, CGM, and HealthKit data.
homepage: https://bestyou.ai/openclaw-setup
metadata:
  openclaw:
    requires:
      env:
        - BESTYOU_API_KEY
    primaryEnv: BESTYOU_API_KEY
---

# BestYou Health Intelligence

BestYou brings real health data from your wearables into your AI agent through MCP. It pulls fitness, nutrition, sleep, and recovery signals from Apple Watch, Oura Ring, CGM sensors, and HealthKit, then coordinates them through 19 specialized on-device agents. The result is an adaptive daily action plan that responds to your actual readiness, not generic templates. Query your readiness score, generate workouts matched to your recovery state, analyze meals against your macro targets, and manage your plan through natural conversation.

**Privacy note:** No health data leaves your device without your explicit consent. BestYou shares processed insights only. Raw HealthKit readings stay on the iPhone. See `references/security.md` for details.

## What Makes This Different

Most health integrations export static data or generate generic prompts. BestYou connects to a live API backed by 19 coordinated AI agents running on-device.

- **Cross-domain coordination.** Sleep quality affects training intensity, which affects nutritional needs, which affects recovery. BestYou's agents talk to each other. A bad night of sleep triggers adjustments across your workout, nutrition targets, and recovery priorities automatically.
- **Real wearable data, not manual logging.** Heart rate, HRV, sleep stages, activity rings, glucose trends: all pulled from HealthKit. No typing in numbers.
- **Adaptive action plans.** Your daily plan is built from your actual readiness, schedule, and recovery state. It adapts as conditions change.
- **19 specialized agents.** Each health domain (sleep, cardiac, nutrition, fitness, stress, hydration, body composition, and more) has a dedicated agent. They coordinate through a readiness engine that produces a single, actionable plan.
- **Metabolic health aware.** Tracks glucose patterns, metabolic flexibility indicators, and coordinates nutrition with training for metabolic optimization. Supports GLP-1 users with protein safety floors and resistance training compliance.

## Setup

### 1. Get your API key

Open the BestYou iOS app: **More → Connected Apps → OpenClaw → Generate Key**

Your key looks like `by_mcp_live_...`. Full walkthrough: [bestyou.ai/openclaw-setup](https://bestyou.ai/openclaw-setup)

### 2. Set the environment variable

```bash
export BESTYOU_API_KEY="YOUR_KEY_HERE"
```

### 3. Connect via mcporter

If you don't have mcporter (OpenClaw's MCP client) installed yet, you can install it with:

```bash
npm install -g mcporter
```

Add BestYou as an MCP server:

```bash
mcporter config add bestyou \
  --url https://mcp.bestyou.ai/mcp \
  --header "Authorization: Bearer $BESTYOU_API_KEY"
```

Verify with `mcporter call bestyou.get_account_link_status`.

For a more detailed setup walkthrough, see `references/setup.md`.

---

## Agent Behavior

### Session Start

Always call `get_account_link_status` first. If the account is not linked or the subscription is inactive, tell the user what to fix (re-link in BestYou app, check subscription) and stop. Do not call other tools until status is confirmed.

### Daily Coaching Flow

1. Call `get_daily_briefing` with today's date to pull the narrative, readiness score, and recommended actions.
2. Summarize in 2-3 sentences: how the user is doing, what stands out.
3. Recommend 1-2 concrete actions from the briefing.

### Plan Management

- Call `get_todays_action_plan` to see scheduled blocks (workouts, meals, recovery) for the day.
- Present blocks grouped by time period (morning, afternoon, evening).
- When the user asks about adjustments, show them what's on the plan and help them prioritize.

### Fitness

- `generate_workout`: Ask for type (strength, mobility, cardio, mixed, hiit), duration, available equipment, and experience level before generating. Optional: body parts, target areas, goal, injuries, warmup/cooldown preferences.

### Nutrition

- `analyze_meal_text`: Accept a text description of what the user ate. Optionally include a timestamp. Returns macro breakdown, components, and insights on how the meal fits the day's targets.

### Progress and Trends

- `get_progress_snapshot`: Shows domain-level scores (sleep, cardiac, fitness, nutrition, hydration, glucose, etc.), top insights, recommendations, and cross-domain patterns.
- `get_weekly_summary`: End-of-week review with trends, achievements, and next week focus areas.

### Style

Direct, calm, practical. You're a coach, not a cheerleader. State what matters, skip the filler.

### Safety

- Never expose internal IDs, suggestion IDs, session IDs, tokens, or raw auth values in responses.
- Never share raw health data outside the conversation. Only surface processed insights.
- If a tool returns an error, explain the issue plainly without leaking technical details.

---

## Tool Reference

| Tool | When to use | Required parameters |
|------|-------------|---------------------|
| `get_account_link_status` | First call every session. Confirms link, subscription, scopes. | (none) |
| `get_daily_briefing` | User asks "how am I doing today?" or starts a health conversation. | `date` (YYYY-MM-DD) |
| `get_todays_action_plan` | User wants to see today's plan or scheduled blocks. | `date` (optional) |
| `get_progress_snapshot` | User asks "how am I doing overall?" or wants domain scores. | `date` (YYYY-MM-DD) |
| `get_weekly_summary` | End-of-week review or "how was my week?" | `weekEndDate` (optional) |
| `generate_workout` | User wants a new workout built from scratch. | `type`, `duration`, `equipment`, `experienceLevel` |
| `analyze_meal_text` | User describes food they ate for nutritional analysis. | `description` |

### generate_workout parameters

**Required:** `type` (strength/mobility/cardio/mixed/hiit), `duration` (minutes), `equipment` (array of strings), `experienceLevel` (Beginner/Intermediate/Advanced)

**Optional:** `bodyParts`, `targetAreas`, `goal`, `injuries`, `includeWarmup`, `warmupStyle` (dynamic/activation), `warmupDuration`, `includeCooldown`, `cooldownStyle` (static/foam_rolling/combined), `cooldownDuration`

---

## Example Conversations

### Morning check-in

> **User:** "What's my day look like?"
>
> **Agent:** Call `get_account_link_status`, then `get_daily_briefing` with today's date. Summarize readiness, highlight top priorities, suggest 1-2 actions.

### Logging a meal

> **User:** "Just had a chicken burrito bowl with brown rice and guac"
>
> **Agent:** Call `analyze_meal_text` with `description="chicken burrito bowl with brown rice and guacamole"`. Report macros and how it fits the day's targets.

### Progress check

> **User:** "How am I doing overall?"
>
> **Agent:** Call `get_progress_snapshot` with today's date. Highlight strongest and weakest domains, surface top recommendation.

### Weekly review

> **User:** "How was my week?"
>
> **Agent:** Call `get_weekly_summary`. Highlight trends (improving/declining domains), top achievement, and next week's focus areas.

### Quick workout

> **User:** "Give me a 20-minute bodyweight workout focused on strength"
>
> **Agent:** Call `generate_workout` with `type="strength"`, `duration=20`, `equipment=["bodyweight"]`, `experienceLevel="Intermediate"`. Present the workout clearly with exercises, sets, reps, and rest periods.

---

## Notes

- **API key source:** Generated in the BestYou iOS app, not a web dashboard.
- **Free trial:** Use code `OPENCLAW1MO` for one free month of BestYou Pro.
- **Privacy:** BestYou shares processed insights only. Raw health data (HealthKit, sensor data) never leaves the device. No data is stored locally by this skill.
- **Playground:** Test your connection at [mcp.bestyou.ai/openclaw](https://mcp.bestyou.ai/openclaw) before wiring into your agent.
