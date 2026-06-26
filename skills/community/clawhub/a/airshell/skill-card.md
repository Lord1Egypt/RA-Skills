## Description: <br>
AirShell gives an agent a playbook for configuring and interpreting a SEN63C/Raspberry Pi air-quality sensor, including CO2, PM2.5, temperature, humidity, webhook alerts, and optional purifier control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oloapiu](https://clawhub.ai/user/oloapiu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to connect an AirShell air-quality sensor to an agent, configure room-specific alarm thresholds, interpret indoor readings, and receive context-aware ventilation or purifier guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow can store sensitive household context such as room use, occupant sensitivity, location, and notification preferences. <br>
Mitigation: Review deployment.md before use, avoid unnecessary health details, and keep the deployment context local and access-controlled. <br>
Risk: The skill may configure a gateway webhook token and query a weather API using the deployment location. <br>
Mitigation: Use revocable limited webhook credentials, restrict device and gateway access, and provide only the location precision needed for ventilation decisions. <br>
Risk: Optional purifier automation can silently run a local Python script that controls a connected device. <br>
Mitigation: Enable purifier automation only after reviewing the script path, Python environment, and environment-variable credential handling. <br>


## Reference(s): <br>
- [AirShell ClawHub Page](https://clawhub.ai/oloapiu/airshell) <br>
- [CO2 Domain Knowledge](references/co2.md) <br>
- [PM2.5 Domain Knowledge](references/pm25.md) <br>
- [Temperature and Humidity Domain Knowledge](references/temp_humidity.md) <br>
- [Deployment Context Template](references/deployment.md) <br>
- [Deployment Context Example](references/deployment.example.md) <br>
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, Shell commands, API calls] <br>
**Output Format:** [Markdown with inline JSON, HTTP, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local deployment context and propose or execute device configuration when the user confirms setup choices.] <br>

## Skill Version(s): <br>
1.1.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
