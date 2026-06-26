## Description: <br>
Operate CoinAPI market data reads through UXC with a curated OpenAPI schema, API-key auth, and read-first guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure authenticated, read-only CoinAPI market data queries for exchange rates, quotes, OHLCV candles, trades, and order book snapshots through UXC. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CoinAPI credentials could be exposed or bound too broadly during setup. <br>
Mitigation: Use a dedicated CoinAPI key, keep it in the COINAPI_KEY environment variable, and confirm the UXC auth binding is limited to https://rest.coinapi.io. <br>
Risk: A mutable remote OpenAPI schema URL could change behavior over time. <br>
Mitigation: Prefer the bundled schema or a pinned schema URL when repeatability matters. <br>


## Reference(s): <br>
- [CoinAPI REST docs](https://docs.coinapi.io/market-data/rest-api) <br>
- [Usage patterns](references/usage-patterns.md) <br>
- [Curated OpenAPI schema](references/coinapi-market.openapi.json) <br>
- [ClawHub skill page](https://clawhub.ai/jolestar/coinapi-openapi-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and OpenAPI operation names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only CoinAPI market data requests using JSON response envelopes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
