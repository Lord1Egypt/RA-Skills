## Description: <br>
Manage OpenClaw agents by creating new agents, configuring workspaces, setting up Feishu bot integrations, and verifying multi-bot routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zouxuyang](https://clawhub.ai/user/zouxuyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to create and configure local OpenClaw agents, bind them to Feishu bots, and verify routing before bringing agents online. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change local OpenClaw agent workspaces and OpenClaw configuration. <br>
Mitigation: Back up ~/.openclaw/openclaw.json before use and review the planned Agent ID, workspace path, and Feishu binding changes before confirming execution. <br>
Risk: Feishu app secrets may be printed, captured, or stored during the authorization and binding flow. <br>
Mitigation: Run authorization only in private terminals, avoid logged or shared sessions, prefer authenticated pairing for private bots, and rotate any Feishu secret that may have been exposed. <br>


## Reference(s): <br>
- [Artifact README](README.md) <br>
- [Artifact Skill Instructions](SKILL.md) <br>
- [ClawHub skill page](https://clawhub.ai/zouxuyang/agent-manager-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local configuration changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute local OpenClaw commands and update ~/.openclaw/openclaw.json after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
