## Description: <br>
Custom Telegram Bot helps agents use an AgentPMT-hosted integration to send and receive Telegram messages, media, and updates through a user-owned custom bot token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and business automation teams use this skill to connect their own Telegram bot to AgentPMT for branded support, business notifications, inbound customer replies, media sharing, and update polling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram messages and attachments may pass through AgentPMT and Telegram. <br>
Mitigation: Install only when this routing is acceptable, keep tool inputs scoped to the minimum needed, and avoid sending secrets or sensitive payment material in prompts or logs. <br>
Risk: Optional attachment ingestion can persist copies of inbound Telegram media in AgentPMT File Manager. <br>
Mitigation: Enable attachment ingestion only for files the user is allowed to store, and set expiration and maximum-file parameters deliberately. <br>
Risk: Mark-as-read behavior can change which updates later polling treats as unread. <br>
Mitigation: Review unread_only, cursor_offset, offset, and mark_as_read settings before polling workflows that depend on unread state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/custom-telegram-bot) <br>
- [AgentPMT marketplace product](https://www.agentpmt.com/marketplace/custom-telegram-bot) <br>
- [Generated action schema](schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration instructions, JSON] <br>
**Output Format:** [Markdown with JSON code blocks and action parameter summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Covers five AgentPMT remote actions: get_updates, list_known_chat_ids, send_document, send_message, and send_photo.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
