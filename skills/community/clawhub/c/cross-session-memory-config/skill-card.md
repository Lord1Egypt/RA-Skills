## Description:

Configures OpenClaw cross-session memory rules by adding memory-sharing guidance to SOUL.md and AGENTS.md when group and private chat memories should interoperate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richardcoder849](https://clawhub.ai/user/richardcoder849)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and administrators use this skill after a new installation or on request to configure persistent memory sharing between group chats and private chats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently changes core OpenClaw instruction files.

Mitigation: Inspect the planned SOUL.md and AGENTS.md changes before installation, and make backups before running the setup script.

Risk: The skill broadly shares group-chat and private-chat long-term memory across future OpenClaw sessions.

Mitigation: Use it only where group participants and private users have consented to shared persistent memory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/richardcoder849/skills/cross-session-memory-config)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and configuration file changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append memory-sharing rules to SOUL.md and AGENTS.md through the provided setup script.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
