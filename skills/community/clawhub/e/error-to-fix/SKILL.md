---
name: error-to-fix
description: >
  Use when (1) user pastes a programming error message, stack trace, or exception and asks what went wrong. 
  (2) user says "this error means", "why is this broken", "what's the fix", or "how to resolve this error". 
  (3) user pastes a bug description and asks for root cause analysis and solution. 
license: MIT
metadata:
  version: "1.0"
  category: productivity
  author: wangjipeng
  sources:
    - https://github.com/MiniMax-AI/skills
---

# Error to Fix

Use when (1) user pastes a programming error message, stack trace, or exception and asks what went wrong. (2) user says "this error means", "why is this broken", "what's the fix", or "how to resolve this error". (3) user pastes a bug description and asks for root cause analysis and solution.

## Core Position

This skill solves the specific problem of: *an error message is cryptic — the user needs a plain-language explanation of what went wrong and how to fix it.*

This skill IS NOT:
- A code rewrite tool — it explains and suggests fixes, does not rewrite entire files
- A debugging environment — it analyzes reported errors, does not run code
- A deployment tool — it does not fix production issues, only advises

This skill IS activated ONLY when: an error message or stack trace + explanation/fix intent are both present.

## Modes

### `/error-to-fix`

**Default mode.** Analyzes the error and provides explanation, root cause, and fix suggestions.

When to use: User pastes an error and wants to understand and resolve it.

### `/error-to-fix/root-cause`

Focuses on the underlying system-level cause, not just the immediate symptom.

When to use: User wants deeper understanding beyond the surface-level fix.

### `/error-to-fix/prevent`

Suggests patterns and practices to prevent this error from recurring.

When to use: User is in a review or learning context and wants to avoid the error long-term.

## Execution Steps

### Step 1 — Parse the Error

1. Receive error input (pasted text, stack trace, screenshot text)
2. Detect error type:
   - **SyntaxError**: Python/JavaScript parse failure — usually a typo or missing token
   - **RuntimeError/Exception**: code ran but crashed — check types, imports, null refs
   - **ImportError / ModuleNotFoundError**: missing or misnamed dependency
   - **ConnectionError / Timeout**: network, database, or API connectivity issue
   - **PermissionError / AccessDenied**: file or resource permission problem
   - **AssertionError / Test failure**: behavior mismatch against expected result
   - **Custom error**: non-standard error from user code or library
3. Extract key identifiers from the error:
   - Error type name (first word in traceback or error class)
   - File path and line number (where error originated)
   - Variable/state values at the point of failure
   - Version information if present (library versions, Python/Node version)

### Step 2 — Identify Root Cause

For each identified error type:

| Error Type | Common Root Cause | Quick Diagnostic |
|---|---|---|
| SyntaxError | Missing `)`, `:`, or `}` | Check line number and surrounding lines |
| ModuleNotFoundError | Typo in import, missing package | `pip install` / `npm install` |
| TypeError | Wrong type passed to function | Check the actual type vs. expected type |
| ReferenceError | Variable used before assignment | Check variable initialization |
| ConnectionError | Wrong URL, firewall, service down | Verify URL and network access |
| ImportError | Circular import, wrong path | Check `__init__.py` and import order |
| ValueError | Invalid argument value | Check the value against allowed range |
| KeyError | Missing dict key | Check if key exists before access |

### Step 3 — Deliver Explanation

Structure each response as:

1. **What happened** (one sentence): plain-language description of the error
2. **Why it happened**: root cause — what the error is actually telling you
3. **How to fix**: specific, actionable steps with code before/after if applicable
4. **How to prevent**: one practice or pattern to avoid this error in the future

### Step 4 — Validate

- Error type is correctly identified
- Root cause is specific, not generic ("something is wrong")
- Fix applies to the exact error — not a similar but different error
- No code changes that contradict or undo the user's existing code

## Mandatory Rules

### Do not

- Do not guess at the root cause if the error message is unambiguous — use what the error says
- Do not provide fixes that require installing packages or modifying files the user hasn't mentioned
- Do not change the user's code logic beyond the minimal fix
- Do not dismiss the error as "not a problem" without explaining it

### Do

- Quote the specific error message in your explanation
- Provide a minimal, targeted fix — not a rewrite of the entire file
- Distinguish between quick fixes and proper architectural solutions
- Ask for the relevant code snippet when the error alone is insufficient to diagnose

## Quality Bar

**A good output:**
- Error type is correctly identified and named
- Root cause is specific and explains why the error occurred in this context
- Fix is minimal and directly addresses the cause
- Prevention tip is actionable and relevant to the error type

**A bad output:**
- "Something went wrong" as the explanation
- Fix requires changing unrelated parts of the codebase
- Root cause contradicts what the error message states
- Provides 5 different possible causes when the error is unambiguous

## Good vs. Bad Examples

| Scenario | Bad Output | Good Output |
|---|---|---|
| Python TypeError | "Type error occurred" | "TypeError: list.append expects str, got int — add `str()` cast around the input" |
| Node ModuleNotFoundError | "Module is missing" | "ModuleNotFoundError: 'requests' not in requirements.txt — run `pip install requests`" |
| React undefined is not an object | "Something is undefined" | "The error means `props.user.address` is accessed before `user` is set. Add a guard: `props.user?.address`" |
| Connection refused | "Network is down" | "ECONNREFUSED: server at localhost:5432 is not accepting connections. Is PostgreSQL running?" |

## References

- `references/` — Error type taxonomy, common stack trace patterns by language, quick-fix cheat sheet