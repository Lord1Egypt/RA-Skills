## Description: <br>
API-first email platform designed for AI agents to create and manage dedicated email inboxes, with access to models for image generation, video generation, text-to-speech, speech-to-text, music, chat, web search, document parsing, email, and SMS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MartinPollitt](https://clawhub.ai/user/MartinPollitt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to guide agents in calling the SkillBoss/heybossai API for model discovery, multimodal generation, search, document processing, email, SMS, and smart model routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to call a third-party API gateway with a live API key. <br>
Mitigation: Use a constrained SKILLBOSS_API_KEY where available, monitor usage and billing, and install only when third-party SkillBoss/heybossai API access is intended. <br>
Risk: Email, SMS, OTP, batch messaging, and generation jobs can create external side effects or costs. <br>
Mitigation: Require explicit approval before sending email, SMS, OTPs, batch messages, or costly generation jobs. <br>
Risk: Prompts, documents, media, contact details, or other inputs may be sent to a third-party provider. <br>
Mitigation: Avoid sending secrets or regulated data unless the provider's data handling is acceptable for the deployment. <br>


## Reference(s): <br>
- [ClawHub listing for Pub Agentmail](https://clawhub.ai/MartinPollitt/agentmails) <br>
- [Publisher profile](https://clawhub.ai/user/MartinPollitt) <br>
- [SkillBoss website](https://www.skillboss.co) <br>
- [SkillBoss API base URL](https://api.heybossai.com/v1) <br>
- [Audio Models](artifact/audio-models.md) <br>
- [Chat Models](artifact/chat-models.md) <br>
- [Image Models](artifact/image-models.md) <br>
- [Search & Scraping Models](artifact/search-models.md) <br>
- [Tool Models](artifact/tools-models.md) <br>
- [Video Models](artifact/video-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash and curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a SKILLBOSS_API_KEY environment variable for API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
