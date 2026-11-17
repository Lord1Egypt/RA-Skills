## Description:

Daily automated health check + mood tracking + proactive alerts for OpenClaw agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lalawgwg99](https://clawhub.ai/user/lalawgwg99)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and agent operators use this skill to generate scheduled daily status reports covering gateway health, memory structure, mood trends, stalled P0/P1 tasks, and recommended follow-up actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled reports may include mood, task status, and operational health information that can be delivered through Telegram.

Mitigation: Review the configured Telegram chat ID and disable Telegram delivery unless automatic sharing of these summaries is intended.

Risk: The skill reads OpenClaw workspace files such as memory, emoji journal, heartbeat, and agent notes to build its reports.

Mitigation: Review the files under ~/.openclaw/workspace-frontdesk before installation and confirm they are appropriate inputs for daily summaries.

Risk: The README includes an unpinned dependency installation command for python-telegram-bot.

Mitigation: Pin dependencies or remove the unused install instruction when maintaining or deploying the skill in a controlled environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lalawgwg99/skills/daily-observatory-lite)
- [Project Homepage](https://github.com/lalawgwg99/daily-observatory-lite)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown-style daily report and Telegram-ready text, with optional shell commands for scheduled execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write dated daily report files under the skill memory folder and optionally send summaries through Telegram when configured]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
