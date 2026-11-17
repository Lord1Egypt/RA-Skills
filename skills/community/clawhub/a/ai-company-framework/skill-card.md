## Description:

AI Company Framework provides schema, naming, modularization, registry, skill-learning, and starter-template guidance for AI-company framework and infrastructure skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnsmithfan](https://clawhub.ai/user/johnsmithfan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent-system maintainers use this skill to standardize AI-company skills, define reusable module patterns, manage registries, prepare prompts, and guide implementation, testing, documentation, and workflow execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad file-write, network, and MCP authority could allow unintended workspace changes, external API use, subagent activity, or shared-state updates.

Mitigation: Use the skill only in a trusted workspace and require explicit approval before write, network, installation, activation, or HQ state-change steps.

Risk: Under-scoped implementation and workflow prompts could produce changes, test plans, documentation, or operational steps that are incomplete or unsuitable for the target environment.

Mitigation: Review generated guidance before execution, validate proposed changes in a sandbox, and confirm dependency, permission, and audit requirements before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/johnsmithfan/skills/ai-company-framework)
- [ClawHub Homepage Metadata](https://clawhub.com/skills/ai-company-framework)
- [Method Patterns & Detailed Specifications](references/method-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured prompt blocks and reference documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces human-reviewable guidance, implementation prompts, test cases, documentation outlines, and workflow execution checklists.]

## Skill Version(s):

3.0.2 (source: server release metadata; artifact frontmatter says 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
