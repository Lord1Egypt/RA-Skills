## Description:

Crypto market signals and pre-trade checks for agents, paid per call in USDC on Base via x402 (from $0.001, no account, no API key): funding rates and predictions, liquidation zones, sentiment, stablecoin peg health, DEX-vs-CEX and cross-exchange spreads, ETF flows, memecoin risk checks, labelled crypto news, a search for x402 services that answer right now, a red-flag check before a trade, wallet liquidation risk with alerts, signed receipts, recorded history anchored on Base. Every predictive signal has a public track record against a naive baseline. Use when the user asks about crypto market conditions, funding, liquidations, depeg risk, a memecoin's risk or crypto news, needs a paid x402 service for some other task, or wants crypto data an agent can pay for itself.

This skill is ready for commercial/non-commercial use.

## Publisher:

[speteai](https://clawhub.ai/user/speteai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can ask agents for current crypto market readings, risk checks, and relevant news. Agents can also retrieve signal history or configure alerts, while checking calibration before treating predictive signals as forecasts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid calls can spend USDC from the connected wallet.

Mitigation: Use a dedicated wallet, set spending limits, and require approval for paid calls.

Risk: Text sent for classification is processed in plain text by external GPU operators.

Mitigation: Do not submit private or sensitive text to the classification endpoint.

## Reference(s):

- [AgentData service](https://agentdata-api.com)
- [Live catalogue and current prices](https://agentdata-api.com/info)
- [Signal calibration and track records](https://agentdata-api.com/calibration)
- [Pricing](https://agentdata-api.com/pricing)
- [Integration guide](https://agentdata-api.com/llms.txt)
- [AgentData on ClawHub](https://clawhub.ai/speteai/skills/agentdata)

## Skill Output:

**Output Type(s):** [API calls, Guidance, Shell commands, Configuration instructions]

**Output Format:** [JSON market data with Markdown guidance and inline shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes current readings, risk checks, signal history, and alert configuration guidance.]

## Skill Version(s):

1.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
