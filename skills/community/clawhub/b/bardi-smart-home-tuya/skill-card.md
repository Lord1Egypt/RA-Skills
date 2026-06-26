## Description: <br>
Controls Tuya and Bardi smart-home devices through the Tuya Cloud API, including lights, plugs, sensors, meters, color and brightness settings, raw DP commands, and local network discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elony-7](https://clawhub.ai/user/elony-7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent discover, inspect, and control Tuya-compatible Bardi smart-home devices from a configured Tuya cloud project. It is suited for device status checks, light color and brightness changes, power control, raw DP commands, batch commands, and local network discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad control over real Tuya/Bardi devices without built-in approval guardrails. <br>
Mitigation: Require explicit user approval before power, raw DP, batch, camera, curtain, or other safety-relevant commands. <br>
Risk: Tuya cloud credentials can expose or control linked smart-home devices if mishandled. <br>
Mitigation: Use a dedicated least-privilege Tuya cloud project, store credentials in environment or secret management, and keep credentials out of logs. <br>
Risk: Local network discovery sends UDP broadcast traffic and may expose device identifiers on the local network. <br>
Mitigation: Run local scans only on trusted networks, keep scan timeouts limited, and avoid scanning networks where this traffic is not expected. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/elony-7/bardi-smart-home-tuya) <br>
- [Setup guide](SETUP.md) <br>
- [API Reference - Bardi-Tuya Smart Home](references/api-reference.md) <br>
- [Tuya IoT Platform](https://iot.tuya.com) <br>
- [Tuya Smart China platform](https://tuyasmart.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TUYA_ACCESS_ID and TUYA_ACCESS_SECRET; TUYA_API_REGION is optional.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
