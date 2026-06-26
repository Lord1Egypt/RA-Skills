## Description: <br>
Control Flipper Zero hardware via USB serial or BLE for SubGHz, IR, NFC, RFID, BadUSB, GPIO, file system, screen capture, and input without Android or intermediary apps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elvisexmachina](https://clawhub.ai/user/elvisexmachina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and hardware engineers use this skill to control an authorized Flipper Zero from an agent workflow for device inspection, storage operations, screen capture, input automation, GPIO, and permitted RF or infrared tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes privileged Flipper Zero actions including radio transmit, BadUSB, storage deletion, reboot or power controls, GPIO, and raw commands. <br>
Mitigation: Require explicit human approval before those actions, review generated commands before execution, and run them only against owned or authorized hardware. <br>
Risk: Radio and infrared operations can affect nearby devices or capture/transmit sensitive RF information. <br>
Mitigation: Use receive and transmit functions only where legally permitted and operationally authorized; avoid transmit commands when authorization is unclear. <br>
Risk: Screen capture and SubGHz watch commands may leave sensitive device or RF information in temporary PNG files. <br>
Mitigation: Clean up generated /tmp screenshot files after use and avoid collecting screens that contain secrets or sensitive identifiers. <br>
Risk: External CC1101 transmit operations can damage hardware if used without an antenna. <br>
Mitigation: Attach an appropriate antenna before transmitting with an external CC1101 module and confirm module setup before enabling 5V GPIO or OTG power. <br>


## Reference(s): <br>
- [ClawHub Flipper Zero release](https://clawhub.ai/elvisexmachina/flipper-zero) <br>
- [Flipper Zero protobuf definitions](https://github.com/flipperdevices/flipperzero-protobuf) <br>
- [V3SP3R reference project](https://github.com/elder-plinius/V3SP3R) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands; command scripts return JSON and may write PNG screenshots.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some screenshot and watch commands write files under /tmp; command outputs can include device, storage, screen, GPIO, or RF information.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
