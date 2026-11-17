## Description:

每天定时查询彩云天气 API，并通过微信或其他消息渠道推送天气早报。

This skill is ready for commercial/non-commercial use.

## Publisher:

[vlalamoon](https://clawhub.ai/user/vlalamoon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure daily weather notifications for a chosen location and delivery channel. It helps agents set up scheduled Caiyun Weather API queries, message formatting, and optional OpenClaw delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Caiyun API token and precise coordinates to fetch weather data.

Mitigation: Use a restricted, rotatable token and avoid exposing token-bearing URLs or location coordinates in logs, shell history, or shared transcripts.

Risk: Weather messages can be sent to a configured channel on a schedule.

Mitigation: Review the cron schedule and delivery channel before enabling automated sends.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vlalamoon/skills/caiyun-weather-daily)
- [彩云开发者平台](https://www.caiyunapp.com/h5/)
- [Caiyun Weather API base endpoint](https://api.caiyunapp.com/v2.6)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, bash, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Caiyun API token, longitude, latitude, and intentional delivery channel configuration.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
