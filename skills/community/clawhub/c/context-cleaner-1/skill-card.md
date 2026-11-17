## Description:

Automatically compress large contexts and clean up expired sessions, sub-agents, and temporary files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liujc007](https://clawhub.ai/user/liujc007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to manage large working contexts, archive old sessions, and prepare cleanup reports while preserving active work and recent history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can alter session history, replace context, archive or delete sessions, and terminate sub-agents with insufficient user control.

Mitigation: Use dry-run or archive-only operation by default, define retention rules before automation, and require explicit confirmation before deletion, context replacement, or sub-agent termination.

Risk: Heartbeat or cron automation could repeatedly perform cleanup before an operator has reviewed active work.

Mitigation: Avoid enabling scheduled cleanup until active-session checks, recent-history preservation, and confirmation requirements are configured.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liujc007/skills/context-cleaner-1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with cleanup reports, shell command examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose context replacement, session archiving, deletion, or sub-agent termination actions that should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
