## Description:

Track tasks in ClickUp from an AI agent: check open tasks before starting work, log completed work after, and capture future ideas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dyagil](https://clawhub.ai/user/dyagil)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to keep ClickUp aligned with meaningful work: checking existing tasks before non-trivial requests, adding new work or future ideas, and recording completed tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may send meaningful work details to ClickUp without explicit per-request consent.

Mitigation: Require approval before each ClickUp read or write when task content may include sensitive, private, or client-specific information.

Risk: Task descriptions can include secrets, vulnerability details, personal information, or private client data.

Mitigation: Sanitize task names and descriptions before writing to ClickUp, and avoid storing secrets or sensitive details in task records.

Risk: The skill relies on a ClickUp token and workspace configuration that allow automated task operations.

Mitigation: Store the token with restrictive file permissions, scope credentials to the minimum needed workspace, and rotate the token if exposed.

## Reference(s):

- [ClickUp API](https://clickup.com/api)
- [ClawHub skill page](https://clawhub.ai/dyagil/skills/dyagil-clickup)
- [Publisher profile](https://clawhub.ai/user/dyagil)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides an agent to read, create, search, and close ClickUp task records using a configured CLI and ClickUp token.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
