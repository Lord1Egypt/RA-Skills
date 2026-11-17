## Description:

Gate unified account operations skill for unified account equity, margin borrowing, repayments, leverage modes, collateral settings, and related account limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaixianggeng](https://clawhub.ai/user/gaixianggeng)

### License/Terms of Use:

MIT-0

## Use Case:

External Gate users and developers use this skill to inspect unified account equity, borrowable and transferable limits, loan and interest records, leverage settings, and collateral status. The skill can also draft and, after explicit confirmation, execute Gate unified-account changes through the configured MCP session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform financial write actions for borrowing, repayment, leverage, account mode, and collateral settings.

Mitigation: Require an Action Draft and immediate explicit user confirmation before every mutation, and treat confirmation as single-use.

Risk: Over-borrowing, invalid leverage settings, or collateral changes can affect margin and liquidation risk.

Mitigation: Run pre-checks for limits, current mode, platform constraints, and account state before drafting or executing changes.

Risk: API keys with broad access could increase account exposure.

Mitigation: Use API keys limited to Unified:Read and Unified:Write, rely on the configured local MCP session, and never paste secrets into chat.

Risk: Rounded or normalized financial values can mislead users.

Mitigation: Preserve API numeric strings exactly and include raw timestamps with readable local times when available.

## Reference(s):

- [Gate skill repository homepage from ClawHub metadata](https://github.com/gate/gate-skills)
- [Gate Unified MCP Specification](references/mcp.md)
- [Gate Unified Account Runtime Rules](references/gate-runtime-rules.md)
- [Unified account scenarios](references/scenarios.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown reports, action drafts, and MCP tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves API numeric strings and includes raw timestamps with readable local times when available.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
