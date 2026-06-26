## Description: <br>
百度地图 Agent Plan ，无需成为百度地图开发者，立即接入百度地图为 Agent 场景原生设计的地图能力，例如 AI 地点检索、AI 路线规划、地理编码与逆地理编码、天气查询、地图展示等开箱即用的工具。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baidu-maps](https://clawhub.ai/user/baidu-maps) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to call Baidu Maps Agent Plan capabilities for place search, route planning, geocoding, reverse geocoding, weather lookup, and optional map visualization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Map searches, addresses, routes, and precise coordinates are sent to Baidu Maps. <br>
Mitigation: Use the skill only when the user intentionally wants Baidu Maps processing and avoid sending unnecessary sensitive location details. <br>
Risk: The skill requires BAIDU_MAP_AUTH_TOKEN for authenticated API calls. <br>
Mitigation: Keep the token in the environment, do not paste it into prompts or logs, and rotate it if exposure is suspected. <br>
Risk: Repeated or broad map requests can consume Baidu Maps Agent Plan quota or billing. <br>
Mitigation: Avoid duplicate requests with identical parameters and confirm expensive or ambiguous searches before running them. <br>
Risk: MapRender can open a Baidu map page in a browser when visualization is requested. <br>
Mitigation: Open generated map links only when the user explicitly asks to view results on a map. <br>


## Reference(s): <br>
- [Baidu AI Map on ClawHub](https://clawhub.ai/baidu-maps/baidu-ai-map) <br>
- [Baidu Maps publisher profile](https://clawhub.ai/user/baidu-maps) <br>
- [Baidu Maps](https://lbs.baidu.com) <br>
- [Baidu Maps Agent Plan Console](https://lbs.baidu.com/apiconsole/agentplan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl commands, environment setup, API response interpretation, and map display links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and BAIDU_MAP_AUTH_TOKEN; API calls use Authorization: Bearer authentication.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
