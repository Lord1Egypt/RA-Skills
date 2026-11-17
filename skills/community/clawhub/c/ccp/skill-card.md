## Description:

Continuous Context Preserver records concise session context during active agent sessions so recent decisions, discoveries, and recovery notes can survive restarts or crashes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivaavimusic](https://clawhub.ai/user/ivaavimusic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to maintain a rolling local archive of key session context for crash recovery and continuity between sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local session-memory files may retain sensitive conversation context if users include secrets, credentials, regulated data, or private personal details.

Mitigation: Log only concise recovery context, avoid sensitive data, and review or delete the sessions directory regularly.

Risk: The cleanup script deletes aged Markdown files under the configured sessions directory, and custom environment variables can change that deletion scope.

Mitigation: Review the configured SESSIONS_DIR and RETENTION_DAYS values before scheduled use, and fix or test the cleanup script before using cron or custom environment variables.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivaavimusic/skills/ccp)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown session notes with shell-command and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates concise local session-memory files and cleanup guidance; no external API output.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
