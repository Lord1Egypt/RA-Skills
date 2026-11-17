## Description:

Provides agent guidance for using the SkillBoss API gateway across chat, media generation, search, scraping, document processing, email, SMS, and related model and tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to draft SkillBoss API requests, shell commands, and request payloads for model and tool tasks. It should not be relied on for CalDAV calendar sync without separate implementation evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CalDAV label can lead users to install the skill for calendar sync even though the artifact instructions describe a broad SkillBoss API gateway.

Mitigation: Review it as a SkillBoss gateway and do not use it for CalDAV calendar sync unless separate calendar-specific implementation evidence is provided.

Risk: API calls may send selected content to SkillBoss and can involve email, SMS, document processing, search, scraping, media generation, and paid model usage.

Mitigation: Review each proposed call before execution, limit sensitive inputs, and verify API key permissions, spending controls, and allowed actions before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tobeyrebecca/skills/caldav-calendars)
- [SkillBoss](https://www.skillboss.co)
- [SkillBoss API Base](https://api.heybossai.com/v1)
- [Chat Models](artifact/chat-models.md)
- [Image Models](artifact/image-models.md)
- [Video Models](artifact/video-models.md)
- [Audio Models](artifact/audio-models.md)
- [Search and Scraping Models](artifact/search-models.md)
- [Tool Models](artifact/tools-models.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, API request guidance]

**Output Format:** [Markdown with inline bash commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for live API calls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
