## Description:

Core Files Management guides OpenClaw agents in organizing, updating, and backing up core workspace Markdown files such as identity.md, agents.md, user.md, memory.md, tools.md, and bootstrap.md.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kofna3369](https://clawhub.ai/user/kofna3369)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw workspace agents use this skill to keep core workspace files organized, avoid duplicated content, apply language rules, and create backups before edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and modify sensitive core workspace files.

Mitigation: Confirm each sensitive file access or modification before allowing the agent to proceed.

Risk: Backup files may persist as plaintext .bak or .backup copies.

Mitigation: Avoid storing secrets in core files and clean up or protect backup copies after edits.

## Reference(s):

- [Core Files Management on ClawHub](https://clawhub.ai/kofna3369/skills/core-files-management)
- [Kofna3369 ClawHub profile](https://clawhub.ai/user/kofna3369)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose reading, writing, editing, and backing up OpenClaw workspace Markdown files.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact body)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
