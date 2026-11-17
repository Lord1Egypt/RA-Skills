## Description:

Provides 24/7 AI customer service automation with common-question replies, sentiment-based escalation, ticket creation, multi-channel support, dashboards, and knowledge-base syncing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Support teams use this skill to automate routine customer conversations across approved channels, escalate negative sentiment or complex issues, and create tickets for human follow-up. Operators can also configure knowledge-base sources and review service metrics such as response time, resolution rate, and satisfaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic handling and reuse of customer conversations can expose PII, account data, or other sensitive support content.

Mitigation: Require redaction of PII and account data, and define retention, deletion, and access controls before using historical conversations or exported tickets.

Risk: Automatic ticket creation and third-party channel forwarding can route sensitive cases without enough operator approval.

Mitigation: Enable only approved support channels and disable or gate automatic ticket creation for sensitive or escalated cases.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/skills/ai-customer-service-automation)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes installation commands, channel configuration, knowledge-base configuration, sentiment thresholds, ticketing setup, and operational guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
