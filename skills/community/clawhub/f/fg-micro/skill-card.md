## Description:

Paid x402 endpoint: $0.007 USDC per call on Base. Returns lightweight Fear & Greed index snapshot for high-frequency polling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading agents use this skill to request a lightweight Fear & Greed snapshot for frequent sentiment checks, trading-decision gates, or before requesting more expensive signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Frequent polling can incur repeated USDC charges, and the documented discounted and standard prices differ.

Mitigation: Check the current per-call price and set an x402 maximum amount before enabling polling; the example uses a payment cap.

Risk: The request signs payments using an EVM private key.

Mitigation: Keep the key in a protected environment variable and use a wallet funded only for the intended spend.

## Reference(s):

- [fg-micro endpoint](https://apexrunner.ai/signals/fg-micro)
- [APEX Runner](https://apexrunner.ai)
- [Fear & Greed signal](https://apexrunner.ai/signals/fear-greed)
- [Regime Micro signal](https://apexrunner.ai/signals/regime-micro)
- [ClawHub release page](https://clawhub.ai/kynto2001-ctrl/skills/fg-micro)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON snapshot with a sentiment label, value, and timestamp, plus request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each request is paid in USDC on Base; the skill documents a $0.007 early-adopter price through 2027-01-01 and a $0.01 standard price.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
