## Description: <br>
Beeper integration for Clawdbot. Send messages and search chats across WhatsApp, Telegram, Signal, Discord, Slack, Instagram, iMessage, LinkedIn, Facebook Messenger, Google Messages via Beeper Desktop API. Reactions, reminders, attachments, mark as read. Unified multi-platform messaging automation-just ask. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nickhamze](https://clawhub.ai/user/nickhamze) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Clawdbot users use this skill to search, summarize, and act on conversations across Beeper-connected messaging networks. It supports message sending, unread review, reactions, reminders, attachments, and read-state updates through the local Beeper Desktop API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and act on messages across connected Beeper chat accounts. <br>
Mitigation: Install only if you are comfortable granting that access, and scope requests to specific chats or time ranges when possible. <br>
Risk: The skill can send messages or change chat state, including reactions, reminders, and read status. <br>
Mitigation: Confirm the recipient, service, message text, and intended state change before sending or modifying chats. <br>
Risk: BEEPER_ACCESS_TOKEN can authorize access to the local Beeper Desktop API. <br>
Mitigation: Treat the token like a password and store it only in local Clawdbot configuration. <br>


## Reference(s): <br>
- [Beeper](https://www.beeper.com) <br>
- [Beeper Developer Docs](https://developers.beeper.com) <br>
- [Beeper Desktop API Reference](https://developers.beeper.com/desktop-api-reference/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with curl commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Beeper Desktop with the Desktop API enabled; BEEPER_ACCESS_TOKEN is optional but should be protected when used.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata; artifact frontmatter says 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
