## Description:

Use when the user asks about token prices, charts, holders, trending tokens, pair data, prediction markets, or any on-chain analytics from Codex, or when building GraphQL queries against the Codex API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nealo](https://clawhub.ai/user/nealo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to choose Codex GraphQL operations and produce API requests for token analytics, holders, pairs, charts, live subscriptions, wallet analytics, and prediction-market data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents API-token and webhook operations that can affect account access or send data to callback URLs.

Mitigation: Before allowing an agent to create or delete API tokens or webhooks, confirm the exact action, callback URL, data sent, and revocation path.

Risk: Agent workflows using this skill may handle sensitive wallet, trader, webhook secret, or API-token values.

Mitigation: Treat those values as sensitive, avoid printing raw API keys, and review outputs before sharing or logging them.

Risk: The optional Codex SDK adds third-party code to the execution environment.

Mitigation: Pin and review the SDK before installation.

## Reference(s):

- [Codex Website](https://www.codex.io)
- [Codex Documentation](https://docs.codex.io)
- [Codex API Key Signup](https://dashboard.codex.io/signup)
- [Codex GraphQL Endpoint](https://graph.codex.io/graphql)
- [Codex Latest GraphQL Schema](https://graph.codex.io/schema/latest.graphql)
- [Codex Latest Introspection JSON](https://graph.codex.io/schema/latest.json)
- [Codex Docs MCP](https://docs.codex.io/mcp)
- [Codex Supergraph Gotchas](references/gotchas.md)
- [Codex Supergraph Query Templates](references/query-templates.md)
- [Codex Supergraph Endpoint Playbook](references/endpoint-playbook.md)
- [Codex Supergraph API Reference](references/apis.md)
- [Prediction Markets](references/prediction-markets.md)
- [Codex Docs Tooling and MCP Setup](references/tooling-and-mcp.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with GraphQL, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API requests, subscription examples, query variables, endpoint selection guidance, and MCP setup snippets.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
