## Description:

Control smart home devices via Homebridge Config UI X REST API. Use to list, turn on/off, adjust brightness, color, or temperature of HomeKit-compatible accessories. Supports lights, switches, thermostats, fans, and other Homebridge-managed devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiasenl](https://clawhub.ai/user/jiasenl)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to inspect and control Homebridge-managed smart-home accessories through the Homebridge Config UI X REST API. It supports listing accessories and rooms, checking device state, and issuing changes such as power, brightness, color, fan, or thermostat settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can immediately change physical smart-home device state, including switches, fans, and thermostats.

Mitigation: Review commands before execution and use the skill only with a trusted Homebridge instance and account scoped to the intended devices.

Risk: Stored Homebridge credentials may grant access to device control.

Mitigation: Protect the credential file and prefer a least-privileged Homebridge account.

Risk: The helper script accepts the configured Homebridge URL without enforcing HTTPS.

Mitigation: Configure an https:// Homebridge URL before use.

## Reference(s):

- [Homebridge Config UI X](https://github.com/homebridge/homebridge-config-ui-x)
- [ClawHub Skill Page](https://clawhub.ai/jiasenl/skills/clawdbot-skill-homebridge)
- [Publisher Profile](https://clawhub.ai/user/jiasenl)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and Python helper usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce API requests that read or change Homebridge accessory state.]

## Skill Version(s):

0.1.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
