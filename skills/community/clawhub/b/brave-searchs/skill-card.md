## Description:

Provides API guidance for SkillBoss/HeyBossAI access to web search, content extraction, and multimodal model services across chat, image, video, audio, documents, email, and SMS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to call SkillBoss/HeyBossAI APIs for web search, scraping, smart model routing, media generation, transcription, document processing, email, and SMS workflows with one API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package is labeled as Brave Search but describes a broad multimodel service with document, media, email, and SMS capabilities.

Mitigation: Install only when the intended use includes broad SkillBoss/HeyBossAI access, and review the enabled workflows before deployment.

Risk: The API key may authorize processing of prompts, files, audio, media URLs, recipients, and phone numbers through third-party services.

Mitigation: Use separate scoped credentials where available and require explicit user confirmation before sending email, SMS, OTP requests, or sensitive documents and media.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/alvisdunlop/skills/brave-searchs)
- [SkillBoss](https://www.skillboss.co)
- [HeyBossAI API base](https://api.heybossai.com/v1)
- [HeyBossAI models endpoint](https://api.heybossai.com/v1/models)
- [Audio Models](audio-models.md)
- [Chat Models](chat-models.md)
- [Image Models](image-models.md)
- [Search & Scraping Models](search-models.md)
- [Tool Models](tools-models.md)
- [Video Models](video-models.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash examples and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; examples call HeyBossAI/SkillBoss APIs and may route data to downstream model and messaging providers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
