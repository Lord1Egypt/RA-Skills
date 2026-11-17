## Description:

Paid x402 endpoint: $0.007 USDC per call on Base. Returns composite APEX score combining regime, momentum, and risk metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this paid market signal endpoint to retrieve a composite crypto score for ranking opportunities. The score can inform a strategy after independent review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Each request signs a USDC payment using the configured EVM wallet key.

Mitigation: Use a dedicated wallet funded only for intended calls, keep the x402 maximum-amount policy at or below the expected per-call price, and protect EVM_PRIVATE_KEY.

Risk: A composite market score may be over-relied on when ranking or trading opportunities.

Mitigation: Treat the returned score as one input and independently validate it against the strategy and risk limits before trading.

## Reference(s):

- [APEX Composite endpoint](https://apexrunner.ai/signals/apex-composite)
- [ClawHub skill release](https://clawhub.ai/kynto2001-ctrl/skills/apex-composite)
- [Publisher profile](https://clawhub.ai/user/kynto2001-ctrl)
- [Related signal: combined-alpha](https://apexrunner.ai/signals/combined-alpha)
- [Related signal: signal-intelligence](https://apexrunner.ai/signals/signal-intelligence)
- [Related signal: apex-alpha-score](https://apexrunner.ai/signals/apex-alpha-score)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Paid x402 HTTP GET request with a JSON response and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each request incurs a USDC payment on Base; authentication signing uses an EVM wallet key.]

## Skill Version(s):

1.0.2 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
