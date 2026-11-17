## Description:

30-day carrier on-time performance prediction for any carrier and trade lane via 5-factor model

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

External logistics, freight, and supply-chain teams use this skill before booking, monitoring, or rebooking ocean freight to compare carrier reliability for specific trade lanes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a raw EVM wallet private key for x402 micropayments without enough documented limits or handling details.

Mitigation: Use only a dedicated low-balance payment wallet and confirm exact charges, recipient, limits, and signing protections before repeated use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kynto2001-ctrl/skills/carrier-reliability)
- [Carrier Reliability Signal homepage](https://datasig.ai/signals/carrier-reliability)
- [Accuracy ledger](https://datasig.ai/accuracy/stats)
- [Blank Sailing related signal](https://datasig.ai/signals/blank-sailing)
- [Berth Congestion related signal](https://datasig.ai/signals/berth-congestion)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON signal response with concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses carrier, origin, and destination query parameters; responses may include reliability score, signal, trend, alternatives, confidence, and cost-of-inaction fields.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
