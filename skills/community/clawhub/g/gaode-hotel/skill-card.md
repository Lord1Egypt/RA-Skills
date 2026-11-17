## Description:

用高德 POI 数据解析任意地名（商圈、地铁站、网红餐厅、小区等），再查询飞猪实时酒店价格和预订链接，让用户能以任意地点为中心查找住宿。

This skill is ready for commercial/non-commercial use.

## Publisher:

[han815757857-cmd](https://clawhub.ai/user/han815757857-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

面向计划出行的用户及旅行助手，用于按城市、目的地和入住日期查询附近酒店，并查看实时价格、房态、预订链接；用户也可选择附加周边餐饮信息。

### Deployment Geography for Use:

China (the documented city matching supports cities in China).

## Known Risks and Mitigations:

Risk: An API key and travel details or hotel coordinates may be sent to an unverified or unencrypted external service.

Mitigation: Before use, verify the configured API destination and HTTPS protections, and understand which travel details and coordinates are transmitted.

Risk: The POI API key could be exposed if stored in files or embedded in code.

Mitigation: Supply GAODE_POI_KEY through an environment variable only; do not write it to files, configuration, or scripts.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/han815757857-cmd/skills/gaode-hotel)
- [FlyAI homepage](https://open.fly.ai/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Travel guidance]

**Output Format:** [Markdown hotel listings with prices, ratings, booking links, and optional nearby dining]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A list of up to the requested number of hotel results; nearby dining is optional.]

## Skill Version(s):

1.0.3 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
