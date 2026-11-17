## Description:

Self-serve OpenClaw skill that provisions a self-hosted content pipeline for TikTok, Twitter/X, newsletters, blog posts, and Telegram briefings using the user's own accounts and API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[olivimic](https://clawhub.ai/user/olivimic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and brand owners use this skill to set up and manage a self-hosted content engine that creates configurations, voice guidance, scheduled posting jobs, and publishing workflows for a product or brand.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad posting authority across social, newsletter, blog, and briefing channels through persistent scheduled jobs.

Mitigation: Keep all crons in test mode until the operator reviews exactly what each channel will publish, then approve only the intended jobs for public posting.

Risk: The skill depends on sensitive service credentials for OpenAI, Postiz, MailerLite, Telegram, Supabase, and Netlify.

Mitigation: Use separate scoped credentials per service and brand, lock down or avoid shared env files, and do not store customer newsletter API keys as plain database text.

Risk: The skill relies on the Larry dependency as the underlying TikTok/content posting engine.

Mitigation: Verify the Larry dependency source and version before installation or execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/olivimic/skills/content-pipeline-provisioner)
- [Setup Checklist](references/setup-checklist.md)
- [Larry Config Schema](references/config-schema.md)
- [Voice Guide Template](references/voice-guide-template.md)
- [Blog Schema](references/blog-schema.md)
- [Supabase Schema](references/supabase-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration, file templates, cron setup instructions, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup instructions and generated content-pipeline artifacts for user-controlled accounts and local OpenClaw/Larry environments.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
