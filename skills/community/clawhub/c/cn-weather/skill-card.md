## Description:

中国天气 API - 使用和風天气 (QWeather) 获取中国城市天气数据。支持双 API（和风天气 + Open-Meteo）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhengge6](https://clawhub.ai/user/zhengge6)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to fetch current weather and short forecasts for configured Chinese cities, using QWeather when configured and Open-Meteo as a fallback. It can produce a daily weather report and optionally send it by email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local email credentials from TOOLS.md.

Mitigation: Treat TOOLS.md as plaintext, keep it out of version control, and use low-privilege dedicated credentials.

Risk: The script can email reports to a hard-coded outside address when no recipient is supplied.

Mitigation: Run the script only with an explicit intended recipient and review the destination before execution.

Risk: Wildcard API host allowlists can expose QWeather credentials more broadly than intended.

Mitigation: Avoid wildcard host allowlists; restrict QWeather credentials to the minimum hosts required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhengge6/skills/cn-weather)
- [QWeather API documentation](https://dev.qweather.com/docs/api/)
- [QWeather developer documentation](https://dev.qweather.com/docs/)
- [QWeather console](https://console.qweather.com)
- [QWeather icons](https://icons.qweather.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration guidance]

**Output Format:** [Markdown setup guidance and plain-text weather reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires QWEATHER_API_KEY for QWeather; can fall back to Open-Meteo when QWeather is unavailable.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
