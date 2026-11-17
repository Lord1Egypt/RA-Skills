## Description:

用元认知引导发现值得被做成小龙虾的机会点，并将其收敛为可开箱即用的基准 Agent 小龙虾。

This skill is ready for commercial/non-commercial use.

## Publisher:

[beachanger](https://clawhub.ai/user/beachanger)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent builders, and workflow owners use this skill to evaluate whether a vague idea is worth turning into an agent, then convert promising opportunities into benchmark-agent blueprints with MVP scope, workspace structure, and next actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated deployment or handoff documents may cause users to store bot tokens, API keys, passwords, or app credentials in workspace files.

Mitigation: Use placeholders in generated documents and keep live secrets in environment variables or a secret manager.

Risk: The skill can write planning and handoff files into a target workspace.

Mitigation: Confirm the target workspace path before allowing files to be written.

Risk: Generated deployment documents may contain incorrect or incomplete setup guidance.

Mitigation: Review generated deployment documents before saving or using them.

## Reference(s):

- [MomClaw skill page](https://clawhub.ai/beachanger/skills/benchmark-lobster-forge)
- [Publisher profile](https://clawhub.ai/user/beachanger)
- [Lobster Opportunity Evaluation](references/lobster-opportunity-evaluation.md)
- [Benchmark Lobster Architecture Framework](references/benchmark-lobster-architecture-framework.md)
- [Product Roundness Framework](references/product-roundness-framework.md)
- [Metacognitive Interview Tree](references/metacognitive-interview-tree.md)
- [Agent Type Taxonomy](references/agent-type-taxonomy.md)
- [Platform Deployment Guide](references/platform-deployment-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Structured Markdown with blueprint templates, scorecards, checklists, and handoff guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated planning and deployment handoff documents into a target agent workspace when the user confirms creation.]

## Skill Version(s):

1.0.2 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
