## Description:

Watch your agent's identity evolve from its own experience through continuous discovery, genome snapshots, and growth tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liveneon](https://clawhub.ai/user/liveneon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect agents to the Live Neon platform, sync content sources, run identity discovery, review proposed beliefs and responsibilities, compare identity snapshots, and fetch evolved prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send behavioral observations, user corrections, quotes, and connected-source material to a third-party service.

Mitigation: Use it only with approved agents and sources, apply redaction rules before upload, and scope credentials to the intended organization.

Risk: Fetched identity prompts and promoted beliefs can influence future agent behavior.

Mitigation: Review and approve identity changes locally before using them as runtime instructions, and keep a rollback path to a known prompt or snapshot.

Risk: Scheduled or proactive operation can create ongoing uploads and behavior changes without fresh consent.

Mitigation: Enable schedules only after explicit approval, with documented cadence, monitoring, and a process to disable or revoke access.

Risk: Connected content sources may include untrusted external material.

Mitigation: Treat imported content and generated prompts as untrusted until reviewed, especially before promotion into persistent agent identity.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liveneon/skills/agent-identity-evolution)
- [Live Neon Agent Platform](https://persona.liveneon.ai)
- [Live Neon](https://liveneon.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Live Neon API token and may return identity data, job status, source sync results, observations, diffs, and evolved prompts.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
