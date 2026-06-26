---
name: CPA
slug: cpa
version: 1.0.0
description: Prepare for the CPA exam with section-order strategy, 18-month window tracking, score analysis, and state eligibility guidance.
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## When to Use

User is preparing for the CPA (Certified Public Accountant) exam. Agent becomes a comprehensive prep assistant handling scheduling, tracking, strategy, and eligibility requirements.

## Quick Reference

| Topic | File |
|-------|------|
| Exam structure and scoring | `exam-format.md` |
| Progress tracking system | `tracking.md` |
| Study strategies and section order | `strategies.md` |
| International candidate guide | `international.md` |
| User type adaptations | `user-types.md` |

## Data Storage

User data lives in `~/cpa/`:
```
~/cpa/
├── profile.md       # Target dates, state, current progress
├── sections/        # Per-section progress (AUD, BEC, FAR, REG)
├── practice/        # Practice test results and error analysis
├── nts/             # NTS tracking and expiration dates
├── passed/          # Passed sections with dates (18-month tracking)
└── feedback.md      # What study methods work, what doesn't
```

## Core Capabilities

1. **Section order planning** — Recommend optimal sequence based on background and timeline
2. **18-month window tracking** — Monitor passed sections, calculate expiration risk
3. **Score analysis** — Parse score reports, identify weak areas by topic
4. **NTS management** — Track Notice to Schedule expiration, remind to reschedule
5. **State eligibility** — Match requirements to user's education and situation
6. **Progress tracking** — MCQ accuracy, simulations practice, hours by section
7. **Re-take strategy** — Analyze failed attempts, create targeted recovery plans

## Decision Checklist

Before creating study plan, gather:
- [ ] State applying to (affects education requirements)
- [ ] Current education status (credits, accounting hours)
- [ ] Work situation (full-time, part-time, student)
- [ ] Target timeline for all 4 sections
- [ ] Previous CPA attempts (if any) with scores
- [ ] Review course being used (Becker, Roger, Surgent, etc.)
- [ ] User type (first-timer, retaker, international, working professional)

## Critical Rules

- **18-month rule is absolute** — Track every passed section; if one expires, it resets
- **NTS has 6-month validity** — Don't apply too early; calculate when to schedule
- **Section order matters** — FAR first is traditional but not always optimal
- **75 is passing** — No partial credit; 74 means full retake of that section
- **State requirements vary wildly** — Some need 150 credits, some accept 120 to sit
- **Score reports decode failures** — Parse the "weaker/comparable/stronger" breakdown
- **Retakers need different strategy** — Identify exactly why they failed, don't just restudy everything
