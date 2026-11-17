## Description:

Custom Telegram Bot enables agents to send and receive Telegram messages, photos, and documents through a user-owned bot token via AgentPMT-hosted tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect an agent to a branded Telegram bot for customer support, business notifications, inbound replies, media sharing, and conversational workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telegram bot messages, media, update metadata, and optional ingested files may be routed through Telegram and AgentPMT.

Mitigation: Use only data approved by policy, avoid secrets or regulated data unless permitted, and keep tool inputs limited to the minimum needed for the task.

Risk: Related setup examples include unpinned npx install commands.

Mitigation: Prefer pinned or official install commands and confirm live schemas before production integrations.

## Reference(s):

- [Custom Telegram Bot on ClawHub](https://clawhub.ai/agentpmt/skills/custom-telegram-bot)
- [AgentPMT Custom Telegram Bot Marketplace Page](https://www.agentpmt.com/marketplace/custom-telegram-bot)
- [Custom Telegram Bot Schema](artifact/schema.md)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, API calls, JSON]

**Output Format:** [Markdown instructions with JSON request examples and action schemas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Describes five AgentPMT actions: get_updates, list_known_chat_ids, send_document, send_message, and send_photo.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
