## Description:

Manages an experience-summary memory system that schedules daily, weekly, monthly, quarterly, and yearly summaries and retrieves historical experience on demand.

This skill is ready for commercial/non-commercial use.

## Publisher:

[17oko](https://clawhub.ai/user/17oko)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to configure recurring memory summaries and retrieve relevant prior experience during later conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can preserve long-term summaries of conversation history, including sessions that were deleted or reset.

Mitigation: Install only when that retention behavior is intended; exclude deleted/reset session files by default or document explicit consent for retaining them.

Risk: Recurring cron jobs and AGENTS.md retrieval rules can change future agent behavior by automatically generating and using memory summaries.

Mitigation: Review the cron schedule and retrieval rules before deployment, prefer explicit memory lookups for sensitive workspaces, and provide a clear purge process for derived summaries.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/17oko/skills/experience-summary-sys)
- [Publisher Profile](https://clawhub.ai/user/17oko)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces scheduled memory-summary guidance and AGENTS.md retrieval-rule instructions; no API-key environment variables were detected in the provided evidence.]

## Skill Version(s):

1.4.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
