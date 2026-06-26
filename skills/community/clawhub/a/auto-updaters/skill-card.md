## Description: <br>
Provides Clawdbot guidance for daily skill updates and SkillBoss API access across chat, image, video, audio, search, document, email, and SMS capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AbelTennyson](https://clawhub.ai/user/AbelTennyson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Clawdbot users can use this skill to configure a SkillBoss API key, discover available models, and generate API request examples for model, media, search, document, email, SMS, and updater-like workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill presents itself as an auto-updater while also enabling broad third-party API gateway behavior. <br>
Mitigation: Install only when broad SkillBoss access is intended, and review requested actions before allowing model calls or updater-like changes. <br>
Risk: The required SkillBoss API key may authorize paid calls or access to multiple third-party providers. <br>
Mitigation: Use a restricted, revocable API key and monitor billing, provider terms, and usage logs. <br>
Risk: Email, SMS, document, media, and search workflows can send sensitive content to external services. <br>
Mitigation: Require explicit approval before email, SMS, paid model calls, or processing sensitive content through third-party providers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AbelTennyson/auto-updaters) <br>
- [SkillBoss API](https://api.heybossai.com/v1) <br>
- [SkillBoss API key](https://www.skillboss.co) <br>
- [Chat Models](chat-models.md) <br>
- [Image Models](image-models.md) <br>
- [Video Models](video-models.md) <br>
- [Audio Models](audio-models.md) <br>
- [Search & Scraping Models](search-models.md) <br>
- [Tool Models](tools-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl examples, parameter tables, model IDs, and setup notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for API examples and live model access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
