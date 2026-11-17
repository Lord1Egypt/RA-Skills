## Description:

Provides Gate unified-account assistance for equity and mode checks, borrowable and transferable limits, borrowing and repayment, loan and interest history, leverage settings, and collateral management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External Gate users and operators use this skill to inspect unified-account status and prepare or execute confirmed borrowing, repayment, mode, leverage, and collateral actions through a configured Gate MCP session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide sensitive financial write actions, including borrowing, repayment, mode changes, leverage settings, and collateral changes.

Mitigation: Install only when the assistant should access a Gate unified account, and require explicit confirmation after reviewing the draft amount, currency, target mode or setting, and risk note.

Risk: The configured Gate session requires Unified:Read and Unified:Write permissions.

Mitigation: Use only the local MCP session with configured credentials, never paste API secrets into chat, and stop write actions on authentication or permission errors.

Risk: Leverage, collateral, and account-mode changes can affect borrow power and liquidation risk.

Mitigation: Validate account mode, limits, and platform constraints before mutation, then verify post-state through a read endpoint.

## Reference(s):

- [Gate Unified MCP Specification](artifact/references/mcp.md)
- [Gate Unified Account Runtime Rules](artifact/references/gate-runtime-rules.md)
- [Gate Unified Account Scenarios](artifact/references/scenarios.md)
- [Gate Skills Repository](https://github.com/gate/gate-skills)
- [Gate API Key Management](https://www.gate.com/myaccount/profile/api-key/manage)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown reports, action drafts, and execution summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves API numeric strings exactly when available; write actions require explicit single-use confirmation.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
