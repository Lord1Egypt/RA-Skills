## Description:

审阅 AI 漫剧及短剧剧本，提供基于文本证据的内容风险筛查、剧作质量与制作可行性评估、可执行修改建议，并生成 Markdown 和离线 HTML 报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shinychris](https://clawhub.ai/user/shinychris)

### License/Terms of Use:

MIT-0

## Use Case:

编剧、制片人和内容审核人员可用它评估已提供的漫剧或短剧剧本、大纲、人物小传或分场材料。它生成带有证据、评分、修改建议和复审清单的 Markdown 与独立 HTML 报告；结论受所提供材料范围限制。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security guidance flags undeclared tool scope for review.

Mitigation: Inspect the skill's requested access and limit it to what the review task needs.

Risk: The report headings are Chinese-only and may not suit every review audience.

Mitigation: Confirm that the intended reviewers can work with Chinese-language reports or arrange a human-reviewed translation.

Risk: General script screening can be mistaken for a platform, regulatory, or legal decision.

Mitigation: Treat findings as a preliminary creative risk review and send material requiring formal determination to the relevant platform or qualified human reviewer.

## Reference(s):

- [剧作质量深度诊断与修改指南](references/drama-quality.md)
- [审核评分与风险分级规则](references/review-rubric.md)
- [ClawHub skill release](https://clawhub.ai/shinychris/skills/ai-comic-drama-review)
- [Publisher profile: shinychris](https://clawhub.ai/user/shinychris)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, HTML]

**Output Format:** [Markdown and standalone HTML review reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Evidence-linked findings, weighted scores, actionable revisions, and a re-review checklist; conclusions are limited to supplied materials.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
