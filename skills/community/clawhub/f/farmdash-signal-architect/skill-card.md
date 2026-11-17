## Description:

OpenClaw DeFi execution with FarmDash's MCP contract: LI.FI and Relay swaps, simulation, zero-custody settlement verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parmasanandgarlic](https://clawhub.ai/user/parmasanandgarlic)

### License/Terms of Use:

MIT-0

## Use Case:

DeFi users and agent developers use this skill to review market and portfolio signals, simulate trades, and prepare user-approved spot or futures actions through FarmDash.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trades, token approvals, destinations, and fees can have irreversible financial consequences.

Mitigation: Before signing, review the fresh quote, token contracts, chain, amounts, destination, and fees; require simulation and explicit user confirmation.

Risk: FarmDash may receive wallet and transaction information needed for service operation.

Mitigation: Understand what wallet and transaction data will be shared; onboarding analytics are optional. Never share private keys or seed phrases.

Risk: Autopilot can take actions within delegated limits.

Mitigation: Enable it only with limits and a revocation path you understand.

## Reference(s):

- [FarmDash Signal Architect on ClawHub](https://clawhub.ai/parmasanandgarlic/skills/farmdash-signal-architect)
- [FarmDash Agent Hub](https://www.farmdash.one/agents)
- [FarmDash documentation](https://www.farmdash.one/docs)
- [FarmDash agent status](https://www.farmdash.one/api/v1/agent/status)
- [FarmDash MCP discovery manifest](https://www.farmdash.one/.well-known/mcp.json)
- [FarmDash OpenAPI specification](https://www.farmdash.one/agents/openapi.yaml)
- [FarmDash fees](https://www.farmdash.one/fees)
- [FarmDash security information](https://www.farmdash.one/security)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Guidance, JSON]

**Output Format:** [Natural-language analysis and guidance with structured API request and response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Market and risk context, simulation results, and transaction preparation details; wallet-changing actions require fresh user approval and local signing.]

## Skill Version(s):

1.2.28 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
