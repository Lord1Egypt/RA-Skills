## Description:

Use to run supervised autopilot cycles under a bounded, revocable session grant: intents, policy checks, approvals, receipts. Execution stays preview-gated.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parmasanandgarlic](https://clawhub.ai/user/parmasanandgarlic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to coordinate DeFi sessions, intent policy checks, approvals, and receipt review under explicit signing and execution controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial automation can lead to wallet-changing actions when valid authority and runtime readiness are present.

Mitigation: Check live domain readiness and grant scope before action; use fresh user signatures for USER_SIGNED actions, and do not treat an autopilot cycle result as submission or settlement.

Risk: Exposed API keys, session tokens, or local signing authority could enable unauthorized access or actions.

Mitigation: Protect credentials and local signing authority, use narrow short-lived grants, and verify current grant status and revocation before enabling autopilot.

## Reference(s):

- [FarmDash Agent Hub](https://www.farmdash.one/agents)
- [FarmDash documentation](https://www.farmdash.one/docs)
- [Agent API status and capability information](https://www.farmdash.one/api/v1/agent/status)
- [OpenAPI specification](https://www.farmdash.one/agents/openapi.yaml)
- [MCP discovery document](https://www.farmdash.one/.well-known/mcp.json)
- [FarmDash security information](https://www.farmdash.one/security)
- [ClawHub skill page](https://clawhub.ai/parmasanandgarlic/skills/farmdash-autonomous-operator)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Structured JSON data with concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Session, policy, intent, approval, and receipt information; execution status depends on current authority and readiness.]

## Skill Version(s):

1.0.15 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
