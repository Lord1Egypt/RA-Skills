## Description: <br>
Enables the OpenClaw Feishu permission tool so an agent can add, inspect, and remove collaborators on Feishu documents and sheets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BenleyL](https://clawhub.ai/user/BenleyL) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users with authorized Feishu app access use this skill to enable Feishu permission management and manage collaborators for intended documents, sheets, folders, and bitables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change real Feishu document and sheet collaborator permissions. <br>
Mitigation: Use it only with an authorized Feishu app or account, verify document and user IDs before each change, and prefer the least privileged role needed. <br>
Risk: The enablement script modifies local OpenClaw configuration and restarts the gateway. <br>
Mitigation: Review the configuration change before running it, keep a rollback path for the OpenClaw config, and confirm the gateway status after restart. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BenleyL/feishu-perm-help) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct the user to edit OpenClaw Feishu tool configuration and restart the OpenClaw gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
