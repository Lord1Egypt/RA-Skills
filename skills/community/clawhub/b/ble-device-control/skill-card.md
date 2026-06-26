## Description: <br>
Controls Bluetooth Low Energy devices through the airctl CLI for scanning, connecting, reading, writing, notifications, and device profile commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skinapi2025](https://clawhub.ai/user/skinapi2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to guide agent interactions with local BLE devices, including discovery, GATT reads and writes, notifications, keep-alive polling, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: BLE write commands and periodic write tasks can change real device behavior. <br>
Mitigation: Review commands before execution, validate device addresses, UUIDs, and write payloads, and require explicit user approval before writes or periodic write tasks. <br>
Risk: Background BLE tasks or daemon activity may keep operating after the immediate request is complete. <br>
Mitigation: Stop background tasks and daemon activity when finished, and prefer bounded snapshot queries for event polling. <br>
Risk: The skill depends on a local airctl CLI installation, which introduces tool provenance and installation risk. <br>
Mitigation: Install airctl only with user approval, verify the package source before installation, and confirm the installed package origin before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skinapi2025/ble-device-control) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON command output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes input-validation guidance and user-confirmation steps for installation and write operations.] <br>

## Skill Version(s): <br>
1.0.4 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
