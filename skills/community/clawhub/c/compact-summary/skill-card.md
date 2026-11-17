## Description:

Generates structured, concise memory summaries during flush or compaction, including conversation stats, tools, user requests, tasks, files, progress, and timeline context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanxiao-bot](https://clawhub.ai/user/hanxiao-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create structured memory summaries during OpenClaw flush or compaction so future agent sessions can resume with key requests, files, progress, and timeline context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Compaction summaries can influence future agent behavior and reduce transparency if treated as authoritative instructions.

Mitigation: Review summaries before using them as resume context, and keep factual resume state separate from instructions where practical.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hanxiao-bot/skills/compact-summary)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown structured summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a compact resume-oriented memory summary; does not execute code or shell commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
