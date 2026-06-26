## Description: <br>
Provides an interactive wizard to configure, validate, and troubleshoot multiple OpenClaw agents for Feishu channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zoopools](https://clawhub.ai/user/Zoopools) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to onboard one or more agents to Feishu by collecting app credentials, writing channel bindings, validating configuration, and running diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu App Secrets are stored in the local OpenClaw configuration as sensitive plaintext credentials. <br>
Mitigation: Use a dedicated Feishu app with minimum required permissions, keep ~/.openclaw/openclaw.json private, avoid committing or backing it up with real secrets, and rotate the secret if exposure is suspected. <br>
Risk: Incorrect Feishu permissions, event subscriptions, or account bindings can prevent agents from receiving or replying to messages. <br>
Mitigation: Run the skill's validation and diagnostic modes, confirm Feishu event subscription and bot permissions, then restart the OpenClaw gateway and approve pairing before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zoopools/feishu-multiagent-onboard) <br>
- [Configuration guide](docs/guide.md) <br>
- [FAQ](docs/faq.md) <br>
- [Feishu Open Platform](https://open.feishu.cn/app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Interactive terminal prompts and Markdown documentation with JSON configuration examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write Feishu channel accounts and agent bindings to the local OpenClaw configuration when run by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, artifact SKILL.md, clawhub.json, and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
