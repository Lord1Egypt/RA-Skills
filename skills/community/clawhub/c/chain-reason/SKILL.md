---
name: chain-reason
description: Explicit multi-step reasoning trace skill for arifOS. Activate when: (1) a question requires more than 2 logical steps to answer; (2) Arif asks to show reasoning, explain how, or walk through logic; (3) a complex decision requires weighing tradeoffs; (4) any multi-constraint problem (e.g., "build me something that does X but not Y"); (5) the words "reason", "explain", "how", "why", "logic", "think through" appear. Produces auditable reasoning traces aligned with arifOS constitutional floors.
metadata: {"openclaw": {"emoji": "⛓️"}}
---

# Chain Reason — Explicit Reasoning Traces

arifOS constitutional floors demand **auditability**. For complex reasoning, show the work.

## When to Use Chain Reason

- Question requires 3+ logical steps
- Decision involves tradeoffs between competing constraints
- Arif asks to see reasoning or explanation
- Something could go wrong in multiple ways
- Multiple valid approaches exist and selection requires judgment

## The 5-Step Trace Format

```
CHAIN REASONING:
1. [GIVEN]  → What is known/established
2. [CONSTRAINT] → What must be satisfied
3. [APPROACH] → How to get from given to solution
4. [STEP-N] → Intermediate steps (numbered)
5. [CONCLUSION] → Final answer with confidence

CONSTRAINT CHECK: [which constraints satisfied / violated]
ALTERNATIVE CONSIDERED: [what else was possible and why rejected]
UNCERTAINTY: [what remains unknown]
```

## Example Trace

**Question:** "Should I deploy arifOS MCP to production now?"

```
CHAIN REASONING:
1. [GIVEN]   → Current vitality 0.82, version 2026.04.11+, nginx proxy configured
2. [CONSTRAINT] → Production requires: stability, rollback plan, human authorization
3. [APPROACH] → Evaluate readiness against deployment checklist
4. [STEP-1]  → Vitality > 0.8 → ✅ sustained healthy
   [STEP-2]  → Version is latest stable → ✅
   [STEP-3]  → Rollback: nginx conf revert = 1 command → ✅ reversible
   [STEP-4]  → Human auth: Arif not yet explicitly approved → ⚠️ FLOOR 13 (Kedaulatan)
5. [CONCLUSION] → Technical readiness: ✅ | Authorization: ❌ → HOLD

CONSTRAINT CHECK: Reversibility ✅ | Authorization ❌ (HOLD triggered)
ALTERNATIVE CONSIDERED: Deploy anyway → violates Floor 13, not acceptable
UNCERTAINTY: What constitutes explicit approval from Arif in this context
```

## Tradeoff Weighing Format

For decisions with competing goods:

```
TRADEOFF ANALYSIS:
  [+W] [Factor A] → why it favors option X
  [+W] [Factor B] → why it favors option X
  [-W] [Factor C] → why it favors option Y
  [-W] [Factor D] → why it favors option Y

NET: [X/Y/EQUAL] — [dominant reason]
RISK: [what could go wrong with the chosen option]
MITIGATION: [how to reduce that risk]
VERDICT: [SEAL/CAUTION/HOLD]
```

## Epistemic Trace (for knowledge questions)

```
EVIDENCE CHAIN:
  [1] OBS: <direct observation or fact>
  [2] DER: <derived from above>
  [3] INT: <interpretation (label as such)>
  [4] SPEC: <speculation (label as such)>

CONFIDENCE: [HIGH/MEDIUM/LOW] — [reason]
GAP: [what evidence is missing]
```

## Rules

1. **Number every step** — enables traceable audit
2. **Label assumptions** — don't silently assume, state explicitly
3. **Show alternatives** — why this approach and not another
4. **End with a verdict** — SEAL / CAUTION / HOLD / VOID
5. **Keep it tight** — if the trace exceeds 20 steps, the problem is not yet decomposed enough
