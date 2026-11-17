## Description:

Clawdbot documentation expert with decision tree navigation, search, and doc fetching, plus instructions for accessing 50+ SkillBoss models for image generation, video generation, text-to-speech, speech-to-text, music, chat, web search, document parsing, email, and SMS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[martinpollitt](https://clawhub.ai/user/martinpollitt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up SkillBoss model documentation, choose model categories, and produce authenticated API examples for chat, media generation, search, document processing, email, SMS, and related tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A documentation-branded skill includes broad authenticated API instructions for model execution, email, SMS, document uploads, media uploads, and file downloads.

Mitigation: Use a limited SKILLBOSS_API_KEY and require explicit user approval before email, SMS, upload, or download commands are run.

Risk: Prompts or files sent through the documented APIs could expose secrets, private documents, media, or audio.

Mitigation: Avoid sending secrets or private documents, media, or audio unless the user has confirmed the data handling requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/martinpollitt/skills/clawddocss)
- [SkillBoss](https://www.skillboss.co)
- [SkillBoss API base](https://api.heybossai.com/v1)
- [Audio Models](artifact/audio-models.md)
- [Chat Models](artifact/chat-models.md)
- [Image Models](artifact/image-models.md)
- [Search & Scraping Models](artifact/search-models.md)
- [Tool Models](artifact/tools-models.md)
- [Video Models](artifact/video-models.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and API parameter guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include authenticated API examples that depend on SKILLBOSS_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
