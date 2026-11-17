## Description:

Reviews recorded on-chain spot activity and costs, highlights confirmation and completeness limits, and exports CSV records for reconciliation; it does not calculate realized P&L.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parmasanandgarlic](https://clawhub.ai/user/parmasanandgarlic)

### License/Terms of Use:

MIT-0

## Use Case:

DeFi users and accounting teams use it after trading to reconcile recorded spot activity and execution costs, check confirmation and missing-data limits, and export records for professional review. It provides informational records, not tax advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial because two local references could not be resolved, so its benign verdict is not complete evidence.

Mitigation: Review the skill instructions and the copy obtained before installing or relying on its outputs.

Risk: Recorded ledger activity and costs may be incomplete and do not establish realized P&L, fills, or tax lots.

Mitigation: Reconcile against authoritative fills, fees, transfers, and cost-basis records, and have records reviewed by a qualified professional before filing.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/parmasanandgarlic/skills/farmdash-ledger-keeper)
- [FarmDash Agent Hub](https://www.farmdash.one/agents)
- [Canonical Ledger Keeper skill manual](https://www.farmdash.one/openclaw-skills/farmdash-ledger-keeper/SKILL.md)
- [FarmDash integration documentation](https://www.farmdash.one/docs)
- [FarmDash OpenAPI contract](https://www.farmdash.one/agents/openapi.yaml)
- [FarmDash MCP discovery manifest](https://www.farmdash.one/.well-known/mcp.json)

## Skill Output:

**Output Type(s):** [Text, CSV, Guidance]

**Output Format:** [Text summaries and CSV records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Activity and cost summaries include confirmation and completeness information; realized P&L is returned as null.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
