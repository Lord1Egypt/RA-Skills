## Description:

Advanced filesystem operations for listing, searching, batch processing, and directory analysis in Clawdbot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucky-2968](https://clawhub.ai/user/lucky-2968)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to list, search, copy, visualize, and analyze files and directories during authorized project maintenance and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad local file searches or analysis can expose sensitive project, home directory, log, temporary, or credential-store contents.

Mitigation: Limit searches and analysis to project or explicitly authorized directories, and avoid credential stores, home directories, broad log folders, and temporary folders.

Risk: Copy operations can write files into unintended destinations or overwrite useful data if broad patterns are allowed.

Mitigation: Review copy targets and patterns before granting write access, use dry-run mode, and require confirmation for overwrite-prone operations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lucky-2968/skills/clawdbot-filesystem-1-0-2)
- [Publisher Profile](https://clawhub.ai/user/lucky-2968)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text, table, tree, list, and JSON-style command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May inspect and copy local files when given authorized paths; dry-run and confirmation settings should be used before write operations.]

## Skill Version(s):

1.0.0 (source: server release metadata); artifact package.json declares 1.0.2

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
