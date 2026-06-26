## Description: <br>
Regulates global agent parameters by sensing system state and dynamically adjusting working modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nic-yuan](https://clawhub.ai/user/nic-yuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to monitor token usage, active tasks, and conversation turns, then receive global parameter adjustment guidance for Apollo-style OpenClaw workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent global parameter state can change future agent behavior beyond the current request. <br>
Mitigation: Review the state file behavior before installation and require explicit confirmation for parameter changes. <br>
Risk: Broad triggers and propagated state may affect multiple Apollo or OpenClaw skills without clear scope limits. <br>
Mitigation: Limit which skills consume the propagated state and document rollback steps for restoring prior parameters. <br>
Risk: The security verdict is suspicious due to unclear user control over persistent behavior changes. <br>
Mitigation: Install only after reviewing the skill and adding clear confirmation, scoped parameters, rollback instructions, and propagation limits. <br>


## Reference(s): <br>
- [Apollo Endo ClawHub release](https://clawhub.ai/nic-yuan/apollo-endo) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style terminal text and JSON state file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script prints a parameter report and persists status to an OpenClaw state JSON file.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
