# Exam Timetable Architect — Reference

## The problem, quantified

Cramming fails predictably: the forgetting curve (Ebbinghaus; modern replications
by Murre & Dros 2015) shows ~50% loss within 24h without retrieval, and massed
practice ("binge chapter 4 tonight") produces recognition fluency that collapses
under exam conditions. Meanwhile, hand-made timetables fail for scheduling
reasons, not studying reasons:

- They're built in **syllabus order**, not priority order — early chapters get
  over-studied, late ones get zero coverage.
- They ignore **exam dates** — the exam in week 2 deserves different treatment
  than the one in week 6.
- They schedule **reviews never** — every topic is touched once.
- They're **load-blind** — 9 hours of blocks on a day that has 3 free hours.
- They never **re-plan** after the first missed day, so by week 2 the plan is
  fiction and gets abandoned.

This tool is a scheduler first: priority ranking + backward scheduling from
exam dates + expanding-interval reviews + load caps + explicit feasibility
math + re-planning that works from today.

## Priority formula

```
priority = exam_weight_norm × weakness (1-5) × difficulty (1-5)
exam_weight_norm = topic_count_weight × proximity_weight(date)
proximity_weight = 1 + 3 × max(0, (28 - days_to_exam)) / 28
```

Rationale: all topics of a near exam get boosted (you'll be tested sooner —
forgetting has less time to decay), and within an exam, weak+hard topics float
up. The user can override with `--pin` (must study early) or `--drop`.

## Spacing: the +1/+3/+7/+14 ladder

Cepeda et al. (2006, 317 experiments, n≈184k): spaced practice beats massed by
a large margin; optimal gap scales with retention interval — roughly **10–20%
of the time until test**. For a 2–6 week horizon that means gaps of 1–7 days,
expanding. We schedule first study + reviews at +1, +3, +7, +14 clamped to
before-exam:

- review cost = 25% of the topic's first-study hours (material is re-seen, not
  learned; consistent with spacing-effect literature where review trials are
  far cheaper than acquisition trials)
- if +14 would land post-exam, compress to exam-eve; if +7 does, compress to
  exam−2. Late compressed review > no review.
- final 2 days before any exam: review-only (no new topics scheduled within
  48h of that exam unless the plan is infeasible otherwise).

## Load model and units

- Unit = **50 min block + 10 min break** (matches attention-cycle findings for
  demanding study; Pomodoro-adjacent but sized for deep problem sets).
- Max units per day derived from declared hours: `units = floor(hours × 60 / 60)`
  → each unit consumes 1h wall-clock including its break.
- Forced long break after 3 consecutive units (30 min, does not count against
  hours).
- Hard warning when declared hours > 6/day (unsustainable for most people over
  multi-week horizons; sleep debt destroys retention — see pitfalls).

## Feasibility and triage

```
required = Σ first_study_hours × (1 + n_reviews_scheduled × 0.25)
available = Σ daily_hours for days from start to last_exam
deficit = required − available
```

If deficit > 0 the tool does NOT silently compress: it prints the honest
number and proposes cuts in order:
1. drop topics with lowest priority (weakness ≤ 2 AND low exam weight)
2. drop the +14 review tier globally (saves 25% × topics, retention cost small
   at short horizons)
3. drop the +7 tier
4. raise daily hours (user decision, flagged as unsustainable above 6h)

## Re-planning semantics

`replan` discards future blocks (keeps completed history), re-derives spacing
from today for un-studied topics, and for studied-but-not-reviewed topics
re-computes overdue reviews at compressed intervals. Missed review = schedule
at next available slot, not never. This mirrors real flashbook behavior
(Anki-style) but at topic granularity.

## What "done" means

A topic is exam-ready when: first study done AND all scheduled pre-exam reviews
done. `progress` reports three numbers: coverage % (topics with first study),
reinforcement % (scheduled reviews completed), and pace (hours burned vs
hours-planned-to-date). Coverage without reinforcement is the classic illusion
of competence — the tool surfaces both separately for exactly that reason.

## Evidence anchors

- Ebbinghaus forgetting curve; Murre & Dros 2015 replication
- Cepeda, Pashler, Vul, Wixted & Rohrer 2006 — spacing meta-analysis
- Roediger & Karpicke 2006 — retrieval practice > restudy (hence review blocks
  are *self-testing* blocks: the reference plan marks them "recall first, then
  check")
- Bjork's "desirable difficulties" — why the plan tolerates harder retrieval
  conditions in reviews (closed book) than in first study
- Distributed-practice effect is one of Dunlosky et al. 2013's two "high
  utility" learning techniques (the other is retrieval practice — both are
  what this tool schedules)

## Operational notes for agents

- Always run the feasibility check before showing a plan; never present an
  over-capacity plan as-is.
- When the user says "I'm behind", run `replan`, don't moralize; the tool
  re-spaces from today automatically.
- Topics added mid-plan get spacing computed from their add date.
- If the user gives a syllabus dump (PDF/notes), extract topics into
  `topic add` commands; estimate hours = pages × 0.25h for problem-solving
  subjects, × 0.1h for reading subjects, then let the user adjust weakness.
