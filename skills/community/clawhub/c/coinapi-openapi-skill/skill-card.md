## Description:

Operate CoinAPI market data reads through UXC with a curated OpenAPI schema, API-key auth, and read-first guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure UXC and perform read-only CoinAPI REST market data lookups for exchange rates, quotes, OHLCV candles, trades, and order book snapshots. It is intended for narrow market data reads with explicit API-key binding and JSON output handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that the default setup trusts a changeable remote API schema while using a CoinAPI key.

Mitigation: Review the UXC link command before installing and prefer the bundled local OpenAPI schema or an immutable, hash-verified schema URL.

Risk: CoinAPI access can consume quota or create billing impact if broad reads are automated.

Mitigation: Keep CoinAPI limits narrow, monitor API quota or billing, and remove the UXC credential, binding, and CLI link when the skill is no longer used.

## Reference(s):

- [CoinAPI REST docs](https://docs.coinapi.io/market-data/rest-api)
- [Usage patterns](references/usage-patterns.md)
- [Curated OpenAPI schema](references/coinapi-market.openapi.json)
- [ClawHub skill page](https://clawhub.ai/jolestar/skills/coinapi-openapi-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented API usage notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only CoinAPI market data operations scoped to the curated OpenAPI paths.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
