## Description:

Inspect supported DeFi wallet balances, allocation, idle capital, and portfolio signals to produce read-only snapshots and research recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parmasanandgarlic](https://clawhub.ai/user/parmasanandgarlic)

### License/Terms of Use:

MIT-0

## Use Case:

External DeFi wallet owners use this skill to review address-based portfolio snapshots, allocation drift, and candidate reserves, then consider possible rebalance plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional onboarding check sends a public wallet address to FarmDash and registers it for service telemetry.

Mitigation: Run the check only after explicit informed consent; use keyless Scout access when the onboarding step is unnecessary.

## Reference(s):

- [FarmDash Agent Integration Documentation](https://www.farmdash.one/docs)
- [FarmDash OpenAPI Contract](https://www.farmdash.one/agents/openapi.yaml)
- [FarmDash MCP Discovery Manifest](https://www.farmdash.one/.well-known/mcp.json)
- [Canonical FarmDash Wagon Steward Manual](https://www.farmdash.one/openclaw-skills/farmdash-wagon-steward/SKILL.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance]

**Output Format:** [Structured portfolio data summarized as concise text or Markdown, with JSON tool results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Time-bound, coverage-aware snapshots and research proposals; no transaction execution.]

## Skill Version(s):

1.7.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
