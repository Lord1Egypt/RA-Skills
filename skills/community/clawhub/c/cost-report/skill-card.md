## Description:

Track OpenClaw usage costs and provide detailed reports by date and model. Supports daily, weekly, and monthly report formats for Discord and other messaging channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentqiu](https://clawhub.ai/user/vincentqiu)

### License/Terms of Use:

MIT

## Use Case:

Developers and operations teams use this skill to inspect local OpenClaw session logs and summarize model usage costs by date and model. It supports one-off reports and scheduled Discord-style summaries for cost monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports a shell-injection flaw in the Node CLI command construction.

Mitigation: Use the shell scripts directly with trusted arguments until the CLI command construction is fixed.

Risk: Discord or cron reporting with error details can expose raw model error messages from local OpenClaw session logs.

Mitigation: Avoid shared-channel reporting with --show-errors unless those session-log details are approved for disclosure.

## Reference(s):

- [OpenClaw JSONL log format](references/JSONL_FORMAT.md)
- [ClawHub skill page](https://clawhub.ai/vincentqiu/skills/cost-report)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [Plain text, Discord-ready Markdown, or JSON cost reports with optional shell commands and scheduling configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local OpenClaw session logs and jq; reports can be scoped to today, yesterday, week, month, or custom date ranges.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
