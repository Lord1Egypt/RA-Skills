## Description:

Runs a daily agent retrospective by reading session history, summarizing actions and lessons across six dimensions, updating memory and configuration files, writing a completion lock, and reporting the result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[morrison230](https://clawhub.ai/user/morrison230)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and operators use this skill to perform a daily review of prior session activity, capture wins, mistakes, improvements, user profile observations, and agent behavior notes, and persist those lessons into workspace memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad access to local session history and can persist profile inferences into memory and configuration files.

Mitigation: Review the proposed summaries and diffs before saving them, and avoid storing raw conversations, tool outputs, secrets, or sensitive personal inferences.

Risk: The package includes an enabled Feishu webhook and can send retrospective content outside the local workspace.

Mitigation: Revoke or replace the packaged webhook, keep notifications disabled until the destination and message content are reviewed, and use only a user-controlled secret.

Risk: Scheduled or privileged execution could modify MEMORY.md, USER.md, SOUL.md, and AGENTS.md without timely review.

Mitigation: Run manually or as an unprivileged user, require explicit approval before core file changes, and keep backups enabled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/morrison230/skills/agent-daily-retro)
- [Publisher profile](https://clawhub.ai/user/morrison230)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown reports, local file updates, console text, and optional Feishu notifications]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes daily memory, report, backup, and lock files in the configured OpenClaw workspace.]

## Skill Version(s):

1.0.0 (source: release evidence and config.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
