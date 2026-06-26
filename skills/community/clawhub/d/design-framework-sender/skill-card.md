## Description: <br>
设计框架自动生成套件的主控路由，监听 Telegram 群消息中的 @mention，并根据当前任务状态路由到对应的子 skill。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[807209066](https://clawhub.ai/user/807209066) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users running a Telegram-based design workflow use this skill as the router for a four-skill design framework suite. It listens for group @mentions, checks task state, and hands work to builder, confirm, or generate companion skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses sensitive credentials and outbound messaging to Telegram and OpenRouter. <br>
Mitigation: Review all companion skills before installation, confirm outbound destinations, and rotate credentials if the scripts have already run on a shared machine. <br>
Risk: Weak scoping or confusing configuration could send messages to the wrong Telegram group or owner. <br>
Mitigation: Replace every Telegram ID and trigger value with intended deployment values and verify the group, owner, and bot targets before enabling the suite. <br>
Risk: Temporary plaintext files may contain credential material during script execution. <br>
Mitigation: Prefer a reviewed version that avoids plaintext secret files in /tmp and clean up temporary files after testing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/807209066/design-framework-sender) <br>
- [OpenRouter chat completions endpoint](https://openrouter.ai/api/v1/chat/completions) <br>
- [Telegram Bot API sendMessage endpoint](https://api.telegram.org/bot{bot_token}/sendMessage) <br>
- [Telegram Bot API sendPhoto endpoint](https://api.telegram.org/bot${BOT_TOKEN}/sendPhoto) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell command examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes Telegram-triggered design requests to companion skills and may send text, images, or status messages through configured Telegram and OpenRouter integrations.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
