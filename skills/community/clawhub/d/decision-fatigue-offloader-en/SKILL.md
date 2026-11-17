---
name: decision-fatigue-offloader-en
display_name: Decision Fatigue Offloader
description: "Offloads low-stakes daily decisions. Triggers when the user says 'whatever', 'you pick', 'what should I eat for lunch', or 'what should I wear' — reads preset rules and the local city cost level, then makes the call immediately. No pros/cons matrices. Asks at most one follow-up field; unknown city falls back to the default city. Trigger words: decision fatigue, you pick, whatever, pick for me, what should I eat, what should I wear."
category: productivity
version: 1.1.0
author: snow
allowed-tools: ""
---
# Decision Fatigue Offloader (City-Adaptive)
## Red Lines
- No pros/cons lists, no decision matrices, no "you might consider…" suggestions.
- When information is incomplete, decide first and label it "based on default rules/default city" — never dump a questionnaire.
- Ask at most one follow-up field; if the user says "whatever", output the main decision directly.
- No networking, no external API calls. City cost data is a local static table, not live scraping.
## Step 1 — Identify City & Rules
Read `references/user-rules.md`. If it does not exist, read `references/default-rules.md`.
**City resolution order:** city name in the user's message → home city saved in user rules → default city (see rules file). Once the city is identified, look up its **dining, shopping, and leisure multipliers** in the "City Cost Multiplier Table" in `references/default-rules.md`. If the city is not listed, use the multiplier of its tier (tier-1 / new tier-1 / tier-2 / tier-3 and below).
**Multipliers apply to price thresholds only, never to preferences:** budget caps and unit-price thresholds are multiplied and rounded to sensible integers; dietary restrictions, clothing temperature bands, and energy preferences never change by city.
## Step 2 — Classify & Extract Minimal Input
Classify the request: dining / clothing / shopping / leisure / other. Extract: city, time, weather, energy level (1–5), budget, companions. If fields are missing, ask only for the **single field with the biggest impact on the outcome**; if the city is missing and the decision is clearly price-sensitive (lunch, shopping), prefer asking "Which city are you in?"; otherwise decide with the default city.
## Step 3 — Generate the Decision Card
Fixed four lines:
**Decision:** one sentence, specific and immediately actionable — never "consider…".
**Why:** 1–2 sentences citing the city multiplier and the rule, without extended argument (e.g., "Based on your city's cost level, the lunch budget was adjusted from the default 50 to 60").
**Fallback:** one option, used only when the main decision clearly does not fit.
**Switch condition:** one sentence stating when to switch (e.g., "if the queue exceeds 15 minutes, take the fallback").
## Step 4 — Feedback Calibration
When the user says "no / another one / too greasy / too far", append the feedback to the preference line in `user-rules.md`. When the user says "I'm in XX", write that city into the "Home City" field of `user-rules.md` so it applies automatically next time. Never modify hard rules unless the user explicitly says "change the rules".
