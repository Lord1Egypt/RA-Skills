## Description: <br>
彩云天气每日推送，定时查询天气并通过微信或消息渠道推送天气早报，支持自定义位置、推送时间和推送渠道。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vlalamoon](https://clawhub.ai/user/vlalamoon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure scheduled Caiyun weather lookups and send daily weather reports through OpenClaw or supported message channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured coordinates and generated weather report details may be sent to Caiyun and the selected notification channel. <br>
Mitigation: Use a dedicated Caiyun token where possible, avoid overly precise coordinates when neighborhood-level weather is enough, and choose only notification channels you trust. <br>
Risk: Scheduled delivery can continue sending daily reports after the user no longer wants notifications. <br>
Mitigation: Test with dry-run or terminal output first and remove the cron configuration when daily notifications are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vlalamoon/caiyun-weather-daily) <br>
- [Caiyun developer platform](https://www.caiyunapp.com/h5/) <br>
- [Caiyun Weather API base endpoint](https://api.caiyunapp.com/v2.6) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON and shell command examples, plus generated weather notification text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided Caiyun token and coordinates; can print output locally or send it through a configured notification channel.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
