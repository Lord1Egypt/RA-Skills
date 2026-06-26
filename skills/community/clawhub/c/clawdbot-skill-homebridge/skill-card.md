## Description: <br>
Control smart home devices via Homebridge Config UI X REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JiasenL](https://clawhub.ai/user/JiasenL) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to inspect Homebridge-managed accessories and control smart-home device characteristics such as power, brightness, color, fan speed, and thermostat targets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change real smart-home devices exposed through a Homebridge account. <br>
Mitigation: Confirm accessory IDs and requested values before changing state, and avoid unattended use for safety-sensitive devices such as thermostats, locks, garage doors, or appliances. <br>
Risk: The skill relies on stored Homebridge credentials. <br>
Mitigation: Keep the credential file private and prefer a least-privilege Homebridge user when available. <br>


## Reference(s): <br>
- [Homebridge Config UI X](https://github.com/homebridge/homebridge-config-ui-x) <br>
- [ClawHub skill page](https://clawhub.ai/JiasenL/clawdbot-skill-homebridge) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline bash, Python, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes API request examples and a helper script that returns JSON responses from Homebridge.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
