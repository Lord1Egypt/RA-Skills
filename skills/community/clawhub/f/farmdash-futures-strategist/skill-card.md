## Description:

Hyperliquid perps strategist: market scans, funding rates, position sizing, and user-signed EIP-712 order execution and cancellation with drawdown guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parmasanandgarlic](https://clawhub.ai/user/parmasanandgarlic)

### License/Terms of Use:

MIT-0

## Use Case:

AI trading agents use this skill to scan Hyperliquid perpetual markets, analyze funding and market conditions, size positions, prepare or cancel orders, and reconcile venue outcomes under approval and risk controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional onboarding can send a public agent wallet address to FarmDash, and bounded autonomous mode can trade without per-order confirmation when enabled.

Mitigation: Skip onboarding unless willing to share the public address. Use USER_SIGNED mode for fresh approval on each order or cancellation; before enabling bounded mode, review the owner-signed policy and verify live authority and runtime gates.

## Reference(s):

- [FarmDash Agent Hub](https://www.farmdash.one/agents)
- [Futures Strategist manual](https://www.farmdash.one/agents/skills/farmdash-futures-strategist)
- [FarmDash OpenAPI contract](https://www.farmdash.one/agents/openapi.yaml)
- [FarmDash MCP endpoint](https://www.farmdash.one/api/mcp)
- [Security and authority boundaries](https://www.farmdash.one/security)

## Skill Output:

**Output Type(s):** [Market analysis, Trading guidance, API calls, JSON]

**Output Format:** [Markdown summaries and structured JSON/API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool-dependent; order payloads require local EIP-712 signing.]

## Skill Version(s):

1.0.31 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
