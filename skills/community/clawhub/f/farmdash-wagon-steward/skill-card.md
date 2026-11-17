## Description:

Use when watching a DeFi portfolio: balances, position health, idle capital, drift. Read-only; never rebalances or moves funds without your signature.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parmasanandgarlic](https://clawhub.ai/user/parmasanandgarlic)

### License/Terms of Use:

MIT-0

## Use Case:

Wallet holders and portfolio analysts use the skill to review observable balances, allocation drift, and candidate liquid reserves, then discuss possible next steps. It produces read-only analysis and rebalance proposals for the user to review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried public wallet addresses are sent to FarmDash; optional onboarding and installation attribution can add analytics linkage.

Mitigation: Use only wallet addresses you are comfortable querying, and skip optional onboarding and installation attribution if you do not want the additional analytics linkage.

Risk: Tier wording conflicts about wallet-read availability, which may affect whether the service can return portfolio data.

Mitigation: Check FarmDash's current status contract and access requirements before relying on wallet reads.

Risk: The supplied security review covers the bundled instructions and manifest, not the remote FarmDash service.

Mitigation: Do not supply private keys or grant transaction authority to this read-only skill.

## Reference(s):

- [FarmDash Wagon Steward on ClawHub](https://clawhub.ai/parmasanandgarlic/skills/farmdash-wagon-steward)
- [FarmDash Agent Hub](https://www.farmdash.one/agents)
- [FarmDash documentation](https://www.farmdash.one/docs)
- [FarmDash API status and access requirements](https://www.farmdash.one/api/v1/agent/status)
- [FarmDash OpenAPI specification](https://www.farmdash.one/agents/openapi.yaml)
- [FarmDash MCP discovery configuration](https://www.farmdash.one/.well-known/mcp.json)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [Portfolio summaries and discussion-level proposals presented as concise Markdown with structured data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only snapshots; state coverage gaps, timestamps, and unpriced assets when available.]

## Skill Version(s):

1.7.4 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
