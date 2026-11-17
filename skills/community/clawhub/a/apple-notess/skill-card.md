## Description:

Manage Apple Notes via the memo CLI on macOS and access 50+ SkillBoss-hosted models for image generation, video generation, text-to-speech, speech-to-text, music, chat, web search, document parsing, email, and SMS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[martinpollitt](https://clawhub.ai/user/martinpollitt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for SkillBoss API commands, model selection guidance, and configuration help across chat, media generation, search, document, email, and SMS workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill name and display text may lead users to expect a local Apple Notes helper, while the security evidence describes a broad external SkillBoss API wrapper.

Mitigation: Review the package before installing and use it only when broad SkillBoss API access is intended.

Risk: The skill can guide agents to send private notes, documents, recordings, contact details, OTP codes, emails, or SMS content to third-party services.

Mitigation: Avoid submitting sensitive content unless the user has approved third-party processing and account usage through SKILLBOSS_API_KEY.

Risk: Commands may consume account quota or trigger external actions such as email or SMS sending.

Mitigation: Inspect generated commands and payloads before execution, especially for email, SMS, document, media, and model-routing actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/martinpollitt/skills/apple-notess)
- [Publisher Profile](https://clawhub.ai/user/martinpollitt)
- [SkillBoss API Base](https://api.heybossai.com/v1)
- [SkillBoss Models Endpoint](https://api.heybossai.com/v1/models)
- [SkillBoss Site](https://www.skillboss.co)
- [Audio Models](artifact/audio-models.md)
- [Chat Models](artifact/chat-models.md)
- [Image Models](artifact/image-models.md)
- [Search and Scraping Models](artifact/search-models.md)
- [Tool Models](artifact/tools-models.md)
- [Video Models](artifact/video-models.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, curl examples, JSON payloads, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that call external SkillBoss API endpoints with SKILLBOSS_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release evidence, created 2026-03-12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
