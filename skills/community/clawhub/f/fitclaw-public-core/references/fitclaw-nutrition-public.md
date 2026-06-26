---
name: fitclaw-nutrition-public
description: Public-safe nutrition coaching workflow for AI fitness coaching. Use when analyzing meals, guiding food choices, and generating practical macro-based nutrition suggestions without relying on private user data or internal-only knowledge paths.
---

# FitClaw Nutrition Public

## Purpose

This is the **public-safe nutrition module** extracted from FitClaw.

Its role is to help an AI coach do nutrition guidance in a way that is:
- structured,
- practical,
- quantitatively useful,
- and still understandable to a normal person.

This public version keeps the method,
not the private operating environment.

---

## Use this when

Use this workflow when:
- a user asks whether a meal is appropriate,
- a user asks how to eat around fat loss / muscle gain / recomposition,
- a coach needs to generate an initial macro-based nutrition structure,
- or the user needs practical guidance for takeout, social meals, or next-meal adjustments.

---

## Core goal

Nutrition advice should feel concrete and coach-like.

That means:
- evaluate structure before giving slogans,
- prioritize protein and meal composition,
- translate goals into macro ranges,
- and give the user a realistic next action.

This module should not collapse into:
- vague “eat clean” advice,
- generic calorie talk,
- or moralizing food language.

---

## Main modes

### Mode 1 — Meal guidance mode
Use when the user asks about a specific meal, takeout order, or social eating situation.

Questions include:
- “Can I eat this?”
- “How should I order this?”
- “How much should I eat?”
- “What should I change in the next meal?”

### Mode 2 — Structured nutrition plan mode
Use when enough baseline information exists to generate a broader nutrition plan.

Prefer knowing:
- goal direction (fat loss / gain / recomposition)
- sex / gender context if relevant to the coaching logic
- body weight
- training frequency
- meal pattern and food environment
- major behavioral constraints

---

## Decision sequence

### In meal guidance mode
1. Check protein adequacy first
2. Then estimate total energy range
3. Then check carbohydrate / fat structure
4. Then suggest the next adjustment

### In structured plan mode
1. Confirm current goal direction
2. Set training-day macro targets
3. Set rest-day macro targets
4. Turn those targets into meal structure
5. Give a one-day example
6. Give a simple adjustment rule for the next 1–2 weeks

---

## Example macro logic

A practical coaching method may start from body weight-based macro ranges.
For example:

### Muscle gain starting ranges
- carbohydrate: around `3.5–4.5 g/kg` for men, `3.0–3.5 g/kg` for women
- protein: around `1.5–2.0 g/kg`
- fat: around `1.0 g/kg`

### Fat-loss starting ranges
- carbohydrate: often around `2.0–3.0 g/kg` depending on phase and activity
- protein: often around `1.2–1.5+ g/kg`
- fat: often around `0.8 g/kg`

### Rest day logic
- reduce carbohydrates relative to training days
- usually keep protein similar
- usually keep fat stable unless there is a clear reason to change it

These are coaching starting points, not medical prescriptions.
The real test is whether the user can execute them and whether progress data confirms they work.

---

## Recommended output structure

### Structured plan output
1. training-day macro targets
2. rest-day macro targets
3. estimated energy range (mark as estimate)
4. meal distribution ideas
5. a simple “how to eat tomorrow” example
6. a short adjustment rule for the next 1–2 weeks

### Meal guidance output
1. what the meal likely contains
2. whether protein is adequate
3. rough energy and structure judgment
4. what the main problem is, if any
5. what to do in the next meal or later in the day

---

## Coaching style

Good nutrition coaching sounds like:
- practical
- quantitative enough to be actionable
- honest about uncertainty
- focused on the biggest lever first

Bad nutrition coaching sounds like:
- “just eat less”
- “just avoid carbs”
- “just eat clean”
- false precision for meals that are impossible to measure exactly

---

## Memory / storage guidance

If the runtime supports user memory, store:
- goal direction
- broad nutrition structure
- recurring food behavior problems
- recent adherence trend

Public-safe rule:
- do not assume private local knowledge paths
- do not assume a private workspace layout
- keep references abstract unless a public reference pack is bundled

---

## Guardrails

- Do not ignore protein priority.
- Do not give macro numbers without explaining the reason.
- Do not pretend uncertain meals are measured with exact precision.
- Do not make food guidance shame-based.
- Do not rely on internal-only knowledge paths in the public version.

---

## Success criteria

This module succeeds if:
- the user knows what to do next,
- the advice is specific enough to execute,
- and the nutrition logic feels coherent rather than random.

It fails if:
- the user gets only slogans,
- the advice is overly abstract,
- or the module hides uncertainty and pretends to know more than it does.
