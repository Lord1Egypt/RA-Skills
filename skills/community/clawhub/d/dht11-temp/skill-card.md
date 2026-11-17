## Description:

Read temperature and humidity from DHT11 sensor. Supports custom GPIO pins via CLI argument or environment variable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noahseeger](https://clawhub.ai/user/noahseeger)

### License/Terms of Use:


## Use Case:

Developers, engineers, and Raspberry Pi users can use this skill to read DHT11 temperature and humidity values from a configured GPIO pin.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run the Python script with sudo.

Mitigation: Prefer least-privilege GPIO permissions and review the runtime environment before installation.

Risk: The example cron entry runs a privileged command on a recurring schedule.

Mitigation: Avoid the privileged cron example unless the script path, permissions, logging, and schedule are hardened.

Risk: The RPi.GPIO dependency is required for hardware access.

Mitigation: Install RPi.GPIO from a trusted source and pin or otherwise verify the dependency before use.

Risk: The current script may report temperature and humidity in the wrong order.

Mitigation: Validate sensor output against expected DHT11 readings before relying on logs or downstream automation.

## Reference(s):

- [Dht11 Temp ClawHub release](https://clawhub.ai/noahseeger/skills/dht11-temp)
- [Publisher profile](https://clawhub.ai/user/noahseeger)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and plain-text sensor output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The runtime script prints one sensor value per line or exits with an error if the DHT11 read fails.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
