## Description:

Connect to 100+ APIs such as Google Workspace, Microsoft 365, Notion, Slack, Airtable, and HubSpot through Maton's managed OAuth gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonymd323](https://clawhub.ai/user/tonymd323)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to call native third-party service APIs through a unified gateway after the user has configured a Maton API key and authorized each service connection. It is suited for workflows that need managed OAuth access to business, productivity, analytics, messaging, CRM, and file services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The gateway can give an agent high-impact access to connected business and productivity services.

Mitigation: Use least-privilege OAuth or API scopes and require explicit user confirmation before sending messages, changing business data, deleting resources, or managing users.

Risk: Troubleshooting commands may expose the Maton API key or connection URLs in logs or transcripts.

Mitigation: Redact secrets before sharing logs, avoid printing live credentials, and rotate the Maton API key if it is exposed.

Risk: Using the skill requires trusting Maton as the broker for connected service access.

Mitigation: Install only in environments where Maton's brokered access model is approved and each connected service has been explicitly authorized by the user.

## Reference(s):

- [Maton Homepage](https://maton.ai)
- [Maton API Reference](https://www.maton.ai/docs/api-reference)
- [API Gateway Source Repository](https://github.com/maton-ai/api-gateway-skill)
- [ClawHub Skill Page](https://clawhub.ai/tonymd323/skills/api-gateway-bak)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include API request examples, connection-management commands, endpoint paths, headers, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
