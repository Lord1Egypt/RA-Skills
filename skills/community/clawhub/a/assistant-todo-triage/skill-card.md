## Description:

Produce a deterministic deadline and priority digest from a local to-do JSON snapshot, without changing tasks or sending data to a service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aniruth1011](https://clawhub.ai/user/aniruth1011)

### License/Terms of Use:

MIT-0

## Use Case:

Personal assistant users use this skill to identify overdue, due-today, and upcoming tasks from an authorized local snapshot. It helps prioritize follow-up while preserving task IDs and leaving the source list unchanged.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is benign but medium confidence because one referenced component was only partly inspected.

Mitigation: Review the remaining component or wait for a complete scan before using private task data.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/aniruth1011/skills/assistant-todo-triage)
- [Publisher profile](https://clawhub.ai/user/aniruth1011)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON task digest with a concise natural-language summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Groups open tasks as overdue, due today, upcoming, and undated, with completion counts; preserves IDs and orders by due date, priority, then ID.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
