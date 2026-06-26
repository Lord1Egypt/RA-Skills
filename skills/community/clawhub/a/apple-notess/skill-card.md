## Description: <br>
Manage Apple Notes via the memo CLI on macOS and generate guidance for SkillBoss API calls across AI, search, document, email, and SMS workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MartinPollitt](https://clawhub.ai/user/MartinPollitt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to generate shell commands and API call guidance for Apple Notes-related workflows and SkillBoss-hosted AI, search, document, email, and SMS capabilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is labeled for Apple Notes, but server security evidence says its files mainly document a broad remote SkillBoss AI/API gateway with search, email, and SMS capabilities. <br>
Mitigation: Install only when that broad gateway behavior is intended, and review the enabled scope before use. <br>
Risk: Private notes, files, audio, images, or documents may be sent to third-party processing services through SkillBoss API calls. <br>
Mitigation: Avoid sending sensitive content unless third-party processing is acceptable, and use a restricted API key when available. <br>
Risk: Email, SMS, OTP, batch messaging, upload, and document-processing actions can affect external recipients or expose data. <br>
Mitigation: Require explicit human approval before those actions and verify recipients, payloads, and uploaded content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MartinPollitt/apple-notess) <br>
- [SkillBoss](https://www.skillboss.co) <br>
- [SkillBoss API base URL](https://api.heybossai.com/v1) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Chat Models](artifact/chat-models.md) <br>
- [Image Models](artifact/image-models.md) <br>
- [Video Models](artifact/video-models.md) <br>
- [Audio Models](artifact/audio-models.md) <br>
- [Search & Scraping Models](artifact/search-models.md) <br>
- [Tool Models](artifact/tools-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for authenticated SkillBoss API calls] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
