---
name: verification-before-completion
description: "Use before claiming any work is complete, correct, or passing. Requires running verification steps and confirming output before making success claims. Trigger before wrapping up any task, delivering results, or reporting completion. Do not skip verification even for simple tasks."
---

# Verification Before Completion

## Overview

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification step in this message, you cannot claim it passes.

## The Gate Function

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What step proves this claim?
2. RUN: Execute the FULL verification (fresh, complete)
3. READ: Full output, check result, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = asserting without verifying
```

## Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Task complete | Checklist verified: all criteria met | "I think it's done" |
| Output correct | Output reviewed against spec | "Looks right" |
| Requirements met | Line-by-line checklist against spec | "Everything seems covered" |
| Problem fixed | Original symptom re-tested: resolved | "Should be fixed now" |
| Subagent completed | Actual output inspected | Subagent reports "success" |
| Quality good | Reviewer approved | "Seems high quality" |

## Red Flags — STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!", etc.)
- About to deliver/report without verification
- Trusting subagent success reports without checking output
- Relying on partial verification
- Thinking "just this once"
- **ANY wording implying success without having run verification**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Subagent said success" | Verify output independently |
| "Partial check is enough" | Partial proves nothing |
| "Different words so rule doesn't apply" | Spirit over letter |

## Key Patterns

**Task completion:**
```
✅ [Run checklist] [See: all criteria met] "Task complete"
❌ "Should be done" / "Looks correct"
```

**Requirements coverage:**
```
✅ Re-read spec → Create checklist → Verify each → Report gaps or completion
❌ "Output produced, task complete"
```

**Subagent delegation:**
```
✅ Subagent reports success → Inspect actual output → Verify criteria → Report actual state
❌ Trust subagent report alone
```

**Problem resolution:**
```
✅ Re-test original symptom: passes → "Issue resolved"
❌ "Changed X, should be fixed"
```

## Why This Matters

- Trust is broken when claims are made without evidence
- Incomplete output gets delivered
- Time wasted on false completion → redirect → rework
- Honesty is a core value. Claiming completion without verification is a lie.

## When To Apply

**ALWAYS before:**
- ANY variation of success/completion claims
- ANY expression of satisfaction
- ANY positive statement about work state
- Delivering, reporting, or moving to next task
- Delegating to subagents

**Rule applies to:**
- Exact phrases
- Paraphrases and synonyms
- Implications of success
- ANY communication suggesting completion or correctness

## The Bottom Line

**No shortcuts for verification.**

Run the check. Read the output. THEN claim the result.

This is non-negotiable.
