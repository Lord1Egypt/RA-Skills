## Description:

AI食品营养管理助手 helps users log meals in natural language, estimate calories and nutrients, query Chinese food nutrition data, and generate daily or weekly HTML reports with dietary suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to track diet entries, estimate nutritional intake, query food data, and generate nutrition summaries for meal planning. It is intended for wellness-oriented guidance and does not replace professional medical or nutrition advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive diet history and body-profile details may be stored locally.

Mitigation: Use the skill only when local storage is acceptable, collect explicit save consent, store only needed data, and provide clear deletion guidance.

Risk: Generated HTML reports may expose untrusted meal text or diary/cache data.

Mitigation: Use trusted inputs and HTML-escape report values before previewing or sharing generated reports.

Risk: Weekly reports load Chart.js from a third-party CDN.

Mitigation: Pin and review the chart dependency or bundle a vetted local copy before wider deployment.

Risk: Nutrition values and dietary suggestions are estimates and may be inaccurate for complex dishes or medical needs.

Mitigation: Present outputs as wellness estimates and defer clinical decisions to qualified healthcare or nutrition professionals.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/food-nutrition)
- [TianAPI](https://www.tianapi.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown responses with generated HTML report files and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local diary/profile/cache files and optional TianAPI nutrition lookup when configured.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
