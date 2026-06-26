---
name: goal-tracker
version: "1.0.0"
description: OKR-style goal tracking for solopreneurs — quarterly goals, weekly check-ins, progress scoring, and an AI accountability partner that flags drift before it becomes failure.
tags: [goals, okr, accountability, quarterly-review, weekly-checkin, progress-tracking, solopreneur, habits, milestones, focus]
platforms: [openclaw, cursor, windsurf, generic]
category: productivity
author: The Agent Ledger
license: CC-BY-NC-4.0
url: https://github.com/theagentledger/agent-skills
---

# Goal Tracker

Set goals that don't disappear. Get an agent that notices when you're drifting and says something.

**by The Agent Ledger** — [theagentledger.com](https://theagentledger.com)

---

## The Problem

Most goal systems fail the same way: you set goals in January, review them in December, and discover you drifted in February and never noticed. The solution isn't a better template — it's an agent that checks in weekly and flags drift before it compounds.

This skill turns your agent into an accountability partner. Not motivational-poster accountability. Honest, data-driven accountability.

---

## Setup

### Step 1 — Create Your Goals Directory

```bash
mkdir -p goals/
```

### Step 2 — Create Your Quarterly Goals File

Create `goals/GOALS.md`:

```markdown
# Goals

**Current Quarter:** Q[N] [YEAR]
**Quarter Dates:** [Start] → [End]
**Last Updated:** [date]

---

## 🎯 This Quarter's Goals

### Goal 1: [Name]

**Why it matters:** [One sentence — the real reason, not the polished reason]
**Success looks like:** [Specific, observable outcome]
**Deadline:** [date or end of quarter]
**Status:** 🟢 On Track | 🟡 At Risk | 🔴 Off Track | ✅ Done | ⏸ Paused

**Key Results:**
- [ ] KR1: [measurable outcome] — current: [X] / target: [Y]
- [ ] KR2: [measurable outcome] — current: [X] / target: [Y]
- [ ] KR3: [measurable outcome] — current: [X] / target: [Y]

**Weekly Progress:**
| Week | Progress | Blocker | Score |
|------|----------|---------|-------|
| Wk1  |          |         |       |

---

### Goal 2: [Name]
<!-- Repeat structure above -->

---

## 📋 Goal Backlog

Goals you want to pursue — not this quarter, but tracked so they don't get lost.

| Goal | Why | Estimated Quarter |
|------|-----|-------------------|
|      |     |                   |

---

## ✅ Completed Goals

| Goal | Quarter | Outcome |
|------|---------|---------|
|      |         |         |
```

### Step 3 — Tell the Agent Your Goals

Simply tell the agent your goals in natural language:

> "I want to hit $5k in monthly revenue by end of March. My key results are: launch the product by March 10, get 50 paying customers, and write 8 newsletter issues."

The agent will structure them into `goals/GOALS.md` using the format above.

---

## Weekly Check-In

Once per week (or when triggered), the agent runs a structured check-in:

### Trigger

Any of:
- "Weekly goal check-in"
- "How are my goals looking?"
- "Goal update" + progress description
- Automatic via heartbeat or cron (see Advanced Patterns)

### Check-In Protocol

The agent will:

1. **Read `goals/GOALS.md`** — load current quarter's goals and KRs
2. **Ask 3 targeted questions:**
   - What progress happened this week toward each goal?
   - Any new blockers or changed assumptions?
   - Do any goals need to be modified, paused, or killed?
3. **Update the weekly progress table** for each goal
4. **Recalculate progress scores** (see Scoring below)
5. **Flag any at-risk goals** with specific observations
6. **Output a Check-In Summary** (see format below)

### Check-In Summary Format

```markdown
## Weekly Check-In — [date]

### 📊 Goal Scores
| Goal | Last Week | This Week | Trend |
|------|-----------|-----------|-------|
| [Goal 1] | [score]% | [score]% | ↑↓→ |
| [Goal 2] | [score]% | [score]% | ↑↓→ |

### ✅ Progress This Week
- [Goal 1]: [what happened]
- [Goal 2]: [what happened]

### ⚠️ Flags
- [Goal X is at risk because: specific observation]
- [KR Y has not moved in 2 weeks — is this still a priority?]

### 🔜 Commitments for Next Week
- [Specific action → [Goal]]
- [Specific action → [Goal]]

### 💭 Agent Observation
[One honest observation about goal trajectory this quarter]
```

---

## Progress Scoring

The agent scores each goal weekly using a simple formula:

**Goal Score = (KRs completed + KRs in progress × 0.5) / Total KRs × 100**

Example: 3 KRs total, 1 complete, 1 in progress, 1 not started → (1 + 0.5) / 3 × 100 = 50%

**Status thresholds:**

| Score | Status | Emoji |
|-------|--------|-------|
| 80–100% | On Track | 🟢 |
| 50–79% | Slight Risk | 🟡 |
| 20–49% | At Risk | 🔴 |
| 0–19% | Off Track | 💀 |

**Time-adjusted scoring:** The agent accounts for how far into the quarter you are. A 40% score in week 2 is fine; the same score in week 11 is a problem.

Formula: `Expected Progress = (Current Week / 13) × 100`
If `Goal Score < Expected Progress - 20%` → flag as At Risk regardless of threshold.

---

## Accountability Rules

These are the behaviors that make this skill useful instead of just a fancy spreadsheet.

### 1. The Drift Flag
If a goal's weekly progress entry is blank for 2+ consecutive weeks, the agent surfaces it: *"Goal X hasn't been updated in 2 weeks. Is this still active?"*

### 2. The Reality Check
When a KR target hasn't moved in 3 weeks, the agent asks: *"KR [name] is at [X]/[Y] and hasn't changed in 3 weeks. What's the plan?"*

### 3. The Mid-Quarter Warning
At week 6 (halfway through the quarter), the agent runs an automatic mid-quarter review and reports whether each goal is mathematically achievable given current pace.

### 4. The Kill Switch
If you tell the agent a goal is no longer relevant, it moves it to the backlog or archives it — but records the reason. "I killed this because [reason]" is valuable data for future goal-setting.

### 5. The Commitment Loop
At the end of every check-in, the agent asks for specific next-week commitments tied to each at-risk goal. These become the opening item for next week's check-in.

---

## Quarter Transition

At the end of each quarter (or when triggered):

1. **Score final results** — mark each KR complete/incomplete with final numbers
2. **Write a quarter retrospective** → `goals/retro-Q[N]-[YEAR].md`
3. **Move goals to Completed table** with outcome notes
4. **Archive the quarter** → `goals/archive/Q[N]-[YEAR]-GOALS.md`
5. **Open next quarter's GOALS.md** with blank structure

### Retrospective Format

```markdown
# Quarter Retrospective — Q[N] [YEAR]

**Overall Score:** [X]% ([N]/[N] goals completed or mostly completed)

## What Worked
- [specific thing]

## What Didn't
- [specific thing] — [honest reason]

## What I'd Do Differently
- [specific change]

## Carry-Over Goals
- [goal] → moving to Q[N+1] because [reason]

## Lessons for Next Quarter
- [lesson]
```

---

## Customization

### Set Your Quarter Dates
If your quarter doesn't follow Jan/Apr/Jul/Oct, tell the agent: *"My Q1 runs February through April."* It will adjust mid-quarter warnings and time-adjusted scoring accordingly.

### Adjust the Number of Goals
Default: 3–5 goals per quarter. Research suggests 3 is the sweet spot. If you want more, tell the agent — it will track them but may flag cognitive overload.

### Weekly vs. Bi-Weekly Check-Ins
If weekly feels like too much, tell the agent to default to bi-weekly check-ins. The drift detection threshold will adjust from 2 weeks to 4 weeks.

### Goal Categories
Optionally tag each goal with a category to track balance:
- `#revenue` — income-generating
- `#product` — building something
- `#audience` — growing reach
- `#learning` — skill development
- `#personal` — non-business

If all your goals are in one category, the agent will note the imbalance.

### Integration with Other Skills
This skill integrates cleanly with the rest of the Agent Ledger portfolio:

- **project-tracker**: Link goals to specific projects. When a project milestone completes, it can update the corresponding goal KR.
- **solopreneur-assistant**: The business dashboard can show goal scores alongside revenue metrics.
- **weekly-review** (via daily-briefing): Include goal status in morning briefings.
- **research-assistant**: When a goal requires research (e.g., entering a new market), spawn a research brief tied to that goal.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Goals feel vague | Break down to KRs with numbers. "Grow newsletter" → "Reach 500 subscribers by March 31" |
| Too many goals | Enforce the 3-goal limit. Ask: "If you could only accomplish one this quarter, which one?" |
| Goals feel stressful | Add a "Why it matters" sentence. Reconnecting to purpose helps more than adjusting targets |
| KRs keep changing | That's fine — log the change with a reason. Changing KRs = learning, not failure |
| Agent not flagging drift | Manually run: "Check my goals for drift and give me an honest assessment" |
| Quarter half-over, goals clearly won't happen | Don't hide it. Run the mid-quarter review early and reset targets based on reality |

---

## Advanced Patterns

See `references/advanced-patterns.md` for:
- Annual goals broken into quarterly milestones
- Multi-area goal tracking (business, health, relationships)
- Goal stacking (how goals support each other)
- Automated check-in via heartbeat/cron
- Public accountability (sharing goal scores in a newsletter or with an accountability partner)
- Post-mortem templates for missed goals
- Goal-to-project linking for tight integration with project-tracker

---

*Part of the Agent Skills collection by [The Agent Ledger](https://theagentledger.com).*
*Subscribe for new skills, premium blueprints, and field notes from a real AI-assisted operation.*

> *DISCLAIMER: This skill was created by an AI agent. It is provided "as is" for informational and educational purposes only. It does not constitute professional, financial, legal, or technical advice. Review all generated files before use. The Agent Ledger assumes no liability for outcomes resulting from use. Use at your own risk.*
