## Description:

A SkillBoss API gateway that helps agents call browser, search, scraping, document, chat, generated media, email, and SMS capabilities through a single API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quincygunter](https://clawhub.ai/user/quincygunter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to have an agent discover and call SkillBoss-hosted model and tool APIs for browsing-related tasks, generated media, chat, search, scraping, document parsing, email, and SMS workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is flagged as suspicious because it is a broad third-party API gateway mislabeled as a browser skill.

Mitigation: Review the full capability surface before installation and limit use to approved SkillBoss actions for the intended workflow.

Risk: The skill can route agent requests to external model providers and submit user data through a SkillBoss API key.

Mitigation: Install only when the publisher and SkillBoss are trusted with submitted data, and scope or rotate SKILLBOSS_API_KEY according to local credential policy.

Risk: Email, SMS, OTP, scraping, document, audio, and batch messaging actions can affect third parties or expose sensitive content.

Mitigation: Require explicit user approval before those actions and review recipients, targets, documents, audio, and generated messages before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/quincygunter/skills/agent-browsers)
- [SkillBoss](https://www.skillboss.co)
- [SkillBoss API base URL](https://api.heybossai.com/v1)
- [Audio model evidence](artifact/audio-models.md)
- [Chat model evidence](artifact/chat-models.md)
- [Image model evidence](artifact/image-models.md)
- [Search and scraping model evidence](artifact/search-models.md)
- [Tool model evidence](artifact/tools-models.md)
- [Video model evidence](artifact/video-models.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and API request snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and may return URLs, generated files, JSON responses, extracted text, messages, or model output depending on the selected API.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
