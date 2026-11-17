## Description:

A paid x402 endpoint returns Bollinger Band analysis with squeeze detection and breakout probability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to request Bollinger Band squeeze, position, and breakout probability signals when assessing potential breakout or mean-reversion trades. Requests require an EVM wallet funded with USDC on Base and incur a per-call charge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The x402 request signs a payment using EVM_PRIVATE_KEY, so mishandling the key or using a wallet with substantial funds could expose assets.

Mitigation: Protect the key in a secret manager, use a dedicated wallet with limited funds, and enforce a per-call payment cap; the example sets the cap to $0.01 USDC.

Risk: Breakout probability and other market signals can be inaccurate and could contribute to poor trading decisions.

Mitigation: Treat the response as one analytical input, verify it against current market data, and apply independent trading and risk controls.

## Reference(s):

- [BB Analysis endpoint](https://apexrunner.ai/signals/bb-analysis)
- [ClawHub skill release](https://clawhub.ai/kynto2001-ctrl/skills/bb-analysis)
- [Mean Reversion Scan](https://apexrunner.ai/signals/mean-reversion-scan)
- [Volume Analysis](https://apexrunner.ai/signals/volume-analysis)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, JSON]

**Output Format:** [JSON signal data, including squeeze status, band position, and breakout probability]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A paid endpoint response; the example response contains squeeze, position, and breakout_probability fields.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
