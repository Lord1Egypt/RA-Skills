## Description:

Controls Bardi and other Tuya-compatible smart home devices through the Tuya Cloud API, including lights, plugs, sensors, meters, raw DP commands, batch commands, and local network device discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elony-7](https://clawhub.ai/user/elony-7)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent discover Tuya-linked devices, check device status, and control Bardi or Tuya-compatible smart home devices. It is suited for smart-home automation tasks such as turning devices on or off, adjusting lighting, reading device details, scanning the local network, and sending explicit device DP commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Tuya cloud access can enumerate and control real smart-home devices linked to the configured account.

Mitigation: Use a dedicated least-privilege Tuya cloud project, limit linked devices to the intended scope, and review state-changing commands before execution.

Risk: Raw and batch DP commands can change device state in ways that are not limited to the named light and switch workflows.

Mitigation: Prefer documented commands, inspect the device model before sending raw DP codes, and require explicit confirmation for raw or batch commands.

Risk: Persistent plaintext environment-variable setup can expose Tuya Access ID and Access Secret.

Mitigation: Store credentials in a vault or restricted per-process environment file and avoid placing secrets in global shell startup files.

Risk: Local discovery sends UDP broadcast packets that may be visible on the network or blocked by firewall policy.

Mitigation: Run scans only on trusted networks where discovery traffic is expected, and keep scan timeouts narrow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/elony-7/skills/bardi-smart-home-tuya)
- [Setup](SETUP.md)
- [API Reference - Bardi-Tuya Smart Home](references/api-reference.md)
- [Tuya IoT Platform](https://iot.tuya.com)
- [Tuya Smart China](https://tuyasmart.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON terminal output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TUYA_ACCESS_ID and TUYA_ACCESS_SECRET for cloud control; TUYA_API_REGION is optional and defaults to sg.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
