## Description: <br>
Headless browser automation CLI optimized for AI agents with accessibility tree snapshots, plus access to 50+ SkillBoss models for chat, image, video, audio, search, document processing, email, and SMS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ModestyRichards](https://clawhub.ai/user/ModestyRichards) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call SkillBoss browser and model APIs from shell commands for multimodal generation, search, scraping, document processing, email, SMS, and smart model routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A single SkillBoss API key can authorize broad actions across model calls, scraping, document processing, email, SMS, and storage. <br>
Mitigation: Use a restricted or low-risk API key where available, scope access outside the skill, and rotate the key if exposed. <br>
Risk: Prompts, files, audio, documents, search targets, and generated content may be sent to SkillBoss or downstream providers. <br>
Mitigation: Avoid submitting secrets, sensitive documents, private audio, or confidential prompts unless the user has approved the provider path and data handling. <br>
Risk: Email, SMS, scraping, storage, and document-processing actions can affect external systems or people. <br>
Mitigation: Require explicit human review before executing those actions and verify recipients, URLs, payloads, and expected costs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ModestyRichards/agent-browser-clawdbots) <br>
- [SkillBoss API base URL](https://api.heybossai.com/v1) <br>
- [SkillBoss model discovery endpoint](https://api.heybossai.com/v1/models) <br>
- [SkillBoss website](https://www.skillboss.co) <br>
- [Chat model reference](chat-models.md) <br>
- [Image model reference](image-models.md) <br>
- [Video model reference](video-models.md) <br>
- [Audio model reference](audio-models.md) <br>
- [Search and scraping model reference](search-models.md) <br>
- [Tool model reference](tools-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for authenticated SkillBoss API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
