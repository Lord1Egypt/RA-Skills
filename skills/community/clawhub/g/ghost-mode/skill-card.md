## Description:

Ghost Mode provides a local OpenClaw incognito workflow that pauses memory writes and scrubs session traces from logs, memory files, transcripts, and search indexes when deactivated.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stelloxx](https://clawhub.ai/user/stelloxx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use Ghost Mode for sensitive, experimental, or one-off sessions where agent memory and session history should not persist after explicit cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to permanently delete OpenClaw memory and session traces and may delete more data than intended.

Mitigation: Use backups, run dry-run previews first, and require explicit confirmation before destructive cleanup.

Risk: Server security guidance reports unsafe failure behavior, including possible cleanup success claims when verification failed.

Mitigation: Review cleanup output and verification status manually; avoid unattended cron cleanup, --yes, and disabled confirmations until the implementation is fixed.

Risk: Server security guidance reports input and path handling bugs.

Mitigation: Run only in a trusted local environment with OPENCLAW_HOME and OPENCLAW_WORKSPACE set to strict OpenClaw subdirectories.

## Reference(s):

- [Ghost Mode Architecture](references/ARCHITECTURE.md)
- [ClawHub Skill Page](https://clawhub.ai/stelloxx/skills/ghost-mode)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local-only workflow; destructive cleanup commands require careful review before execution.]

## Skill Version(s):

1.2.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
