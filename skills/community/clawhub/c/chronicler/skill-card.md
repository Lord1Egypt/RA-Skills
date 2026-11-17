## Description:

Chronicler turns OpenClaw session history into publish-ready narrative dispatches for LinkedIn, Twitter/X, Instagram, and blogs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moltbotmolty-del](https://clawhub.ai/user/moltbotmolty-del)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert OpenClaw session transcripts into reviewable social and blog-ready narrative content while preserving a running chronicle.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes broad private session history and can turn it into draft public content.

Mitigation: Use only transcript ranges that are safe to send to the configured model, sanitize sensitive sessions first, and review every dispatch before posting.

Risk: A recurring cron job may continue processing future session transcripts after initial setup.

Mitigation: Confirm the cron schedule, keep the chat-memory dependency's scheduled tasks visible, and know how to list, pause, or remove both jobs.

## Reference(s):

- [Chronicler on ClawHub](https://clawhub.ai/moltbotmolty-del/skills/chronicler)
- [AI Advantage](https://aiadvantage.ai)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces chronicle files, reporter state, and recurring cron-job guidance when followed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
