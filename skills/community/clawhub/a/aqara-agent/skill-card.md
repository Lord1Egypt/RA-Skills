## Description:

Aqara Agent helps agents operate Aqara smart-home workflows through natural-language guidance and Aqara Open API CLI calls for account setup, home and device queries, device control, firmware updates, scenes, automations, ambience, weather-scoped recommendations, and energy statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aqara](https://clawhub.ai/user/aqara)

### License/Terms of Use:

MIT-0

## Use Case:

External users, smart-home operators, and developers use this skill to let an agent answer Aqara home questions and prepare or execute supported Aqara Open API actions. It covers account setup, home selection, device status and control, firmware upgrade, ambience and lighting presets, scene and automation workflows, and energy or electricity-cost summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and uses an Aqara API key that can read and change smart-home state.

Mitigation: Install only if the publisher is trusted, prefer a least-privilege or revocable key, and restrict permissions on assets/user_account.json.

Risk: Device-control, firmware, scene, and automation workflows can make real changes in a home.

Mitigation: Review device-changing actions and API responses before allowing an agent to execute them.

Risk: Custom API endpoint overrides can redirect Aqara Open API requests.

Mitigation: Avoid AQARA_OPEN_API_URL or disk-based API URL overrides unless the endpoint is fully trusted.

## Reference(s):

- [Skill specification](SKILL.md)
- [Package README](README.md)
- [Account management](references/aqara-account-manage.md)
- [Home and space management](references/home-space-manage.md)
- [Device inquiry](references/devices-inquiry.md)
- [Device control](references/devices-control.md)
- [Device control action table](assets/device_control_action_table.csv)
- [Ambience and lighting effects](references/ambience.md)
- [Device firmware configuration](references/devices-config.md)
- [Scene management](references/scene-manage.md)
- [Automation management](references/automation-manage.md)
- [Automation creation](references/automation-create.md)
- [Energy statistics](references/energy-statistic.md)
- [Outdoor weather scope](references/weather-forecast.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call local Python scripts that read or change Aqara smart-home state when the user has configured credentials and selected a home.]

## Skill Version(s):

0.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
