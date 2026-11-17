## Description:

Gate Exchange Spot Demo helps agents handle Gate spot trading account queries, order drafting, order amendments and cancellations, trigger orders, and post-trade verification through the Gate MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaixianggeng](https://clawhub.ai/user/gaixianggeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to guide Gate spot trading workflows, including balance checks, buy/sell order drafts, open-order management, trigger orders, and fill verification through Gate MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place, amend, and cancel live Gate spot orders when granted Spot:Write access.

Mitigation: Install only in trusted Gate MCP environments, grant permissions deliberately, and require fresh explicit user confirmation before each trade, amendment, cancellation, cancel-all, batch operation, or trigger-order placement.

Risk: The skill depends on remote runtime rules that are not bundled with this release and may change independently.

Mitigation: Prefer a release that bundles or pins the runtime rules locally before use, and review the effective rules before enabling live trading.

## Reference(s):

- [Gate Spot MCP Specification](references/mcp.md)
- [Gate Spot Scenario Reference](references/scenarios.md)
- [Gate Spot Exchange Skill README](README.md)
- [Gate Runtime Rules](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- [Gate API Key Management](https://www.gate.io/myaccount/profile/api-key/manage)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown responses with order drafts, status tables, and structured MCP tool call arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Gate MCP access and explicit user confirmation before live trade, amendment, cancellation, or trigger-order placement.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
