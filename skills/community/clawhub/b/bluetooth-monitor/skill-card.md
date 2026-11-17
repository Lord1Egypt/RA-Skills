## Description:

蓝牙设备监控 / Bluetooth Device Monitor helps inspect connected and paired Mac Bluetooth devices, show battery information when available, and connect, disconnect, or change Bluetooth power state when explicitly invoked.

This skill is ready for commercial/non-commercial use.

## Publisher:

[franky0617](https://clawhub.ai/user/franky0617)

### License/Terms of Use:


## Use Case:

Mac users and support engineers use this skill to inspect Bluetooth device connection state, paired-device addresses, battery readings, and to issue explicit connect, disconnect, or power commands through a local helper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bluetooth power-off or disconnect commands can interrupt local input devices and active peripherals.

Mitigation: Run control commands only when the target device and fallback input path are understood, especially before turning Bluetooth off.

Risk: Displayed device names and status can be misleading because terminal output and grep handling have caveats in the security guidance.

Mitigation: Treat names and status as informational, verify device addresses before acting, and review output before using it for device-control decisions.

Risk: Some older Bluetooth devices may not report battery level.

Mitigation: Use battery output as best-effort information and avoid relying on it as complete coverage for every paired device.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/franky0617/skills/bluetooth-monitor)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash commands and terminal-style text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS with blueutil installed; Bluetooth device addresses are expected in hyphen-separated format.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
