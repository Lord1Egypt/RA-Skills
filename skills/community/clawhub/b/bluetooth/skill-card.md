## Description:

Discover, connect, and control Bluetooth devices with automatic profile learning, cross-platform tools, and device management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to discover, profile, connect to, troubleshoot, and control authorized Bluetooth devices across Linux, macOS, Windows, and cross-platform BLE libraries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control local Bluetooth devices and trigger high-impact smart-home or app actions.

Mitigation: Require explicit user confirmation for new devices, pairing, smart-home actions, health-data export or sync, and any operation that changes device state.

Risk: The skill can persist sensitive device identifiers, pairing details, health data, and interaction history under ~/bluetooth/.

Mitigation: Keep the profile directory private or encrypted, avoid storing PINs or passkeys in profile files, and do not send MAC addresses or logs to external services.

Risk: Bluetooth packet capture and diagnostics can expose private traffic and may require elevated privileges.

Mitigation: Run btmon or similar capture tools with sudo only for authorized diagnostics, limit capture duration, and store captures in a controlled location.

Risk: Cross-platform Bluetooth libraries and tools may introduce dependency or environment risk.

Mitigation: Install Bluetooth libraries in an isolated, pinned environment and keep operating-system Bluetooth components updated.

## Reference(s):

- [Bluetooth skill on ClawHub](https://clawhub.ai/ivangdavila/skills/bluetooth)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local Bluetooth profile and history files under ~/bluetooth/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
