---
name: requesting-review
description: "Use when completing significant work to verify it meets requirements before delivery. Trigger after finishing a major task, completing a project phase, or before submitting results to a stakeholder. Do not trigger for minor or trivial tasks where review would be disproportionate."
---

# Requesting Review

Dispatch a reviewer subagent to catch issues before delivery. The reviewer gets precisely crafted context for evaluation — never your session's history. This keeps the reviewer focused on the work product, not your thought process, and preserves your own context for continued work.

**Core principle:** Review early, review often.

## When to Request Review

**Mandatory:**
- After each task in subagent-driven execution
- After completing a major deliverable
- Before final delivery to stakeholder

**Optional but valuable:**
- When stuck (fresh perspective)
- Before significant rework (baseline check)
- After resolving a complex problem

## How to Request

**1. Define scope of work to review:**
- What was produced
- What it should accomplish (spec or requirements)
- Any specific concerns to check

**2. Dispatch reviewer subagent:**

Use the following template:

```markdown
## Review Request

### What Was Produced
[Description of the output — what it is and where it lives]

### Requirements / Spec
[What the output is supposed to accomplish]

### Specific Concerns (optional)
[Any areas you're unsure about]

### Your Task
Review the output against the requirements.

Report:
- **Critical:** Issues that must be fixed before delivery (wrong, missing, broken)
- **Important:** Issues that should be fixed soon (gaps, inconsistencies)
- **Minor:** Nice-to-have improvements
- **Assessment:** Ready to deliver / Needs fixes
```

**3. Act on feedback:**
- Fix Critical issues immediately
- Fix Important issues before proceeding
- Note Minor issues for later
- Push back if reviewer is wrong (with reasoning)

## Example

```
[Just completed Task 2: Draft executive summary]

You: Let me request review before proceeding.

[Dispatch reviewer subagent]
  WHAT_WAS_PRODUCED: Executive summary for Q1 report
  REQUIREMENTS: Task 2 from docs/plans/q1-report-plan.md
  SPECIFIC_CONCERNS: Not sure if the tone matches the audience

[Subagent returns]:
  Strengths: Clear structure, covers all key points
  Issues:
    Important: Tone is too technical for executive audience
    Minor: Missing one metric from requirements
  Assessment: Needs fixes before delivery

[Fix tone and add missing metric]
[Continue to Task 3]
```

## Integration with Workflows

**Subagent-Driven Execution:**
- Review after EACH task
- Catch issues before they compound
- Fix before moving to next task

**Executing Plans:**
- Review after each checkpoint
- Get feedback, apply, continue

**Ad-Hoc Work:**
- Review before final delivery
- Review when stuck

## Red Flags

**Never:**
- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Critical or Important issues
- Argue with valid feedback

**If reviewer is wrong:**
- Push back with clear reasoning
- Show evidence that the output meets requirements
- Request clarification
