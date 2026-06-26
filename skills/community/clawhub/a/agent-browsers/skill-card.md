## Description: <br>
Guides agents in using SkillBoss commands for browser-style automation plus chat, media generation, search, scraping, document processing, email, SMS, and smart model routing through a single API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QuincyGunter](https://clawhub.ai/user/QuincyGunter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let agents discover and invoke SkillBoss model and utility endpoints for content generation, search and scraping, document parsing, messaging, and smart model routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A single SkillBoss API key can enable broad remote actions, including model calls, scraping, document processing, email, SMS/OTP, and billing-impacting requests. <br>
Mitigation: Use a limited or separate API key where possible, monitor usage and billing, and require explicit approval before messaging, OTP, scraping, document-processing, or batch actions. <br>
Risk: Sensitive documents, media, prompts, recipient data, or phone numbers may be processed by third-party services. <br>
Mitigation: Avoid sensitive inputs unless third-party processing is acceptable and authorized; review data handling requirements before use. <br>
Risk: The skill is presented as browser automation while the security evidence describes broader API gateway capabilities. <br>
Mitigation: Deploy only when users need the full SkillBoss gateway and document the enabled action classes before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/QuincyGunter/agent-browsers) <br>
- [SkillBoss](https://www.skillboss.co) <br>
- [SkillBoss API base URL](https://api.heybossai.com/v1) <br>
- [Chat Models](artifact/chat-models.md) <br>
- [Image Models](artifact/image-models.md) <br>
- [Audio Models](artifact/audio-models.md) <br>
- [Search & Scraping Models](artifact/search-models.md) <br>
- [Tool Models](artifact/tools-models.md) <br>
- [Video Models](artifact/video-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown instructions with bash and curl examples plus API parameter tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; generated calls may invoke third-party model, search, document, email, or SMS services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
