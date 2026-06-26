## Description: <br>
Guide to set up and configure IM channels(Telegram, Discord, Slack, Feishu, Dingtalk) for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[petopagi](https://clawhub.ai/user/petopagi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure OpenClaw messaging integrations for Telegram, Discord, Slack, Feishu, and Dingtalk and apply the changes by restarting the gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Channel setup requires chat bot tokens, app secrets, and gateway credentials that could expose services if mishandled. <br>
Mitigation: Use least-privilege credentials, keep ~/.openclaw/openclaw.json private, and review each configuration change before applying it. <br>
Risk: Restarting the OpenClaw gateway can briefly interrupt service. <br>
Mitigation: Warn users before restarting and perform the restart during an acceptable maintenance window. <br>


## Reference(s): <br>
- [Feishu Channel Setup Guide](/root/.openclaw/extensions/feishu/README.md) <br>
- [Dingtalk Channel Setup Guide](/root/.openclaw/extensions/dingtalk-connector/README.md) <br>
- [OpenClaw Channel Setup Guide](/root/.local/share/pnpm/global/5/node_modules/openclaw/docs/channels) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes channel setup steps and gateway restart guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
