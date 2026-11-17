## Description:

Gate Simple Earn management skill for flexible and fixed-term savings product queries, subscriptions, redemptions, interest, positions, APY, and minimum-rate workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate Gate Simple Earn flexible and fixed-term products through an agent, including product discovery, position and interest queries, subscriptions, redemptions, and minimum-rate changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial write actions can subscribe, redeem, or change Simple Earn positions when Earn:Write is enabled.

Mitigation: Require a fresh explicit confirmation that shows the final asset, amount, product, rate or term, order ID when applicable, and consequences before every write call.

Risk: Security evidence reports mutable remote runtime rules and conflicting safeguards around financial actions.

Mitigation: Pin or vendor shared runtime rules and reconcile write-path safeguards before deployment; treat the suspicious security verdict as requiring review before installation.

Risk: APY and rate displays may be mistaken for investment advice or guaranteed returns.

Mitigation: Keep rates as reference information, avoid recommending specific currencies or predicting rates, and include the product-terms disclaimer when showing APY.

## Reference(s):

- [Simple Earn Flexible (Uni) MCP Tools Reference](references/earn-uni-mcp-tools.md)
- [Fixed Earn (Fixed-term) MCP Tools Reference](references/fixed-earn-mcp-tools.md)
- [Gate SimpleEarn MCP Specification](references/mcp.md)
- [Simple Earn Scenarios & Prompt Examples](references/scenarios.md)
- [Gate MCP](https://github.com/gate/gate-mcp)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, API Calls]

**Output Format:** [Markdown responses with MCP tool call requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation before financial write actions; flexible Uni outputs omit time fields.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
