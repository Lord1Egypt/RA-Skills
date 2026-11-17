## Description:

Guides agents through Bluetooth Low Energy device scanning, connection, GATT read and write operations, notifications, background tasks, and airctl configuration using the airctl CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skinapi2025](https://clawhub.ai/user/skinapi2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to plan and review airctl commands for Bluetooth Low Energy devices, including scans, connections, GATT reads and writes, notifications, and local BLE configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to rely on mutable remote code for the airctl dependency.

Mitigation: Install airctl only from a pinned, trusted release or reviewed commit, preferably in a virtual environment without elevated privileges.

Risk: BLE writes, daemon actions, periodic tasks, aliases, and presets can affect physical devices or persist local configuration.

Mitigation: Require explicit user approval before these operations, especially for unfamiliar devices or UUIDs.

Risk: Incorrect addresses, UUIDs, handles, or write payloads can target the wrong device or characteristic.

Mitigation: Validate user inputs against the documented formats and confirm the selected device and characteristic before issuing commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skinapi2025/skills/ble-device-control)
- [ClawHub publisher profile](https://clawhub.ai/user/skinapi2025)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command blocks and validation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user review before installing airctl or running BLE write, daemon, background task, alias, or preset commands.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
