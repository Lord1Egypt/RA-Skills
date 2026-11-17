## Description:

A markdown onboarding manual that helps new OpenClaw agents learn operating principles, workspace conventions, communication practices, tool usage, cron and heartbeat routines, common mistakes, recommended skills, and an onboarding checklist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrot90-code](https://clawhub.ai/user/harrot90-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill as a human-readable onboarding manual for new OpenClaw agents. It provides training guidance, operational checklists, and examples for building reliable agent work habits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The manual teaches persistent automation and cron routines with too little scoping or approval.

Mitigation: Review and edit automation guidance before installation; require explicit approval before creating cron jobs and verify delivery targets, time zones, and error monitoring.

Risk: The manual discusses local memory, logs, backups, and user context that may contain sensitive information.

Mitigation: Add retention, redaction, and access rules for memory, logs, and backups; restrict sensitive memory access to appropriate private sessions.

Risk: The manual includes broad token-search guidance and global package installation examples.

Mitigation: Remove broad token-search commands from live agent instructions and replace global unpinned installs with scoped, pinned, reviewed installation steps.

Risk: The manual covers external communications such as messages, documents, and email.

Mitigation: Require user confirmation before sending or sharing externally, and check recipients, permissions, formatting, and privacy-sensitive content before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrot90-code/skills/agent-training-manual)
- [Publisher profile](https://clawhub.ai/user/harrot90-code)
- [Artifact README](artifact/README.md)
- [Artifact SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown documents with headings, checklists, tables, and inline shell or JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces human-facing training guidance rather than executable automation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
