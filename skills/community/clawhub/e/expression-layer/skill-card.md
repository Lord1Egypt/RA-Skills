## Description:

表达层 routes direct questions, source material, drafts, links, and output requests to content-generation, format-conversion, visualization, and publishing workflows without requiring a separate reasoning layer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lj22503](https://clawhub.ai/user/lj22503)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to route content tasks into plain-language explanation, long-form writing, visual cards, presentations, paper or word breakdowns, travel reports, and WeChat publishing flows. It is intended as an orchestration layer for multi-format Chinese content production rather than as a source of deep analysis or data retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill declares broad command execution tools.

Mitigation: Review commands before execution and remove Bash or Exec access unless a concrete workflow requires it.

Risk: Publishing workflows can expose drafts, links, or user-provided material.

Mitigation: Require explicit confirmation before any WeChat publishing action and treat drafts and links as sensitive inputs.

Risk: Downstream routing can fail or produce inappropriate output if required skills are missing or misconfigured.

Mitigation: Verify downstream skills before deployment and review generated content before delivery or publication.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lj22503/skills/expression-layer)
- [README](README.md)
- [路由编排矩阵](references/orchestration-matrix.md)
- [投教工作流与表达层编排分析](references/ie-orchestration.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Configuration, Guidance]

**Output Format:** [Markdown, plain text, HTML, PNG assets, and publishing drafts routed through downstream skills]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the selected route and downstream skill availability.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, clawhub.yaml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
