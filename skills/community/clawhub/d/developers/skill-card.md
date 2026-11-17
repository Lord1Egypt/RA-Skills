## Description:

Longbridge helps agents analyze markets and portfolios and build with Longbridge CLI, MCP, Python SDK, Rust SDK, and LLM documentation across HK, US, CN, SG, and crypto markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longbridge](https://clawhub.ai/user/longbridge)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, analysts, and finance-focused agents use this skill to retrieve Longbridge market data, inspect portfolio information, configure MCP access, and draft Python or Rust integrations for quote, content, and trade workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents toward real brokerage account access, portfolio reads, or order submission.

Mitigation: Use least-privilege OAuth scopes, protect cached session files, and require explicit user confirmation before reading portfolio data or submitting any order.

Risk: The artifact includes a curl-to-shell install path for the Longbridge terminal.

Mitigation: Prefer verified package-manager installs or pinned releases, and review install scripts before execution.

Risk: Market or portfolio guidance can be incomplete, stale, or unsuitable for a user's financial situation.

Mitigation: Treat analysis as decision support, verify live data and catalysts, and avoid presenting outputs as personalized financial advice.

## Reference(s):

- [Longbridge OpenAPI Documentation](https://open.longbridge.com)
- [Longbridge llms.txt](https://open.longbridge.com/llms.txt)
- [Longbridge Terminal GitHub](https://github.com/longbridge/longbridge-terminal)
- [Setup and Authentication](references/setup.md)
- [CLI Overview](references/cli/overview.md)
- [MCP Server](references/mcp.md)
- [LLM and AI Integration](references/llm.md)
- [Python SDK Overview](references/python-sdk/overview.md)
- [Python SDK QuoteContext](references/python-sdk/quote-context.md)
- [Python SDK TradeContext](references/python-sdk/trade-context.md)
- [Rust SDK Overview](references/rust-sdk/overview.md)
- [Rust SDK QuoteContext](references/rust-sdk/quote-context.md)
- [Rust SDK TradeContext](references/rust-sdk/trade-context.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks, shell commands, and JSON or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include financial analysis, CLI command suggestions, SDK examples, MCP configuration, and confirmation prompts for sensitive trading actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
