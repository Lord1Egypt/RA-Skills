## Description:

Paid x402 endpoint: $0.007 USDC per call on Base. Returns an execute-now-or-wait verdict before a large order: scores the current execution window 0-100 from session, regime, Fear & Greed and volatility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Crypto traders and agents use the skill before a large order to review an execution-window score, an execute-now-or-wait verdict, and a suggested order type. The response is a short-lived market signal to consider alongside the user's own trading checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An execute-now-or-wait verdict and suggested order type may be stale or unsuitable for current market conditions.

Mitigation: Check the response timestamp and validity period, and consider the result as a signal rather than a standalone trading decision.

Risk: The authenticated request uses an EVM private key and signs a USDC payment on Base.

Mitigation: Keep the private key secret, use a wallet funded only for intended calls, and set the x402 maximum-payment policy to the amount you authorize.

## Reference(s):

- [Execution Window Optimizer API](https://apexrunner.ai/signals/execution-window-optimizer)
- [Slippage Forecast](https://apexrunner.ai/signals/slippage-forecast)
- [Optimal Order Routing](https://apexrunner.ai/signals/optimal-order-routing)
- [ClawHub skill release](https://clawhub.ai/kynto2001-ctrl/skills/execution-window-optimizer)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Trading guidance]

**Output Format:** [JSON response with an execution-window score, verdict, suggested order type, rationale, component scores, and validity period]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The endpoint charges per call; the skill documents a $0.007 USDC early-adopter price and a $0.01 USDC maximum-payment example.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
