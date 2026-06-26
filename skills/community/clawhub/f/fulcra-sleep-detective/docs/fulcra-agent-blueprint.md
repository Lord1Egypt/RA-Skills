<!--
MIT License

Copyright (c) 2026 Open Source Community

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
-->

# Fulcra Biometric Intelligence System — Blueprint

*For AI agents running on agent runtime (or similar) with access to Fulcra's health data API.*

---

## The Idea in 30 Seconds

Your agent pulls biometric data every few hours. But instead of reporting numbers, it maintains a living document of theories about your human's health — informed by everything they've told you in conversation. It asks one question at a time, remembers every answer, and gets smarter. The data is the evidence. The context of their life is the interpretation. The feedback loop between conversation and data is what makes it intelligent.

**It's not a dashboard. It's a health detective that knows your life.**

---

## Why This Works (The Philosophy)

A dashboard says: "Your HRV dropped 5ms."

This system says: "Your HRV dropped 5ms — but it's Sunday, the day after your weekly injection, and you mentioned having drinks Saturday night. Two compounding factors. This same pattern has happened 3 of the last 4 weeks. Should normalize by Tuesday. But here's my question: on the one Sunday it DIDN'T drop, what was different?"

The difference is **context** and **curiosity**.

Three principles:

1. **Numbers without life context are noise.** The same HRV reading means completely different things depending on whether someone slept 4 hours because of insomnia vs. a newborn vs. a late flight. Your job is to know which.

2. **The human is the sensor you can't automate.** Fulcra gives you heart rate, sleep stages, steps. It can't tell you they switched medications, had a stressful meeting, stopped drinking, or feel "off." You get that from conversation — and you have to capture it immediately or it's gone.

3. **Theories beat reports.** Nobody wants a daily health report. They want someone who's *thinking* about their health in the background and speaks up when they notice something. Form hypotheses. Test them against data. Ask the one question that would confirm or kill the theory. Be wrong sometimes — that's data too.

---

## Architecture: Three Feedback Loops

```
              ┌──────────────────┐
              │   CONVERSATION   │
              │  (daily chats)   │
              └────────┬─────────┘
                       │ human mentions health info
                       ▼
              ┌──────────────────┐
              │  CONTEXT FILE    │◄─── the shared brain
              │  (life + theories│
              │   + questions +  │
              │   answers)       │
              └───┬──────────┬───┘
                  │          │
        cron reads│          │main session reads
                  ▼          ▼
          ┌────────────┐  ┌──────────────┐
          │ DATA CRON  │  │  MAIN CHAT   │
          │ (periodic) │  │  (reactive)  │
          │            │  │              │
          │ pull data  │  │ human says   │
          │ diff state │  │ "I'm tired"  │
          │ test theory│  │ → agent knows│
          │ ask or hush│  │   why        │
          └─────┬──────┘  └──────┬───────┘
                │                │
                │ updates        │ updates
                └───────┬────────┘
                        ▼
              ┌──────────────────┐
              │  CONTEXT FILE    │ ← loop closes, system learns
              └──────────────────┘
```

### Loop 1: Data → Insight (automated)
The cron pulls biometric data, compares to last run, and interprets changes through the lens of life context. It only speaks when something changed AND it's interesting. Most runs are silent.

### Loop 2: Conversation → Context (mandatory, immediate)
Whenever the human mentions anything health-related — sleep, meds, exercise, diet, stress, mood, symptoms — the agent immediately writes it to the context file. This is the most important loop. If you don't capture it, the system stays dumb.

### Loop 3: Theory → Question → Answer → Smarter Theory
The context file contains active theories (hypotheses). Each has evidence, status, and one or two questions that would help confirm or kill it. The cron asks one question when the data makes it relevant. The human answers in regular chat. The agent updates the theory. The cron gets smarter.

---

## Setup: Phase 1 — Bootstrapping (Day 1)

The system is useless without life context. Before any cron runs, you need to interview your human. This is a one-time conversation.

### The Bootstrap Interview

Have a natural conversation covering these areas. Don't make it feel like a medical intake form — just talk. Write everything to the context file as you go.

**Sleep:**
- What time do you usually go to bed? Wake up?
- What disrupts your sleep? (kids, pets, partner, insomnia, anxiety, noise)
- Do you track sleep? (Apple Watch, Oura, etc.)

**Medications & Supplements:**
- Taking anything regularly? (prescriptions, supplements, vitamins)
- Any recent changes? Starting/stopping anything?
- When do you take them? (timing matters for correlations)

**Exercise:**
- What's your routine? How often?
- Any recent changes? (injury, new program, stopped going)
- Indoor vs outdoor? Cardio vs strength vs both?

**Nutrition:**
- Do you track food? (app name if yes)
- Alcohol? How often, roughly?
- Caffeine? When do you cut off?
- Any dietary patterns? (fasting, keto, vegetarian, etc.)

**Work & Stress:**
- What does a typical week look like? Heavy days?
- What stresses you out? (meetings, deadlines, travel, people)
- Remote or in-office? Commute?

**Health Goals:**
- What are you trying to improve? (sleep, fitness, weight, energy, longevity)
- Anything you're worried about?
- Any conditions the data should account for?

**Environment:**
- Where do you live? (climate, altitude matter for some metrics)
- Do you travel often? Where?

Write all of this to `memory/topics/biometric-context.md`. This is the foundation.

### The Baseline Data Pull

Pull 30-90 days of historical data from Fulcra. Don't just look at yesterday — you need patterns.

```python
from fulcra_api.core import FulcraAPI
from datetime import datetime, timezone, timedelta

api = FulcraAPI()
# (authenticate and set token)

end = datetime.now(timezone.utc)
start = end - timedelta(days=90)

# Core metrics
sleep = api.sleep_agg(start.isoformat(), end.isoformat())
hrv = api.metric_samples(start.isoformat(), end.isoformat(), 'HeartRateVariabilitySDNN')
rhr = api.metric_samples(start.isoformat(), end.isoformat(), 'RestingHeartRate')
hr = api.metric_samples(start.isoformat(), end.isoformat(), 'HeartRate')
steps = api.metric_samples(start.isoformat(), end.isoformat(), 'StepCount')
workouts = api.apple_workouts(start.isoformat(), end.isoformat())
calendar = api.calendar_events(start.isoformat(), end.isoformat())

# Nutrition (if food tracking app connected)
calories = api.metric_samples(start.isoformat(), end.isoformat(), 'CaloriesConsumed')
protein = api.metric_samples(start.isoformat(), end.isoformat(), 'DietaryProteinConsumed')

# Optional but valuable
spo2 = api.metric_samples(start.isoformat(), end.isoformat(), 'OxygenSaturation')
resp = api.metric_samples(start.isoformat(), end.isoformat(), 'RespiratoryRate')
vo2 = api.metric_samples(start.isoformat(), end.isoformat(), 'VO2Max')
glucose = api.metric_samples(start.isoformat(), end.isoformat(), 'BloodGlucose')  # if CGM
```

Analyze the baseline for:
- **Averages and ranges** (what's normal for THIS person)
- **Day-of-week patterns** (do Mondays look different from Fridays?)
- **Trends** (is HRV improving or declining over 90 days?)
- **Outliers** (which days were dramatically different? Why?)
- **Correlations** (does bad sleep predict low HRV next day? Does meeting-heavy days correlate with higher HR?)

Write your initial findings and 3-5 initial theories to the context file. These are your starting hypotheses.

---

## Setup: Phase 2 — The Insights Script

Build a Python script that the cron will call. It should:

### Pull current data
Use the Fulcra API calls above, but for a shorter window (7 days gives enough context for trends without being expensive).

### Generate cross-domain insights
The value is in connecting domains. Don't just report each metric — cross-correlate:
- Sleep quality × next-day meeting load
- HRV × day of week × medication schedule
- Workout intensity × recovery state (HRV, RHR)
- Nutrition (especially protein) × training days
- Sleep architecture (deep/REM %) × supplement timing

### Diff against last run (critical)
This is what prevents parrot mode. Save a state file after each run:

```json
{
  "timestamp": "...",
  "last_sleep": {"date": "2026-02-17", "total_hours": 4.8, ...},
  "workout_ids": ["2026-02-17T12:51:34...", ...],
  "last_hrv_avg": 35.2,
  "last_rhr_avg": 73.0,
  "last_nutrition_date": "2026-02-16",
  "last_nutrition_cal": 2802
}
```

On `--diff` mode, compare current data to this state. Only output what changed:
- New sleep night appeared
- New workout detected
- HRV shifted meaningfully (use percentage, not fixed threshold — 10% of their baseline)
- RHR shifted meaningfully
- Nutrition data filled in (catches late logging)

If nothing changed: output `NO_CHANGES`. The cron should stay silent.

### Detect anomalies intelligently
- **Phantom workouts:** Indoor workouts with abnormal duration (>2h indoor cycling = probably forgot to end it on the watch). Flag these so calorie data isn't misinterpreted.
- **Incomplete nutrition logging:** Very low calories (<500) early in the day = probably hasn't logged yet, not starvation. Don't alarm.
- **Sensor gaps:** Zero CGM readings = sensor needs changing, not a health emergency.

### Output as JSON
Let the cron agent interpret the data — don't bake in the insight language. The script provides structured data; the cron provides the personality and context.

---

## Setup: Phase 3 — The Context File

This is the shared brain. Both the cron and the main session read it. It should have:

### Life Factors
Everything that affects biometric data. Organized by domain (sleep disruptors, medications, exercise, nutrition, work, environment). Written in plain language, not medical jargon.

### Known Correlations
Numbered list of confirmed connections. These are facts, not theories:
> "3 AM heart rate spikes = baby wake-ups (confirmed Feb 2026)"

### Active Theories
Each theory is a structured hypothesis:

```markdown
### Theory: [Name]
- **Status**: HYPOTHESIS | INVESTIGATING | STRONG EVIDENCE | CONFIRMED | KILLED
- **Evidence**: What data supports this?
- **Counter-evidence**: What contradicts it?
- **Questions for human**: 
  - [ ] Specific question that would help confirm/kill
  - [ ] Another question
- **If confirmed**: What would you recommend?
- **If killed**: What alternative explanation?
```

Theories should be:
- **Specific** ("Alcohol suppresses REM sleep within 3 hours of last drink" not "alcohol is bad for sleep")
- **Testable** (there's a question or experiment that could confirm/kill it)
- **Falsifiable** (you know what data would prove it wrong)
- **Actionable** (if confirmed, there's something the human can do)

### Answered Questions
When you learn something, move it from "Active Theories" to here with the date. This is institutional memory. Example:

> **Q: What time do you take [medication]?** (asked Feb 17)  
> A: "Right before bed, around 1 AM" (answered Feb 18)  
> → Updated Theory 1: timing is likely too late for optimal effect. Need to test earlier timing.

### What To Watch For
Open monitoring items — things you're tracking but don't have theories about yet.

---

## Setup: Phase 4 — The Cron Job

**Schedule:** Every 2 hours during waking hours. Adjust to your human's schedule.

**Model:** Needs judgment — use a model capable of reasoning (Sonnet-class minimum).

**Delivery:** `none` by default. The cron decides whether to message. MOST RUNS SHOULD BE SILENT.

**Prompt structure:**

```
1. Read the biometric context file — life context and active theories.

2. Run the insights script with --diff

3. If nothing changed: HEARTBEAT_OK. Done.

4. If something changed, think through:
   - Does this connect to a known life factor?
   - Does it support or contradict an active theory?
   - Does it suggest a new theory?
   - Is it expected (e.g., known weekly pattern) or surprising?

5. Only message the human if:
   - Something genuinely surprising or concerning
   - A theory just got stronger/weaker with new evidence
   - You have a specific question the data makes timely
   
6. Message style: Sharp friend texting, not medical report.
   One or two observations. One question max. No walls of numbers.

7. If the change is explained by known patterns: stay silent.
```

---

## Setup: Phase 5 — The Rules

### Mandatory Context Updates
Add to your agent's operating instructions:

> Whenever the human mentions sleep, medications, supplements, exercise, diet, alcohol, caffeine, stress, travel, schedule changes, health symptoms, illness, energy, or mood — **immediately** update the biometric context file. If it answers a theory question, resolve it. If it suggests a new pattern, add a theory. This file feeds the biometric cron. If you don't write it down, the system stays dumb.

### Main Session Access
The agent should load the context file every session so it can:
- Connect casual comments to health data ("I'm exhausted" → "Makes sense, 4.2h sleep + Monday meetings")
- Naturally ask theory questions when the moment is right
- Update context from throwaway comments the human wouldn't think to flag

### Epistemic Humility
The agent is NOT a doctor. It should:
- Say "I notice" not "you have"
- Frame insights as patterns, not diagnoses
- Distinguish between "interesting correlation" and "you should talk to your doctor"
- Be explicit about confidence levels: "strong pattern over 4 weeks" vs. "just one data point"
- Never recommend stopping medications or dramatically changing treatment

### When to Escalate
Flag for the human to discuss with their doctor if:
- Sustained RHR increase (>10 bpm above baseline over 5+ days)
- VO2Max declining steadily over months
- SpO2 consistently below 95%
- Any metric that's moved dramatically AND you can't explain it with life context
- Patterns that suggest their medication isn't working as expected

Frame as "worth mentioning to your doctor" — never as a diagnosis.

### Handling Wrong Theories
Theories will be wrong. When data contradicts a theory:
1. Update the theory status to WEAKENED or KILLED
2. Log the counter-evidence with the date
3. Move to Answered Questions with what you learned
4. Don't defend dead theories — kill them fast and form new ones
5. Being wrong is fine. Staying wrong isn't.

---

## How It Gets Smarter

**Week 1:** Generic observations. "Your HRV averaged 42ms this week." The agent is learning baselines and forming initial theories based on the bootstrap interview.

**Week 2-4:** Pattern recognition. "Your HRV drops every Sunday." "Your deep sleep is better on days you work out." Theories get evidence. Questions get asked.

**Month 1-2:** Contextual intelligence. "Your HRV dropped but it's post-injection day + you mentioned drinking Saturday. Two compounding factors." Cross-domain correlations emerge. The answered questions accumulate.

**Month 3+:** Predictive. "Tomorrow is Monday with 5 meetings and you slept 4h. Based on your pattern, I'd move the 2 PM if you can." The context file is now a deep model of one person's health, built from data AND conversation. No generic health app can do this.

---

## What You Need

- **Fulcra account** with connected data sources (Apple Health, nutrition app, etc.)
- **agent runtime** (or similar agent framework) with cron jobs and messaging
- **Python 3** with the `fulcra-api` package installed and `uv` available for Fulcra CLI commands (`uv tool run fulcra-api`)
- **Token refresh cron** (every 12h) to keep API access alive
- **~30 min** for the bootstrap interview
- **A human willing to answer questions** — the system only gets as smart as the context it's given

---

## File Reference

| File | Purpose |
|------|---------|
| `scripts/fulcra-daily-insights.py` | Data pull + cross-correlation + diff engine |
| `memory/topics/biometric-context.md` | Life context + theories + questions + answers |
| `data/last_report_state.json` | Diff state (what was already reported) |
| Agent config (AGENTS.md) | Mandatory update rule + session startup |

---

## Privacy

- All data stays on your machine. Fulcra API → your local storage.
- The context file contains deeply personal health information. Treat as private.
- Never send biometric context to group chats, public channels, or external services.
- Calendar data is used for meeting *load* (count), not content or attendees.
- When discussing with the human, never share their data with third parties.

---

## The One Thing to Remember

The script is replaceable. The cron schedule is adjustable. The file structure is flexible.

The thing that makes this system work is the **feedback loop between conversation and data**. Every time your human tells you something about their life, you write it down. Every time the data changes, you interpret it through what you know about their life. Every theory you form makes the next insight sharper.

The data is evidence. The conversation is context. The loop is intelligence.

---

*Built with Fulcra for intelligent health monitoring.*
