## Description:

Monitor iMessage/SMS conversations and auto-respond based on configurable rules, AI prompts, and rate-limiting conditions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[koba42corp](https://clawhub.ai/user/koba42corp)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use iResponder to configure macOS Messages auto-replies for selected contacts, prompts, response windows, keyword triggers, rate limits, and status/history review. The skill is intended for managed personal messaging automation where the user accepts the privacy and account-control risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires private Messages access and Terminal Full Disk Access, which can expose message history and local account data.

Mitigation: Install only when those permissions are acceptable, restrict the watch list to contacts intended for automation, and review configuration and logs regularly.

Risk: Selected conversation content may be sent to external AI providers to generate replies.

Mitigation: Avoid enabling the skill for sensitive contacts or conversations, confirm provider configuration before use, and test prompts before sending live responses.

Risk: Automatic replies are sent from the user's account and may produce unwanted, misleading, or excessive messages.

Mitigation: Use rate limits, daily caps, time windows, keyword triggers, response history review, and the global disable toggle to limit or stop automation.

Risk: The security guidance flags the Telegram management interface as sensitive admin access and warns about unsafe command handling and plaintext logging.

Mitigation: Avoid the Telegram management interface until those issues are fixed; prefer local management commands and limit admin access to trusted users.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/koba42corp/skills/autoresponder)
- [iMessage CLI](https://imsg.to)
- [OpenAI API Keys](https://platform.openai.com/api-keys)
- [macOS](https://www.apple.com/macos/)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include contact-specific status, response history, test response previews, and local management command results.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
