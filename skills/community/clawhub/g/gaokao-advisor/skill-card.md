## Description:

高考志愿规划顾问。根据考生省份、科类、成绩/位次、意向专业和区域，联网检索招生计划和录取数据，生成个性化志愿填报推荐（含保研率、就业去向、薪资待遇、专业前景批判分析）。当用户询问高考志愿填报、院校选择、专业推荐时调用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[edmandcui](https://clawhub.ai/user/edmandcui)

### License/Terms of Use:

MIT-0

## Use Case:

Students, families, and advisors use this skill to prepare Chinese gaokao application plans based on province, subject track, score or rank, intended majors, and preferred regions. It researches current admissions and employment data, asks for missing critical inputs, and returns advisory reach, match, and safety recommendations with risk notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may produce admissions advice from current web search results that are incomplete, stale, or inconsistent across sources.

Mitigation: Verify admissions plans against official provincial exam authority publications and university admissions materials before acting on the recommendations.

Risk: The skill may ask for student province, subject track, score or rank, target majors, and target regions.

Mitigation: Share only the information needed for the advising task and avoid including unnecessary personal identifiers.

Risk: Recommendations can affect high-stakes education decisions but remain advisory.

Mitigation: Treat the output as planning support and make final decisions with official sources, qualified advisors, and the student's guardians where appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edmandcui/skills/gaokao-advisor)
- [Publisher profile](https://clawhub.ai/user/edmandcui)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown advisory report with structured recommendation tiers, tables, source notes, and disclaimers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses web search for current public admissions and employment data; recommendations are advisory and should be verified against official exam authority and university sources.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
