## Description:

Routes A-share market, sector, stock, financial report, news, and capital-flow requests to the appropriate daxiapi specialist skill or CLI/API command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ksky521](https://clawhub.ai/user/ksky521)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route A-share data and analysis requests to focused ClawHub skills or to get daxiapi CLI/API commands for market, sector, stock, financial, news, and capital-flow data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to run mutable npm code through daxiapi-cli@latest.

Mitigation: Review the skill before installing and use a pinned, trusted daxiapi-cli version instead of @latest.

Risk: The skill handles API tokens and token-check output in ways that could expose credentials in command lines, logs, or chats.

Mitigation: Avoid pasting real tokens into chats or command histories, prefer environment or secret management where available, and treat token-check output as sensitive.

Risk: Market and stock outputs may be mistaken for financial advice.

Mitigation: Treat all market and stock guidance as informational and require independent review before investment decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ksky521/skills/daxiapi)
- [Daxiapi Website](https://daxiapi.com)
- [Daxiapi API Base Endpoint](https://daxiapi.com/coze)
- [API Reference](artifact/references/api-reference.md)
- [Field Descriptions](artifact/references/field-descriptions.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown, Text]

**Output Format:** [Markdown with inline shell commands and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes to specialist skills when available; otherwise provides daxiapi CLI commands and token configuration guidance.]

## Skill Version(s):

3.0.10 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
