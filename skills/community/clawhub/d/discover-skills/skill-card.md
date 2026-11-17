## Description:

Helps users discover and install agent skills and access SkillBoss APIs for 50+ AI models across chat, media generation, search, document processing, email, and SMS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quincygunter](https://clawhub.ai/user/quincygunter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to discover and install agent skills by natural-language request, then use SkillBoss API guidance for model discovery, smart routing, and multimodal tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, files, audio, document URLs, phone numbers, email content, and generated outputs may be sent to a third-party service and downstream providers.

Mitigation: Use only after reviewing the provider's terms and controls; avoid confidential or regulated data unless approved for this service.

Risk: The release is packaged as a skill finder but includes broad remote API broker capabilities such as email, SMS, document parsing, audio, and media generation.

Mitigation: Install only when those broad remote API capabilities are intended, scope credentials appropriately, and review generated commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/quincygunter/skills/discover-skills)
- [Publisher profile](https://clawhub.ai/user/quincygunter)
- [SkillBoss website](https://www.skillboss.co)
- [SkillBoss API base](https://api.heybossai.com/v1)
- [Audio models](artifact/audio-models.md)
- [Chat models](artifact/chat-models.md)
- [Image models](artifact/image-models.md)
- [Search and scraping models](artifact/search-models.md)
- [Tool models](artifact/tools-models.md)
- [Video models](artifact/video-models.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline curl commands, API parameters, and model reference tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for authenticated remote API use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
