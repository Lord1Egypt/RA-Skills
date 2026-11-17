## Description:

Gate spot trading and account operations skill for buying and selling spot assets, checking account value, and placing conditional or trigger orders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate Gate spot accounts through a configured Gate MCP session, including balance checks, order drafting, order placement, amendments, cancellations, trigger-order workflows, and post-trade verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place, amend, and cancel real Gate spot orders using the configured API key.

Mitigation: Use a restricted Gate API key, review each order draft, and require explicit confirmation immediately before any write action.

Risk: TP/SL behavior is inconsistent across the evidence, with both trigger-order support and a statement that TP/SL is not supported.

Mitigation: Review and correct TP/SL handling before relying on it; require clear trigger price, side, amount, and execution semantics in every TP/SL draft.

Risk: Broad activation language could route adjacent intents into a real trading workflow.

Mitigation: Keep execution limited to documented Gate spot tools and route futures, DEX, and analysis-only requests away from spot write actions.

## Reference(s):

- [Gate skills repository](https://github.com/gate/gate-skills)
- [Gate Spot Runtime Rules](references/gate-runtime-rules.md)
- [Gate Spot MCP Specification](references/mcp.md)
- [Gate Spot Scenarios](references/scenarios.md)
- [Gate API key management](https://www.gate.com/myaccount/profile/api-key/manage)

## Skill Output:

**Output Type(s):** [Markdown, API Calls, Guidance]

**Output Format:** [Markdown reports with order drafts, execution summaries, status explanations, and MCP tool call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured Gate MCP session with GATE_API_KEY and GATE_API_SECRET; write actions require explicit confirmation before execution.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
