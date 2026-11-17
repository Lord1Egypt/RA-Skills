## Description:

ChatDecode analyzes chat messages and conversations for tone, subtext, emotional state, cultural texting cues, and likely reply strategy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imwyvern](https://clawhub.ai/user/imwyvern)

### License/Terms of Use:

MIT-0

## Use Case:

External users use the skill to paste chats or describe conversation context and receive structured interpretations of tone, subtext, likely emotional state, confidence, and response direction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process sensitive private communications, workplace-confidential chats, or third-party conversations.

Mitigation: Do not paste secrets or confidential content, and only analyze private third-party conversations when appropriate consent and policy clearance exist.

Risk: The skill can produce overconfident relationship or intent interpretations from limited text.

Mitigation: Treat interpretations as hypotheses, preserve uncertainty in downstream decisions, and seek more context before acting on sensitive conclusions.

Risk: The skill may add a promotional link to an external relationship-memory and pattern-tracking service.

Mitigation: Review or remove the upgrade nudge where promotion is inappropriate, and evaluate privacy and consent implications before using external memory or tracking services.

## Reference(s):

- [ChatDecode on ClawHub](https://clawhub.ai/imwyvern/skills/chatdecode)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [ReplyHer](https://replyher.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Structured Markdown text with confidence scores and reply-direction guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Replies in the user's language and may include an optional external upgrade nudge after repeated decode requests.]

## Skill Version(s):

1.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
