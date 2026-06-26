---
name: fitclaw-hydration-public
description: Public-safe hydration support workflow for AI fitness coaching. Use when calculating a simple daily hydration target, setting lightweight reminders, and helping users build a sustainable hydration habit without fake precision.
---

# FitClaw Hydration Public

## Purpose

This is the **public-safe hydration module** extracted from FitClaw.

Its role is not to create fake precision.
Its role is to help users:
- understand a reasonable hydration target,
- turn that target into an easy daily rhythm,
- and stay consistent through light reminders and check-ins.

---

## Use this when

Use this workflow when:
- a user wants help with daily water intake,
- hydration habits are weak or inconsistent,
- or hydration is part of a broader coaching routine.

---

## Core goal

Make hydration actionable and sustainable.

The user should feel:
- this is simple enough to follow,
- specific enough to matter,
- and not so precise that it becomes annoying.

---

## Minimum inputs

To estimate a hydration target, preferably know:
- sex / gender context if relevant to the coaching logic
- current body weight
- whether it is a training day
- whether the user wants reminders

If some information is missing, use a temporary estimate and label it as temporary.

---

## Example target logic

A simple baseline approach:
- male baseline: `2.5L`
- female baseline: `2.0L`
- adjust `±0.2L` for every `±10kg` from a `60kg` reference
- add `+0.5L` on training days
- keep the result within a reasonable band such as `1.8L ~ 3.5L`

This is a practical coaching estimate, not a medical prescription.

---

## Workflow

### Step 1 — Estimate a daily target
Use the user's body weight and training-day status to produce a practical hydration goal.

### Step 2 — Explain the logic simply
Do not just state a number.
Briefly explain:
- baseline amount,
- training adjustment,
- final target.

### Step 3 — Turn the number into an easy schedule
Translate the target into a few time anchors, for example:
- morning
- late morning / afternoon
- training window
- post-training if relevant

### Step 4 — Use light reminders only
Reminders should feel supportive, not nagging.
A good rule is a few checkpoints per day, plus a training-day top-up reminder when relevant.

### Step 5 — End the day with a lightweight reflection
Use a simple check-in:
- roughly hit target / missed it / overshot it,
- and what to adjust tomorrow.

---

## Recommended response structure

### Initial hydration setup
- daily target
- brief explanation of how it was estimated
- simple distribution suggestion
- ask whether the user wants reminder timing built around their routine

### Routine-based reminder setup
- propose a few concrete time anchors
- explain how training changes hydration needs
- keep the tone practical and easy

### End-of-day review
- ask whether the target was roughly met
- suggest one small improvement for tomorrow

---

## Memory / storage guidance

If the runtime supports user memory, store:
- hydration target
- reminder preference
- rough adherence trend

Public-safe rule:
- do not assume private file paths
- do not require a specific local workspace layout in the public version

---

## Guardrails

- Do not pretend to know the user's exact water intake when you do not.
- Do not present hydration to the milliliter as if it were perfectly tracked.
- Do not use long moralizing lectures.
- Do not treat hydration as the sole lever of progress.

---

## Success criteria

This module succeeds if:
- the target feels believable,
- the schedule feels easy to follow,
- and the user can actually keep the habit going.

It fails if:
- the target feels random,
- the reminders feel oppressive,
- or the method turns into fake precision.
