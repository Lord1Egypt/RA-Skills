## Description:

Paid x402 endpoint: $0.007 USDC per call on Base. Returns current Hyperliquid perpetual funding rates across tracked coins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can request current Hyperliquid perpetual funding rates across tracked coins to assess funding costs and potential arbitrage before opening or holding positions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan's benign verdict does not guarantee the skill is safe or suitable for a particular use.

Mitigation: Review the skill and decide whether it suits your needs before installing, as the security guidance advises.

Risk: The skill signs paid requests using an EVM private key, so calls can spend wallet funds.

Mitigation: Use a wallet funded for the intended calls, keep the private key private, and retain the documented per-request spend cap.

## Reference(s):

- [Funding Rate HL endpoint](https://apexrunner.ai/signals/funding-rate-hl)
- [Related funding-rate signal](https://apexrunner.ai/signals/funding-rate)
- [Related arb-spread signal](https://apexrunner.ai/signals/arb-spread)
- [ClawHub release page](https://clawhub.ai/kynto2001-ctrl/skills/funding-rate-hl)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Market data]

**Output Format:** [JSON object containing per-coin funding rates and a timestamp]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an EVM private key and USDC on Base; each call is paid. The skill states a $0.007 early-adopter price per call through 2027-01-01, with a $0.01 standard price.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
