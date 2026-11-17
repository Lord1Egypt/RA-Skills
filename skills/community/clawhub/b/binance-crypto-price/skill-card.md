## Description:

Query real-time cryptocurrency prices using the Binance API. Get latest prices for Bitcoin, Ethereum, and all BN listed cryptocurrencies. No API key required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangzhe1991](https://clawhub.ai/user/yangzhe1991)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to retrieve current Binance spot-market cryptocurrency prices for popular coins, specific trading pairs, or USDT pairs, with optional JSON output for downstream workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Binance's public API to fetch market prices.

Mitigation: Run it in a normal least-privilege environment and ensure outbound access to Binance is acceptable for the deployment context.

Risk: The script may install or resolve the Python requests dependency through uv.

Mitigation: Use a pinned lockfile or reviewed dependency source when reproducible dependency resolution is required.

## Reference(s):

- [Binance Spot API ticker price endpoint](https://api.binance.com/api/v3/ticker/price)
- [ClawHub skill page](https://clawhub.ai/yangzhe1991/skills/binance-crypto-price)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON from a Python command-line script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can display popular coin prices, query a single symbol, auto-complete common symbols to USDT pairs, or list available USDT trading pairs.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
