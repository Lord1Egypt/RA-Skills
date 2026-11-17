## Description:

获取中国城市当前天气、未来预报、生活指数和气象预警查询辅助信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[libaoming](https://clawhub.ai/user/libaoming)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to answer weather questions for Chinese cities, including current conditions, tomorrow or weekly forecasts, lifestyle indices, and optional alert guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local shell script and sends city names to external weather services.

Mitigation: Review the script before installing and avoid submitting sensitive location queries.

Risk: The security evidence reports unsecured request URLs for wttr.in weather lookups.

Mitigation: Prefer or update to a version that uses HTTPS endpoints for network requests.

Risk: Cached weather results are stored in a shared temporary directory.

Mitigation: Use a private user-owned cache directory or clear the shared cache after use.

## Reference(s):

- [中国天气 skill page](https://clawhub.ai/libaoming/skills/china-weather)
- [wttr.in weather service](https://wttr.in)
- [QWeather developer platform](https://dev.qweather.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Weather results depend on external weather services, network availability, and optional QWEATHER_KEY configuration.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
