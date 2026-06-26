## Description: <br>
Route Aqara Open API requests across device, space, and automation skills with a relationship-first router, shared CLI contract, and structured handoff contract. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aqara](https://clawhub.ai/user/aqara) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and smart-home operators use this skill to route agent requests to Aqara device, space, and automation workflows, generate validated Aqara CLI commands, and manage cache-backed Open API interactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an Aqara Open API token and can control real smart-home devices and automations. <br>
Mitigation: Install only if the aqara publisher is trusted, keep tokens out of chat/logs/files, and verify credential source before running commands. <br>
Risk: Mutating operations can delete automations, move devices between spaces, or trigger device-control automations. <br>
Mitigation: Confirm exact IDs and names, and require explicit confirmation before deletes, broad room moves, or device-control automations. <br>
Risk: Automation examples may contain button or event enum assumptions that differ from live device capabilities. <br>
Mitigation: Check live capabilities and enum values before creating automations from examples. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/aqara/aqara-open-api-local) <br>
- [README](README.md) <br>
- [ClawHub Deployment Guide](README-CLAWHUB.md) <br>
- [CLI Command Catalog](docs/commands.md) <br>
- [Intent-Based Example Index](references/examples.md) <br>
- [Automation HTTP Lifecycle Examples](references/automation-http-examples.md) <br>
- [Automation Configuration Guide](references/automation_config.md) <br>
- [Automation Instance Schema](references/automation-instance-v0.schema.json) <br>
- [Aqara Open API Endpoint](https://aiot-open-3rd.aqara.cn/open/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration or API request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or execute Aqara CLI commands; mutating device, space, and automation actions require confirmed identifiers and credentials.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
