## Description: <br>
Helps agents propose and apply validated, minimal changes to OpenClaw configuration, including model, channel, auth, tools, gateway, session, hooks, plugins, and related settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onenameneo](https://clawhub.ai/user/onenameneo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to safely update OpenClaw settings in openclaw.json, diagnose configuration errors, and validate unfamiliar fields against OpenClaw documentation before changes are applied. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect OpenClaw configuration changes can prevent startup or alter sensitive auth, environment, gateway, browser, sandbox, skills, plugins, command, or hook behavior. <br>
Mitigation: Review every proposed minimal patch before approval, and validate unfamiliar fields against OpenClaw documentation before applying changes. <br>
Risk: Suggested recovery commands may modify configuration automatically after startup failures. <br>
Mitigation: Use diagnostic commands first and approve auto-repair commands only after reviewing their intended effect. <br>


## Reference(s): <br>
- [OpenClaw configuration overview](https://docs.openclaw.ai/gateway/configuration) <br>
- [OpenClaw configuration reference](https://docs.openclaw.ai/gateway/configuration-reference) <br>
- [OpenClaw configuration examples](https://docs.openclaw.ai/gateway/configuration-examples) <br>
- [ClawHub skill page](https://clawhub.ai/onenameneo/configure-openclaw) <br>
- [Publisher profile](https://clawhub.ai/user/onenameneo) <br>


## Skill Output: <br>
**Output Type(s):** [Configuration instructions, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with minimal JSON5 patches and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Proposes changed fields only and requires user confirmation before writing configuration.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
