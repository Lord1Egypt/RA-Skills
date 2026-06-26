## Description: <br>
为 OpenClaw 配置 MiniMax 作为模型源，覆盖 API Key 直连和 OAuth 门户两种接入方式，并提供 provider 注册、模型定义、别名、fallback 链接入和验证流程。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jooey](https://clawhub.ai/user/jooey) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw administrators use this skill to add MiniMax models as OpenClaw providers, test API availability, configure aliases and fallback behavior, and validate the gateway after configuration changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configuration changes may expose or misuse MiniMax API keys if pasted into chats, logs, or shared files. <br>
Mitigation: Review the proposed ~/.openclaw/openclaw.json changes before installing, keep a backup, use a dedicated MiniMax API key where possible, and avoid sharing keys in chats or logs. <br>
Risk: Prompts routed through MiniMax may be subject to MiniMax billing, quota, and privacy terms. <br>
Mitigation: Confirm MiniMax billing and privacy terms are acceptable before routing prompts through this provider. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jooey/add-minimax-provider) <br>
- [MiniMax platform](https://platform.minimaxi.com) <br>
- [MiniMax chat completions API endpoint](https://api.minimaxi.com/v1/chat/completions) <br>
- [MiniMax provider source repository](https://github.com/jooey/openclaw-skill-add-minimax-provider) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, Code] <br>
**Output Format:** [Markdown with JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes OpenClaw provider snippets, API test commands, alias and fallback examples, and validation steps.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
