## Description: <br>
Creates a new Feishu or Lark bot through the Feishu App Registration API Device Flow and saves the bot credentials to the OpenClaw config file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hashstacs-hk](https://clawhub.ai/user/hashstacs-hk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to create and connect a new Feishu or Lark bot when appId and appSecret have not yet been configured. It guides the agent through checking existing configuration, starting authorization, polling for completion, and saving the resulting bot credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow stores a Feishu or Lark app ID and app secret in the local OpenClaw config, and may create a backup file containing the previous config. <br>
Mitigation: Keep the OpenClaw config and any .bak backup private, restrict local file access, and rotate credentials if either file is exposed. <br>
Risk: The user must approve a returned Feishu or Lark authorization link to create and connect a new bot. <br>
Mitigation: Install only when creating a new Feishu or Lark bot is intended, use the returned verification URL as provided, and stop if the request is unexpected. <br>
Risk: Additional Feishu permissions can expand what the bot can access. <br>
Mitigation: Review the bot's Feishu permissions after setup and enable only the permissions needed for the intended OpenClaw workflows. <br>


## Reference(s): <br>
- [Feishu permissions guide](references/feishu-permissions.md) <br>
- [Troubleshooting guide](references/troubleshooting.md) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>
- [ClawHub skill page](https://clawhub.ai/hashstacs-hk/feishu-quick-setup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and single-line JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may ask the user to open a returned Feishu or Lark verification URL and may save app credentials to the local OpenClaw configuration.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
