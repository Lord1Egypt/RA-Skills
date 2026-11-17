## Description:

Monitors publicly accessible Feishu/Lark document tables for changes to model listings, prices, rates, and version dates, and prepares Markdown notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quqi1599](https://clawhub.ai/user/quqi1599)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users monitor public Feishu/Lark price or model tables and receive readable change summaries for notification workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Monitoring a private or login-required document is outside the skill's intended scope.

Mitigation: Use only publicly accessible Feishu/Lark documents; do not supply credentials or bypass access controls.

Risk: Overlapping scheduled runs or an unreviewed schedule can disrupt monitoring.

Mitigation: Use a dedicated state directory, review cron jobs before enabling them, and avoid overlapping runs.

Risk: Writing a snapshot does not confirm that a change notification was delivered.

Mitigation: Have the scheduler handle notification failures and retries independently of snapshot updates.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/quqi1599/skills/feishu-public-table-monitor)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown change notice or status text; optional JSON snapshot]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prints INIT_ONLY on baseline creation and NO_REPLY when unchanged; keeps a local baseline snapshot.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
