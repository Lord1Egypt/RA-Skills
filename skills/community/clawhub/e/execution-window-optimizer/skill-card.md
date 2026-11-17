## Description:

Provides paid x402 access to execution-window guidance based on volatility and liquidity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading agents can query current ratings and best-window data to inform order timing, especially in volatile or latency-sensitive conditions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid requests use an EVM private key to authorize USDC payments, so an exposed key or an excessive payment cap could put wallet funds at risk.

Mitigation: Keep EVM_PRIVATE_KEY in a secrets manager and out of logs, review the endpoint, and cap each payment at the expected per-call amount.

## Reference(s):

- [Execution window signal endpoint](https://apexrunner.ai/signals/execution-window-optimizer)
- [APEX Runner](https://apexrunner.ai)
- [Slippage forecast signal](https://apexrunner.ai/signals/slippage-forecast)
- [Optimal order routing signal](https://apexrunner.ai/signals/optimal-order-routing)
- [ClawHub release page](https://clawhub.ai/kynto2001-ctrl/skills/execution-window-optimizer)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON market signal with a current rating, execution recommendation, and best-window data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid x402 request; requires an EVM wallet with USDC on Base and EVM_PRIVATE_KEY. The example caps payment at $0.01 USDC per call.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
