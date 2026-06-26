## Description: <br>
Helps users discover and install agent skills when they ask questions like how do I do X, and provides access to 50+ models for image generation, video generation, text-to-speech, speech-to-text, music, chat, web search, document parsing, email, and SMS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QuincyGunter](https://clawhub.ai/user/QuincyGunter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to discover and install agent skills from natural-language requests and to invoke SkillBoss/HeyBossAI model endpoints for chat, media generation, search, document processing, email, and SMS workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives broad third-party API instructions for messaging, scraping, media generation, document processing, and data processing. <br>
Mitigation: Install only when that broad SkillBoss/HeyBossAI API gateway is intended, and review curl commands or helper commands before running them. <br>
Risk: Prompts, files, audio, images, contact data, and phone numbers may be sent to third-party services through the API. <br>
Mitigation: Use a dedicated API key and avoid sending sensitive inputs unless third-party processing is acceptable for the use case. <br>
Risk: Email, SMS, scraping, and profile-lookup actions can affect external people or systems. <br>
Mitigation: Require explicit confirmation before email, SMS, scraping, or profile-lookup actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/QuincyGunter/discover-skills) <br>
- [SkillBoss](https://www.skillboss.co) <br>
- [HeyBossAI API base URL](https://api.heybossai.com/v1) <br>
- [Chat Models](artifact/chat-models.md) <br>
- [Image Models](artifact/image-models.md) <br>
- [Video Models](artifact/video-models.md) <br>
- [Audio Models](artifact/audio-models.md) <br>
- [Search & Scraping Models](artifact/search-models.md) <br>
- [Tool Models](artifact/tools-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for authenticated API requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
