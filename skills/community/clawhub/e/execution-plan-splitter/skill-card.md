## Description:

Splits large goals into 30/60/90-day execution paths, stage deliverables, resource needs, and exit criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, developers, and planning teams use this skill to turn long-term goals, resource constraints, and time windows into review-ready 30/60/90-day plans, milestones, resource requests, and stop conditions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plans may be incomplete or misleading when the input goal, constraints, or time window are underspecified.

Mitigation: Treat outputs as reviewable drafts and confirm assumptions, missing inputs, resource needs, and exit criteria before execution.

Risk: Planning inputs may contain personal, confidential, or sensitive business material.

Mitigation: Provide only material suitable for local summarization and redact sensitive details before processing.

Risk: The included script contains inactive audit modes that can broaden the perceived scope of the package.

Mitigation: Remove or document inactive audit modes before further maintenance or distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/execution-plan-splitter)
- [README](artifact/README.md)
- [Structured output specification](artifact/resources/spec.json)
- [Output template](artifact/resources/template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or JSON from local planning inputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reviewable drafts, executable checklists, explicit to-be-confirmed items, and optional local file output when run with python3.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
