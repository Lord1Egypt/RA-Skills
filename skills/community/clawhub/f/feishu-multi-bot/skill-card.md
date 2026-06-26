## Description: <br>
配置多个 OpenClaw Agent 使用独立飞书机器人，支持免配对直接聊天，自动重启生效并提供状态摘要。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gitxuzhefeng](https://clawhub.ai/user/gitxuzhefeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to configure multiple agents with separate Feishu bot credentials, enable direct DM and group chat access, apply the Gateway configuration, and verify service status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill collects Feishu App Secrets and uses them to update live Gateway configuration. <br>
Mitigation: Treat App Secrets as sensitive, avoid shared transcripts or logs, and rotate any secret that may have been exposed. <br>
Risk: Open DM and group policies allow users to chat with the configured bots without pairing. <br>
Mitigation: Confirm that open DM and group access is acceptable before applying the configuration. <br>
Risk: Applying the configuration restarts the OpenClaw Gateway. <br>
Mitigation: Apply changes during an acceptable maintenance window and verify Gateway status after the restart. <br>


## Reference(s): <br>
- [OpenClaw Feishu Documentation](https://docs.openclaw.ai/channels/feishu.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/gitxuzhefeng/feishu-multi-bot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration snippets, shell commands, and a status summary table.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu App IDs and App Secrets plus permission to update live OpenClaw Gateway Feishu settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
