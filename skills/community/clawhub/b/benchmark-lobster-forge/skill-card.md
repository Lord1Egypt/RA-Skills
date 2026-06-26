## Description: <br>
用元认知引导发现值得被做成小龙虾的机会点，并将其收敛为可开箱即用的基准 Agent 小龙虾。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BeAChanger](https://clawhub.ai/user/BeAChanger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent builders, and workflow owners use this skill to evaluate whether a vague idea is worth turning into an agent, scope the MVP boundary, and produce a creation-ready benchmark agent blueprint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated planning or handoff documents may be written into the wrong target workspace if the creation target is ambiguous. <br>
Mitigation: Confirm the exact target workspace before using the creation handoff and review generated memory, report, card, and skill files before deployment. <br>
Risk: Deployment planning can lead users to place real platform tokens or credentials in Markdown documents. <br>
Mitigation: Keep real platform tokens and credentials in a secret manager or environment configuration, and reference only non-secret setup status in generated documents. <br>
Risk: Blueprint proposals could introduce incorrect or misleading guidance into downstream skills or agent workspaces. <br>
Mitigation: Review and scan generated skill or workspace files before deployment. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Lobster Opportunity Evaluation](references/lobster-opportunity-evaluation.md) <br>
- [Benchmark Lobster Architecture Framework](references/benchmark-lobster-architecture-framework.md) <br>
- [Product Roundness Framework](references/product-roundness-framework.md) <br>
- [Metacognitive Interview Tree](references/metacognitive-interview-tree.md) <br>
- [Agent Type Taxonomy](references/agent-type-taxonomy.md) <br>
- [Lobster Case Cards](references/lobster-case-cards.md) <br>
- [Anti-Patterns](references/anti-patterns.md) <br>
- [Platform Deployment Guide](references/platform-deployment-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance, files] <br>
**Output Format:** [Structured Markdown plans, blueprints, checklists, workspace handoff notes, and deployment setup guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce target workspace documentation when the user confirms creation or deployment handoff.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
