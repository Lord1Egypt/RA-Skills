## Description:

Fetches live fiat currency exchange rates and conversions from XE.com, with a disclosed exchangerate-api.com fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeltennyson](https://clawhub.ai/user/abeltennyson)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users use this skill to answer fiat currency conversion and exchange-rate requests with a unit rate, converted amount, source, and timestamp. It is scoped to currency conversion rather than stocks, crypto, or broader financial-market analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested currency pairs and amounts are sent to SkillBoss API Hub, and exchangerate-api.com may be used as a fallback.

Mitigation: Install only when that network behavior is acceptable and check the returned source field before relying on the result.

Risk: Returned rates may be unsuitable as the sole source for accuracy-sensitive or compliance-sensitive financial work.

Mitigation: Review the returned source and timestamp, and verify critical conversions against an authoritative rate source.

Risk: Server evidence does not include stored GitHub import provenance for this version.

Mitigation: Review the artifact files and recorded file hashes before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abeltennyson/skills/abe-exchange-rates)
- [XE.com currency converter](https://www.xe.com/currencyconverter/convert/?Amount=${amount}&From=${from}&To=${to})
- [ExchangeRate-API fallback endpoint](https://open.er-api.com/v6/latest/${from})

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [JSON from the script, typically summarized for the user in concise Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes amount, source currency, target currency, rate, converted value, source, and timestamp.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
