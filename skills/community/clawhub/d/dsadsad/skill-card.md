## Description:

极简的城市实时天气查询技能，支持国内主流城市。

This skill is ready for commercial/non-commercial use.

## Publisher:

[liaolei666](https://clawhub.ai/user/liaolei666)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking users ask the agent for concise weather details for supported major Chinese cities. The skill is suitable for simple city weather lookups where simulated, non-live results are acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill returns simulated weather data rather than live forecasts.

Mitigation: Present results as simulated examples and verify real weather with an authoritative forecast source before operational use.

Risk: Broad Chinese weather-related triggers may activate on ordinary weather questions.

Mitigation: Confirm the user's target city and intent before relying on or presenting the response.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text or Markdown weather response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns simulated weather details such as temperature, condition, and wind for recognized cities.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
