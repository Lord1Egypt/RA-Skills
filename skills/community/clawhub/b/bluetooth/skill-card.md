## Description: <br>
Discover, connect, and control Bluetooth devices with automatic profile learning, cross-platform tools, and device management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and personal automation users use this skill to discover, pair, profile, troubleshoot, and control Bluetooth audio, smart-home, wearable, and maker devices across common desktop platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can scan, pair with, connect to, and command nearby Bluetooth devices, which can affect device state or expose nearby-device presence. <br>
Mitigation: Require explicit user confirmation for new scans and pairings, interact only with authorized devices, log connection attempts, and use timeouts for scans, commands, and idle connections. <br>
Risk: Device profiles, logs, packet captures, and Bluetooth identifiers may contain sensitive device traffic or persistent identifiers. <br>
Mitigation: Run packet captures only when intended, keep ~/bluetooth/ profiles and logs private, avoid exposing MAC addresses externally, and delete stale records when they are no longer needed. <br>


## Reference(s): <br>
- [Bluetooth skill release](https://clawhub.ai/ivangdavila/bluetooth) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, code snippets, device-profile examples, and step-by-step procedures] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local Bluetooth profiles and logs under ~/bluetooth/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
