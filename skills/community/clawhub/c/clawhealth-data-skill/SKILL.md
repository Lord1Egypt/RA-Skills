---
name: clawhealth-data-skill
description: ClawHealth is an agent-native precision health service that connects wearable data, nutrition, goals, readiness, reports, anomaly context, and temporary visual panels to the user's own Agent. 小爪健康 / ClawHealth 是面向 Agent 的个人精准健康服务，把可穿戴数据、营养记录、目标、准备度、报告、异常上下文和临时可视化面板连接到用户自己的 Agent。Visit https://clawhealth.site to request access.
metadata:
  openclaw:
    emoji: "❤️"
---

# ClawHealth Data Skill

## What ClawHealth Does

**English.** ClawHealth is an agent-native precision health service. It lets a user's own Agent call structured health services instead of guessing from screenshots or generic advice. The current hosted service connects recent Apple Health / HealthKit data, nutrition records, personal goals, readiness signals, anomaly context, temporary visual panels, and feedback workflows. Users can request access and learn more at:

```text
https://clawhealth.site
```

After a user joins the test program, they use the ClawHealth iOS app to sync the latest 30 days of authorized health data and create an Agent Token. This skill then helps the Agent answer questions such as "How am I doing today?", "What should I pay attention to this week?", "Am I ready to train hard?", "What did this meal do to my nutrition target?", and "Open my health panel."

**中文。** 小爪健康 / ClawHealth 是面向 Agent 的个人精准健康服务。它不是让 Agent 凭截图或通用模板猜测，而是把用户授权的健康数据、营养记录、个人目标、恢复准备度、异常上下文、临时可视化面板和反馈流程，整理成 Agent 可以调用的结构化服务。欢迎前往官网注册体验：

```text
https://clawhealth.site
```

用户加入测试后，可以通过 ClawHealth iOS App 同步最近 30 天已授权的 Apple Health / HealthKit 数据，并创建 Agent Token。之后用户可以直接向自己的 Agent 提问，例如「我今天整体状态怎么样？」「这周需要关注什么？」「今天适合高强度训练吗？」「这顿饭对我的营养目标有什么影响？」「打开我的健康面板」。

Use this skill when a user asks for a ClawHealth report, health-data analysis, readiness, nutrition, anomaly context, or a visual ClawHealth panel.

## Natural User Experience

Never make the user say endpoint names or function names during normal use. Natural prompts include:

- "Show my ClawHealth daily report."
- "帮我看看今天身体状态。"
- "这周恢复怎么样？"
- "打开我的健康面板。"
- "记录这顿饭的营养。"
- "今天适合训练吗？"
- "帮我设置减脂目标。"

After setup, keep using the stored `customer_id` and Agent API token. Do not ask the user to repeat their customer ID, access code, endpoint names, or raw tool sequence unless debugging.

## Setup Order

Use this sequence for a new user:

1. Ask the user to open the ClawHealth iOS app and finish beta login.
2. The iOS app should request HealthKit permission during first setup and complete the first rolling 30-day sync.
3. Ask the user to create an Agent Token in the app.
4. Ask the user to copy the Agent setup prompt from the app. If the prompt includes the one-time token, store it securely as `Authorization: Bearer <token>` and do not repeat it in normal chat.
5. Call `send_agent_heartbeat` with the current channel, then call `get_daily_health_report` for the first pattern check.
6. If the Agent has a WeChat bridge, proactive reminders can be sent through that bridge. If not, return reminders in the current Agent conversation and suggest connecting WeChat later.

新用户设置顺序：

1. 让用户打开小爪健康 iOS App 并完成内测登录。
2. iOS App 会在首次设置时请求 HealthKit 权限，并完成最近 30 天的首次同步。
3. 让用户在 App 里创建 Agent Token。
4. 让用户复制 App 里的 Agent 设置提示。如果提示里包含一次性 Token，请把它保存为 `Authorization: Bearer <token>`，之后不要在普通聊天里重复展示。
5. 先调用 `send_agent_heartbeat`，再调用 `get_daily_health_report` 完成首次 pattern 检查。
6. 如果 Agent 已经有微信桥接，就可以通过微信推送主动提醒；如果没有，就先在当前 Agent 对话里返回提醒，并引导之后连接微信。

## Access Model

ClawHealth uses two token types:

- Agent API token: long-lived token created in the ClawHealth iOS app. The app shows it once. Store and use it as `Authorization: Bearer <token>`. The backend stores only a hash. If the user deletes it in the app, the token stops working.
- Panel token: short-lived token created by `create_panel_link`. It opens a temporary web panel and currently expires in about 20 minutes.

Required runtime values:

- `customer_id`: supplied by the ClawHealth iOS app or copied Agent setup prompt.
- `api_token`: long-lived Agent API token. Do not ask for the invite/access code in normal Agent chat.

Use only this host:

```text
https://clawhealth.site
```

Do not use raw Vercel deployment URLs.

## Proactive Health and WeChat Bridge

ClawHealth itself provides the health context, event queue, and polling contract. It does not directly log into a personal WeChat account.

Two modes are supported:

- WeChat already connected: the Agent runtime calls ClawHealth, checks `poll_agent_events`, follows `next_poll_after_seconds`, and sends important reminders through its WeChat bridge.
- WeChat not connected: answer inside the current Agent session and offer setup guidance for a bridge later.

Do not poll aggressively. `poll_agent_events` is the cheap first step. Only call daily/weekly reports, readiness, nutrition, or health analysis when an event or user question requires it.

主动健康的实现方式：

- 小爪健康负责健康上下文、事件队列和低成本轮询协议，不直接登录用户个人微信。
- 如果用户的 Agent 已经连接微信，Agent 调用小爪健康后，通过微信桥接把重要提醒发给用户。
- 如果尚未连接微信，就先在当前 Agent 对话里返回提醒，并引导之后配置微信桥接。
- 不要高频轮询。先调用 `poll_agent_events`，遵守 `next_poll_after_seconds`，只有必要时再调用日报、周报、准备度、营养或深度分析。

## Report Modes

Choose the report mode from the user's intent:

- Daily report: first response for "today", "now", "how am I doing", "日报", "今天". Focus on top signal, missing data, and one next action.
- Weekly report: use for "this week", "weekly", "一周", "最近几天". Compare the recent seven-day pattern with the available 30-day baseline.
- Long-term report: use for "long term", "baseline", "趋势", "长期". Current MVP is a 30-day baseline; say clearly that stronger conclusions need repeated 30-day windows.
- Deep analysis: use when the user asks why, wants charts, evidence, or domain-by-domain interpretation.
- Nutrition monitor: use when the user asks about meals, calories, macros, protein, carbs, fat, fiber, or a food photo.
- Readiness and passive state recognition: use when the user asks whether to train, asks about recovery readiness, or asks why ClawHealth detected strain, high arousal, recovery limits, or body-load changes.

## First 7 Days Experience

Use ClawHealth as a simple three-part product:

- Trend analysis: help the user understand a period of accumulated Apple Health data.
- Passive reminders: surface daily or proactive reminders when ClawHealth events indicate something worth noticing.
- Active interaction: answer user questions through the Agent using ClawHealth tools.

Suggested cadence:

- First use: confirm the iOS app has synced recent Apple Health data, then run `get_daily_health_report` and `analyze_health_data` for the initial pattern check. Explain available data, missing data, and what the user can ask next.
- Days 1-3: focus on daily summaries, sync reliability, missing-data guidance, and simple Agent questions. Avoid strong trend claims if only a few days are available.
- Days 4-7: start comparing recent patterns. If enough data exists, run `get_weekly_health_report`, highlight changes versus available baseline, and create lightweight reminders only when useful.

前三天和七天体验：

- 首次使用：确认 iOS App 已同步最近 Apple Health 数据，然后调用 `get_daily_health_report` 和 `analyze_health_data` 做首次 pattern 检查。告诉用户目前有哪些数据、缺哪些数据、接下来可以问什么。
- 1-3 天：重点是每日摘要、同步是否稳定、缺失数据提示，以及几个简单的主动提问入口。不要在数据很少时做过强趋势判断。
- 4-7 天：开始做近期趋势比较。数据足够时调用 `get_weekly_health_report`，解释最近变化，并在必要时创建轻量提醒。

## Tools

### get_daily_health_report

Use first for everyday check-ins.

```http
GET /api/clawhealth/daily-report?customer_id={customer_id}
Authorization: Bearer {api_token}
```

Return:

- Latest 30-day sync window
- Overall summary
- Top attention domains
- Missing data
- One practical next action
- Relevant scientific references if needed

### get_weekly_health_report

Use for weekly review.

```http
GET /api/clawhealth/weekly-report?customer_id={customer_id}
Authorization: Bearer {api_token}
```

Return:

- Seven-day review against the available 30-day baseline
- Domain-by-domain trend interpretation
- Missing data
- Citation keys and references returned by ClawHealth

### get_long_term_health_report

Use for baseline and longer-horizon questions.

```http
GET /api/clawhealth/long-term-report?customer_id={customer_id}
Authorization: Bearer {api_token}
```

Return:

- Current 30-day baseline quality
- Persistent focus candidates
- Next-cycle recommendation
- Limits of the data

### analyze_health_data

Use when the user asks for deeper evidence, charts, or domain-by-domain interpretation.

```http
GET /api/clawhealth/health-analysis?customer_id={customer_id}
Authorization: Bearer {api_token}
```

Use only evidence returned by ClawHealth. Distinguish `attention`, `needs_data`, and `ok`.

### create_panel_link

Use when the user asks to see a visual panel.

```http
GET /api/clawhealth/panel-token?customer_id={customer_id}
Authorization: Bearer {api_token}
```

Return the exact temporary `panel_url`. Tell the user it expires in about 20 minutes.

Important:

- A valid temporary panel link must contain both `customer_id` and `panel_token`.
- If a chat renderer escapes the URL as `&amp;panel_token=...`, replace `&amp;` with `&` before returning/opening the link.
- If the API call fails and you only have `https://clawhealth.site/health-panel?customer_id={customer_id}`, that is not a temporary panel link. It is only a manual unlock page and may ask the user to unlock in the browser.

### update_basic_profile

Use when the user gives age, sex, height, weight, goal, or activity level. This enables calorie and macro targets.

```http
POST /api/clawhealth/profile
Authorization: Bearer {api_token}
Content-Type: application/json

{
  "customer_id": "{customer_id}",
  "age": 29,
  "sex": "male",
  "height_cm": 178,
  "weight_kg": 74,
  "goal": "fat_loss",
  "activity_level": "moderate"
}
```

Return the saved profile and explain that targets use Mifflin-St Jeor plus activity and goal adjustment. It is an estimate, not measured metabolism.

### record_meal_nutrition

Use after the user provides a food photo, meal description, or Agent-estimated nutrition JSON.

Workflow:

1. Estimate calories, protein, carbohydrate, fat, and fiber from the image/description.
2. Be explicit that image-based nutrition is an estimate.
3. Save the estimate to ClawHealth.
4. Return daily totals and remaining targets.

```http
POST /api/clawhealth/nutrition
Authorization: Bearer {api_token}
Content-Type: application/json

{
  "customer_id": "{customer_id}",
  "meal_name": "lunch bowl",
  "calories_kcal": 650,
  "protein_g": 38,
  "carbohydrate_g": 72,
  "fat_g": 21,
  "fiber_g": 9,
  "confidence": "medium",
  "raw_agent_json": {}
}
```

The current MVP stores nutrition in ClawHealth. HealthKit writeback is not enabled yet because the iOS SDK needs a native write/save method and user write permission.

### get_nutrition_summary

Use when the user asks about calories, macros, remaining limits, or recent meals.

```http
GET /api/clawhealth/nutrition?customer_id={customer_id}
Authorization: Bearer {api_token}
```

### record_mood

Use when the user states mood, stress, energy, soreness, or subjective recovery.

```http
POST /api/clawhealth/mood
Authorization: Bearer {api_token}
Content-Type: application/json

{
  "customer_id": "{customer_id}",
  "mood_score": 3,
  "energy_score": 4,
  "stress_score": 2,
  "note": "slept late but feels okay"
}
```

### get_readiness_check

Use when the user asks whether to train, whether recovery is good, or how mood relates to HRV.

```http
GET /api/clawhealth/readiness?customer_id={customer_id}
Authorization: Bearer {api_token}
```

Explain the readiness score as a transparent MVP heuristic from recovery, sleep, training, mood, and stress. Do not present it as a validated medical or performance diagnosis.

### submit_feedback

Use when the user wants to report a bug, improve a recommendation, or leave demo feedback.

```http
POST /api/clawhealth/feedback
Content-Type: application/json

{
  "customer_id": "{customer_id}",
  "feedback": "text",
  "context": {}
}
```

## Evidence, Literature, and State Recognition Rules

ClawHealth API responses include `scientific_references` and may include `state_model`. Use those first. You may cite them in normal language, but do not invent citations.

When discussing passive state recognition:

- Do not say the user "is anxious" or "has an illness" from wearable data.
- Say "physiological load", "high arousal", "recovery looks limited", or "strain signal".
- Explain which signals were used: HRV vs personal baseline, resting heart rate vs baseline, sleep debt, low-activity high heart rate, training-recovery conflict, respiratory/temperature/oxygen context if available.
- Night events should be queued and summarized in the morning sleep/recovery report. Do not recommend waking the user for routine wellness alerts.
- Prefer N-of-1 wording: "compared with your recent baseline", not generic thresholds.

Current reference library:

- Watson et al., 2015, AASM/SRS sleep-duration consensus, J Clin Sleep Med: adults should generally sleep 7+ hours regularly; use as sleep context, not diagnosis.
- WHO, 2020 physical activity guidelines: adults should do regular activity, including 150-300 minutes moderate aerobic activity weekly where appropriate.
- Zhang et al., 2016, CMAJ resting-heart-rate meta-analysis: higher resting heart rate is associated with higher population-level mortality risk; individual clinical context is required.
- Maki et al., 2024, HRV/autonomic review: HRV is a non-invasive autonomic marker, but baseline and context matter.
- Hjort et al., 2024, CGM variability review: glucose variability in people without diabetes is emerging and should be interpreted cautiously.
- Kim et al., 2018, stress and HRV meta-analysis: HRV is useful for stress-response context but must be interpreted carefully.
- Sensors, 2021, wearable stress systematic review: wearable stress work commonly uses HRV, HR, EDA, and respiration; HR alone is not enough.
- International Journal of Medical Informatics, 2023, wearable stress ML systematic review: wearable stress models remain context-sensitive and need cautious generalization.
- Frontiers in Physiology, 2013, HRV in normal and pathological sleep: sleep stages change autonomic balance, with NREM and REM showing different patterns.
- Frontiers in Neurology, 2025, sleep deprivation and HRV meta-analysis: sleep loss is associated with autonomic changes reflected in HRV.
- JMIR mHealth and uHealth, 2024, Fitbit/Garmin/WHOOP sleep accuracy review: consumer sleep trackers support longitudinal context but sleep-stage estimates are approximate.
- Lancet Digital Health, 2020, Fitbit influenza-like illness surveillance: RHR and sleep changes can provide population-level physiological context.
- Nature Biomedical Engineering, 2020, smartwatch pre-symptomatic COVID detection: extreme RHR elevations relative to individual baseline can indicate physiological changes, but this is not diagnostic.
- IJERPH, 2021, HRV-guided training meta-analysis: HRV can guide training adjustment as a trend-based decision aid.
- Sports Medicine, 2019, portable HRV accuracy meta-analysis: device, timing, posture, and artifact handling affect HRV reliability.
- Mifflin et al., 1990, AJCN resting energy expenditure equation: use for estimated calorie target only.
- Institute of Medicine / National Academies AMDR reference tables: adult macro ranges are commonly cited as carbohydrate 45-65%, fat 20-35%, and protein 10-35% of energy.
- Jager et al., 2017, ISSN protein and exercise position stand: many exercising individuals use 1.4-2.0 g/kg/day as a protein target range.
- Apple HealthKit Nutrition Type Identifiers: HealthKit supports dietary energy, protein, carbohydrate, fat, fiber, water, and related nutrition types.

## Response Style

- Match the user's language. Chinese and English are both supported.
- Lead with what the data says, then what it may mean, then what to do next.
- Say "latest 30-day synced snapshot" somewhere in the answer.
- Use "needs attention / 需要关注", not "Watch".
- Separate data from interpretation from next monitoring action.
- When data is missing, say exactly which data needs authorization or syncing.
- Keep daily reports concise. For "deep analysis", write a longer structured answer with headings: Data Coverage, Main Signals, Anomaly Context, Evidence Notes, Limits.
- For food-photo estimates, return both a user-friendly explanation and a JSON-like nutrient breakdown before saving.
- For readiness, separate objective wearable signals from subjective mood/stress entries.
- Do not diagnose, treat, or make emergency recommendations.

## Network Fallback

If the Agent runtime cannot reach `https://clawhealth.site` or TCP/HTTPS to the hosted API times out, do not keep retrying.

Tell the user:

```text
The current Agent server cannot reach the ClawHealth API from its network, so I cannot create a temporary panel token right now. You can still open the manual unlock page directly:
https://clawhealth.site/health-panel?customer_id={customer_id}
```

Ask the user to open that URL and unlock in the browser. Do not call it a temporary panel link, and do not put the access code into a URL unless the user explicitly requests a prefilled private link.
