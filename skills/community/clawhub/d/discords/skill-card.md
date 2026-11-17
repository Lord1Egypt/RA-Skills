## Description:

Control Discord from Clawdbot and access SkillBoss models for chat, media generation, transcription, search, document processing, email, and SMS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godferylindsay](https://clawhub.ai/user/godferylindsay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Clawdbot users use this skill to operate Discord workflows and call SkillBoss-hosted AI models through documented API examples. It supports message actions, reactions, stickers, emojis, media generation, speech, search, document processing, email, and SMS tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is packaged as a Discord skill but exposes broad SkillBoss API actions including email, SMS, document processing, and model calls.

Mitigation: Review it as a broad external API integration before installation, not as a Discord-only skill.

Risk: Prompts, media, document URLs, search queries, email contents, and phone numbers may be sent to SkillBoss and possibly downstream providers.

Mitigation: Only provide SKILLBOSS_API_KEY and run examples when those data transfers are acceptable for the intended use.

Risk: The artifact includes run.mjs examples whose executable resolution may be unclear in a local environment.

Mitigation: Verify exactly which executable will run before using run.mjs examples.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/godferylindsay/skills/discords)
- [SkillBoss website](https://www.skillboss.co)
- [SkillBoss API base URL](https://api.heybossai.com/v1)
- [Audio models](artifact/audio-models.md)
- [Chat models](artifact/chat-models.md)
- [Image models](artifact/image-models.md)
- [Search and scraping models](artifact/search-models.md)
- [Tool models](artifact/tools-models.md)
- [Video models](artifact/video-models.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and may send prompts, media, document URLs, search queries, email contents, and phone numbers to SkillBoss or downstream providers.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
