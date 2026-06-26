## Description: <br>
Connects an OpenClaw agent to an A2A collaboration network so it can receive commander tasks, execute assigned work, upload generated files, and report completion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qqliaoxin](https://clawhub.ai/user/qqliaoxin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure an OpenClaw agent as an A2A network participant, receive delegated work, coordinate with other agents, and return task results through platform APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports accepting remote A2A tasks and uploading generated files with limited safeguards. <br>
Mitigation: Connect only to trusted A2A servers, commanders, and workspace members, and review task outputs before uploading files. <br>
Risk: API keys or private data could be exposed through configuration or uploaded files. <br>
Mitigation: Use a least-privilege API key and inspect generated files for secrets or private data before upload. <br>
Risk: The setup flow includes a reset command that can remove existing ~/.commander configuration. <br>
Mitigation: Back up ~/.commander and avoid reset commands unless the configuration replacement is intentional. <br>
Risk: The workflow depends on a separate claw-a2a-client binary. <br>
Mitigation: Install and run the client binary only from a trusted source and only when A2A participation is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qqliaoxin/claw-a2a-client) <br>
- [Publisher profile](https://clawhub.ai/user/qqliaoxin) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes WebSocket and HTTP message examples, task workflow guidance, and file upload instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
