---
name: coaching
description: Coaching practice support with session preparation, question generation, client progress tracking, and goal setting. Use when user mentions coaching sessions, coaching questions, client progress, or coaching goals. Prepares sessions, generates powerful questions, tracks client commitments, supports goal setting with clarity framework, and maintains momentum between sessions. STRICT client confidentiality.
---

# Coaching

Coaching practice system. Transform every session.

## Critical Privacy & Safety

### Data Storage (CRITICAL)
- **All client data stored locally only**: `memory/coaching/`
- **STRICT CONFIDENTIALITY** - client information never shared
- **No cross-client data mixing** - complete isolation
- **No external coaching platforms** connected
- User controls all data retention and deletion

### Safety Boundaries
- ✅ Prepare sessions and generate questions
- ✅ Track client progress and commitments
- ✅ Support goal setting with frameworks
- ✅ Provide between-session support
- ❌ **NEVER share** client information across contexts
- ❌ **NEVER make** client decisions
- ❌ **NEVER replace** coach judgment or intuition

### Confidentiality Note
Coaching effectiveness depends on trust. This skill maintains strict confidentiality - no client data is ever shared, mixed, or exposed outside your local system.

### Data Structure
Coaching data stored locally:
- `memory/coaching/clients.json` - Client records (isolated per client)
- `memory/coaching/sessions.json` - Session history and notes
- `memory/coaching/goals.json` - Client goals and progress
- `memory/coaching/questions.json` - Question libraries
- `memory/coaching/commitments.json` - Client commitments tracking

## Core Workflows

### Prepare Session
```
User: "Prep me for session with client John"
→ Use scripts/prep_session.py --client "John" --session 5
→ Summarize previous session, check commitments, generate tailored questions
```

### Generate Questions
```
User: "Give me questions for exploring career transition"
→ Use scripts/generate_questions.py --topic "career-transition" --depth "deep"
→ Generate powerful questions calibrated to situation
```

### Track Progress
```
User: "Show me Sarah's progress over the last 3 months"
→ Use scripts/track_progress.py --client "Sarah" --period "3months"
→ Display goals, session history, patterns, breakthroughs
```

### Set Goal
```
User: "Help my client set a clear goal"
→ Use scripts/set_goal.py --client "Mike" --area "leadership"
→ Apply clarity, specificity, timeline, obstacles, support framework
```

### Between Sessions
```
User: "Send between-session support to Lisa"
→ Use scripts/between_sessions.py --client "Lisa" --days 3
→ Provide reflection prompts, action reminders, preparation for next session
```

## Module Reference
- **Session Preparation**: See [references/session-prep.md](references/session-prep.md)
- **Powerful Questions**: See [references/questions.md](references/questions.md)
- **Goal Setting Framework**: See [references/goal-setting.md](references/goal-setting.md)
- **Progress Tracking**: See [references/progress.md](references/progress.md)
- **Between-Session Support**: See [references/between-sessions.md](references/between-sessions.md)
- **Client Confidentiality**: See [references/confidentiality.md](references/confidentiality.md)

## Scripts Reference
| Script | Purpose |
|--------|---------|
| `prep_session.py` | Prepare for coaching session |
| `generate_questions.py` | Generate powerful questions |
| `track_progress.py` | Track client progress |
| `set_goal.py` | Set structured goals |
| `between_sessions.py` | Between-session support |
| `log_session.py` | Log session notes |
| `track_commitment.py` | Track client commitments |
| `prepare_review.py` | Prepare progress review |
