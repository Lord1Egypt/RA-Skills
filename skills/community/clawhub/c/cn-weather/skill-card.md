## Description: <br>
中国天气 API - 使用和風天气 (QWeather) 获取中国城市天气数据。支持双 API（和风天气 + Open-Meteo）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhengge6](https://clawhub.ai/user/zhengge6) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to configure and run China-focused weather reporting through QWeather, with Open-Meteo as a fallback data source. It can produce current conditions, a three-day forecast, and optional email delivery for configured cities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local TOOLS.md content that may contain QWeather and QQ SMTP credentials. <br>
Mitigation: Keep TOOLS.md out of Git and synced backups, store only the required credentials, and rotate credentials if the file is exposed. <br>
Risk: The weather report script can send email automatically and includes a hardcoded default recipient. <br>
Mitigation: Remove or override the default recipient before running the script, and execute it only when email delivery is intended. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhengge6/cn-weather) <br>
- [QWeather API documentation](https://dev.qweather.com/docs/api/) <br>
- [QWeather documentation](https://dev.qweather.com/docs/) <br>
- [QWeather console](https://console.qweather.com) <br>
- [QWeather icons](https://icons.qweather.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell snippets and plain-text weather report output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires QWEATHER_API_KEY for QWeather access and may use configured QQ SMTP credentials for email delivery.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
