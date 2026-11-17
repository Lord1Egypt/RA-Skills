## Description:

Queries a paid x402 endpoint for signals that identify crowded trades and potential liquidation risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Trading agents use this signal before entering popular trades or as a risk gate to assess crowded positions and possible liquidation cascade exposure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The example uses an EVM private key to authorize paid USDC requests, and the endpoint price may change.

Mitigation: Use a dedicated wallet with only the intended USDC balance, protect the private key, and confirm the current per-call price and payment cap before approving requests.

## Reference(s):

- [Crowded Trade Detector endpoint](https://apexrunner.ai/signals/crowded-trade-detector)
- [Agent Stress Index](https://apexrunner.ai/signals/agent-stress-index)
- [Liquidation Pressure](https://apexrunner.ai/signals/liquidation-pressure)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON market-signal response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One paid response per request; requires an EVM wallet with USDC on Base and an EVM_PRIVATE_KEY.]

## Skill Version(s):

1.0.2 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
