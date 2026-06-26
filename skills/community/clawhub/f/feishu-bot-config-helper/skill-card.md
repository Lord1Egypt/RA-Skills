## Description: <br>
Helps configure Feishu bots for OpenClaw by parsing bot credentials, matching an Agent profile, updating local configuration, and producing a setup report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiebao360](https://clawhub.ai/user/jiebao360) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up Feishu bot accounts for OpenClaw Agents from a chat-style configuration request or CLI input. It is intended for creating bot-specific workspaces, Agent entries, Feishu channel account settings, and route bindings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically change OpenClaw configuration and restart the Gateway. <br>
Mitigation: Back up ~/.openclaw/openclaw.json, inspect planned changes, and test with non-production OpenClaw configuration before use. <br>
Risk: Feishu app secrets may be copied into local configuration. <br>
Mitigation: Use test Feishu credentials first, rotate any secret copied from examples, and restrict credential access after configuration. <br>
Risk: Feishu allowlists, group access, and Agent skill bindings may be broader than intended. <br>
Mitigation: Manually restrict Feishu allowlists, group access, and enabled Agent skills after configuration. <br>
Risk: The installer is commonly run from a remote shell command. <br>
Mitigation: Inspect the installer before running it instead of piping remote content directly to bash. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jiebao360/feishu-bot-config-helper) <br>
- [Publisher profile](https://clawhub.ai/user/jiebao360) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown-style setup report with JSON configuration changes and command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update ~/.openclaw/openclaw.json, create workspace directories, store Feishu app credentials, and restart the OpenClaw Gateway.] <br>

## Skill Version(s): <br>
0.1.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
