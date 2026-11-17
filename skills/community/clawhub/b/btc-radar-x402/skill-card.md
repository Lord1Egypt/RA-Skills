## Description:

Provides pay-per-call Bitcoin ecosystem data and Base/BSC token risk reports through x402, with candidate signals clearly identified as unverified.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaodongmei478](https://clawhub.ai/user/gaodongmei478)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users can request Bitcoin L1 inscription and token radar data, inspect unverified protocol-candidate signals, and review Base or BSC token risk indicators before a swap.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid calls spend real USDC, and advertised prices can change.

Mitigation: Check current pricing and confirm the amount, recipient, network, and asset before authorizing payment; use a wallet or client with spending limits.

Risk: Candidate protocol signals are unverified, and a low token risk score does not establish safety.

Mitigation: Label candidate signals as unverified and treat risk scores as indicators rather than guarantees.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/gaodongmei478/skills/btc-radar-x402)
- [BTC Radar x402 service](https://x402-btc-radar.jinli-x402.workers.dev)
- [Live x402 service catalog](https://x402-btc-radar.jinli-x402.workers.dev/.well-known/x402.json)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON API data with concise natural-language summaries and interpretation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pay-per-call data; candidate protocol signals are unverified, and risk scores are not guarantees of safety.]

## Skill Version(s):

1.0.0 (source: artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
