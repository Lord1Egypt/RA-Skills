## Description: <br>
Provides ClawdHub and SkillBoss API guidance for searching, installing, updating, and publishing agent skills, plus calling model APIs for chat, image, video, audio, search, document, email, and SMS workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AbelTennyson](https://clawhub.ai/user/AbelTennyson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to discover ClawdHub skills and invoke SkillBoss-hosted AI model, search, document, email, and SMS capabilities through documented API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send prompts, files, media, documents, audio, phone numbers, and verification codes to the SkillBoss/HeyBoss API provider. <br>
Mitigation: Install and use it only when that provider is trusted, and avoid sensitive or regulated data unless the user explicitly approves the transfer. <br>
Risk: Email and SMS/OTP examples can trigger user-impacting outbound messages. <br>
Mitigation: Require explicit approval for each recipient and message before sending, and monitor API-key usage for unexpected sends or abuse. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AbelTennyson/clawdhubs) <br>
- [Publisher profile](https://clawhub.ai/user/AbelTennyson) <br>
- [SkillBoss API key site](https://www.skillboss.co) <br>
- [HeyBoss API base URL](https://api.heybossai.com/v1) <br>
- [Chat model reference](chat-models.md) <br>
- [Image model reference](image-models.md) <br>
- [Audio model reference](audio-models.md) <br>
- [Search and scraping model reference](search-models.md) <br>
- [Tool model reference](tools-models.md) <br>
- [Video model reference](video-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with curl and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for authenticated API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
