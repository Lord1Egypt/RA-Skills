## Description: <br>
Query DexScreener market data - search pairs, inspect liquidity/volume, check boosted tokens, and fetch token orders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BRS999](https://clawhub.ai/user/BRS999) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to retrieve public DexScreener market data for token pair discovery, liquidity and volume checks, boosted-token review, and token order lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market lookup queries are sent to DexScreener or to the configured DEXSCREENER_BASE_URL. <br>
Mitigation: Do not include wallet seed phrases, private keys, credentials, or other secrets in lookup text. <br>
Risk: Changing DEXSCREENER_BASE_URL sends lookup queries to a different endpoint. <br>
Mitigation: Only override DEXSCREENER_BASE_URL with an endpoint the user trusts. <br>


## Reference(s): <br>
- [DexScreener](https://dexscreener.com) <br>
- [DexScreener Public API](https://api.dexscreener.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/BRS999/dexscreener) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON from CLI commands, with markdown usage examples in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only public market lookup output; no API key required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
