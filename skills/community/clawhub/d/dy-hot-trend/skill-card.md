## Description: <br>
专注于获取抖音最新的热榜数据，每小时更新，包含热点事件、热度值和跳转链接；支持查询近7天、近30天历史热榜，并支持订阅定时推送。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[if530770](https://clawhub.ai/user/if530770) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, MCN operators, brand marketers, and short-video operations teams use this skill to fetch Douyin hot-list data, review recent trend history, compare time periods, and generate creator-oriented insight reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RedFox API key and may read it from environment or shell profile configuration. <br>
Mitigation: Set REDFOX_API_KEY directly in the runtime environment, avoid hardcoding or sharing it in prompts, logs, or files, and rotate or revoke the key if exposure is suspected. <br>
Risk: The skill sends requests to redfox.hk and depends on that service for Douyin trend data. <br>
Mitigation: Install only where outbound requests to redfox.hk are acceptable and use explicit Douyin trend prompts when invoking data retrieval, subscriptions, or reports. <br>
Risk: The skill can create local JSON, HTML, and PDF report files containing trend data and links. <br>
Mitigation: Review generated files before sharing and store or delete reports according to the workspace's data handling expectations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/if530770/dy-hot-trend) <br>
- [Publisher profile](https://clawhub.ai/user/if530770) <br>
- [RedFoxHub](https://redfox.hk/) <br>
- [RedFoxHub API keys](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [Core workflow reference](references/core_workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, HTML files, PDF files, shell commands, configuration guidance] <br>
**Output Format:** [Markdown responses with trend tables and analysis, plus generated local JSON, HTML, and PDF report files when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY and network access to redfox.hk; supports real-time, recent-history, comparison, and subscription-style workflows.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
