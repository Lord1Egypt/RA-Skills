## Description:

Helps agents plan, audit, and improve email workflows with explicit tool handoffs, review loops, approval gates, and safe execution boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polnikale](https://clawhub.ai/user/polnikale)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to plan, review, implement, audit, or improve agent-managed email work. It helps define agent roles, tool-safe handoffs, acceptance criteria, QA checkpoints, approval gates, and audit-friendly next steps before any live email action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent-managed email work can affect live sends, contact imports, DNS settings, suppression rules, or production automations.

Mitigation: Require explicit human approval before high-risk live-system actions and identify the responsible reviewer for risky changes.

Risk: Missing source evidence, consent status, or suppression state can lead to unsafe email recommendations.

Mitigation: State supporting source material, preserve assumptions, and avoid filling missing consent or suppression facts by inference.

Risk: Tool handoffs can blur authority between agents and operators.

Mitigation: Define what each agent may read, draft, change, and execute, with inputs, outputs, acceptance criteria, and an audit trail.

## Reference(s):

- [Email Agent Skill Operating Checklist](artifact/references/operating-checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/polnikale/skills/emailagentskill)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent routing plans, approval matrices, tool handoff specs, review loops, execution checklists, and audit-friendly status reports.]

## Skill Version(s):

0.1.0 (source: evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
