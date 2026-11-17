## Description:

Guides an agent through A-share stock analysis using Eastmoney market data, technical indicators, position monitoring, stop-loss rules, and structured daily reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zooagentpm](https://clawhub.ai/user/zooagentpm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to collect A-share market data, calculate technical signals, evaluate buy, sell, hold, stop-loss, and take-profit actions, and maintain trading review records. It is decision support and should not be treated as guaranteed investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce buy, sell, stop-loss, and take-profit guidance that may be incorrect or misleading.

Mitigation: Treat outputs as decision support only, verify market data independently, and require human review before making financial decisions.

Risk: Optional Datasaver, Cookie, and bearer-token workflows may expose personal browser credentials in shared workspaces.

Mitigation: Use the no-Datasaver workflow by default; if Datasaver is needed, use a dedicated browser profile and never store real cookies or bearer tokens in shared files.

Risk: Scheduled monitoring and memory-writing workflows can create persistent trading records and automated financial alerts.

Mitigation: Enable cron and memory-writing workflows only intentionally, review schedules before activation, and keep position records out of shared or untrusted environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zooagentpm/skills/astock-analyst)
- [Data collection API guide](references/data-api.md)
- [Datasaver setup guide](references/datasaver-setup.md)
- [Error handling guide](references/error-handling.md)
- [Technical indicator guide](references/indicators.md)
- [Daily review template](references/review-template.md)
- [Watchdog scheduled monitoring guide](references/watchdog.md)
- [Further reading and extensions](references/further-reading.md)
- [Datasaver documentation](https://docs.qq.com/doc/DT3FZT09Zd254c1Bv)
- [InStock open source quantitative system](https://github.com/myhhub/stock)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell, Python, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include trading decision-support language, cron task JSON, optional browser-tool setup, and memory-file update guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
