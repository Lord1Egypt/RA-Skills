## Description:

Gate multi-account asset manager L2 skill for total asset views, margin and liquidation risk checks, earnings snapshots, affiliate commissions, and confirmed unified-account actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External Gate users use this skill to aggregate account balances, risk indicators, earn positions, and affiliate commission data across Gate account domains. It can prepare and execute unified-account borrow, collateral, leverage, or mode changes only after an Action Draft and explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads sensitive Gate account, asset, rebate, and position data across many account domains.

Mitigation: Install only with least-privilege Gate API credentials and prefer read-only permissions unless unified-account mutations are required.

Risk: The release is marked suspicious because it depends on mutable external runtime rules while using sensitive financial reads and write-capable tools.

Mitigation: Verify the external gate-runtime-rules.md source before use and review the skill before enabling write-capable workflows.

Risk: Unified-account borrow, collateral, leverage, and mode changes can affect margin, debt, or account configuration.

Mitigation: Require an Action Draft, risk disclosure, and immediate explicit confirmation before each mutation; use read-only mode when confirmation is missing or stale.

## Reference(s):

- [Gate Assets Manager MCP Specification](references/mcp.md)
- [Account and Asset Manager Scenarios](references/scenarios.md)
- [Gate Runtime Rules](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- [Gate API Key Management](https://www.gate.io/myaccount/profile/api-key/manage)
- [ClawHub Skill Page](https://clawhub.ai/gate-exchange/skills/gate-exchange-assets-manager)
- [Publisher Profile](https://clawhub.ai/user/gate-exchange)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown reports and Action Drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include data timestamps and module-level degradation notes when available.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
