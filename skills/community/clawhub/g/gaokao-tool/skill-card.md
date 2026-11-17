## Description:

A Chinese gaokao admissions-advice skill that helps users gather exam and preference details, compare recent admissions data, assess school and major fit, and structure reach, target, and safety recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jannik689](https://clawhub.ai/user/jannik689)

### License/Terms of Use:

MIT-0

## Use Case:

External users, students, and families use this skill to discuss Chinese gaokao志愿填报 decisions, including admissions score lookup, province and subject-type context, major fit, school shortlist planning, and follow-up verification steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process sensitive educational and preference details such as scores, province, subject category, interests, and family constraints.

Mitigation: Share only the information needed for the recommendation and avoid unnecessary personally identifying details.

Risk: Admissions cutoffs, rankings, and school data can be stale or inaccurate if not checked against current official sources.

Mitigation: Verify all admissions cutoffs, one-score-one-rank tables, enrollment plans, and school information against provincial exam authorities or official school sources before making final decisions.

Risk: Recommendation outputs can influence high-stakes education decisions.

Mitigation: Treat outputs as planning guidance, compare multiple authoritative sources, and involve the student and family in the final decision.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jannik689/skills/gaokao-tool)
- [Gaokao admissions data sources](references/data-sources.md)
- [Gaokao hexagon analysis methodology](references/hexagon-analysis.md)
- [Major selection and employment guide](references/majors-guide.md)
- [National Government Service Platform gaokao services](https://gjzwfw.www.gov.cn/col/col1567/index.html)
- [Sunshine Gaokao](https://gaokao.chsi.com.cn/)
- [China Education Online](https://www.eol.cn/)
- [Gaokao.cn](https://www.gaokao.cn/)

## Skill Output:

**Output Type(s):** [guidance, markdown, text]

**Output Format:** [Markdown-style conversational guidance with tables, ranked recommendations, source links, and data disclaimers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask for exam score, province, subject category, preferences, and optional personal-interest details before giving recommendations.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
