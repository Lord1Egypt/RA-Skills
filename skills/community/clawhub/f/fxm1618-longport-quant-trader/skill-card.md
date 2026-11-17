## Description:

LongPort Quant Trader automates Longport broker-based HK/US stock monitoring, strategy scanning, backtesting, order execution, Feishu notifications, and performance reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fxm1618-gmail](https://clawhub.ai/user/fxm1618-gmail)

### License/Terms of Use:

MIT-0

## Use Case:

External individual investors and quant trading enthusiasts use this skill to configure and run Longport-based automated market monitoring, strategy evaluation, alerts, and order workflows for HK/US equities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place broker orders automatically.

Mitigation: Run only with a paper account or dry-run controls until every order path, position limit, stop-loss rule, and alert path has been reviewed.

Risk: The security evidence reports exposed Longport or Feishu credentials and a fixed Feishu notification recipient.

Mitigation: Rotate any exposed credentials, remove hardcoded secrets and recipients, and configure a user-owned notification target before use.

Risk: Unpinned dependencies or shared environments can make execution harder to audit.

Mitigation: Pin dependencies and run the skill in a dedicated virtual environment before connecting it to any trading account.

## Reference(s):

- [Longport OpenAPI Documentation](https://open.longportapp.com/docs)
- [Longport Developer Portal](https://open.longportapp.com)
- [ClawHub Skill Page](https://clawhub.ai/fxm1618-gmail/skills/fxm1618-longport-quant-trader)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and user-provided Longport API credentials; Feishu notification configuration is optional.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
