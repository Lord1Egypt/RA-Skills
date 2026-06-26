---
name: fitclaw-training-public
description: Public-safe training workflow for AI fitness coaching. Use when selecting a training split, building a sustainable training structure, calibrating starting loads, and guiding users through progression without relying on private internal-only knowledge paths.
---

# FitClaw Training Public

## Purpose

This is the **public-safe training module** extracted from FitClaw.

Its job is not to dump a random workout list.
Its job is to help an AI coach:
- choose an appropriate training structure,
- explain why that structure fits the user,
- calibrate starting loads conservatively,
- and guide progression through feedback.

This public version keeps the method,
not the private operating environment.

---

## Use this when

Use this workflow when:
- a user needs an initial training framework,
- a coach is choosing between a 3-day and 4-day split,
- a user says they are ready to start training,
- or a user reports workout performance and needs adjustment.

---

## Core goal

Training guidance should create a loop, not a one-time list.

That means:
- choose a split that matches real frequency and recovery,
- use movement categories and anchor lifts,
- set conservative starting loads,
- and update the plan from actual performance.

---

## Baseline inputs

Before giving a structured training framework, preferably know:
- training days per week
- session duration
- training setting (gym / home / mixed)
- recovery constraints or injuries
- at least a few strength anchors

Strength anchors ideally include:
- one push pattern
- one pull pattern
- one lower-body pattern
- optionally one hinge / posterior-chain movement

Each anchor is more useful if it includes:
- exercise
- load
- reps
- whether it was near failure

---

## Decision sequence

### Step 1 — Choose the split
A practical default logic:
- if frequency is unclear, start with a 3-day structure
- if the user can reliably train 4–5 times per week and recovery is reasonable, a 4-day split often works well
- avoid prematurely over-fragmenting into a 5-day split unless the context clearly supports it

### Step 2 — Explain the choice
Do not just announce the split.
Explain:
- why this structure fits frequency,
- why it fits recovery,
- and what problem it solves.

### Step 3 — Define day structure
Give each day a clear role, for example:
- push
- pull
- legs + core
- optional weak-point / accessory day

### Step 4 — Calibrate starting loads
Use recent working-set data when available.
If data is vague, ask a single calibration question before pretending to know exact loads.

### Step 5 — Turn the framework into execution
When the user is actually starting the session, provide:
- today's goal
- warm-up guidance
- working sets
- rest timing
- breathing / execution cues when useful

### Step 6 — Adjust from feedback
Use reported reps, fatigue, difficulty, and movement quality to decide whether to:
- increase load,
- add reps,
- hold steady,
- or stay conservative.

---

## Practical split examples

### 4-day example
- Day 1: back + rear delts + biceps
- Day 2: chest + front/side delts + triceps
- Day 3: legs + core
- Day 4: weak-point or accessory emphasis

### 3-day example
- Day 1: push
- Day 2: pull
- Day 3: legs + core

These are workflow examples, not mandatory laws.
The real point is matching the structure to the user's frequency and recovery reality.

---

## Load calibration guidance

Use this order:
1. recent working-set data first
2. rep + load data to estimate a reasonable starting zone
3. if data is unclear, ask one clarifying question
4. if a movement has no anchor, stay conservative instead of bluffing

Good public-safe guidance sounds like:
- “Start here, then adjust based on your first session feedback.”

Bad guidance sounds like:
- pretending exact loads are known without usable anchor data.

---

## Recommended output structure

### Framework mode
1. why this split
2. weekly day structure
3. main movement categories per day
4. starting load guidance for 1–2 anchor lifts per day when possible
5. what the user should report back after training

### Execution mode
1. today's objective
2. warm-up
3. working sets
4. rest times
5. execution cues
6. what feedback to send back after the session

---

## Memory / storage guidance

If the runtime supports user memory, store:
- preferred split
- current cycle position
- strength anchors
- recent training feedback
- progression decisions

Public-safe rule:
- do not assume private workspace file paths
- do not depend on internal-only knowledge routes in the public version

---

## Guardrails

- Do not overcomplicate the split too early.
- Do not prescribe exact loads without enough anchor data.
- Do not present the framework as fixed forever.
- Do not detach exercise selection from recovery reality.
- Do not depend on internal-only knowledge paths in the public version.

---

## Success criteria

This module succeeds if:
- the user gets a framework they can actually run,
- the starting loads feel realistic,
- and the plan evolves through feedback rather than guesswork.

It fails if:
- the plan is overbuilt,
- the loads are bluff-based,
- or the user gets a template that ignores their real context.
