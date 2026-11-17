## Description:

Helps agents send and update Feishu interactive cards using Card JSON 2.0 for forms, choices, confirmations, quick actions, and structured data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afk101](https://clawhub.ai/user/afk101)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a Feishu conversation needs an interactive card instead of plain text, such as collecting form input, presenting choices, confirming higher-risk actions, or displaying structured data. It requires configured Feishu card tools to send forms, raw card JSON, and card updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can post or update Feishu messages and collect form responses through configured bot credentials.

Mitigation: Install only in workspaces where Feishu bot credentials are tightly scoped and recipients or account usage are limited by configuration and review.

Risk: Callers can choose a configured Feishu account without a clear authorization boundary.

Mitigation: Review or patch accountId handling before using the plugin with multiple Feishu accounts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/afk101/skills/feishu-card-v2)

## Skill Output:

**Output Type(s):** [JSON, API Calls, Guidance]

**Output Format:** [Feishu Card JSON 2.0 objects and tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May post or update Feishu messages through configured Feishu accounts.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
