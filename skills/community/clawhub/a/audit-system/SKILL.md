---
name: audit-system
description: "Perform structured audits on code, workflows, prompts, and products. Use when: (1) Something is not working as expected, (2) User asks for review or feedback, (3) A system behaves inconsistently, (4) Before deploying or shipping, (5) When optimizing performance or UX, (6) When debugging recurring issues."
---

# Audit System Skill

Perform structured audits and generate actionable reports with clear severity, evidence, and fixes.

This is an instruction-only skill.
It does not perform external verification, blockchain auditing, or legal certification.

---

## Quick Reference

| Situation | Action |
|----------|--------|
| Code not working | Run Code Audit |
| Workflow failing | Run Workflow Audit |
| UX feels bad | Run Product Audit |
| Prompt/AI unstable | Run Prompt Audit |
| Before deploy | Run Full Audit |
| Repeated bugs | Focus on root-cause analysis |

---

## Audit Types

### 1. Code Audit
Check:
- logic errors
- missing validation
- security risks
- bad patterns
- performance issues

---

### 2. Workflow Audit
Check:
- broken steps
- missing retries
- failure points
- unnecessary complexity
- automation gaps

---

### 3. Product Audit
Check:
- onboarding friction
- unclear UX
- conversion blockers
- trust issues
- missing features

---

### 4. Prompt / Agent Audit
Check:
- unclear instructions
- conflicting rules
- missing constraints
- unstable outputs
- over-autonomy risks

---

## Audit Process

### Step 1 — Define Scope
Identify:
- what is being audited
- expected behavior
- actual behavior
- available data

---

### Step 2 — Inspect
Analyze inputs:
- code
- prompts
- configs
- logs
- workflows

Look for:
- inconsistencies
- missing logic
- unclear flow
- hidden risks

---

### Step 3 — Detect Issues

For each issue:
- describe clearly
- link to evidence
- explain impact

---

### Step 4 — Classify Severity

- **Critical** → breaks system / risk of loss
- **High** → likely failure
- **Medium** → important weakness
- **Low** → improvement

---

### Step 5 — Recommend Fixes

For each issue:
- what to fix
- why it matters
- exact fix
- quick workaround

---

### Step 6 — Prioritize

Always output:
- top 3 issues
- quick wins
- long-term fixes

---

## Output Format

# Audit Report

## Scope
- Target:
- Type:
- Evidence:
- Limitations:

## Findings

### [Severity] Title
- Area:
- Problem:
- Evidence:
- Impact:
- Fix:

## Priority Actions
1. ...
2. ...
3. ...

## Quick Wins
- ...
- ...

## Long-Term Improvements
- ...

## Open Questions
- ...

---

## Behavior Rules

- Be precise, not vague
- Do not invent missing data
- Do not exaggerate severity
- Do not claim certification
- Focus on actionable fixes

---

## When NOT to use this skill

Do NOT use for:
- legal certification
- financial compliance guarantees
- blockchain verification
- cryptographic proof generation

Only analyze what is provided.

---

## Upgrade Path (Advanced)

If repeated issues appear:
- suggest system redesign
- suggest automation improvements
- suggest monitoring/logging additions