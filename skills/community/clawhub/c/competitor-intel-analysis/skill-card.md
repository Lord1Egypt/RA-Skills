## Description:

根据招投标记录生成企业竞对情报报告，分析中标实力、客户关系、竞争格局及公开风险，并支持双公司对比。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhiliaobiaoxun](https://clawhub.ai/user/zhiliaobiaoxun)

### License/Terms of Use:

MIT-0

## Use Case:

投标与商务团队可用公司名称生成单家企业背调或两家公司对比，了解公开招投标业绩、合作客户、竞争对手及有来源的公开风险信息。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends company queries and an API key to zhiliaobiaoxun.com and checks account status.

Mitigation: Review the requested network access and account checks before installation; use a key you are comfortable sharing with this service.

Risk: Trial registration derives a hashed device identifier and may store an API key locally.

Mitigation: Require explicit consent before registration; supply an existing API key to avoid device registration, and protect the local credential file.

Risk: Saved HTML reports may contain signed access links that grant access to underlying records.

Mitigation: Treat generated reports as sensitive and remove or restrict signed links before sharing.

Risk: Competitive conclusions and public-risk summaries may be incomplete or misinterpreted.

Mitigation: Check cited records, reporting periods and data gaps; distinguish sourced facts from inferences before acting.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhiliaobiaoxun/skills/competitor-intel-analysis)
- [知了标讯 Skill 文档](https://ai.zhiliaobiaoxun.com/docs/skill)
- [企业情报工作流](artifact/references/workflow.md)
- [报告模板](artifact/references/report-template.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, HTML reports]

**Output Format:** [Markdown conversation report and shareable HTML file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes supporting citations, reporting period and explicit data gaps; optional weekly change summary.]

## Skill Version(s):

1.0.6 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
