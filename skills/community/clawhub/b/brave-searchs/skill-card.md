## Description: <br>
Provides agent guidance for using a SkillBoss/HeyBossAI API gateway for web search, scraping, chat, image, video, audio, document, email, SMS, embedding, and presentation tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AlvisDunlop](https://clawhub.ai/user/AlvisDunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to choose SkillBoss/HeyBossAI models and compose API calls for search, content extraction, generation, and communication workflows. Users should treat it as a broad multi-provider gateway rather than a narrow Brave Search-only tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is presented as Brave Search but provides broad SkillBoss/HeyBossAI access, including email and SMS actions. <br>
Mitigation: Install only when a broad multi-provider gateway is intended, and require explicit user approval before any email or SMS action. <br>
Risk: API use may expose prompts, documents, audio, images, phone numbers, email content, or other sensitive data to external providers. <br>
Mitigation: Avoid submitting sensitive data unless provider terms are acceptable for the use case. <br>
Risk: A single API key can enable many provider-backed operations and may create unexpected spend or access exposure. <br>
Mitigation: Use a limited or spend-capped SKILLBOSS_API_KEY where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AlvisDunlop/brave-searchs) <br>
- [Publisher profile](https://clawhub.ai/user/AlvisDunlop) <br>
- [SkillBoss](https://www.skillboss.co) <br>
- [Audio Models](artifact/audio-models.md) <br>
- [Chat Models](artifact/chat-models.md) <br>
- [Image Models](artifact/image-models.md) <br>
- [Search & Scraping Models](artifact/search-models.md) <br>
- [Tool Models](artifact/tools-models.md) <br>
- [Video Models](artifact/video-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a SKILLBOSS_API_KEY environment variable for API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
