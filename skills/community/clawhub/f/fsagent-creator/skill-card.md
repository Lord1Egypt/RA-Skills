## Description: <br>
Creates, deletes, and lists OpenClaw Feishu agent instances, including Feishu app credentials, model selection, workspace setup, and OpenClaw configuration updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1054570699](https://clawhub.ai/user/1054570699) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw administrators use this skill to manage Feishu-connected agents by creating workspaces, updating OpenClaw configuration, listing agents, and removing non-main agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu App IDs and App Secrets can be exposed if pasted into shared chat, shell history, or logs. <br>
Mitigation: Use a protected environment variable, masked prompt, or secrets manager for credentials, and avoid sharing real secrets in command examples. <br>
Risk: The scripts make persistent administrative changes under /home/admin/.openclaw, including OpenClaw configuration and agent workspace directories. <br>
Mitigation: Back up openclaw.json and relevant workspaces before creating or deleting agents, then review the generated configuration before restarting the gateway. <br>
Risk: The Feishu binding includes a fixed group identifier that may not match the user's intended deployment. <br>
Mitigation: Review and replace the group binding with the intended Feishu account and group before using the created agent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1054570699/fsagent-creator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include credential-handling reminders, OpenClaw configuration changes, and gateway restart guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
