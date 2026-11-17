## Description:

Gate Flash Swap Skill helps an agent preview, execute, and review Gate cryptocurrency flash swaps across one-to-one, one-to-many, and many-to-one modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage Gate flash swap workflows: checking supported pairs, previewing quotes, placing confirmed conversion orders, and reviewing order status or history.

### Deployment Geography for Use:

Global, subject to Gate service availability and regional compliance restrictions.

## Known Risks and Mitigations:

Risk: The skill can place real cryptocurrency conversion orders using a user's Gate account.

Mitigation: Use narrowly scoped API keys and require explicit confirmation of the exact returned quote before every create call.

Risk: The security summary flags under-scoped confirmation rules for a high-impact financial workflow.

Mitigation: Disable or review one-click execution policies unless the client can enforce immediate quote confirmation before order creation.

Risk: The security summary flags undeclared balance access in some workflows.

Mitigation: Disclose balance reads before consolidation workflows and grant only the minimum account permissions needed.

Risk: The workflow references mutable remote runtime rules.

Mitigation: Bundle or pin the runtime rules before trusting the workflow in production.

## Reference(s):

- [MCP Execution Specification](artifact/references/mcp.md)
- [Flash Swap Scenarios](artifact/references/scenarios.md)
- [Gate Runtime Rules](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- [Gate API Key Management](https://www.gate.io/myaccount/profile/api-key/manage)
- [ClawHub Skill Page](https://clawhub.ai/gate-exchange/skills/gate-exchange-flashswap)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown status summaries, quote drafts, confirmation prompts, result tables, and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live Gate quote, order, pair, limit, error, and status fields returned by MCP tools.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence; artifact frontmatter version: 2026.3.23-1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
