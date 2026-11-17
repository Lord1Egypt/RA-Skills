## Description:

Query DexScreener market data - search pairs, inspect liquidity/volume, check boosted tokens, and fetch token orders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brs999](https://clawhub.ai/user/brs999)

### License/Terms of Use:


## Use Case:

Developers, analysts, and external users use this skill to query public DexScreener pair, liquidity, volume, profile, boost, and token-order data from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes network requests to DexScreener, and DEXSCREENER_BASE_URL can redirect those requests.

Mitigation: Use the default DexScreener API URL unless you intentionally trust an alternate endpoint.

## Reference(s):

- [DexScreener](https://dexscreener.com)
- [DexScreener API](https://api.dexscreener.com)
- [ClawHub Skill Page](https://clawhub.ai/brs999/skills/dexscreener)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [JSON responses with Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public market data; no API key required.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
