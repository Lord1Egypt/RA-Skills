## Description: <br>
三省六部 is an OpenClaw multi-agent orchestration and governance skill for coordinating nine specialized agents with dashboard monitoring, model configuration, workflow support, and audit trails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhmza](https://clawhub.ai/user/zhmza) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI operations teams use this skill to coordinate complex multi-agent workflows, allocate resources, review risks, manage compliance checks, and monitor execution through an Edict-style governance model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default setup can expose a sensitive dashboard. <br>
Mitigation: Bind the dashboard to localhost unless remote access is intentional, and add strong authentication before any external exposure. <br>
Risk: Installation can alter the user's Python environment. <br>
Mitigation: Install in a virtual environment and avoid --break-system-packages. <br>
Risk: Audit logs may contain sensitive data and be retained for a long period. <br>
Mitigation: Reduce retention where appropriate and redact logs before processing sensitive information. <br>
Risk: Runtime behavior depends on the external Edict implementation that is installed or imported. <br>
Mitigation: Inspect the implementation that will actually run before deploying the skill. <br>


## Reference(s): <br>
- [三省六部 reference notes](artifact/references/README.md) <br>
- [ClawHub skill page](https://clawhub.ai/zhmza/edict) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples, shell commands, and YAML configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may guide local setup, dashboard launch, model routing, audit logging, and governance workflow configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, skill metadata, and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
