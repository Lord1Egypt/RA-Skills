## Description:

Generates structured daily reports that summarize completed tasks, ongoing work, pending items, blockers, and notable notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nopedijah](https://clawhub.ai/user/nopedijah)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers can use this skill to turn daily memory, recent conversation context, and relevant project notes into concise daily progress reports. It is intended for status summaries that highlight accomplishments, active work, pending tasks, blockers, and decisions needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read broad private context, including memory files, recent conversation history, and project files.

Mitigation: Use it only in workspaces where those sources are acceptable inputs, and review the generated report for sensitive details before sharing.

Risk: The skill may update persistent memory without clear user approval or scoping.

Mitigation: Require user confirmation before saving a generated report back into memory, and limit saved content to the intended daily-report scope.

## Reference(s):

- [Daily Report (HuangYang) on ClawHub](https://clawhub.ai/nopedijah/skills/daily-report-huangyang)
- [Publisher profile: nopedijah](https://clawhub.ai/user/nopedijah)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown daily report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task statuses, blockers, priorities, notes, and links when relevant.]

## Skill Version(s):

2.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
