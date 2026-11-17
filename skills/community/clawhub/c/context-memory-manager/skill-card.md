## Description:

Context Memory Manager helps an agent monitor context usage, preserve full conversations before memory extraction, update structured memory files, and run daily memory review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[csl3170](https://clawhub.ai/user/csl3170)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to maintain long-running workspace memory by saving chat logs, extracting project memories, updating MEMORY.md, and reviewing accumulated memory on a daily schedule.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can preserve complete local conversation transcripts and update long-lived memory files.

Mitigation: Use it in a private workspace, avoid sharing secrets in chats that may be stored, and periodically review retained memory.

Risk: The skill can add a daily cron workflow and write review reports in shared /tmp storage.

Mitigation: Review or remove the cron entry after installation and treat /tmp/cmm_review_report.json as untrusted unless the implementation is changed to use a private workspace state directory.

Risk: Automatically updated memory can retain stale, redundant, or sensitive project details.

Mitigation: Review MEMORY.md and project memory files before relying on them for future agent work.

## Reference(s):

- [Model Context Windows](references/model-contexts.md)
- [ClawHub skill page](https://clawhub.ai/csl3170/skills/context-memory-manager)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON review reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local memory files, update MEMORY.md, configure a daily cron job, and produce /tmp/cmm_review_report.json.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
