## Description:

Paid x402 endpoint: $0.007 USDC per call on Base. Returns funding rate analysis across perps with arb opportunity scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and crypto traders use the endpoint to retrieve perp funding-rate analysis and arb opportunity scores before opening positions or while monitoring funding costs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The x402 client signs a paid request using an EVM private key and spends USDC on Base.

Mitigation: Use a dedicated wallet with only the intended USDC balance, keep its private key secret, and retain the configured payment cap.

Risk: Funding-rate analysis and suggested actions may be incomplete or unsuitable for a trading decision.

Mitigation: Check the returned data against current market conditions and independent sources before acting.

## Reference(s):

- [Funding Rate API](https://apexrunner.ai/signals/funding-rate)
- [Funding Rate HL signal](https://apexrunner.ai/signals/funding-rate-hl)
- [Arbitrage Spread signal](https://apexrunner.ai/signals/arb-spread)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance]

**Output Format:** [JSON response with funding-rate metrics, arb score, and recommended action]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each endpoint call incurs a USDC payment on Base.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
