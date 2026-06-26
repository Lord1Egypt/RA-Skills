## Description: <br>
绑定飞书机器人到Agent。用户发送App ID和App Secret即可自动配置飞书账号并绑定到指定Agent。用于：(1) 用户提供App ID和App Secret (2) 创建或选择要绑定的Agent (3) 自动配置openclaw.json并重启Gateway。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aigcpro](https://clawhub.ai/user/aigcpro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw Gateway administrators use this skill to bind a Feishu bot account to a selected OpenClaw agent by collecting Feishu credentials, updating channel configuration, binding the agent, restarting the Gateway, and checking channel status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for Feishu App Secrets and could expose sensitive credentials if they are pasted into shared chat or stored carelessly. <br>
Mitigation: Do not paste real App Secrets into shared chat; use least-privilege Feishu credentials and handle secrets through an approved private channel. <br>
Risk: The skill changes OpenClaw Gateway configuration and restarts the Gateway, which can affect an active deployment if the target agent or configuration is wrong. <br>
Mitigation: Install only when administering the target Gateway, back up the existing configuration, verify the target agent, and explicitly approve config writes and Gateway restarts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aigcpro/feishu-agents-bind) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides credential collection, OpenClaw configuration changes, Feishu agent binding, Gateway restart, and status verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
