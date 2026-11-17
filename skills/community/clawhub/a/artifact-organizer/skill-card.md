## Description:

Organizes mixed task artifacts by workflow stage rather than file type, including planning staged directories, cleaning already messy workspaces, and routing precise sensitive values into an existing secrets system.

This skill is ready for commercial/non-commercial use.

## Publisher:

[big-dust](https://clawhub.ai/user/big-dust)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, researchers, and automation users use this skill to plan or reorganize task workspaces so intermediate files, final deliverables, logs, scripts, notes, and sensitive references remain easier to find and maintain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be asked to reorganize workspace files and can affect files that contain credentials or other sensitive values.

Mitigation: Require explicit user confirmation before reading, moving, or summarizing sensitive files, and preserve task continuity when moving files could affect scripts or workflows.

Risk: The security evidence warns that placing credentials under predictable plaintext secrets paths can create exposure through source control, backups, logs, or indexing.

Mitigation: Prefer a secret manager or encrypted store for precise secrets, and ensure local secret paths are excluded from source control, backups, logs, and indexing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/big-dust/skills/artifact-organizer)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown guidance with optional directory trees and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or perform workspace file moves and summarize the resulting structure.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
