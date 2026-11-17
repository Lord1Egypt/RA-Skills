## Description:

Controls and monitors Bambu Lab 3D printers over MQTT on a local network for status checks, print control, progress updates, and notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[photonixlaser-ux](https://clawhub.ai/user/photonixlaser-ux)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to operate Bambu Lab printers in LAN mode, inspect print status and temperatures, send pause, resume, stop, light, and fan commands, and monitor print completion or failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill ships real-looking printer credentials and identifiers.

Mitigation: Replace the embedded printer IP, serial number, access code, and chat ID with securely stored user-specific values, and rotate the exposed access code if it was ever real.

Risk: Printer control commands can affect physical hardware immediately.

Mitigation: Run commands only against the intended printer on a trusted LAN and confirm that pause, resume, stop, light, and fan actions are appropriate before execution.

Risk: Background or cron monitoring can continue running with unsafe credential handling and temporary-file behavior.

Mitigation: Avoid unattended monitoring until credential handling, TLS verification, input validation, and temporary-file handling are reviewed and fixed.

## Reference(s):

- [Bambu Lab MQTT API Reference](references/mqtt.md)
- [Bambu Lab LAN Wiki](https://wiki.bambulab.com/en/home)
- [bambu-mqtt Documentation](https://github.com/Doridian/bambu-mqtt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces commands and configuration guidance for MQTT-based printer control and monitoring.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
