## Description:

对用户提出的具体话题/课题/行业进行深度调研，输出结构化报告。结合多智能体并行搜索（借鉴女娲Nuwa）和克制调用原则（借鉴AutoGLM DeepResearch），先展示中间发现再决策。

This skill is ready for commercial/non-commercial use.

## Publisher:

[realpda](https://clawhub.ai/user/realpda)

### License/Terms of Use:

MIT-0

## Use Case:

External users and employees use this skill to research a specific topic, industry, market, or policy question and receive a sourced structured report. The workflow emphasizes interim findings, restrained search depth, credible sources, balanced analysis, and actionable recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Obsidian export can write to a user-provided note path without enough clarity about create, append, or overwrite behavior.

Mitigation: Before using the Obsidian option, require an exact note path and confirm whether the agent will create, append to, or overwrite the file.

Risk: Research reports can mislead users if weak sources, missing evidence, or one-sided findings are treated as final conclusions.

Mitigation: Use the workflow's interim findings, source weighting, citation requirements, balanced opportunity-and-risk analysis, and final self-check before relying on the report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/realpda/skills/deep-topic-research)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown research report with cited references and optional Obsidian note output when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes interim finding summaries before final report generation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
