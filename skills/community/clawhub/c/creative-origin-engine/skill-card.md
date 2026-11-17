## Description:

多Agent并行辩论式创意决策引擎。输入模糊创意→三独立视角(建构/解构/数据锚定)并行分析→Critic+Defender交叉验证→20分制量化评分→可执行策划案+Skill双格式输出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[vane1981](https://clawhub.ai/user/vane1981)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external creators, strategists, and developers use this skill to turn early creative, product, campaign, IP, or business ideas into challenged planning outputs with constructive, critical, and data-grounded perspectives. It is suited for brainstorming, feasibility analysis, business model review, marketing concepts, and executable planning drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad auto-activation can run the planning workflow on prompts that only loosely match creative or business-planning intent.

Mitigation: Prefer explicit invocation or narrow trigger configuration so the user intentionally starts the skill.

Risk: Web research can send sensitive product ideas, client plans, or strategy terms to external search services.

Mitigation: Confirm before web research and redact confidential terms before searching.

Risk: Task-derived ideas may be stored across projects without clear consent or retention controls.

Mitigation: Disable automatic memory writes when possible or review and delete stored planning notes after each session.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vane1981/skills/creative-origin-engine)
- [Project homepage](https://github.com/Vane1981-2011/creative-origin-engine)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown planning report with scoring tables, evidence tables, and optional Agent Skill content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a 20-point scoring card, challenged assumptions, risk matrix, validation plan, execution blueprint, and source table when the workflow is followed.]

## Skill Version(s):

2.0.1 (source: server evidence, frontmatter, config.yaml, CHANGELOG released 2026-08-03)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
