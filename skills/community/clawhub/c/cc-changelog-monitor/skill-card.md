## Description: <br>
Monitors Claude Code releases and sends Telegram alerts when new versions ship, using bash monitoring without AI credits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[assistant-design](https://clawhub.ai/user/assistant-design) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators who rely on Claude Code use this skill to check npm for new Claude Code releases and send Telegram alerts with version and change-summary details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The monitor can send Telegram messages to a built-in bot/chat destination before the user configures their own credentials. <br>
Mitigation: Remove hardcoded Telegram defaults, require TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID from the user, and confirm the destination before enabling alerts. <br>
Risk: The setup script runs the monitor during setup, which can trigger network calls and alerts before review. <br>
Mitigation: Review the scripts first, avoid running setup until credentials and destinations are confirmed, and enable the cron job only after a successful manual test. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/assistant-design/cc-changelog-monitor) <br>
- [npm package: @anthropic-ai/claude-code](https://www.npmjs.com/package/@anthropic-ai/claude-code) <br>
- [npm registry latest metadata](https://registry.npmjs.org/@anthropic-ai/claude-code/latest) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Telegram BotFather](https://t.me/BotFather) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and shell-script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runtime monitoring writes local version/configuration files and can send Telegram API messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
