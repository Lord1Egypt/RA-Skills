## Description:

Provides cryptocurrency prices in USD using the CoinGecko API, with SkillPay billing for each call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loverun321](https://clawhub.ai/user/loverun321)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to request current USD prices, 24-hour changes, or top cryptocurrency listings. It is intended for paid price lookups rather than financial advice or trading execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Billing implementation exposes an API key in the package.

Mitigation: Rotate the exposed key and move billing credentials out of distributed skill files.

Risk: Billing trusts caller-provided identities and may charge before delivering a result.

Mitigation: Bind charges to authenticated platform identity, validate requests before charging, and fail closed on billing errors.

Risk: The security verdict is suspicious and recommends review before installation.

Mitigation: Review the skill carefully before installing and verify the billing path before production use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/loverun321/skills/crypto-price-skill)
- [CoinGecko API endpoint](https://api.coingecko.com/api/v3/simple/price)
- [SkillPay billing endpoint](https://skillpay.me/api/v1/billing)

## Skill Output:

**Output Type(s):** [text, JSON, API calls, guidance]

**Output Format:** [JSON responses with price, 24-hour change, listing, payment status, or error fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May contact CoinGecko and SkillPay during execution; output is not financial advice.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
