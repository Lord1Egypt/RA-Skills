## Description: <br>
飞书新机器人创建工作流，用于指导代理协助用户创建、配置并验证新的飞书/OpenClaw 机器人。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinchenjia](https://clawhub.ai/user/jinchenjia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to guide setup of a new Feishu/OpenClaw bot, including app creation handoff, credential collection, workspace setup, gateway configuration, file synchronization, identity files, and connection validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may expose Feishu APP SECRET values to an agent or chat transcript. <br>
Mitigation: Use a secret manager or environment variable where possible, and share the secret in chat only when that is acceptable for the environment. <br>
Risk: The workflow changes OpenClaw gateway configuration and can affect local bot routing or access. <br>
Mitigation: Require explicit user approval, back up openclaw.json, and review the exact diff before restarting the gateway. <br>
Risk: Copied AGENTS, TOOLS, USER, or MEMORY files may carry private or stale instructions into the new bot workspace. <br>
Mitigation: Inspect copied files before use and remove private, obsolete, or Thanos-specific content. <br>
Risk: A newly created bot may need to be revoked or removed if setup is incorrect. <br>
Mitigation: Keep a clear revocation and removal plan for the Feishu app, credentials, workspace, and gateway entry. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jinchenjia/feishu-new-bot) <br>
- [Feishu Open Platform OpenClaw app creation page](https://open.feishu.cn/page/openclaw?form=multiAgent) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, markdown] <br>
**Output Format:** [Markdown guidance with configuration steps, checklists, and command-oriented instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May involve local workspace files, OpenClaw gateway configuration, Feishu app credentials, and bot validation messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
