## Description:

Specify an autonomous or tool-using AI agent before building it, including goals, tools, guardrails, approval gates, memory, escalation, evaluation, and failure handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent designers use this skill to draft an agent specification before implementation, making the agent's authority, tools, approval gates, evaluation, and failure handling explicit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent specifications could omit approval gates, budgets, or escalation rules for real-world actions.

Mitigation: Review generated specs before implementation and require explicit human approval gates, max-step or max-cost budgets, and escalation triggers.

Risk: Separately linked companion skills may have different behavior or risk profiles.

Mitigation: Review any companion skill before using it as part of an agent design workflow.

## Reference(s):

- [Agent Spec homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/agent-spec.html)
- [ClawHub skill page](https://clawhub.ai/mohitagw15856/skills/agent-spec)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Configuration]

**Output Format:** [Markdown agent specification with tables and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured sections for goal and scope, tools, control loop, guardrails, memory, escalation, evaluation, and failure handling.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
