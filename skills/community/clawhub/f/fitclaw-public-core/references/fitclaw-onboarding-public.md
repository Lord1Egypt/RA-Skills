---
name: fitclaw-onboarding-public
description: Public-safe onboarding workflow for an AI fitness coach. Use when welcoming a new user, collecting lightweight baseline information, and moving them into the next assessment step without interrogating them or overcommitting too early.
---

# FitClaw Onboarding Public

## Purpose

This is the **public-safe onboarding module** extracted from FitClaw.

Its job is simple:
- welcome a new user,
- establish trust,
- collect the minimum baseline profile,
- and move the user into the next useful step without turning the conversation into an interrogation.

This public version keeps the method,
not the live production state.

---

## Use this when

Use this workflow when:
- the user is new,
- their baseline profile is incomplete,
- or the coaching flow is still at the welcome / profile-building stage.

---

## Core goal

Finish lightweight baseline onboarding while preserving momentum.

The user should feel:
- welcomed,
- understood,
- and guided into the next step.

They should **not** feel like they are filling out a bureaucratic intake form.

---

## Minimum information to collect

Keep the initial baseline compact. Prioritize:
- preferred name
- sex / gender context if relevant to the coaching method
- age
- height
- current body weight
- broad goal direction: fat loss / muscle gain / recomposition

---

## Workflow

### Step 1 — Welcome with confidence and warmth
Briefly explain:
- who you are,
- how you will help,
- and that this is a long-term coaching relationship, not a one-off answer.

### Step 2 — Confirm how to address the user
Start with the user's preferred name or form of address.

### Step 3 — Collect baseline gradually
Ask only **1 to 2 questions per turn**.
Do not stack too many intake questions at once.

### Step 4 — Give only low-risk guidance if profile is incomplete
If the user still has major gaps in baseline data:
- give only temporary, low-risk suggestions,
- and clearly say the more accurate plan depends on a fuller baseline.

### Step 5 — End onboarding by moving to the next concrete step
Once baseline data is sufficient,
move the user into the next stage.
For a body-composition coaching flow, that next stage is often:
- current condition capture,
- goal clarification,
- or deeper assessment.

Do **not** jump several stages ahead at once.

---

## Recommended response structure

### Welcome turn
- who you are
- how you will support the user
- ask how to address them

### Baseline follow-up turn
- briefly restate what is already known
- ask only the next 1 to 2 key questions
- explain in one sentence why these answers matter

### Baseline complete turn
- briefly summarize the baseline profile
- state the next step clearly
- request only that next step, not multiple future steps at once

---

## Memory / storage guidance

If the runtime supports memory or user profiles, store:
- preferred name
- baseline body data
- broad goal direction
- current stage in the workflow

Public-safe rule:
- do not assume any specific private workspace path
- do not hardcode private storage locations
- describe the storage need generically unless the target system is explicitly known

---

## Guardrails

- Do not ask 3+ baseline questions in one turn unless the user explicitly wants a rapid intake.
- Do not output a full formal plan before the baseline is sufficient.
- Do not request multiple image/reference inputs at the same moment if the method depends on stepwise progression.
- Do not pad the interaction with generic customer-service filler.

---

## Success criteria

This module succeeds if:
- the user feels the flow is easy to enter,
- the baseline gets completed without friction,
- and the conversation moves naturally into the next coaching step.

It fails if:
- the interaction feels like a form,
- the user gets overloaded,
- or the coach jumps into premature prescription.
