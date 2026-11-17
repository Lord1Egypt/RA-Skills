## Description:

校验文章、发布、AI回答和经营导出，形成有来源、分母和可比性说明的周期数据摘要。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

面向 aimeGeo 项目运营者和内容团队，用于按指定周期核验文章、发布、AI 回答及经营导出，并生成可复核的指标摘要。团队可据来源、分母和统计边界解释变化，再将有证据支持的发现交给已授权的内容工作流跟进。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Business reports may expose private project or account data.

Mitigation: Provide only the exports needed for the report and keep generated business reports private.

Risk: Optional content edits or publication may exceed the approved project, account, or scope.

Mitigation: Identify the project, account, permitted edits, and publication authorization before content work; leave public actions outside that authorization as drafts.

## Reference(s):

- [Input fields](references/input-schema.md)
- [Metric interpretation notes](references/metric-notes.md)
- [aimeGeo content creation guide](https://geo.aimmme.com/docs/content-production/)
- [aimeGeo cover creation guide](https://geo.aimmme.com/docs/cover-generation/)
- [aimeGeo publishing workflow](https://geo.aimmme.com/docs/publish-flow/)

## Skill Output:

**Output Type(s):** [JSON, CSV, Guidance]

**Output Format:** [summary.json and 指标明细.csv, with concise source-aware interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves source IDs, metric denominators, missing and non-success states, and comparison limits; does not infer causation.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
