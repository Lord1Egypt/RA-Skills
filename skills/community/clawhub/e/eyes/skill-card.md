## Description:

Eyes monitors global news and market-moving events, prepares daily or hourly briefings, and analyzes potential impacts across equities, sectors, currencies, and commodities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kobenfang](https://clawhub.ai/user/kobenfang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and investors use Eyes to request or schedule global news briefings that classify events by urgency and summarize likely market impact across A-shares, Hong Kong stocks, U.S. stocks, sectors, FX, and commodities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outbound messaging behavior is under-scoped and could send reports to unexpected destinations.

Mitigation: Review all cron jobs and message destinations before installation, and require explicit confirmation before sending reports or changing cron settings.

Risk: Hard-coded Feishu examples and fallback delivery configuration can route content through unintended channels.

Mitigation: Replace example targets with user-approved channel and target values, and remove the BigA shared configuration fallback before deployment.

Risk: The helper can append promotional BigA text to outgoing reports.

Mitigation: Remove the promotion behavior so delivered reports contain only the requested news and market analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kobenfang/skills/eyes)
- [Event Impact Matrix](references/event-impact-matrix.md)
- [Cron Templates](references/cron-templates.json)
- [Cron Install Shell](references/cron-install-shell.sh)
- [User Preferences](references/user-preferences.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown briefings with JSON helper output and shell commands for OpenClaw messaging and cron configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Briefings may be segmented for delivery; helper commands can update local memory, schedule cron jobs, and send messages to configured channels.]

## Skill Version(s):

5.3.13 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
