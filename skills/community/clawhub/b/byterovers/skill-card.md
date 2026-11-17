## Description:

Pub Byterover helps agents store and retrieve project context and access SkillBoss models for generation, transcription, search, document processing, email, and SMS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to preserve project context and call external AI models through the SkillBoss API for chat, media generation, search, document processing, messaging, and related automation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted prompts, files, URLs, audio, contact details, and generated outputs are sent to SkillBoss/HeyBossAI and downstream model providers.

Mitigation: Use the skill only when the destination service is trusted, and avoid sending secrets or regulated data unless approved.

Risk: The skill can trigger email and SMS actions that affect external recipients.

Mitigation: Require explicit user confirmation before invoking email or SMS workflows.

Risk: The example run.mjs commands depend on whatever executable is present in the runtime environment.

Mitigation: Confirm the intended executable and command arguments before running run.mjs examples.

Risk: Branding and scope are inconsistent across Byterover, SkillBoss, and HeyBossAI references.

Mitigation: Confirm the service identity, endpoint, and data-handling expectations before installation or use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alvisdunlop/skills/byterovers)
- [Publisher Profile](https://clawhub.ai/user/alvisdunlop)
- [SkillBoss Website](https://www.skillboss.co)
- [SkillBoss API Base](https://api.heybossai.com/v1)
- [Chat Models](artifact/chat-models.md)
- [Image Models](artifact/image-models.md)
- [Video Models](artifact/video-models.md)
- [Audio Models](artifact/audio-models.md)
- [Search and Scraping Models](artifact/search-models.md)
- [Tool Models](artifact/tools-models.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for authenticated API calls.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
