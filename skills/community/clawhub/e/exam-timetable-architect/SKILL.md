---
name: exam-timetable-architect
description: Use when exams are 1-8 weeks away and a syllabus or topic list needs to become a day-by-day spaced study plan — prioritized by weight × weakness, with spaced repetition, active-recall blocks, and load-capped days that survive contact with real life.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [exams, study-plan, spaced-repetition, scheduling, students, education]
---

# Exam Timetable Architect

## Overview

Turns "I have 6 exams in 5 weeks and 40 topics" into a concrete day-by-day plan.
Topics are ranked by **exam weight × self-rated weakness × recency of first
study**, then scheduled backwards from each exam date so every topic gets an
initial study block **plus spaced reviews at expanding intervals** (1–3–7–14
days). Days are load-capped by available hours; the tool tells you the truth
about infeasible plans ("you need 4.2h/day but declared 2h/day") instead of
silently producing fantasy schedules.

## When to Use

- "I have exams in N weeks, help me plan" / "make me a study timetable"
- Multiple exams with dates and a syllabus/topic list per exam
- One big exam with many topics (bar exam, boards, finals, driving theory)
- Re-planning after a missed day ("I lost 3 days to flu")
- Deciding what to drop when there isn't time for everything

Don't use for: single-topic tutoring plans, habit building (habit-trigger-
detective), or timeblocking whole weeks beyond exam study.

## The Engine

1. **Input**: exams (name, date), topics per exam (name, difficulty 1–5,
   self-rated weakness 1–5, estimated hours), daily available hours.
2. **Priority** = `weight(normalized exam proximity) × weakness × difficulty` —
   near exams and weak heavy topics float to the top.
3. **Spacing**: each topic's first study is followed by reviews at +1, +3, +7,
   +14 days (review cost = 25% of first-study hours). Reviews must land
   **before** the exam; clips to exam-eve if needed.
4. **Load capping**: no day exceeds declared available hours (study blocks are
   50 min + 10 min break units; max 3 units before a long break is forced).
5. **Feasibility check**: total required hours vs total available hours before
   the last exam. If over capacity, the tool ranks what to cut (lowest priority
   first) and rebuilds — triage, not silence.
6. **Output**: `plan` (per-day schedule), `today` (what to do now), `done`
   (check off, triggers re-plan of the remainder), `progress` (coverage %,
   hours burned vs remaining).

## Numbered Workflow

1. `init` with exam dates and daily hours.
2. `topic add` each syllabus item with difficulty/weakness/hours (or bulk from
   a JSON/CSV dump).
3. `plan` → review the day map; if infeasible, follow the triage suggestions
   (`topic drop <id>` or raise daily hours).
4. Daily: `today` → study → `done <block-id>`; missed blocks auto-reschedule.
5. Weekly: `progress` — coverage and pace vs plan.
6. Exam eve: the plan converges to light review-only days by design.

## Commands

```
python3 scripts/exam_planner.py init --hours 3.5 --start 2026-10-01
python3 scripts/exam_planner.py exam add "Calculus II" --date 2026-10-20 --weight 40
python3 scripts/exam_planner.py topic add "CalcII: integration by parts" \
  --difficulty 4 --weakness 4 --hours 3
python3 scripts/exam_planner.py plan
python3 scripts/exam_planner.py today
python3 scripts/exam_planner.py done c1-r2
python3 scripts/exam_planner.py progress
python3 scripts/exam_planner.py replan   # after missed days / new topics
```

Store: `exam_plan.json` next to the script (`--store` to override).

## Spacing rationale

The +1/+3/+7/+14 ladder approximates expanding-interval retrieval practice
(Cepeda et al. 2006 meta-analysis: spaced beats massed by ~10–30% on retention
at test). Reviews are cheap (25% of original hours) because material was seen
before. Reviews never schedule after their exam; they compress into exam-eve
if the plan is tight — late compression is still better than none.

## Pitfalls

1. **Rating everything weakness 5** — the ranking collapses. Force honesty:
   weakness is *relative to you*, 3 = average.
2. **Planning 8h/day** — sustainable for almost nobody. The tool caps units/day
   and warns above 6h; believe it.
3. **Studying in date order instead of priority order** — the classic fatal
   mistake (chapter 1 gets mastered, chapter 14 gets nothing). Follow `plan`'s
   ordering, not the textbook's.
4. **Skipping reviews to cover new material** — coverage feels good, retention
   collapses. Reviews are locked unless the day is genuinely overloaded >150%.
5. **Never re-planning** — real life invalidates plans weekly. Run `replan`
   after any 2+ missed days; it re-spaces from *today*, not from the past.

## Example

5 exams in 4 weeks, 40 topics, 3.5h/day: feasibility check reports needed
4.1h/day → tool suggests dropping the two lowest-priority topics (weakness 2,
weight-light exam) → plan fits at 3.4h/day. Each hard topic appears ~4 times
(study + 3 reviews) before its exam; exam week itself is review-heavy by
construction.
