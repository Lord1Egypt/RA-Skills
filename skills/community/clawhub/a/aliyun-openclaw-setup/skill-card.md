## Description: <br>
Installs, configures, and troubleshoots OpenClaw channels for DingTalk, Feishu, Discord, and documented additional channels with Bailian/DashScope models on Linux hosts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to provision Linux-hosted OpenClaw gateways, configure channel credentials and model defaults, discover supported channels from OpenClaw documentation, and verify gateway health. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup workflow can install software, start a persistent OpenClaw gateway, and modify host-level or user-level service configuration. <br>
Mitigation: Run it only on a host you control, review and pin install commands before execution, avoid running the gateway or agent workspace as root, and confirm stop or disable procedures before production use. <br>
Risk: Channel setup requires app secrets, bot tokens, gateway tokens, and DashScope API keys. <br>
Mitigation: Store real credentials only in server-local configuration or a secret manager, restrict file permissions, and redact logs before sharing evidence or support tickets. <br>
Risk: Open chat channels can expose the gateway to unintended users or groups. <br>
Mitigation: Use pairing, allowlists, group policies, and mention requirements where supported, and validate real send/receive behavior before enabling production access. <br>
Risk: Documentation-driven channel discovery may become stale or produce incorrect installation details if package names or config keys change. <br>
Mitigation: Read the current official OpenClaw channel documentation for each requested channel and use exact documented install commands and configuration keys. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cinience/aliyun-openclaw-setup) <br>
- [Publisher profile](https://clawhub.ai/user/cinience) <br>
- [OpenClaw channel documentation](https://docs.openclaw.ai/channels/index) <br>
- [Channel discovery workflow](references/channel-discovery.md) <br>
- [OpenClaw configuration reference](references/config.md) <br>
- [DingTalk bot setup guide](references/dingtalk-setup.md) <br>
- [Feishu channel setup guide](references/feishu-setup.md) <br>
- [Discord channel setup guide](references/discord-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup steps, channel configuration mappings, gateway health checks, troubleshooting guidance, and evidence collection instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
