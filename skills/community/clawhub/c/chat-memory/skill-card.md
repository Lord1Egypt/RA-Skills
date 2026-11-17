## Description:

Chat Memory converts OpenClaw session logs into searchable Markdown memory, builds an indexed glossary of people, projects, decisions, and timelines, and suggests memory-aware cron prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moltbotmolty-del](https://clawhub.ai/user/moltbotmolty-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external ClawHub users who run OpenClaw agents use this skill to preserve context across compactions and make past sessions searchable for future agent work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill broadly copies and indexes private agent conversations without built-in redaction, retention controls, or strong scoping.

Mitigation: Use it only on approved workspaces, and add redaction, session allowlists, retention limits, and a purge process before indexing sensitive work.

Risk: Long-lived searchable memory may retain credentials, customer data, legal, medical, HR, or confidential business material if those appear in chat history.

Mitigation: Avoid those workspaces unless sensitive content is excluded or scrubbed before conversion and vector indexing.

Risk: Cron-based automation can repeatedly refresh memory indexes and extend the lifetime of copied session content.

Mitigation: Review the cron schedule and scope before enabling automation, and test manually before running unattended updates.

## Reference(s):

- [ClawHub Chat Memory release](https://clawhub.ai/moltbotmolty-del/skills/chat-memory)
- [AI Advantage](https://aiadvantage.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands; scripts generate Markdown memory files, JSON state and cache files, and a Markdown cron optimization report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local filesystem outputs include session transcripts, a glossary, state/cache files, and cron optimization reports.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
