## Description:

A Stock Monitor helps agents configure an A-share market monitoring workflow with market sentiment scoring, short- and long-term stock selection, realtime price monitoring, ranking views, automation commands, and alert setup guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shifengwang333-ai](https://clawhub.ai/user/shifengwang333-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide setup of an A-share stock monitoring assistant for market sentiment analysis, stock screening, price dashboards, scheduled updates, and notification workflows. It is decision-support guidance and should be reviewed before use in financial workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shipped artifact describes cron jobs and Python scripts, but those scripts are not present in the artifact.

Mitigation: Do not create the cron job or run the documented commands until the missing scripts are supplied and audited.

Risk: The workflow depends on market-data libraries and possible alert integrations that may send requests or data to third-party services.

Mitigation: Confirm what data is sent to market-data providers or messaging services before enabling alerts.

Risk: The documented dependency installation does not pin package versions.

Mitigation: Install dependencies in an isolated environment with reviewed, pinned versions.

Risk: Stock screening, expected return, and buy/sell guidance can be mistaken for investment advice.

Mitigation: Treat outputs as decision support only and independently review recommendations before trading or investment use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shifengwang333-ai/skills/a-stock-monitor)
- [Publisher profile](https://clawhub.ai/user/shifengwang333-ai)
- [Author blog](https://www.cnblogs.com/Jame-mei)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell, JSON, and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; documented package requirements include akshare, flask, and ccxt.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact text references 1.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
