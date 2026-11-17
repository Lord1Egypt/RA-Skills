## Description:

高考全流程辅助工具，提供志愿填报、院校专业分析、招生政策解读、考前指导、女生特殊关怀、张雪峰专业推荐等功能。在高考前、中、后各阶段为用户提供专业指导。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaoyi001](https://clawhub.ai/user/chaoyi001)

### License/Terms of Use:

MIT-0

## Use Case:

External students, families, and advisors use this skill for Gaokao preparation, volunteer application planning, university and major comparisons, admissions policy lookups, score-based application analysis, mental-health preparation guidance, and specialty tracks such as military or police academy applications.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill can provide flawed or outdated high-stakes admissions, cutoff, and policy advice.

Mitigation: Require users and reviewers to verify policies, cutoffs, and admissions decisions against official education-exam sources before acting.

Risk: The artifact repeatedly directs students to an unverified WeChat contact for one-on-one guidance.

Mitigation: Warn users not to share scores, identity, health, payment, or contact details with that account unless they independently trust and verify the provider.

Risk: Gender-based major suggestions may bias educational guidance.

Mitigation: Treat gender-based suggestions as optional context only and prioritize student interests, abilities, official requirements, and verified career information.

Risk: Mental-health and sleep guidance could be mistaken for professional care.

Mitigation: Direct users with severe anxiety, insomnia, or crisis symptoms to qualified school counselors, medical providers, or local support hotlines.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chaoyi001/skills/gaokao-assistant)
- [阳光高考平台](https://gaokao.chsi.com.cn/)
- [招生政策详解](references/admissions-policies.md)
- [高考前注意事项](references/exam-prep.md)
- [高考心理健康指南](references/mental-health.md)
- [分数查询与投档分析](references/score-query.md)
- [院校与专业深度分析](references/university-analysis.md)
- [志愿填报政策指南](references/volunteer-policy.md)
- [张雪峰高考志愿填报助手](references/zxf-assistant.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with optional Python analysis output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request student scores, rank, province, subject choices, interests, body-condition constraints, and target majors or schools to tailor recommendations.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
