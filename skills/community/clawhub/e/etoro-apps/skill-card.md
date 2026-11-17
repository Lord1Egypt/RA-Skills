## Description:

Enables agents to interact with the eToro API to access market data, portfolio and social features, and execute trades programmatically. Supports both OAuth SSO and manual API key authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marian2js](https://clawhub.ai/user/marian2js)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let agents read eToro market and account data, manage watchlists and social features, and prepare or execute demo or live trading actions through the eToro Public API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading and account-changing actions could be taken without clear user confirmation.

Mitigation: Require the agent to show the exact order, position, watchlist, or post and obtain explicit confirmation before any trade, cancellation, deletion, close, or public feed action.

Risk: Real eToro account credentials and OAuth materials are sensitive.

Mitigation: Prefer read-only or demo credentials unless live trading is specifically required, and treat tokens, API keys, user keys, PKCE values, and client secrets as secrets.

Risk: Demo and real trading environments may be confused.

Mitigation: Verify that the credential environment matches the selected endpoint, and default to demo or read-only use unless the user explicitly requests live trading.

## Reference(s):

- [eToro API Portal](https://api-portal.etoro.com/)
- [eToro Public API base URL](https://public-api.etoro.com/api/v1)
- [eToro MCP server](https://api-portal.etoro.com/mcp)
- [ClawHub skill page](https://clawhub.ai/marian2js/skills/etoro-apps)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash, JSON, and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes endpoint paths, authentication headers, request-body conventions, and demo/live environment guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
