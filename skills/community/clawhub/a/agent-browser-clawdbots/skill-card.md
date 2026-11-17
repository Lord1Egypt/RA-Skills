## Description:

Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and API examples for chat, image, video, audio, search, document parsing, email, and SMS models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modestyrichards](https://clawhub.ai/user/modestyrichards)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to guide agents in calling the SkillBoss/HeyBoss API for model discovery, model execution, and smart routing across text, media, search, document, email, and SMS capabilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task inputs may be sent to the SkillBoss/HeyBoss API and downstream providers.

Mitigation: Avoid sensitive documents, private audio, personal data, and regulated content unless an approved data handling policy covers the use.

Risk: Email and SMS examples can trigger actions that affect external recipients.

Mitigation: Require explicit user confirmation, verify recipients and message content, and limit API key access before email or SMS actions.

Risk: Broad smart routing and model access can make data sharing scope unclear.

Mitigation: Review the selected model, provider, and task payload before execution and use the least-privileged key available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/modestyrichards/skills/agent-browser-clawdbots)
- [SkillBoss](https://www.skillboss.co)
- [HeyBoss API v1](https://api.heybossai.com/v1)
- [Chat Models](artifact/chat-models.md)
- [Image Models](artifact/image-models.md)
- [Video Models](artifact/video-models.md)
- [Audio Models](artifact/audio-models.md)
- [Search and Scraping Models](artifact/search-models.md)
- [Tool Models](artifact/tools-models.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks and API parameter tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for API calls.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
