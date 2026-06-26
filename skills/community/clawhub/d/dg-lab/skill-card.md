## Description: <br>
Control DG-LAB Coyote 3.0 pulse devices through a local WebSocket controller for pairing, strength changes, waveform presets, and emergency stop handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YuuLuo](https://clawhub.ai/user/YuuLuo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they intentionally want an agent to help operate a DG-LAB Coyote 3.0 device through a localhost controller. It guides environment setup, device pairing, channel confirmation, strength changes, waveform output, and emergency stop actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a physical pulse device, so incorrect setup or unwanted output could create real physical discomfort or injury. <br>
Mitigation: Install only when intentional, complete the documented safety and channel confirmations before output, start at low strength, keep emergency stop available, and stop services after use. <br>
Risk: The workflow installs and runs an external relay server dependency. <br>
Mitigation: Review the relay-server install source before use and keep the control API bound to localhost as described in the security guidance. <br>


## Reference(s): <br>
- [Protocol reference](references/protocol.md) <br>
- [Waveform format reference](references/waveform-format.md) <br>
- [DG-LAB official relay server](https://github.com/DG-LAB-OPENSOURCE/DG-LAB-OPENSOURCE) <br>
- [DG-LAB V3 Bluetooth protocol](https://github.com/DG-LAB-OPENSOURCE/DG-LAB-OPENSOURCE/blob/main/coyote/v3/README_V3.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and localhost HTTP API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces human-facing setup and operation instructions; device actions are executed through local commands only after user safety and channel confirmations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
