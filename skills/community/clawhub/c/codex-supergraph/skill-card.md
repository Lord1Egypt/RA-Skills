## Description: <br>
Helps agents build valid Codex GraphQL requests for token prices, charts, holders, pair data, prediction markets, and on-chain analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nealo](https://clawhub.ai/user/nealo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to select Codex Supergraph operations and produce authenticated GraphQL queries, subscriptions, shell examples, and integration guidance for on-chain and prediction-market analytics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Long-lived Codex API keys could be exposed or misused if copied into prompts, logs, or shared output. <br>
Mitigation: Keep CODEX_API_KEY protected, avoid printing raw keys, and review generated requests before execution. <br>
Risk: Generated examples may include token management or webhook operations that change service state. <br>
Mitigation: Allow token creation, token deletion, webhook creation, or webhook deletion only when explicitly requested, and review callback URLs and returned tokens before use. <br>
Risk: On-chain and prediction-market analytics can be incomplete, stale, or shaped by rate limits and schema changes. <br>
Mitigation: Validate network IDs and GraphQL shapes against the current Codex schema, keep selection sets minimal, and handle 401, 402, 429, and validation errors before relying on results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nealo/codex-supergraph) <br>
- [Codex website](https://www.codex.io) <br>
- [Codex documentation](https://docs.codex.io) <br>
- [Codex GraphQL endpoint](https://graph.codex.io/graphql) <br>
- [Codex GraphQL schema](https://graph.codex.io/schema/latest.graphql) <br>
- [Codex Supergraph API Reference](references/apis.md) <br>
- [Codex Supergraph Endpoint Playbook](references/endpoint-playbook.md) <br>
- [Codex Supergraph Gotchas](references/gotchas.md) <br>
- [Codex Supergraph Query Templates](references/query-templates.md) <br>
- [Prediction Markets](references/prediction-markets.md) <br>
- [Codex Docs Tooling and MCP Setup](references/tooling-and-mcp.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline GraphQL, JSON, TypeScript, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include authenticated API request examples, GraphQL operation selections, WebSocket subscription guidance, and MCP setup snippets.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
