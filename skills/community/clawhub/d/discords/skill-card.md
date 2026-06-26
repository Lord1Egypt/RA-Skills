## Description: <br>
Control Discord from Clawdbot and access SkillBoss models for chat, image, video, audio, search, document processing, email, and SMS tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GodferyLindsay](https://clawhub.ai/user/GodferyLindsay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Clawdbot users use this skill to call SkillBoss APIs for Discord-oriented actions and broad multimodal model workflows. It requires a SkillBoss API key and includes examples for model discovery, generation, transcription, search, document parsing, email, and SMS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is labeled as a Discord skill, but the evidence describes a broad SkillBoss API wrapper that can send user data to third-party services. <br>
Mitigation: Install only when broad SkillBoss API access is intended, and review planned requests before sending private files, audio, documents, or prompts. <br>
Risk: The skill can trigger email, SMS, and OTP-related actions. <br>
Mitigation: Require explicit approval before email, SMS, or OTP actions and use a limited SkillBoss API key. <br>
Risk: The skill requires an API key with access to external model and tool providers. <br>
Mitigation: Store SKILLBOSS_API_KEY securely, scope or rotate it where possible, and avoid exposing it in logs or generated command output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/GodferyLindsay/discords) <br>
- [SkillBoss website](https://www.skillboss.co) <br>
- [SkillBoss API base URL](https://api.heybossai.com/v1) <br>
- [SkillBoss model discovery endpoint](https://api.heybossai.com/v1/models) <br>
- [Audio Models](audio-models.md) <br>
- [Chat Models](chat-models.md) <br>
- [Image Models](image-models.md) <br>
- [Search & Scraping Models](search-models.md) <br>
- [Tool Models](tools-models.md) <br>
- [Video Models](video-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl examples and API request patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; responses may include generated text, media URLs, parsed documents, search results, email actions, or SMS actions depending on the selected SkillBoss model.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
