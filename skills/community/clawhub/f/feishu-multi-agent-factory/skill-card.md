## Description: <br>
Configures multiple OpenClaw agents and Feishu channels through a guided workflow that writes local OpenClaw configuration and initializes agent workspaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cchenwei](https://clawhub.ai/user/cchenwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to add, preview, list, or remove OpenClaw agents that are bound to Feishu bot accounts. It is intended for local OpenClaw administration where the user can review a dry run before writing configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup script can write real local OpenClaw configuration and optionally restart the gateway. <br>
Mitigation: Back up ~/.openclaw/openclaw.json, review the dry-run output first, and confirm write or restart actions separately. <br>
Risk: Feishu App Secrets are collected and stored in the local OpenClaw configuration. <br>
Mitigation: Protect Feishu App Secrets, avoid echoing them in conversation, and keep the OpenClaw configuration file access-controlled. <br>
Risk: Removing an agent changes OpenClaw configuration while leaving workspace directories for manual cleanup. <br>
Mitigation: Confirm any --remove action separately and inspect remaining workspace directories before deleting them manually. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cchenwei/feishu-multi-agent-factory) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/cchenwei) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON payloads and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces dry-run previews and local OpenClaw configuration changes when executed by the user.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
