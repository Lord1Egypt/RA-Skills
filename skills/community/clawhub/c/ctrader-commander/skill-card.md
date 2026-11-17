## Description:

Place and manage cTrader orders (market, limit, stop), check open positions, fetch live quotes and OHLC candles, and query account balance and equity via a local HTTP proxy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elmoyeldo](https://clawhub.ai/user/elmoyeldo)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manage cTrader account workflows through a local proxy, including finding broker-specific symbols, checking account state, fetching market data, and preparing order-management commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control real cTrader accounts through an unauthenticated local proxy.

Mitigation: Use a demo or limited-risk account, restrict access to localhost:9009, avoid shared or container network exposure, and require explicit confirmation before order, close, cancel, or account-switch actions.

Risk: The skill depends on running unpinned external proxy code that uses trading credentials.

Mitigation: Review the proxy repository before installation and pin it to a known commit where possible.

## Reference(s):

- [cTrader OpenAPI Proxy](https://github.com/LogicalSapien/ctrader-openapi-proxy)
- [ClawHub Skill Page](https://clawhub.ai/elmoyeldo/skills/ctrader-commander)
- [Endpoint Reference](artifact/endpoints.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and a running local cTrader OpenAPI proxy on localhost:9009.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
