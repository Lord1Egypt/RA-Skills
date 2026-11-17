## Description:

A framework for AI agents to systematically record, index, and review detailed failure events to improve memory accuracy and reduce survivor bias.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sly27](https://clawhub.ai/user/sly27)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agent operators use this skill to create and maintain a structured FAILURES.md log that captures failures, lessons, indexes, and recurring patterns for later review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Failure logs may accidentally capture secrets, session details, private customer data, or unreleased business information.

Mitigation: Use the skill only in workspaces where a long-lived local failure log is acceptable, and redact credentials and sensitive details before writing entries.

Risk: Failure records can preserve incomplete or misleading postmortems if they are not reviewed.

Mitigation: Review entries periodically and update lessons or status when better information becomes available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sly27/skills/failures-md)
- [FAILURES.md reference template](artifact/FAILURES.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance and failure-log template content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable output; the skill guides creation, indexing, and review of local failure records.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
