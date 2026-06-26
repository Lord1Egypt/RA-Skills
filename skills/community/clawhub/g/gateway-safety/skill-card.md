## Description: <br>
Safely update OpenClaw gateway configuration (openclaw.json) with automatic validation, backup, and 30-second health-check rollback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allthebadthings](https://clawhub.ai/user/allthebadthings) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill when changing OpenClaw gateway settings, ports, provider credentials, or network bindings while preserving a rollback path if the gateway fails health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A proposed OpenClaw gateway configuration could break access or expose provider settings if applied without review. <br>
Mitigation: Review the proposed openclaw.json before running the update script and use the skill only when an agent is expected to modify gateway settings. <br>
Risk: Backups and known-good configuration copies may retain old provider credentials locally. <br>
Mitigation: Keep ~/.openclaw permissions restrictive and handle backup files as sensitive local configuration. <br>


## Reference(s): <br>
- [Gateway Safety on ClawHub](https://clawhub.ai/allthebadthings/gateway-safety) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces commands and safety steps for updating local OpenClaw gateway configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
