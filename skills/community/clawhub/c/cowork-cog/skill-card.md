## Description:

AI pair programming powered by CellCog Desktop. Code, debug, refactor, and build directly on the user's machine. Terminal access, file operations, full development workflows — auto-approved for agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cellcog](https://clawhub.ai/user/cellcog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use CellCog Desktop with cloud agents to work on local projects, including writing and changing code, debugging, refactoring, and development tasks. The agent can run local commands and access files in its working directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud agents can run local commands with automatic approval, while the limits on destructive actions are unclear.

Mitigation: Use an isolated project with backups and confirm how consequential commands are restricted before execution.

Risk: Co-work can expose local project data to cloud agents, and Browse can use the user's real browser.

Mitigation: Use a dedicated browser profile without sensitive accounts, and review the dependency and desktop installer separately.

## Reference(s):

- [Pair Programming on ClawHub](https://clawhub.ai/cellcog/skills/pair-programming-cellcog)
- [CellCog](https://cellcog.ai)
- [CellCog Co-work](https://cellcog.ai/cowork)

## Skill Output:

**Output Type(s):** [Code, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Code and file changes, shell commands, and text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and modify files and run commands within the configured project working directory.]

## Skill Version(s):

1.0.16 (source: server-resolved ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
