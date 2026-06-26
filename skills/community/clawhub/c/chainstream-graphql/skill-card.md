## Description: <br>
Executes flexible GraphQL queries against ChainStream's on-chain data warehouse for custom analytics such as cross-cube joins, aggregations, filters, time series, and SQL-level blockchain data exploration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harry5556](https://clawhub.ai/user/harry5556) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent builders use this skill to construct and run ChainStream GraphQL queries for custom on-chain analytics across Solana, Ethereum, BSC, Polygon, and trading data. It is suited to cases where prebuilt REST or MCP endpoints are too limited, such as joins, aggregations, complex filters, and custom time-series analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses ChainStream's external CLI and MCP service and may require API keys, wallet signatures, and subscription checks. <br>
Mitigation: Use a scoped API key or generated low-balance wallet, avoid importing valuable private keys, and review authentication steps before use. <br>
Risk: Subscription or paid plan flows can spend funds if approved by the user. <br>
Mitigation: Require explicit user review and confirmation before any paid plan purchase. <br>
Risk: The broader ChainStream skill set includes DeFi actions, while this release is focused on GraphQL analytics. <br>
Mitigation: Keep this skill to read-oriented GraphQL analytics and require separate explicit review before any DeFi transaction action. <br>


## Reference(s): <br>
- [ChainStream GraphQL Schema Guide](references/schema-guide.md) <br>
- [ChainStream GraphQL Query Patterns](references/query-patterns.md) <br>
- [Authentication](shared/authentication.md) <br>
- [Payment Protocols](shared/x402-payment.md) <br>
- [Supported Chains](shared/chains.md) <br>
- [Error Handling](shared/error-handling.md) <br>
- [ChainStream Documentation](https://docs.chainstream.io) <br>
- [ChainStream API Reference](https://docs.chainstream.io/api-reference) <br>
- [ChainStream Dashboard](https://app.chainstream.io) <br>
- [ChainStream MCP Server](https://mcp.chainstream.io/mcp) <br>
- [ChainStream GraphQL Endpoint](https://graphql.chainstream.io/graphql) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline GraphQL, JSON, and bash snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ChainStream CLI commands, GraphQL queries, JSON result interpretation, authentication guidance, and subscription workflow guidance.] <br>

## Skill Version(s): <br>
1.0.7 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
