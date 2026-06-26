---
name: systematic-problem-solving
description: "Use when actively debugging a reproducible problem — errors, regressions, or failed outputs that need root-cause diagnosis. Trigger ONLY when the user is troubleshooting a concrete, reproducible issue (e.g. error messages, test failures, broken behavior). Do NOT trigger for: planning, brainstorming, creative tasks, straightforward one-step tasks, general questions, or situations where the user wants immediate simple fixes."
---

# Systematic Problem Solving

## Overview

Random fixes waste time and create new problems. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of problem-solving.**

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## When to Use

Use for ANY unexpected situation:
- Task produces wrong output
- Process breaks or stalls
- Unexpected behavior from a tool or system
- Results don't match expectations
- A previous fix didn't work

**Use this ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

**Don't skip when:**
- Issue seems simple (simple problems have root causes too)
- You're in a hurry (rushing guarantees rework)
- Someone wants it fixed NOW (systematic is faster than thrashing)

## The Four Phases

You MUST complete each phase before proceeding to the next.

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read Error Messages or Failure Signals Carefully**
   - Don't skip past errors or warnings
   - They often contain the exact solution
   - Note specific locations, codes, or descriptions

2. **Reproduce Consistently**
   - Can you trigger it reliably?
   - What are the exact conditions?
   - Does it happen every time?
   - If not reproducible → gather more data, don't guess

3. **Check Recent Changes**
   - What changed that could cause this?
   - New inputs, config changes, environmental differences
   - What was different when it last worked?

4. **Gather Evidence in Multi-Component Systems**

   **WHEN the system has multiple components (e.g., input → process → output, API → service → storage):**

   **BEFORE proposing fixes, add diagnostic instrumentation:**
   ```
   For EACH component boundary:
     - Log what data enters the component
     - Log what data exits the component
     - Verify config/state propagation
     - Check state at each layer

   Run once to gather evidence showing WHERE it breaks
   THEN analyze evidence to identify the failing component
   THEN investigate that specific component
   ```

   **Example (multi-layer process):**
   ```
   Layer 1: Input received?
   → Log: "Input value: [X]"

   Layer 2: Processing step applied correctly?
   → Log: "After step A: [Y]"

   Layer 3: Output produced correctly?
   → Log: "Final output: [Z], expected: [W]"
   ```

   **This reveals:** Which layer fails (input ✓, processing ✗, output not reached)

5. **Trace Data Flow**

   **WHEN the error is deep in a process:**
   - Where does the bad value or wrong result originate?
   - What produced this with the wrong value?
   - Keep tracing back until you find the source
   - Fix at source, not at symptom

### Phase 2: Pattern Analysis

**Find the pattern before fixing:**

1. **Find Working Examples**
   - Locate similar working cases in the same project
   - What works that's similar to what's broken?

2. **Compare Against References**
   - If implementing a pattern, read the reference COMPLETELY
   - Don't skim — read every detail
   - Understand the pattern fully before applying

3. **Identify Differences**
   - What's different between working and broken?
   - List every difference, however small
   - Don't assume "that can't matter"

4. **Understand Dependencies**
   - What does this component depend on?
   - What settings, config, or inputs does it assume?

### Phase 3: Hypothesis and Testing

**Scientific method:**

1. **Form Single Hypothesis**
   - State clearly: "I think X is the root cause because Y"
   - Write it down
   - Be specific, not vague

2. **Test Minimally**
   - Make the SMALLEST possible change to test hypothesis
   - One variable at a time
   - Don't fix multiple things at once

3. **Verify Before Continuing**
   - Did it work? Yes → Phase 4
   - Didn't work? Form NEW hypothesis
   - DON'T add more fixes on top

4. **When You Don't Know**
   - Say "I don't understand X"
   - Don't pretend to know
   - Ask for help or research more

### Phase 4: Implementation

**Fix the root cause, not the symptom:**

1. **Define a Verification Case**
   - Simplest possible reproduction of the problem
   - Must be checkable before and after fix
   - MUST have this before fixing

2. **Implement Single Fix**
   - Address the root cause identified
   - ONE change at a time
   - No "while I'm here" improvements
   - No bundled changes

3. **Verify Fix**
   - Problem resolved now?
   - No other things broken?
   - Issue actually gone?

4. **If Fix Doesn't Work**
   - STOP
   - Count: How many fixes have you tried?
   - If < 3: Return to Phase 1, re-analyze with new information
   - **If ≥ 3: STOP and question the approach (step 5 below)**
   - DON'T attempt Fix #4 without discussing the approach

5. **If 3+ Fixes Failed: Question the Approach**

   **Pattern indicating a structural problem:**
   - Each fix reveals new coupling or dependency in a different place
   - Fixes require large-scale changes to implement
   - Each fix creates new symptoms elsewhere

   **STOP and question fundamentals:**
   - Is this approach fundamentally sound?
   - Are we "sticking with it through sheer inertia"?
   - Should we reconsider the approach vs. continue fixing symptoms?

   **Discuss with the user before attempting more fixes.**

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, check results"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing the issue
- **"One more fix attempt" (when already tried 2+)**
- **Each fix reveals a new problem in a different place**

**ALL of these mean: STOP. Return to Phase 1.**

**If 3+ fixes failed:** Question the approach (see Phase 4.5)

## User Signals You're Doing It Wrong

**Watch for these redirections:**
- "Is that not happening?" — You assumed without verifying
- "Will it show us...?" — You should have added evidence gathering
- "Stop guessing" — You're proposing fixes without understanding
- "We're stuck?" (frustrated) — Your approach isn't working

**When you see these:** STOP. Return to Phase 1.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple problems. |
| "Emergency, no time for process" | Systematic problem-solving is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new problems. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = structural problem. Question approach, don't fix again. |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read signals, reproduce, check changes, gather evidence | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare | Identify differences |
| **3. Hypothesis** | Form theory, test minimally | Confirmed or new hypothesis |
| **4. Implementation** | Define verification case, fix, verify | Problem resolved |

## When Process Reveals "No Root Cause"

If systematic investigation reveals the issue is truly environmental, timing-dependent, or external:

1. You've completed the process
2. Document what you investigated
3. Implement appropriate handling (retry, fallback, error message)
4. Add monitoring or logging for future investigation

**But:** 95% of "no root cause" cases are incomplete investigation.

## Real-World Impact

- Systematic approach: 15-30 minutes to resolve
- Random fixes approach: 2-3 hours of thrashing
- First-time resolution rate: 95% vs 40%
- New problems introduced: Near zero vs common
