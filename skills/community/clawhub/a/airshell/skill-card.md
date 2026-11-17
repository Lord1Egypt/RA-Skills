## Description:

Agent playbook for the AirShell air quality sensor that helps an agent configure a sensor webhook, interpret CO2, PM2.5, temperature, and humidity readings, and decide when to notify the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oloapiu](https://clawhub.ai/user/oloapiu)

### License/Terms of Use:


## Use Case:

Developers and end users use this skill to connect an AirShell sensor to an agent, maintain deployment context, set alarm thresholds, interpret indoor air quality readings, and produce context-aware notifications or configuration updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deployment context can store room, occupant, and location details.

Mitigation: Store only the detail needed for air-quality decisions and review deployment.md before sharing or committing it.

Risk: Webhook credentials and gateway details may be posted to a configured device URL.

Mitigation: Confirm the device URL is trusted and local or private, and require clear approval before sending or changing gateway configuration.

Risk: Optional purifier automation can run local commands from editable deployment configuration.

Mitigation: Enable purifier control only with fixed trusted script and Python paths, credentials stored in environment variables or a secrets file, and explicit approval for configuration changes.

Risk: Real-time air-quality readings can be mistaken for regulatory or medical determinations.

Mitigation: Treat outputs as practical guidance, preserve the skill's caveats about real-time measurements, and escalate health concerns to appropriate professionals.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oloapiu/skills/airshell)
- [CO2 domain knowledge](references/co2.md)
- [PM2.5 domain knowledge](references/pm25.md)
- [Temperature and humidity domain knowledge](references/temp_humidity.md)
- [Deployment context template](references/deployment.md)
- [Deployment context example](references/deployment.example.md)
- [Open-Meteo forecast API](https://api.open-meteo.com/v1/forecast)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance, Shell commands, Code, API calls]

**Output Format:** [Plain-language text, Markdown deployment context, JSON device configuration, inline shell commands, and optional Python command execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update deployment context, POST sensor configuration to a configured device URL, query weather and sensor APIs, and optionally run a local purifier-control script.]

## Skill Version(s):

1.1.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
