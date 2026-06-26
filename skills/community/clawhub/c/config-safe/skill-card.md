## Description: <br>
Config Safe helps agents change OpenClaw configuration safely by reading current documentation, previewing changes, validating them, and requiring user confirmation before writing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[glfruit](https://clawhub.ai/user/glfruit) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to plan, preview, validate, and apply OpenClaw configuration changes while reducing the chance of breaking Gateway startup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A malformed OpenClaw configuration can prevent Gateway from starting. <br>
Mitigation: Preview the proposed diff, validate against the schema, and keep a recovery path such as openclaw doctor or manual editing of ~/.openclaw/openclaw.json. <br>
Risk: Configuration previews may expose secrets such as channel tokens. <br>
Mitigation: Mask sensitive values in previews and review every diff before approving a write. <br>
Risk: A full config.apply replacement has broader blast radius than a partial change. <br>
Mitigation: Prefer config.patch for targeted updates and use config.apply only when the full replacement and its risks are understood. <br>


## Reference(s): <br>
- [Config Safe ClawHub release](https://clawhub.ai/glfruit/config-safe) <br>
- [Source skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before configuration writes; masks sensitive values in previews.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
