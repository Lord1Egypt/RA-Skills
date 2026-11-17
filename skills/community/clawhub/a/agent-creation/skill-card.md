## Description:

Create a new OpenClaw agent with a workspace directory and SOUL.md configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to create a new agent workspace, configure the agent identity, replace SOUL.md, and initialize the agent memory structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent OpenClaw agent workspaces and replace SOUL.md configuration under the user's home directory.

Mitigation: Require the agent to show planned paths, commands, and SOUL.md changes before writing or replacing files.

Risk: User-provided agent and identity names may be used in shell commands or file paths without enough validation.

Mitigation: Validate agent and identity names, show the exact commands before execution, and avoid shell interpolation for user-provided values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openlark/skills/agent-creation)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent setup guidance, command examples, SOUL.md content, and memory file structure.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
