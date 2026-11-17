## Description:

Monitor CamelCamelCamel price drop alerts via RSS and send Telegram notifications when items go on sale.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jgramajo4](https://clawhub.ai/user/jgramajo4)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to configure scheduled monitoring of their personal CamelCamelCamel RSS feed and receive Telegram-formatted alerts for Amazon price drops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup creates a recurring scheduled shell command that fetches a user-supplied RSS URL.

Mitigation: Review the cron command before installation and use only the user's own HTTPS CamelCamelCamel alert URL.

Risk: The cache defaults to a shared temporary directory, which can expose or collide with local state on multi-user systems.

Mitigation: Store cache state in a private per-user directory with appropriate filesystem permissions.

Risk: The included notification script emits alert records and may require additional integration before Telegram delivery works as expected.

Mitigation: Test the fetch and notification pipeline manually before relying on scheduled alerts.

## Reference(s):

- [CamelCamelCamel Alerts Setup Guide](references/SETUP.md)
- [CamelCamelCamel](https://camelcamelcamel.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and JSON alert output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The RSS fetch script emits JSON containing new alerts, timestamps, and counts; the notification script emits pipe-delimited alert lines for downstream Telegram handling.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
