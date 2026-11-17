## Description:

Hyperliquid perps strategist: market scans, funding rates, position sizing, and user-signed EIP-712 order execution & cancellation with drawdown guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parmasanandgarlic](https://clawhub.ai/user/parmasanandgarlic)

### License/Terms of Use:

MIT-0

## Use Case:

Traders and agent developers use it to research Hyperliquid perpetual markets, compare setups, size exposure, and manage locally signed orders or cancellations under the selected execution policy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trading can lose funds despite local signing and risk checks.

Mitigation: Review each order and the disclosed 0.001% builder fee, keep private keys local, and review policy limits, expiry, and revocation before enabling autonomy.

Risk: Server-side safeguards were not independently verified because their implementation is unbundled.

Mitigation: Check the publisher's deployment status before execution.

## Reference(s):

- [FarmDash Agents](https://www.farmdash.one/agents)
- [FarmDash Security and Authority Boundaries](https://www.farmdash.one/security)
- [FarmDash Deployment Status](https://www.farmdash.one/api/v1/agent/status)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance, API Calls]

**Output Format:** [Structured strategy data and concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Market scans, position sizing, strategy recommendations, and order preparation or execution results; no profit or loss-limit guarantee.]

## Skill Version(s):

1.0.29 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
