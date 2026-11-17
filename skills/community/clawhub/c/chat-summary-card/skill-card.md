## Description:

An AI-powered tool that turns conversations into polished, structured summary cards by extracting key ideas, action items, and next steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuminliu026](https://clawhub.ai/user/shuminliu026)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to convert chat conversations into concise visual recap cards with key ideas, decisions, and next steps. It is intended for conversation summarization workflows where an image card is preferred over a plain-text summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide a mew.design API key in chat.

Mitigation: Use a short-lived or low-scope key where possible, avoid retaining the key beyond the active conversation, and rotate it if exposure is suspected.

Risk: Chat-derived content is sent to an external Mew API for image generation.

Mitigation: Avoid using the skill with confidential, regulated, or sensitive conversations unless external processing is approved.

Risk: Changing the validation or generation base URL away from api.mew.design could send credentials or content to an unintended service.

Mitigation: Review commands before execution and keep API validation and generation endpoints on the expected Mew domain unless the user explicitly authorizes a change.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shuminliu026/skills/chat-summary-card)
- [Chat Summary Image Patterns](references/patterns.md)
- [Mew API Key Setup](https://mew.design/login)
- [Mew Design Generation API](https://api.mew.design/open/api/design/generate)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown image link with a one-sentence summary, plus command guidance for key validation and image generation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a conversation-derived visual summary card through the Mew design API after API key validation.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
