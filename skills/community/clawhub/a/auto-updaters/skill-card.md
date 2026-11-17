## Description:

Provides agent guidance and command examples for using a SkillBoss API gateway across chat, image, video, audio, search, document processing, email, SMS, and related model tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeltennyson](https://clawhub.ai/user/abeltennyson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover and call SkillBoss-hosted models and tools through documented API endpoints. The release should be reviewed as a broad third-party AI and communications gateway rather than as an automatic updater.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is presented as an auto-updater, but the security evidence says it documents a broad third-party AI, media, search, email, and SMS gateway.

Mitigation: Install only when that gateway behavior is intended, and do not rely on this package as a safe automatic updater until the name, description, implementation, and disclosures are corrected.

Risk: The SKILLBOSS_API_KEY may authorize external model, search, document, email, and SMS actions.

Mitigation: Scope and rotate keys, confirm who operates api.heybossai.com, and require explicit approval, allowlists, and rate limits for email and SMS operations.

Risk: Prompts, documents, audio, images, phone numbers, email addresses, and message content can be sent outside the local environment.

Mitigation: Use only data approved for SkillBoss/HeyBoss and downstream providers, and avoid sensitive or regulated data unless privacy, retention, and provider controls have been reviewed.

Risk: The artifact examples reference a run.mjs helper, but the evidence guidance calls out uncertainty about where that helper comes from.

Mitigation: Prefer the documented curl calls or an audited local helper, and verify executable provenance before running helper commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abeltennyson/skills/auto-updaters)
- [SkillBoss website](https://www.skillboss.co)
- [HeyBoss API base URL](https://api.heybossai.com/v1)
- [Models endpoint](https://api.heybossai.com/v1/models)
- [Audio Models](audio-models.md)
- [Chat Models](chat-models.md)
- [Image Models](image-models.md)
- [Search & Scraping Models](search-models.md)
- [Tool Models](tools-models.md)
- [Video Models](video-models.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with curl and run.mjs command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends requests to third-party SkillBoss/HeyBoss API endpoints.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
