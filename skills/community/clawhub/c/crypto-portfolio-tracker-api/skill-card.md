## Description:

Track cryptocurrency portfolios with real-time prices, P&L calculations, and allocation analysis. Query Bitcoin, Ethereum, Solana and 10,000+ token holdings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[strykragent](https://clawhub.ai/user/strykragent)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to query cryptocurrency prices, value portfolios, calculate profit and loss, and summarize asset allocation for crypto holdings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or running the package without pinning may expose users to package identity or supply-chain risk.

Mitigation: Review the package identity before installation and use a pinned version or lockfile-managed install instead of unpinned npx commands.

Risk: PRISM_API_KEY may be sent to a custom PortfolioTracker baseUrl if untrusted code can configure the endpoint.

Mitigation: Only set PRISM_API_KEY in trusted execution contexts and do not allow untrusted code to pass a custom baseUrl.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/strykragent/skills/crypto-portfolio-tracker-api)
- [PRISM API](https://prismapi.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript and shell examples, plus JSON-like portfolio and price data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use PRISM_API_KEY for higher rate limits and network calls to PRISM API endpoints.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
