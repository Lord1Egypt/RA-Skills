## Description: <br>
Clawdbot documentation expert with decision tree navigation, search, and doc fetching. And also 50+ models for image generation, video generation, text-to-speech, speech-to-text, music, chat, web search, document parsing, email, and SMS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MartinPollitt](https://clawhub.ai/user/MartinPollitt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to find Clawdbot and SkillBoss model documentation, list available model categories, and prepare API calls for chat, image, video, audio, search, document, email, and SMS workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward broad external-service use through a SkillBoss API key. <br>
Mitigation: Use a dedicated or restricted API key where available and confirm that prompts, documents, audio, images, URLs, phone numbers, and email content may be sent to external services. <br>
Risk: Email, SMS, OTP, and batch messaging capabilities can affect third parties. <br>
Mitigation: Require explicit user confirmation before any email, SMS, OTP, or batch messaging action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MartinPollitt/clawddocss) <br>
- [Publisher profile](https://clawhub.ai/user/MartinPollitt) <br>
- [SkillBoss website](https://www.skillboss.co) <br>
- [SkillBoss API base URL](https://api.heybossai.com/v1) <br>
- [artifact/SKILL.md](artifact/SKILL.md) <br>
- [artifact/chat-models.md](artifact/chat-models.md) <br>
- [artifact/image-models.md](artifact/image-models.md) <br>
- [artifact/audio-models.md](artifact/audio-models.md) <br>
- [artifact/video-models.md](artifact/video-models.md) <br>
- [artifact/search-models.md](artifact/search-models.md) <br>
- [artifact/tools-models.md](artifact/tools-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for authenticated SkillBoss API access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
