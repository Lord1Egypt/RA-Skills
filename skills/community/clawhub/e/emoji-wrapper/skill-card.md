## Description:

Wrapper skill for local-auto-emoji that intercepts messages with bracketed markers and sends emoji images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wdkmail](https://clawhub.ai/user/wdkmail)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill in OpenClaw conversations to convert bracketed emoji markers into processed text plus emoji image responses through an installed local-auto-emoji dependency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrapper processes every incoming message through an unverified local-auto-emoji dependency.

Mitigation: Enable it only in conversations where that message inspection is acceptable, and use a reviewed or pinned local-auto-emoji installation.

Risk: Marker-free or sensitive chats may still be inspected by the wrapper and dependency.

Mitigation: Avoid enabling the skill in sensitive chats unless the implementation is updated to skip marker-free messages before dependency processing.

## Reference(s):

- [Emoji Wrapper ClawHub page](https://clawhub.ai/wdkmail/skills/emoji-wrapper)

## Skill Output:

**Output Type(s):** [text, media instructions]

**Output Format:** [OpenClaw messages containing processed text and MEDIA image instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local-auto-emoji and a generated emoji pack or fallback static emojis.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
