## Description:

Discovers available WorkBuddy connectors and helps compose on-demand, scheduled, or reusable workflows with cross-connector suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng)

### License/Terms of Use:

MIT-0

## Use Case:

Teams and developers use this skill to explore available connectors, plan and validate multi-connector workflows, and propose automations or reusable processes for business tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connector workflows may read sensitive business data or send messages to unintended recipients.

Mitigation: Check connector permissions and confirm destinations and recipients before running the workflow.

Risk: Scheduled automations or other write actions may cause unintended changes.

Mitigation: Review the schedule and each write step; require explicit user confirmation before creating or executing them.

Risk: Custom reference examples may expose private information.

Mitigation: Use only trusted, desensitized examples when extending the skill's references.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/wangjiaocheng/skills/connector-workflow-composer)
- [Connector workflow requirements](artifact/references/connector-workflow-requirements.md)
- [Connector workflow catalog](artifact/references/connector-workflow-catalog.md)
- [Workflow plan template](artifact/templates/workflow-plan-template.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Configuration instructions]

**Output Format:** [Markdown workflow plans, connector tables, and automation suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plans cover connector authorization, read/write steps, scheduling where relevant, and confirmation points.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; bundled skill frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
