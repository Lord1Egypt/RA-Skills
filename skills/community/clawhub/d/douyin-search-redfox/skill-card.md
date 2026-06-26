## Description: <br>
抖音爆款作品查询工具，根据关键词搜索抖音热门爆款作品，支持按日期范围筛选，并以结构化表格展示结果。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, brand operators, MCN teams, growth teams, and marketing teams use this skill to search Douyin viral content by keyword, filter by date range, and review engagement metrics for trend research and content planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a locally stored RedFox API key. <br>
Mitigation: Store REDFOX_API_KEY in an environment or agent secret store, avoid hard-coding it in prompts or files, and rotate or revoke it if exposure is suspected. <br>
Risk: Search terms are sent to RedFox when the Douyin search script runs. <br>
Mitigation: Avoid submitting sensitive, confidential, or regulated terms unless that data sharing is acceptable for the deployment. <br>
Risk: Subscription behavior may create recurring background jobs. <br>
Mitigation: Before enabling a subscription, confirm the schedule, where the task is stored, and the exact procedure to view, disable, and delete it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/douyin-search-redfox) <br>
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [RedFoxHub](https://redfox.hk) <br>
- [Chinese README](README.md) <br>
- [English README](README.en.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown tables with linked Douyin works, concise text guidance, and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY. May include date-filtered search results, hot recommendations, topic lists, and subscription scheduling guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
