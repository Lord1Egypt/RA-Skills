## Description:

Clever Compact helps OpenClaw agents preserve working context across new sessions, compaction, and restarts by restoring recent local state at session start and supporting explicit state flushes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jfulmines-star](https://clawhub.ai/user/jfulmines-star)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this plugin to reduce session amnesia and compaction loss by saving concise state files and restoring recent state into the first prompt of a new session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext compact-state files may retain sensitive session details.

Mitigation: Keep the memory directory trusted, review or delete compact-state files before sensitive work, and do not store secrets in state files.

Risk: Unvalidated local compact-state content is restored into system context.

Mitigation: Restrict write access to the memory directory and review state files if local workspace integrity is uncertain.

Risk: Session-start restore can overlap with memory-core when both plugins inject context.

Mitigation: Use the documented memory-core configuration to disable overlapping memory flush behavior or direct the tools to separate state targets.

Risk: Some release-note troubleshooting commands affect ownership or overwrite configuration.

Mitigation: Review deployment impact and keep backups before running ownership changes or configuration reset commands.

## Reference(s):

- [Clever Compact on ClawHub](https://clawhub.ai/jfulmines-star/skills/clever-compact)
- [Security policy](SECURITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration snippets, and Markdown compact-state files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Restores the most recent compact-state Markdown file when it is within the configured state age window; the documented default is 72 hours.]

## Skill Version(s):

2.2.5 (source: server release, SKILL.md, CHANGELOG.md, openclaw.plugin.json; package.json and code headers contain older version strings)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
