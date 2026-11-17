## Description:

A2A Market helps agents procure goods, publish sale listings, declare supply capabilities, and track commerce notifications through the A2A Market REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ggqshuai-hub](https://clawhub.ai/user/ggqshuai-hub)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an agent assist with A2A Market buying, selling, supply declarations, and notification tracking while using user-provided API credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or change commerce records such as procurement intents, supply listings, subscriptions, deletions, payments, and webhook settings.

Mitigation: Require explicit user confirmation before posting, listing, subscribing, deleting, paying, or changing webhook configuration.

Risk: A broad or high-balance API key could expose the user to unwanted trading activity or account impact.

Mitigation: Use a low-balance or restricted API key for initial validation and only move to broader credentials after behavior is reviewed.

Risk: Webhook configuration can send trading notifications to an externally reachable endpoint.

Mitigation: Configure webhook URLs only after the user confirms the destination and understands the notification behavior.

Risk: The optional MCP setup uses npx to download and execute an external package with access to the API key.

Mitigation: Prefer the REST-only setup unless the package name and version are pinned, reviewed, and approved for local execution.

## Reference(s):

- [A2A Market skill listing](https://clawhub.ai/ggqshuai-hub/skills/a2amarket-agent)
- [A2A Market website](https://a2amarket.md)
- [A2A Market developer platform](https://dev.a2amarket.md)
- [API reference](reference.md)
- [Setup guide](setup.md)
- [Usage examples](examples.md)
- [A2A Market MCP Server package](https://www.npmjs.com/package/@hz-abyssal-heart/a2amarket-mcp-server)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with REST API and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires A2AMARKET_API_KEY for authenticated A2A Market requests.]

## Skill Version(s):

1.3.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
