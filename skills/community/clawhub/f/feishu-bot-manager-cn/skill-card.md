## Description: <br>
Manages Feishu bot accounts and OpenClaw routing bindings, including account-level or group-level routing to existing agents or newly initialized agent workspaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Alex-Shen1121](https://clawhub.ai/user/Alex-Shen1121) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to add Feishu bot credentials, bind bot or group traffic to an agent, and optionally initialize a new agent workspace for that bot. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu App Secret values may be stored in plaintext OpenClaw config and backup files. <br>
Mitigation: Use a dedicated Feishu bot secret, restrict permissions on ~/.openclaw, and rotate or remove secrets and backups when they are no longer needed. <br>
Risk: The skill can change global OpenClaw routing behavior through bindings and session.dmScope. <br>
Mitigation: Review the generated OpenClaw config before use and confirm the intended account-level or group-level binding. <br>
Risk: Gateway restart behavior can affect active service sessions. <br>
Mitigation: Prefer a manual or explicitly confirmed restart and coordinate timing when the Gateway is serving users. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Alex-Shen1121/feishu-bot-manager-cn) <br>
- [Feishu OpenClaw Bot Creation Page](https://open.feishu.cn/page/openclaw?form=multiAgent) <br>
- [New Agent Governance Reference](references/new-agent-governance.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update OpenClaw configuration, create backups, adjust Feishu routing bindings, and restart Gateway when executed.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
