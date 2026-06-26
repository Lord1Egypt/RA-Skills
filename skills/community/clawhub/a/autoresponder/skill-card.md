## Description: <br>
Monitor iMessage/SMS conversations and auto-respond based on configurable rules, AI prompts, and rate-limiting conditions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Koba42Corp](https://clawhub.ai/user/Koba42Corp) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to configure an agent that monitors selected iMessage/SMS conversations, generates context-aware replies, and manages reply rules, contacts, history, and watcher status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read private iMessage/SMS history and send recent conversation context to AI providers. <br>
Mitigation: Use it only for conversations where automatic AI replies are acceptable, avoid sensitive conversations, and keep contact allowlists narrow. <br>
Risk: The skill can automatically send text messages on the user's behalf. <br>
Mitigation: Use test mode before enabling, configure nonzero delays, keyword triggers, time windows, daily caps, and keep the system toggle available for immediate disablement. <br>
Risk: Plaintext logs and response history may contain message contents or generated replies. <br>
Mitigation: Review log retention and consider disabling, redacting, or tightly protecting plaintext logs. <br>
Risk: Telegram management commands expose an unsafe command-execution path when untrusted input reaches shell command construction. <br>
Mitigation: Avoid running Telegram management commands with untrusted input until the command construction is fixed. <br>


## Reference(s): <br>
- [iResponder ClawHub page](https://clawhub.ai/Koba42Corp/autoresponder) <br>
- [Publisher profile: Koba42Corp](https://clawhub.ai/user/Koba42Corp) <br>
- [imsg CLI](https://imsg.to) <br>
- [OpenAI API keys](https://platform.openai.com/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger local command execution and configuration changes when used by an agent with filesystem and shell access.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
