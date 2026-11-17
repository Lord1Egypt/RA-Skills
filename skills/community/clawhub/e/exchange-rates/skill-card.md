## Description:

Fetches live exchange rates between currency pairs from XE.com, with a fallback exchange-rate API, and returns the rate, converted amount, source, and timestamp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrinvincible29](https://clawhub.ai/user/mrinvincible29)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to answer currency conversion and exchange-rate questions for standard ISO 4217 currency codes. It is not intended for stock, crypto, or broader financial-market queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill embeds a browser-control token and can use a shared browser session beyond what a rate lookup needs.

Mitigation: Remove embedded browser-control credentials, use an isolated browser context for each run, and avoid closing shared browser resources.

Risk: The fallback data source can change the source of returned exchange rates when XE lookup fails.

Mitigation: Clearly identify whether results came from XE.com or the fallback API in user-facing responses.

## Reference(s):

- [XE Currency Converter](https://www.xe.com/currencyconverter/convert/)
- [ExchangeRate API fallback endpoint](https://open.er-api.com/v6/latest/USD)
- [ClawHub skill page](https://clawhub.ai/mrinvincible29/skills/exchange-rates)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON from the script, typically summarized to the user in concise Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes amount, source currency, target currency, rate, converted amount, source, and timestamp when lookup succeeds.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
