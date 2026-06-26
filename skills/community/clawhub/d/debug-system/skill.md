---
name: debug-system
description: Identify root causes of errors and failures in code, APIs, workflows, and systems. Provides structured debugging steps, explanations, and fixes.
---

# Debug System

Find, explain, and fix errors by identifying the root cause.

Use this skill when:
- something is not working
- an error message appears
- a workflow fails
- an API request breaks
- behavior does not match expectations
- the same issue keeps happening

This is an instruction-only skill.
It does not execute code or access external systems unless the user provides the data.

---

## What this skill does

This skill helps an agent:

- analyze errors and unexpected behavior
- identify the real root cause (not just symptoms)
- explain what went wrong in simple terms
- suggest concrete fixes
- guide step-by-step debugging
- prevent the issue from happening again

---

## What this skill does not do

This skill does not:

- guess without evidence
- invent missing logs or results
- claim something is fixed without validation
- access external systems without user input
- provide fake certainty

---

## Inputs

Use what the user provides:

- error messages
- logs
- code snippets
- API responses
- workflow steps
- expected vs actual behavior
- screenshots or descriptions

If information is missing, state assumptions clearly.

---

## Debugging process

### Step 1 — Understand the problem
Identify:
- expected behavior
- actual behavior
- when the issue occurs
- what changed recently

---

### Step 2 — Analyze the error

Look for:
- exact error message
- stack trace (if available)
- failing step or node
- invalid inputs
- missing fields
- wrong data types
- permission/auth issues
- network/API failures

---

### Step 3 — Find root cause

Do not stop at symptoms.

Ask:
- what caused this error?
- what condition triggered it?
- is this reproducible?
- is it a config issue, logic issue, or external failure?

---

### Step 4 — Propose fixes

For each issue, provide:

- root cause
- why it happens
- exact fix
- alternative fix (if needed)
- how to verify the fix

---

### Step 5 — Prevent recurrence

Suggest:
- validation checks
- better error handling
- logging improvements
- retry mechanisms
- safer defaults

---

## Output format

# Debug Report

## Problem Summary
- Expected:
- Actual:
- Context:

## Root Cause
- ...

## Evidence
- ...

## Fix

### Recommended Fix
- ...

### Alternative Fix
- ...

## Verification Steps
1. ...
2. ...
3. ...

## Prevention
- ...
- ...

## Open Questions
- ...
- ...

---

## Behavior rules

- Focus on root cause, not just symptoms
- Be clear and actionable
- Do not assume missing data without stating it
- Prefer simple fixes over complex ones
- Explain in a way the user can follow step-by-step

---

## Quality checklist

Before finishing, ensure:

- root cause is identified
- fix is actionable
- verification steps are clear
- no fake assumptions
- prevention is included

---

## When not to use this skill

Do not use this skill for:
- general explanations without a problem
- theoretical discussions without real issues
- tasks unrelated to debugging

Use only when there is a failure, bug, or unexpected behavior.