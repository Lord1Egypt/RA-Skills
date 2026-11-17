## Description:

Control Dyson air purifiers, fans, and heaters via local MQTT. Use when asked to control Dyson devices, adjust fan speed, set temperature/heat, enable oscillation, or check room temperature/humidity. Requires being on the same WiFi network as the device.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tmustier](https://clawhub.ai/user/tmustier)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to control supported Dyson air purifiers, fans, and heaters on the same WiFi network through local MQTT commands after one-time Dyson account setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved Dyson device credentials can grant local control of configured devices.

Mitigation: Run setup only when comfortable entering Dyson account credentials and restrict ~/.dyson/config.json to the local user account.

Risk: Heat commands can affect physical device behavior if issued to the wrong device or target temperature.

Mitigation: Confirm the target device before issuing heat commands and verify the requested heating setting before execution.

## Reference(s):

- [README.md](README.md)
- [libdyson-neon](https://github.com/libdyson-wg/libdyson-neon)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require local network access to the Dyson device and saved credentials in ~/.dyson/config.json.]

## Skill Version(s):

0.1.0 (source: release evidence, pyproject.toml, src/dyson_cli/__init__.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
