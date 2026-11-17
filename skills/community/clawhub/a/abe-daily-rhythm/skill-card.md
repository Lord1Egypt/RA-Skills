## Description:

Daily Rhythm automates daily planning and reflection with morning briefs, evening wind-down prompts, sleep nudges, and weekly reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to set up automated morning briefings, evening planning prompts, sleep reminders, and weekly reviews that combine tasks, calendar context, and optional business metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accesses Google Tasks, calendar ICS data, and optional subscription or ARR data that may expose sensitive personal or business information.

Mitigation: Use a dedicated Google OAuth setup with read-only Tasks scope, keep credentials, tokens, ICS URLs, and API keys out of shared folders and repositories, and restrict permissions on credential and memory directories.

Risk: Scheduled cron automation can run scripts and write local memory files without direct review at execution time.

Mitigation: Review each cron entry and script path before enabling automation, run scripts manually first, and disable scheduled jobs that are not needed.

Risk: The optional ARR sync can store customer identifiers and subscription metrics locally.

Mitigation: Inspect or remove ARR sync if it is not required, minimize stored customer identifiers, and protect generated business-data files.

## Reference(s):

- [Daily Rhythm Configuration Guide](references/CONFIGURATION.md)
- [Heartbeat Template](assets/HEARTBEAT_TEMPLATE.md)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Google Tasks read-only OAuth scope](https://www.googleapis.com/auth/tasks.readonly)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, and generated planning prompts or briefs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can read and write local memory JSON/Markdown files and can call Google Tasks and optional SkillBoss API Hub services when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
