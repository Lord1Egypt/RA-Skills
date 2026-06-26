# Discovery and Diagnosis Playbook

Use this playbook when a request is ambiguous, high impact, or politically sensitive.

## Discovery Core

Capture these six items before making recommendations:

1. Decision question
2. Business objective
3. Time and budget constraints
4. Existing baseline metrics
5. Stakeholders and decision rights
6. Failure conditions to avoid

## Fast Discovery Prompts

Use focused prompts, not long interviews:
- What decision must be made now?
- What happens if we do nothing for 90 days?
- Which constraint is hardest right now: time, money, people, or risk?
- Who can approve this and who can block it?
- What metric would prove this worked?

## Problem Tree Method

Structure diagnosis in three layers:

- Symptoms: what is visible now
- Drivers: what causes those symptoms
- Root causes: what must change to remove the drivers

If evidence is weak, mark each driver with confidence: High, Medium, Low.

## Assumption Register

Track assumptions in this format:

| Assumption | Why it matters | How to test | Owner | Date |
|------------|----------------|------------|-------|------|
| Example | Changes recommendation | Interview top account | Analyst | YYYY-MM-DD |

Any assumption that can flip the recommendation must get a test plan.

## Stakeholder Map

Classify each key stakeholder:

| Stakeholder | Role | Influence | Likely stance | Action |
|-------------|------|-----------|---------------|--------|
| Sponsor | Budget owner | High | Supportive | Weekly pre-wire |
| Ops lead | Implementation | High | Concerned | Co-design rollout |

## Discovery Exit Criteria

Discovery is complete when:
- Decision objective is explicit
- Constraints are documented
- Root-cause hypotheses are testable
- Decision rights are clear
- No unknown with critical impact is hidden
