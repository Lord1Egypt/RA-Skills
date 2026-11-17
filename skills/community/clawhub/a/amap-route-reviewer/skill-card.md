## Description:

派出四位性格迥异的虚拟体验官，帮你提前"走完"路线方案。基于高德路径规划、天气、POI真实数据，用热血、毒舌、碎碎念、高冷四种性格视角给出路线评价，帮助选择困难症患者、情侣分歧、旅行纠结党快速做出决策。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qhvssonic](https://clawhub.ai/user/qhvssonic)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to compare commuting routes or travel plans with personality-driven reviews grounded in map, route, weather, POI, cost, and facility data. It helps users choose among route options by showing tradeoffs in concise group-chat style text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Useful route reviews require sharing origin, destination, timing, preferences, and related travel context with the dependent map-service skill.

Mitigation: Avoid providing unnecessary personal details and limit route inputs to the information needed for the comparison.

Risk: Results depend on disclosed map, route, POI, and weather data from amap-lbs-skill.

Mitigation: Install and configure amap-lbs-skill with AMAP_WEBSERVICE_KEY before use, and review generated recommendations before acting on travel or safety-sensitive guidance.

Risk: The skill content and examples are primarily in Chinese, which may affect users expecting another language.

Mitigation: Ask the agent to respond in the desired language when Chinese output is not appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qhvssonic/skills/amap-route-reviewer)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text or Markdown group-chat style route and travel reviews]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires amap-lbs-skill and AMAP_WEBSERVICE_KEY for map-service data.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
