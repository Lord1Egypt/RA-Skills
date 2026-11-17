## Description:

Connect to 100+ external APIs through Maton's managed OAuth gateway so an agent can call native service endpoints and manage authorized connections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayakolin](https://clawhub.ai/user/ayakolin)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill when they need an agent to interact with external services such as Google Workspace, Microsoft 365, GitHub, Notion, Slack, Airtable, and HubSpot through user-authorized Maton connections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent direct API-level authority for connected third-party services.

Mitigation: Use least-privilege OAuth or API scopes, connect only needed services, and require confirmation before write, delete, payment, or public-posting actions.

Risk: The security scan flags unsafe guidance that may expose the reusable MATON_API_KEY.

Mitigation: Do not print or paste MATON_API_KEY; verify key presence without revealing the value and rotate the key if it may have been exposed.

Risk: The security scan verdict is suspicious because broad third-party account control is combined with API key handling risk.

Mitigation: Install only if the user trusts Maton with brokered access to connected services and accepts the account-control scope.

## Reference(s):

- [Maton homepage](https://maton.ai)
- [API reference](https://www.maton.ai/docs/api-reference)
- [Slack routing guide](references/slack/README.md)
- [Google Sheets routing guide](references/google-sheets/README.md)
- [HubSpot routing guide](references/hubspot/README.md)
- [Stripe routing guide](references/stripe/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access, a MATON_API_KEY, and user-authorized service connections.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
