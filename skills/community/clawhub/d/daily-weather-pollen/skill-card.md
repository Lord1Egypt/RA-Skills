## Description:

查询中国主要城市的花粉浓度和天气，并生成或定时推送花粉过敏预警。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengdzh](https://clawhub.ai/user/fengdzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to query pollen concentration and weather for supported Chinese cities, then prepare daily allergy-risk guidance or schedule WeCom push notifications.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The bundled push scripts use root-oriented HOME and PATH settings.

Mitigation: Run the skill under a dedicated unprivileged account and adjust HOME, PATH, and config paths before installation.

Risk: Broad browser cleanup can terminate unrelated Chrome or agent-browser processes.

Mitigation: Remove the global pkill cleanup or scope cleanup to an isolated session owned by this task.

Risk: Some push scripts write logs under /tmp.

Mitigation: Move logs to a protected per-user directory with appropriate permissions and retention.

Risk: The WeCom webhook key is sourced from shell configuration and used to send messages.

Mitigation: Protect and rotate the key, keep it outside version control, and avoid sourcing arbitrary shell files.

Risk: The release claims configurable city support, but bundled scripts still fetch Beijing weather in places.

Mitigation: Validate non-Beijing city behavior before relying on scheduled push notifications.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fengdzh/skills/daily-weather-pollen)
- [Publisher profile](https://clawhub.ai/user/fengdzh)
- [Pollen data source](https://richerculture.cn/hf/)
- [wttr.in weather service](https://wttr.in/)
- [Open-Meteo forecast API](https://api.open-meteo.com/v1/forecast)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call external weather, pollen, browser, cron, and WeCom webhook services; push delivery requires a configured WECOM_WEBHOOK_KEY.]

## Skill Version(s):

4.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
