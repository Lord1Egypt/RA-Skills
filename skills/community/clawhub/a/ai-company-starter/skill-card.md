## Description:

AI Company Starter scaffolds a multi-agent OpenClaw company with management, HR, engineering, sales, marketing, and finance roles, including persistent memory files and Telegram group coordination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gdp6539](https://clawhub.ai/user/gdp6539)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to bootstrap a coordinated set of AI agent roles for company-style workflows, including role files, memory files, and team communication setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes persistent agent state and generated memory/user files into an OpenClaw workspace, including a hard-coded owner identity in generated USER.md files.

Mitigation: Inspect generated USER.md and MEMORY.md files before use, and edit or remove unintended identity, ownership, or business data.

Risk: Company IDs and custom workspace paths affect where files are created.

Mitigation: Run the script only with simple company IDs made of letters, numbers, hyphens, or underscores, and use custom workspaces only when the path is trusted.

Risk: Telegram group coordination can expose operational or business information to shared chat participants.

Mitigation: Do not place secrets, customer records, financial records, credentials, or private business data into shared Telegram groups or generated memory files without clear access and retention controls.

Risk: The server security verdict is suspicious because of under-scoped file writes and advertised messaging behavior.

Mitigation: Review and scan the skill before deployment, then test it in a non-sensitive workspace before using it for business workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gdp6539/skills/ai-company-starter)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [ClawHub](https://clawhub.com)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates persistent agent directories and role, memory, heartbeat, user, and company files in the selected OpenClaw workspace.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact _meta.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
