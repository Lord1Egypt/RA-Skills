## Description: <br>
蓝牙设备监控 / Bluetooth Device Monitor - 查看Mac已连接的蓝牙设备列表，支持配对、连接、断开操作 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[franky0617](https://clawhub.ai/user/franky0617) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Mac users and support or developer operators use this skill to inspect connected and paired Bluetooth devices, view battery and power status, and run local blueutil commands to connect, disconnect, or power Bluetooth devices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Disconnecting devices or turning Bluetooth off can interrupt keyboards, trackpads, mice, audio devices, or other active peripherals. <br>
Mitigation: Review the target device address before running disconnect or power off commands, and avoid disabling Bluetooth when critical input devices depend on it. <br>
Risk: The skill depends on blueutil for Bluetooth control. <br>
Mitigation: Install blueutil only from a trusted Homebrew source before using the command wrapper. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/franky0617/bluetooth-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text output and Markdown usage guidance with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS with blueutil installed; battery details may be unavailable for some Bluetooth devices.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
