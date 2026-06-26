---
name: doubt-list
description: |
  Generate a Cartesian verification artifact before trusting a plan, claim,
  implementation, or release. Turn confidence into explicit checks.
version: 0.1.0
---

# Doubt List

## Purpose

Convert confidence into verifiable skepticism.

This skill asks: what must be checked before we trust this?
It is not for performative negativity. It exists to separate fact, inference, preference, and guess.

## Activate when

Use this skill when:
- a plan sounds persuasive but has not been stress-tested
- a release is nearing shipment
- a claim is important, risky, or governance-sensitive
- the team wants a verification checklist before execution
- consequences of error are high

## Inputs

Expected inputs may include:
- a feature or release plan
- a design proposal
- a decision memo
- a claim or assertion set
- implementation notes or test results

## Classification rule

Before generating doubts, classify each major statement as one of:
- Fact — directly established or evidenced
- Inference — reasoned from available evidence
- Preference — normative or taste-based judgment
- Guess — plausible but currently unverified

Unclassified claims are not ready for trust.

## Doubt categories

Always produce doubts across five categories.

### 1. Happy path doubts
- What must go right for the main story to hold?
- Which "obvious" success condition has not actually been verified?

### 2. Edge case doubts
- What happens under uncommon but realistic conditions?
- What retries, partial failures, or weird inputs have been ignored?

### 3. Boundary doubts
- What breaks at minimum, maximum, empty, overloaded, concurrent, or delayed conditions?

### 4. Ambiguity doubts
- Which terms or promises could be interpreted in more than one way?
- Which claims sound specific but are not operationally defined?

### 5. Evil demon scenarios
- What if the most confidence-inducing assumption is false?
- What if the evidence is incomplete, stale, biased, or misread?
- What catastrophic but low-frequency scenario would embarrass the team later?

## Procedure

### Step 1 — State the object of doubt
Name exactly what is being reviewed.

### Step 2 — Classify key claims
Mark each important claim as Fact / Inference / Preference / Guess.

### Step 3 — Generate doubts across all five categories
Do not stop at happy path concerns.

### Step 4 — Convert doubts into checks
Every serious doubt should map to a concrete verification action.

### Step 5 — Assign release posture
Conclude whether the work is:
- Clear enough to proceed
- Proceed with conditions
- Do not proceed yet

## Output artifact

```markdown
## Doubt List

### Object of Review
- ...

### Claim Classification
- Claim: ... -> Fact / Inference / Preference / Guess

### Happy Path Doubts
- Doubt: ...
- Verification: ...

### Edge Case Doubts
- Doubt: ...
- Verification: ...

### Boundary Doubts
- Doubt: ...
- Verification: ...

### Ambiguity Doubts
- Doubt: ...
- Verification: ...

### Evil Demon Scenarios
- Doubt: ...
- Verification: ...

### Clarity Gate
- Clear: ...
- Not clear: ...

### Release Posture
- Proceed / Proceed with conditions / Do not proceed yet
```

## Guardrails

- Do not confuse disagreement with evidence.
- Do not mark a guess as fact because the team likes it.
- Do not stop at implementation QA; plans, memos, and claims also need doubt.
- Do not generate abstract doubts without corresponding verification actions.

## Failure modes

Common failure modes:
- only checking the happy path
- writing doubts that are too vague to test
- skipping claim classification
- treating rhetorical confidence as evidence
- using this skill to block progress without naming concrete conditions for trust

## Escalation points

Escalate when:
- the key claim cannot be verified with currently available evidence
- the team is relying on guesswork for a high-consequence decision
- release pressure is overriding clarity
- terms in the proposal are too ambiguous for meaningful review

## Completion condition

This skill is complete only when a reviewer could pick up the output and know what to verify next.