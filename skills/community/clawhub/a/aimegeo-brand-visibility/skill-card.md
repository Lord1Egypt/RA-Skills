## Description:

根据品牌资料和真实 AI 回答，评估品牌提及、推荐、原生引用及描述准确性，并生成体检报告、逐问题证据和优先行动。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

面向品牌团队和营销人员，用于分析导入的 AI 回答与品牌事实，识别品牌缺席、描述冲突和引用证据缺口，并规划后续改进与复测。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment is benign with medium confidence, but incomplete: tool permissions are undeclared and part of a referenced script could not be fully assessed.

Mitigation: Review the skill's requested capabilities and the incompletely assessed script portion before installing or enabling it.

## Reference(s):

- [Input and metrics guidance](references/input-and-metrics.md)
- [Report and action guidance](references/report-and-actions.md)
- [Configured skill repository (manifest)](https://github.com/xxjrq/aimegeo-brand-visibility)
- [aimeGeo GitHub project](https://github.com/xxjrq/aimegeo)
- [aimeGeo Gitee mirror](https://gitee.com/xxjrq/aimegeo)
- [aimeGeo website](https://geo.aimmme.com/)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Guidance]

**Output Format:** [Markdown report and priority actions, plus a JSON evidence table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Conclusions are limited to supplied samples; observed, failed, missing, unrun, and simulated records remain distinct.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata, manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
