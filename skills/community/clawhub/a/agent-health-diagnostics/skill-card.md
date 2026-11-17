## Description:

Diagnoses common OpenClaw agent failures including heartbeat spam, API rate limit cascades, channel death loops, and memory or embedding errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agenthyjack](https://clawhub.ai/user/agenthyjack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to diagnose misbehaving OpenClaw agents, inspect service logs and configuration, and choose fixes for common health failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Operational commands may change OpenClaw configuration or restart services if applied without review.

Mitigation: Review commands before running them, back up OpenClaw configuration first, and apply changes only to agents and services the operator administers.

Risk: The linked external scripts are outside the inspected artifact.

Mitigation: Review and scan any downloaded scripts separately before use.

## Reference(s):

- [Agent Health Diagnostics on ClawHub](https://clawhub.ai/agenthyjack/skills/agent-health-diagnostics)
- [Collective Skills references](https://github.com/Bobalouie44/collective-skills/tree/main/references)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are diagnostic and operational; review them before running against administered OpenClaw services.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter and _meta.json list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
