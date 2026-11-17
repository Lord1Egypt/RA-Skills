## Description:

Use Finnhub-backed market intelligence through the `aigroup-finnhub-mcp` server for stock, crypto, forex, calendar, news, sentiment, filing, ownership, analyst, and technical-analysis tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackdark425](https://clawhub.ai/user/jackdark425)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market-research agents use this skill to route ticker, crypto, forex, calendar, news, sentiment, filing, ownership, analyst, and technical-analysis requests through the Finnhub MCP server. It is suited for event-driven research briefs that need source-aware summaries of news flow, filings, analyst revisions, ownership activity, or technical signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market-related prompts may invoke the external MCP server automatically.

Mitigation: Run the MCP server with minimal filesystem and environment access, and review outputs before using them for decisions.

Risk: The documented launch pattern uses an unpinned npm package.

Mitigation: Prefer a pinned and audited package version, and review the MCP package source and publisher before installing.

## Reference(s):

- [Finnhub MCP Capabilities](references/capabilities.md)
- [Project homepage](https://github.com/jackdark425/aigroup-finnhub-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text market-research summaries with tool-routing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke an external MCP server for Finnhub-backed market data and event intelligence.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
