## Description:

Gate multi-collateral loan management skill for borrowing crypto against collateral and managing existing collateral-loan positions through Gate MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to inspect Gate multi-collateral loan rates, quotas, orders, and to prepare confirmed create, repay, add-collateral, or redeem-collateral actions through Gate MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create loans, repay loans, and change collateral through write-capable Gate MCP tools.

Mitigation: Grant Mcl:Write only when those workflows are intended, review each action draft, and require explicit confirmation before any write call.

Risk: The security summary says the skill asks agents to trust mutable remote instructions before using write-capable financial tools.

Mitigation: Install only if the Gate publisher is trusted and the external runtime-rules document can be verified before deployment.

Risk: Loan actions expose users to collateral, LTV, and liquidation risk.

Mitigation: Surface rates and LTV as reference information, avoid investment advice, and leave the borrow or repayment decision to the user.

## Reference(s):

- [MCP execution specification](artifact/references/mcp.md)
- [MCP tools reference](artifact/references/mcl-mcp-tools.md)
- [Scenarios and prompt examples](artifact/references/scenarios.md)
- [Gate MCP repository](https://github.com/gate/gate-mcp)
- [Gate API v4 multi-collateral loan documentation](https://www.gate.com/docs/developers/apiv4/zh_CN/#multi-collateral-loan)
- [Gate API key management](https://www.gate.io/myaccount/profile/api-key/manage)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration]

**Output Format:** [Markdown with action drafts, MCP tool-call guidance, and JSON payload descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write operations require an explicit user confirmation draft before the agent calls MCP tools.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
