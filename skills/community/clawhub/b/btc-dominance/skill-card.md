## Description:

Paid x402 endpoint: $0.007 USDC per call on Base. Returns BTC dominance percentage with trend direction signal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers can retrieve BTC dominance and its trend as context when assessing BTC versus altcoin allocation, altcoin season, or capital rotation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Each request incurs a USDC charge; the discounted price is time limited and the standard price is $0.01 per call.

Mitigation: Check the current price before calling and set a per-request spending cap at or below the amount you intend to pay.

Risk: The x402 client uses an EVM private key to authorize payments, so exposure of that key could put the wallet's funds at risk.

Mitigation: Use a dedicated wallet with only the funds needed for these requests, keep the key in a protected environment variable, and never place it in prompts or logs.

## Reference(s):

- [BTC dominance endpoint](https://apexrunner.ai/signals/btc-dominance)
- [Altcoin season signal](https://apexrunner.ai/signals/altcoin-season)
- [Capital rotation signal](https://apexrunner.ai/signals/capital-rotation-signal)
- [Regime signal](https://apexrunner.ai/signals/regime)

## Skill Output:

**Output Type(s):** [API Calls, JSON]

**Output Format:** [JSON response with dominance_pct, trend, and altcoin_season fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid per-call x402 request using USDC on Base]

## Skill Version(s):

1.0.2 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
