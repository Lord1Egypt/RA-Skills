## Description:

百度地图 Agent Plan ，无需成为百度地图开发者，立即接入百度地图为 Agent 场景原生设计的地图能力，例如 AI 地点检索、AI 路线规划、地理编码与逆地理编码、天气查询、地图展示等开箱即用的工具。

This skill is ready for commercial/non-commercial use.

## Publisher:

[baidu-maps](https://clawhub.ai/user/baidu-maps)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent call Baidu Maps Agent Plan APIs for place search, route planning, geocoding, reverse geocoding, weather lookup, and optional map visualization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Map queries, addresses, coordinates, and the Baidu Maps authorization token are sent to Baidu's map APIs.

Mitigation: Use the skill only when this data sharing is acceptable, keep the token in BAIDU_MAP_AUTH_TOKEN, and avoid exposing the token in prompts, logs, or shared outputs.

Risk: Map visualization may open a browser window by default when the user asks to view results on a map.

Mitigation: Use map visualization only for explicit visualization requests and disable or avoid browser opening where an interactive browser launch is not appropriate.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/baidu-maps/skills/baidu-ai-map)
- [Baidu Maps Homepage](https://lbs.baidu.com)
- [Baidu Maps Agent Plan Console](https://lbs.baidu.com/apiconsole/agentplan)
- [Baidu Maps API Base URL](https://api.map.baidu.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline curl commands and API request parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Baidu Maps API calls and browser-opening map visualization links when explicitly requested by the user.]

## Skill Version(s):

1.0.9 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
