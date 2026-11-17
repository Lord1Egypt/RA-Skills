## Description:

Paid x402 endpoint: $0.007 USDC per call on Base. Returns altcoin season index — measures capital rotation from BTC to alts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Agents supporting people who compare altcoin and Bitcoin market regimes can retrieve an altcoin season index as market context when considering portfolio sizing or rotation timing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the signal incurs a USDC payment and the example gives the client access to an EVM private key for payment signing.

Mitigation: Use a dedicated wallet with only the USDC needed for intended calls, keep its private key in a secret store, and set a strict per-call payment cap.

## Reference(s):

- [Altcoin season signal endpoint](https://apexrunner.ai/signals/altcoin-season)
- [BTC dominance signal](https://apexrunner.ai/signals/btc-dominance)
- [Capital rotation signal](https://apexrunner.ai/signals/capital-rotation-signal)
- [Market regime signal](https://apexrunner.ai/signals/regime)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Code]

**Output Format:** [JSON signal response and Markdown usage guidance with a Python example]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid x402 request; requires an EVM wallet with USDC on Base and EVM_PRIVATE_KEY.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
