## Description:

Todo list and task management for AI agents. Add, track, and complete tasks with autonomy levels; agents propose work and humans approve.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lepetitpince](https://clawhub.ai/user/lepetitpince)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to maintain a persistent task queue for AI agents across conversations, heartbeat loops, cron jobs, and sub-agent workflows. It supports human approval of agent-proposed tasks and structured task status updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned global npm CLI whose reviewed code is not included in the artifact.

Mitigation: Review or pin the exact npm package version before installing and prefer an isolated or project-local environment over a global install.

Risk: Heartbeat or cron workflows may let agents process auto tasks without immediate human review.

Mitigation: Use the documented human approval flow for proposed tasks and be cautious before enabling unattended auto-task processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lepetitpince/skills/clawdo)
- [npm package: clawdo](https://www.npmjs.com/package/clawdo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON-oriented CLI usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the clawdo CLI binary; examples prefer structured JSON command output for agent parsing.]

## Skill Version(s):

1.1.4 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
