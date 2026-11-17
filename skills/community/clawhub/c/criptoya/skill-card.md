## Description:

Retrieves cryptocurrency prices and withdrawal fees from CriptoYa by exchange or aggregate market view.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ferminrp](https://clawhub.ai/user/ferminrp)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to look up Latin American crypto quotes, compare exchange ask and bid prices, inspect spreads, and retrieve withdrawal fee data for supported coins, fiat currencies, exchanges, and networks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Coin, fiat, exchange, and volume values are sent to CriptoYa when the skill retrieves market data.

Mitigation: Avoid using the skill for private trading plans if disclosing those query parameters to CriptoYa is unacceptable.

Risk: Crypto market data can be stale, unavailable, or returned as unexpected text for invalid pairs.

Mitigation: Check response timestamps, handle invalid-pair responses explicitly, and present results as informational rather than financial advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ferminrp/skills/criptoya)
- [CriptoYa](https://criptoya.com)
- [CriptoYa aggregate quote endpoint example](https://criptoya.com/api/BTC/ARS/0.1)
- [CriptoYa exchange quote endpoint example](https://criptoya.com/api/belo/BTC/ARS/0.1)
- [CriptoYa fees endpoint](https://criptoya.com/api/fees)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summaries with tables and inline shell commands; API responses are JSON when CriptoYa returns valid data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public CriptoYa endpoints without credentials; outputs are informational and not financial advice.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
