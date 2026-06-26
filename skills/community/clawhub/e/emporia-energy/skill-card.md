## Description: <br>
Direct Emporia Vue energy queries via Emporia cloud (PyEmVue) or local ESPHome API, including guidance on choosing/configuring cloud vs local modes and running list/summary/circuit commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[urosorozel](https://clawhub.ai/user/urosorozel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and home energy users use this skill to query Emporia Vue energy readings through either Emporia cloud credentials or a local ESPHome API and inspect summaries, channel lists, or specific circuits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to Emporia account credentials or local ESPHome connection details to retrieve energy readings. <br>
Mitigation: Keep credentials in environment or config files rather than chat, and avoid sharing outputs that expose private device, channel, or household energy details. <br>
Risk: ESPHome local mode depends on LAN reachability and native API credentials for the target device. <br>
Mitigation: Use ESPHome mode only for devices intentionally flashed with ESPHome and reachable on the local network, and provide the API key or legacy password through local configuration. <br>
Risk: The ESPHome dependency is specified as a minimum version, so future dependency updates may change behavior. <br>
Mitigation: Pin the ESPHome dependency when repeatable installs are required. <br>


## Reference(s): <br>
- [Emporia Energy Skill References](references/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands; scripts emit JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [JSON output includes timestamp, mode, unit, total, top circuits, channels used, or matched circuit channels depending on command.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
