## Description:

战略/市场分析咨询报告工作流——判断+数据双轨。先出有排他性的框架判断,再用真实数据验证(数据文件或公开信息),输出结构化 Markdown 咨询报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuobadaidai](https://clawhub.ai/user/tuobadaidai)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external consultants, analysts, and strategy teams use this skill to produce Chinese strategic, market, competitive, market-entry, growth, and consulting reports. It structures work around clear hypotheses, evidence discipline, and Markdown report delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports may contain incorrect or unsupported strategic conclusions if evidence is missing, stale, or misread.

Mitigation: Apply the workflow's source, method, recency, confidence, and final data-verification checks before relying on conclusions.

Risk: The workflow may process sensitive local data files supplied by the user.

Mitigation: Review input data sensitivity and sharing permissions before analysis, and avoid using public research tools for confidential internal facts.

Risk: Complex analyses may rely on optional parallel subagents, which can produce inconsistent findings.

Mitigation: Compare subagent outputs, explicitly mark unresolved conflicts, and downgrade unsupported conclusions to unverified.

## Reference(s):

- [Data Analysis Discipline](references/data-analysis.md)
- [Report Output Specification](references/output-spec.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown consulting report with evidence labels and optional code or shell commands for data analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to Chinese report prose; may use Python, local data files, public web research, and optional parallel subagents for complex analyses.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
