## Description:

AI-powered context management for OpenClaw sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plgonzalezrx8](https://clawhub.ai/user/plgonzalezrx8)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to inspect session context usage, generate session summaries, and optionally compress long-running sessions by resetting them with summarized context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The replace mode can delete a live OpenClaw session JSONL file after creating a backup.

Mitigation: Run summary-only mode first, confirm the backup path exists, and use replace mode only on sessions where reset behavior has been manually verified.

Risk: Generated summaries and backups may contain sensitive plaintext session history.

Mitigation: Review generated files for secrets or sensitive content before reuse, sharing, or retention.

Risk: Slack, cron, group, or other sensitive sessions may have destination behavior that differs from a direct main session.

Mitigation: Avoid replace mode on those sessions unless the destination behavior has been fixed or manually verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/plgonzalezrx8/skills/context-manager)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and generated summary files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create plaintext summaries, transcript extracts, continuation prompts, and session backups under memory/compressed.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
