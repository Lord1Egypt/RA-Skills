## Description:

A CellCog Co-work coding agent for code generation, debugging, refactoring, codebase exploration, terminal operations, and on-demand multimedia tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cellcog](https://clawhub.ai/user/cellcog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to delegate codebase exploration, code generation and editing, debugging, refactoring, and project command execution to CellCog Co-work. Tasks run against a specified project directory, with user approval required for writes and command execution unless approval settings are changed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Co-work can access project files and run terminal commands on the user's machine; unreviewed actions could affect project data or the local environment.

Mitigation: Use a dedicated project directory and keep write and command approvals enabled. Review proposed changes and commands before approving them.

Risk: Code and logs shared for debugging may be handled by an external service, and debugging context can contain secrets or personal information.

Mitigation: Remove credentials and personal information from prompts, code excerpts, and logs before sharing them.

Risk: The external SDK and CellCog Desktop implementation were not verified in the supplied security evidence.

Mitigation: Review the prerequisite CellCog skill and downloaded software before enabling access.

## Reference(s):

- [CellCog](https://cellcog.ai)
- [Coding Agent release on ClawHub](https://clawhub.ai/cellcog/skills/coding-agent-cellcog)

## Skill Output:

**Output Type(s):** [Code, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Code and task results, with shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write project files and run commands through CellCog Co-work; task results are returned to the calling agent.]

## Skill Version(s):

1.0.16 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
