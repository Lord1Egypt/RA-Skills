## Description: <br>
花粉过敏指数权威发布。当用户需要查询花粉浓度、设置每日定时推送花粉过敏预警时使用。支持自定义城市，可查询花粉浓度和天气，并可设置定时任务自动推送。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengdzh](https://clawhub.ai/user/fengdzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to query Chinese city weather and pollen levels, configure daily allergy-risk alerts, and send WeCom markdown notifications with execution logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The v4 push helper may forcibly terminate Chrome processes while trying to clean browser sessions. <br>
Mitigation: Avoid running the v3/v4 helpers on shared or active machines unless browser cleanup is limited to processes started by this skill. <br>
Risk: WeCom webhook credentials are required for scheduled push notifications. <br>
Mitigation: Use a dedicated low-impact WeCom bot key and keep ~/.openclaw/config/wecom.env private with owner-only permissions. <br>
Risk: Weather and pollen alerts depend on external web sources and page parsing. <br>
Mitigation: Review failed or missing data in the generated push logs before relying on the alert content. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/fengdzh/daily-weather-pollen) <br>
- [Publisher profile](https://clawhub.ai/user/fengdzh) <br>
- [Pollen data source](https://richerculture.cn/hf/) <br>
- [Weather data source](https://wttr.in/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and WeCom markdown message content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces city-specific pollen risk summaries, weather notes, scheduled push instructions, and log entries.] <br>

## Skill Version(s): <br>
4.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
