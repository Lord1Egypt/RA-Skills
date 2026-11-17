## Description:

Matches Chinese-language conversation context to suitable sticker images and returns them from a remotely updated sticker index.

This skill is ready for commercial/non-commercial use.

## Publisher:

[studyworklife](https://clawhub.ai/user/studyworklife)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to add context-aware stickers to Chinese-language chats based on emotion, keywords, and scenario. It helps an agent select and send an appropriate sticker while relying on configurable frequency and caching behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts a GitHub-hosted sticker repository and keeps a local cache.

Mitigation: Install only in environments where outbound access to that sticker index and local caching are acceptable.

Risk: Automatic sticker selection may send stickers in Chinese-language chat contexts without explicit per-message approval.

Mitigation: Use the configurable send frequency and deploy only where automatic sticker posting is acceptable.

## Reference(s):

- [Crayfish Sticker on ClawHub](https://clawhub.ai/studyworklife/skills/crayfish-sticker)
- [Crayfish Sticker Index](https://raw.githubusercontent.com/StudyWorkLife/crayfish-stickers/main/index.json)

## Skill Output:

**Output Type(s):** [markdown, configuration, guidance]

**Output Format:** [Markdown image links or short chat responses with selected sticker URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use a cached remote sticker index; automatic send frequency is configurable.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
