## Description: <br>
Control local LSC/Tuya lamps and groups to turn on or off, set brightness, change colors or white modes, query status, and onboard devices after repair or network changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ooxtcoo](https://clawhub.ai/user/ooxtcoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate locally configured Tuya/LSC lamps through the project CLI or Python fallback, including routine control and key refresh after device repair or network changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can control the configured local lamps and groups. <br>
Mitigation: Install only where agent-initiated lamp control is acceptable, and review the lamp registry before use. <br>
Risk: The skill asks the agent to update its installed SKILL.md for machine-specific paths. <br>
Mitigation: Keep machine-specific paths in a separate user-reviewed configuration or review any instruction changes before deployment. <br>
Risk: Local Tuya keys are sensitive and required for device control. <br>
Mitigation: Store real local_key values only in expected local files, verify their location, and use sanitized values in shared artifacts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ooxtcoo/fully-local-tuya-light-control-skill-lsc-connect-app-devices) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May issue local CLI or Python fallback commands against configured Tuya devices; requires a valid local registry and local_key values.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
