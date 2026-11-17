## Description:

Generates a daily brief including urgent emails (himalaya), upcoming calendar events (gog), and relevant news.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rajtejani61](https://clawhub.ai/user/rajtejani61)

### License/Terms of Use:


## Use Case:

External users use this skill to produce a morning briefing that combines recent email triage, calendar events, due tasks, and current news into a saved digest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local email and calendar data to build the digest.

Mitigation: Install and run it only where access to those local data sources is intended, and review configured CLI permissions before scheduling automated runs.

Risk: The skill creates permanent local digest archives that may contain private information.

Mitigation: Restrict file permissions, redact sensitive fields when needed, and define retention or deletion controls for saved digest files.

Risk: Scheduled unattended runs may collect and send daily summaries through a configured messaging channel.

Mitigation: Review or disable the cron setup unless unattended daily execution and notifications are desired.

## Reference(s):

- [Daily Brief Digest ClawHub Page](https://clawhub.ai/rajtejani61/skills/daily-brief-digest)
- [Setting Up the Daily Digest Cron Job](references/cron-guide.md)
- [Daily Digest Templates](references/templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown report with embedded HTML, terminal summary text, and optional notification summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves a dated local digest file under ~/.openclaw/cron/DailyDigest_logs/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
