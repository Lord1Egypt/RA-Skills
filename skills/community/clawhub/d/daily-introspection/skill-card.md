## Description:

Provides autonomous daily self-introspection and self-improvement for OpenClaw agents by reviewing daily conversation logs, identifying mistakes and improvement opportunities, and promoting mature lessons to persistent guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raydoomed](https://clawhub.ai/user/raydoomed)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to schedule daily review of conversation logs and weekly promotion of validated lessons into persistent agent guidance. It is intended for autonomous self-improvement workflows that collect introspection records, summarize recurring issues, and prepare rule updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled self-modification can change persistent agent guidance before a user reviews the proposed update.

Mitigation: Require explicit human approval before any AGENTS.md, MEMORY.md, or TOOLS.md edits are applied.

Risk: Daily introspection records may retain sensitive conversation, learning, or error details in the workspace.

Mitigation: Define retention, access control, and redaction rules for the .daily-introspection directory before enabling the cron jobs.

Risk: Users may lose track of unattended daily and weekly cron execution.

Mitigation: Document the installed cron entries, target session, timezone, and disable procedure as part of deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown records and reports with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates private introspection records and weekly evolution reports in the configured OpenClaw workspace.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
