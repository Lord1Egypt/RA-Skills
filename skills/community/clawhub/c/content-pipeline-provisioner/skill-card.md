## Description: <br>
Content Pipeline Provisioner helps OpenClaw users set up and operate a self-hosted AI content pipeline for TikTok, Twitter/X, newsletters, blog publishing, and Telegram briefings using their own accounts and API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[olivimic](https://clawhub.ai/user/olivimic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, content operators, and developers use this skill to provision a self-hosted marketing content engine for a product or brand, generate its configuration and voice guide, register scheduled jobs, review test outputs, and move the pipeline live or pause/resume it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent public posting can publish incorrect, unwanted, or brand-inappropriate content across connected channels. <br>
Mitigation: Keep generated jobs in SELF_ONLY or dry-run mode until the exact accounts, channels, schedule, and test outputs are reviewed before go-live. <br>
Risk: The skill requires broad local secrets for services such as OpenAI, Postiz, MailerLite, Telegram, Supabase, and Netlify. <br>
Mitigation: Use dedicated low-privilege accounts and keys, restrict ~/.openclaw/.env, and never commit secrets. <br>
Risk: The Supabase/Xero schema and Larry dependency introduce data-flow and dependency uncertainty. <br>
Mitigation: Review the Supabase schema purpose and separately review the Larry dependency before installing or running the pipeline. <br>


## Reference(s): <br>
- [Setup Checklist](references/setup-checklist.md) <br>
- [Larry config.json Field Mapping](references/config-schema.md) <br>
- [Voice Guide Template](references/voice-guide-template.md) <br>
- [Blog Schema - Supabase Setup](references/blog-schema.md) <br>
- [Supabase Schema - pipeline_clients](references/supabase-schema.md) <br>
- [ClawHub Release Page](https://clawhub.ai/olivimic/content-pipeline-provisioner) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local configuration files, voice guides, cron records, and generated content drafts after user review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
