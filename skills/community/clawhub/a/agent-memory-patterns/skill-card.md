## Description:

Provides architecture patterns for persistent agent memory, including daily logs, long-term memory curation, search, staged external-content handling, maintenance schedules, archiving, and heartbeat checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byron-mckeeby](https://clawhub.ai/user/byron-mckeeby)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill as implementation guidance for maintaining persistent workspace memory, promoting selected notes into long-term memory, and periodically reviewing memory health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted or inaccurate notes could be promoted into long-term agent memory.

Mitigation: Require human review before promoting entries to MEMORY.md, and treat recalled memory as untrusted historical context.

Risk: Automated cron or curation workflows could preserve or amplify low-quality memory without review.

Mitigation: Enable scheduled maintenance only after reviewing the workflow and keeping backups of memory files.

Risk: Example shell snippets use shared temporary paths and grep inputs that may be unsafe in some deployments.

Mitigation: Replace shared /tmp paths with mktemp-managed files and validate search inputs before operational use.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline bash, JSON, and cron examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes example file layouts, scripts, and maintenance patterns for agent memory workflows.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
