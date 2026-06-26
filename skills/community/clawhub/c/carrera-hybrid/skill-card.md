## Description: <br>
Controls Carrera HYBRID RC cars by Sturmkind over Bluetooth Low Energy, including drive, steering, light control, Telegram remote control, protocol sniffing, and text-drawing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marcel030](https://clawhub.ai/user/marcel030) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and BLE hobbyists use this skill to control their own Carrera HYBRID/Sturmkind RC cars and to understand the BLE packet protocol for authorized analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: BLE drive commands can cause physical movement of a Carrera HYBRID RC car. <br>
Mitigation: Verify the BLE address, supervise the car while commands run, operate in a clear area, and stop or idle the car after motion commands. <br>
Risk: Telegram remote control can expose vehicle commands to unintended users if the bot is broadly accessible. <br>
Mitigation: Restrict any Telegram bot to trusted chat IDs and avoid sharing bot credentials or control links. <br>
Risk: Protocol sniffing and MITM capture can be misused against devices or traffic the user does not own. <br>
Mitigation: Use MITM and protocol-analysis steps only on devices and BLE traffic the user owns or is explicitly authorized to analyze. <br>


## Reference(s): <br>
- [Carrera HYBRID BLE Protocol - Reverse Engineering Notes](references/protocol.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/marcel030/carrera-hybrid) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include BLE control commands, packet formats, calibration notes, and safety guidance for authorized devices.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
