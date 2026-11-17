## Description:

Installable CEO assistant agent package for foreign-trade teams that provides the CEO小茂 coordinator persona, role boundaries, routing rules, workspace scaffolding, operating templates, installation steps, quick-start examples, and companion skill guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xingfan0828](https://clawhub.ai/user/xingfan0828)

### License/Terms of Use:

MIT-0

## Use Case:

External users and foreign-trade teams use this agent package to set up a CEO-style coordination layer that assigns work, tracks progress, summarizes outcomes, and reports risks across specialist roles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package creates durable local workspace files that may later contain business context, customer details, or operational memory.

Mitigation: Review USER.md and MEMORY.md before reuse, and do not place passwords or private customer data in memory files.

Risk: The optional companion package can add outreach or automation capabilities beyond this coordinator package.

Mitigation: Inspect the separate ceo-xiaomao companion package before installing or using automation and outreach capabilities.

## Reference(s):

- [CEO小茂 Agent package details](references/PACKAGE-DETAILS.md)
- [QUICKSTART.md](references/QUICKSTART.md)
- [SETUP.md](references/SETUP.md)
- [RULES.md — 团队协作规则](references/RULES.md)
- [SOUL.md - CEO小茂](references/SOUL.md)
- [WORKFLOW.md](references/WORKFLOW.md)
- [Install examples](references/INSTALL-EXAMPLES.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and workspace template files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a local coordinator workspace with Markdown memory, identity, agent, task, document, lead, CRM, attachment, and daily memory paths when the initialization script is run.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
