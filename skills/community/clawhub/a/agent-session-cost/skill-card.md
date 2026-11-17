## Description:

Track and analyze OpenClaw session costs by parsing transcripts, calculating per-model spend, setting budgets, and alerting on overruns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imaflytok](https://clawhub.ai/user/imaflytok)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to inspect OpenClaw session transcript costs, summarize daily spend, break down spend by model, and configure budget alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads broad OpenClaw session transcript files that may contain sensitive conversation or usage metadata.

Mitigation: Review and narrow the commands to the specific agent or session paths needed before running them.

Risk: The skill suggests a recurring heartbeat budget check.

Mitigation: Enable recurring checks only when intentional, and choose a budget threshold and cadence appropriate for the workspace.

Risk: Security evidence reports hidden external endpoint metadata unrelated to the cost-tracking purpose.

Mitigation: Ask the publisher to clarify or remove the endpoint metadata before installation or operational use.

## Reference(s):

- [Agent Session Cost on ClawHub](https://clawhub.ai/imaflytok/skills/agent-session-cost)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local cost summaries and budget alert guidance from OpenClaw session transcript files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
