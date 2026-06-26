## Description: <br>
Creates a Feishu enterprise self-built bot and completes permission import, event subscriptions, card callbacks, version creation, and release submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[big-dust](https://clawhub.ai/user/big-dust) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create Feishu enterprise self-built bots, configure permissions, event subscriptions, card callbacks, QR login handoff, version release, and return app credentials after setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad Feishu permissions. <br>
Mitigation: Review the permission list before use and reduce requested scopes to the minimum needed for the bot. <br>
Risk: The create flow returns app_secret in ordinary agent output. <br>
Mitigation: Treat app_secret like a password, avoid logging or reposting it, and rotate it if exposed in chat or logs. <br>
Risk: Setup can modify the local runtime by installing or using browser automation dependencies. <br>
Mitigation: Run in an isolated machine or container and preinstall trusted dependencies where possible. <br>
Risk: The workflow can create and submit a Feishu app release. <br>
Mitigation: Confirm the intended publication impact and account permissions before running the create command. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/big-dust/feishu-bot-full-setup) <br>
- [Publisher profile](https://clawhub.ai/user/big-dust) <br>
- [Default permissions list](artifact/references/permissions.md) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with bash commands, environment variables, local QR PNG handling, and JSON result parsing] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The create flow returns app_id and app_secret when successful; the login QR code is written as a local PNG.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
