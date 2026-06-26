## Description: <br>
Control interactive BLE devices (scan/connect/playback/timeline) from terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LovappenCava](https://clawhub.ai/user/LovappenCava) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and terminal users use this skill to install and operate the dokidoki CLI for scanning, connecting to, and controlling BLE devices, including timeline playback and direct device actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: BLE scanning may reveal nearby device names or identifiers. <br>
Mitigation: Scan only in the intended environment and confirm the target device before connecting. <br>
Risk: Commands can control a nearby BLE device through action and playback operations. <br>
Mitigation: Confirm the connected device before running action or playback commands, and use pause, disconnect, or stop when finished. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LovappenCava/dokidoki) <br>
- [Publisher profile](https://clawhub.ai/user/LovappenCava) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the doki CLI, Node.js 18+, and Bluetooth Low Energy support; audio playback may require ffplay or afplay.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
