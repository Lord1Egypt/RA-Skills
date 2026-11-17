## Description:

Pub Gemini helps agents call SkillBoss/HeyBossAI models for Q&A, summarization, content generation, media generation, transcription, web search, document parsing, email, and SMS tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[martinpollitt](https://clawhub.ai/user/martinpollitt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to route prompts and task inputs through SkillBoss/HeyBossAI models for text, image, video, audio, search, document, email, and SMS workflows. It is suited to workflows where the user has approved use of the SkillBoss API key and any downstream provider processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task content, documents, media, and prompts may be sent to SkillBoss/HeyBossAI and downstream model or tool providers.

Mitigation: Require user approval before sending sensitive data, documents, media, or secrets, and disclose that third-party processing may occur.

Risk: Email, SMS, and OTP actions can contact external recipients or phone numbers.

Mitigation: Ask the user to confirm recipients, phone numbers, message bodies, and OTP intent before making API calls that send or verify communications.

Risk: API responses may return download URLs for generated media or parsed documents.

Mitigation: Validate returned URLs and expected content types before fetching or saving files.

Risk: Search, scraping, and document parsing tasks may process private URLs or restricted documents.

Mitigation: Confirm authorization to access the target URL or document and avoid submitting confidential material unless explicitly approved.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/martinpollitt/skills/geminis)
- [SkillBoss website](https://www.skillboss.co)
- [SkillBoss API base](https://api.heybossai.com/v1)
- [SkillBoss models endpoint](https://api.heybossai.com/v1/models)
- [Chat models](artifact/chat-models.md)
- [Image models](artifact/image-models.md)
- [Video models](artifact/video-models.md)
- [Audio models](artifact/audio-models.md)
- [Search and scraping models](artifact/search-models.md)
- [Tool models](artifact/tools-models.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, files, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API payloads; API responses may include text, JSON, URLs, media files, or generated documents.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends task content to SkillBoss/HeyBossAI and potentially downstream providers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
