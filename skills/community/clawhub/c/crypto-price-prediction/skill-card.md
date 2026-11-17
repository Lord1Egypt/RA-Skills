## Description:

Fetches next-hour predicted price for BTC/ETH from external prediction API. Supports BTCUSDT and ETHUSDT symbols only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenho1394](https://clawhub.ai/user/stevenho1394)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request a quick next-hour BTCUSDT or ETHUSDT price prediction from an external prediction service, with current price and direction returned when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends BTC/ETH lookup requests to an external prediction service and CoinGecko.

Mitigation: Use it only in environments where those outbound requests are approved, and review or restrict network access before deployment.

Risk: The external prediction methodology is opaque and the output may be inaccurate or misleading.

Mitigation: Treat predictions as informational only and require independent review before making trading or financial decisions.

Risk: The skill stores a timezone preference under the user's home configuration directory.

Mitigation: Confirm local preference storage is acceptable for the deployment environment and avoid entering sensitive values as timezone input.

Risk: Server security guidance notes that the OpenClaw manifest should be updated to match the fuller SKILL.md documentation.

Mitigation: Align manifest metadata and output fields with the documented v1.0.1 behavior before relying on generated integration docs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stevenho1394/skills/crypto-price-prediction)
- [ClawHub publisher profile](https://clawhub.ai/user/stevenho1394)
- [External next-hour prediction API](https://myfastapi.zeabur.app/v1/demo/predictions/next_hour)
- [CoinGecko simple price API](https://api.coingecko.com/api/v3/simple/price)

## Skill Output:

**Output Type(s):** [json, text]

**Output Format:** [JSON object with optional human-readable text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns timestamp, symbol, one-hour horizon, current price when available, predicted price, and predicted direction.]

## Skill Version(s):

1.0.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
