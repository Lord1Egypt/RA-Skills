## Description:

Enables agents to interact with the eToro API to access market data, portfolio and social features, and execute trades programmatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marian2js](https://clawhub.ai/user/marian2js)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to work with eToro market data, portfolio information, watchlists, social feed features, user analytics, and demo or real trading workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can support live trading and other account-changing eToro actions.

Mitigation: Prefer Virtual/Demo or read-only keys, and require explicit approval before any live trade, close, cancel, watchlist change, or feed post.

Risk: Using a real portfolio key or non-demo endpoint by mistake could affect a user's live account.

Mitigation: Confirm the key environment before each trading workflow and use demo endpoints for testing or paper trading.

## Reference(s):

- [eToro API Portal](https://api-portal.etoro.com/)
- [eToro Public API Base URL](https://public-api.etoro.com/api/v1)
- [eToro MCP Server](https://api-portal.etoro.com/mcp)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline bash commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers authenticated eToro API requests for market data, portfolio data, watchlists, social features, and trading actions.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
