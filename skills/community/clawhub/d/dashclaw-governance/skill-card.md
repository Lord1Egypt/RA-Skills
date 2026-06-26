## Description: <br>
Governance behavior for AI agents governed by DashClaw, covering guard checks, approval handling, action recording, session lifecycle management, and DashClaw MCP policy and capability loading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dashclaw](https://clawhub.ai/user/dashclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to make agents follow DashClaw governance while performing actions, including risk checks, approvals, audit recording, session handoff, and credential hygiene. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill changes the agent's workflow through DashClaw governance controls. <br>
Mitigation: Install it only when DashClaw governance is intended for the agent, and review the enabled policies, capabilities, and approval settings before use. <br>
Risk: Audit records, handoff bundles, learning notes, and related governance context may retain sensitive task information. <br>
Mitigation: Use a trusted DashClaw MCP server and avoid recording unnecessary secrets or sensitive details in summaries, records, and handoffs. <br>


## Reference(s): <br>
- [DashClaw Governance Patterns](references/governance-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code] <br>
**Output Format:** [Markdown guidance with tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; relies on configured DashClaw MCP resources and tools.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
