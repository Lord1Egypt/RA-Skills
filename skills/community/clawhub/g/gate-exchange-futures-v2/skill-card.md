## Description:

Gate Exchange USDT perpetual futures trading skill for opening and closing positions, managing leverage, canceling or amending orders, and setting TP/SL or conditional orders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading operators use this skill to guide an agent through Gate USDT perpetual futures workflows, including position management, order updates, TP/SL, conditional opens, and trigger-order management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to perform live Gate USDT perpetual futures actions with Fx:Write permissions.

Mitigation: Use restricted exchange credentials and require explicit confirmation before every order, cancellation, leverage change, or margin-mode switch.

Risk: Mutable remote runtime instructions can change behavior outside the released artifact.

Mitigation: Prefer a version that vendors or pins runtime rules before deployment.

Risk: Inconsistent confirmation rules could lead to unintended financial write actions.

Mitigation: Enforce immediate explicit confirmation for every write action and review order drafts before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gate-exchange/skills/gate-exchange-futures-v2)
- [Gate publisher profile](https://clawhub.ai/user/gate-exchange)
- [Gate website](https://www.gate.com)
- [Gate API key management](https://www.gate.io/myaccount/profile/api-key/manage)
- [MCP execution specification](artifact/references/mcp.md)
- [Open position reference](artifact/references/open-position.md)
- [Close position reference](artifact/references/close-position.md)
- [Take profit and stop loss reference](artifact/references/tp-sl.md)
- [Conditional order reference](artifact/references/conditional.md)
- [Triggered order management reference](artifact/references/manage.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, API Calls]

**Output Format:** [Markdown text with confirmation prompts, order drafts, execution summaries, and MCP tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation before financial write actions.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
