## Description:

Dailynewsreport collects scheduled news from multiple sources, deduplicates, classifies, ranks, rewrites items into one-sentence briefs, and can deliver Markdown daily reports to Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frankle1117](https://clawhub.ai/user/frankle1117)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to automate daily news monitoring for policy, public-company, and industry topics, then generate structured Markdown reports with optional Telegram delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telegram delivery uses shell-based curl execution, which can expose the bot token and create command-injection risk.

Mitigation: Review before installing, keep Telegram tokens secret, use non-sensitive news topics, and prefer a version that uses a native HTTP client instead of shell execution.

Risk: The skill requests broad internet and file-system permissions for collecting and generating reports.

Mitigation: Run with least privilege, review configured sources and output paths, and remove unused broad permissions before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/frankle1117/skills/daily-news-report)
- [Skill behavior notes](artifact/Skill.md)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown daily report with categorized bullet items, source links, and optional Telegram message delivery.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scheduled runs default to Asia/Shanghai at 08:00, 17:30, and 22:30, with full and focused monitoring modes.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
