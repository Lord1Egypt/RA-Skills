## Description:

Reconciles recorded on-chain activity and costs, and exports spot transaction records as CSV for review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parmasanandgarlic](https://clawhub.ai/user/parmasanandgarlic)

### License/Terms of Use:

MIT-0

## Use Case:

DeFi users and portfolio operators use the skill after trading to review confirmed spot activity and recorded costs, then export transaction records for accounting review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill can send wallet-scoped requests to FarmDash.

Mitigation: Review FarmDash’s security information and query only wallet addresses you intend to share.

Risk: The security scan was partial because two local path-like references could not be resolved.

Mitigation: Review the unresolved references and scan the complete release before installation.

## Reference(s):

- [Canonical FarmDash Ledger Keeper manual](https://www.farmdash.one/agents/skills/farmdash-ledger-keeper)
- [FarmDash agent integration documentation](https://www.farmdash.one/docs)
- [FarmDash OpenAPI contract](https://www.farmdash.one/agents/openapi.yaml)
- [FarmDash MCP discovery manifest](https://www.farmdash.one/.well-known/mcp.json)
- [FarmDash security and authority boundaries](https://www.farmdash.one/security)
- [FarmDash fees and commercial terms](https://www.farmdash.one/fees)

## Skill Output:

**Output Type(s):** [Text, CSV, Accounting guidance]

**Output Format:** [Text activity and cost summaries; CSV spot transaction records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records are for review; the skill does not claim realized P&L or provide tax advice.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
