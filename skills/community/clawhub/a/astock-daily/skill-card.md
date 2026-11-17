## Description:

Astock Daily retrieves A-share IPO information and selected stocks priced under 20 yuan, then sends a daily email report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[batype](https://clawhub.ai/user/batype)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to gather daily A-share IPO and low-price stock data and deliver it as an email report. The generated information is for reference and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mail credentials can be exposed or mishandled.

Mitigation: Remove hard-coded recipients and test credentials, rotate any exposed SMTP password, and store mail secrets in a protected secret manager or tightly permissioned configuration file.

Risk: Credential-bearing configuration may be logged or stored in persistent shell configuration.

Mitigation: Avoid logging full SMTP configuration and review any shell-profile changes before enabling persistent environment variables.

Risk: Scheduler setup can create persistent cron jobs.

Mitigation: Review the cron entry, execution path, and log destination before enabling scheduled runs.

Risk: Network and mail helpers can weaken local security controls.

Mitigation: Keep TLS certificate validation enabled and avoid the sudo hosts-file helper unless an administrator has reviewed the change.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/batype/skills/astock-daily)
- [Publisher Profile](https://clawhub.ai/user/batype)
- [README](artifact/README.md)
- [Configuration Guide](artifact/CONFIG.md)
- [SMTP Guide](artifact/README-SMTP.md)
- [Cron Setup Guide](artifact/CRON-JOB.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; runtime output includes HTML email and JSON data files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches market data from external stock data sources, sends email through SMTP or sendmail, and can write local daily data files.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
