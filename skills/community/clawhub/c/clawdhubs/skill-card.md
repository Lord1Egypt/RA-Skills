## Description:

Use the ClawdHub CLI to search, install, update, and publish agent skills, and to access AI models for image, video, speech, music, chat, web search, document processing, email, and SMS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeltennyson](https://clawhub.ai/user/abeltennyson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to discover SkillBoss models, call supported model APIs, and perform ClawHub skill marketplace operations from an agent workflow. It is also used for model-backed content generation, search, document parsing, and communication workflows that require a SkillBoss API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts, files, audio, document URLs, email content, recipient addresses, and phone numbers to SkillBoss/HeyBoss and downstream model or messaging providers.

Mitigation: Use only with authorization, avoid confidential or regulated data unless approved, and confirm that the service and downstream providers are acceptable for the intended data.

Risk: The skill documents email and SMS actions that can contact external recipients.

Mitigation: Confirm recipients, consent, message content, and business purpose before invoking email or SMS endpoints.

Risk: The security summary reports inconsistent identity and limited privacy or consent guardrails.

Mitigation: Verify the publisher, service identity, API endpoints, and organizational policy fit before installation or production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abeltennyson/skills/clawdhubs)
- [SkillBoss API base URL](https://api.heybossai.com/v1)
- [SkillBoss models endpoint](https://api.heybossai.com/v1/models)
- [SkillBoss API key site](https://www.skillboss.co)
- [Audio Models](audio-models.md)
- [Chat Models](chat-models.md)
- [Image Models](image-models.md)
- [Search & Scraping Models](search-models.md)
- [Tool Models](tools-models.md)
- [Video Models](video-models.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; API response shapes vary by selected model and endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
