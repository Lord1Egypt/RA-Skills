## Description:

Use when comparing lending and yield pools by net expected APY, TVL depth, stablecoin and impermanent-loss risk. Read-only; deposits need user-signed approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parmasanandgarlic](https://clawhub.ai/user/parmasanandgarlic)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents can compare lending and yield pools using expected yield, liquidity depth, stability history, stablecoin exposure, and impermanent-loss risk. The results support research and pool selection before any deposit decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan found a mismatch between stated deposit approval limits and a handoff that allows bounded autonomous execution.

Mitigation: Review the deposit authorization terms before installing. Confirm each deposit requires explicit approval, or that any delegation is clearly disclosed and limited.

Risk: The security scan was partial, and unresolved references leave some evidence incomplete.

Mitigation: Review the remaining authorization references and do not treat the partial scan as complete evidence.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/parmasanandgarlic/skills/farmdash-supply-master)
- [FarmDash Supply Master manual](https://www.farmdash.one/agents/skills/farmdash-supply-master)
- [FarmDash agent documentation](https://www.farmdash.one/docs)
- [FarmDash OpenAPI contract](https://www.farmdash.one/agents/openapi.yaml)
- [FarmDash MCP discovery manifest](https://www.farmdash.one/.well-known/mcp.json)
- [FarmDash security and authority boundaries](https://www.farmdash.one/security)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, JSON]

**Output Format:** [Structured yield comparison and ranking with risk context]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on available yield data and the selected pool filters.]

## Skill Version(s):

1.0.1 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
