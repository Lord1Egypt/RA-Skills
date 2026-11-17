## Description:

Manage personal knowledge, store insights, track tasks, and stay accountable by syncing and updating DeepThink user data and todos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[addisonhellum](https://clawhub.ai/user/addisonhellum)

### License/Terms of Use:


## Use Case:

Agents assisting a user use this skill to query and maintain the user's DeepThink knowledge base, records, todos, daily plans, chats, and transcripts. It is intended for personal context retrieval, reviewed record updates, task tracking, and accountability workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ongoing sync and transcript monitoring can expose sensitive personal information beyond the immediate chat.

Mitigation: Require explicit opt-in for background sync and transcript monitoring; otherwise limit use to user-initiated lookups.

Risk: Automatic record, todo, external messaging, HEARTBEAT.md, or SOUL.md changes can alter user data or agent behavior without clear consent.

Mitigation: Require explicit approval or review before writes, outbound messages, task updates, and workspace memory changes.

Risk: Transcript text can include misheard audio, background speech, or third-party speech that should not be treated as a user instruction.

Mitigation: Confirm the speaker and intent before taking significant action based on transcript content.

## Reference(s):

- [ClawHub DeepThink skill page](https://clawhub.ai/addisonhellum/skills/deepthink)
- [DeepThink API base URL](https://api.deepthink.co)

## Skill Output:

**Output Type(s):** [guidance, API calls, text, markdown, configuration]

**Output Format:** [Markdown instructions with HTTP request examples and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided DeepThink API key; record, task, transcript, messaging, and workspace changes should be explicitly authorized or reviewed.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
