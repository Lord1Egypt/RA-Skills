## Description:

Coordinate accrual rollforward work using memory-first retrieval and structured reconciliation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Finance operations users and agents use this skill to coordinate accrual rollforward reconciliation, issue tracking, reminders, and local file updates while preserving established tracker paths, labels, and owner conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved finance workflow memory may contain sensitive tracker paths, report paths, labels, or ownership conventions.

Mitigation: Review saved memory contents before installation or use in shared workspaces, and limit reuse to the intended finance operations context.

Risk: The skill can direct edits to local reconciliation or issue-tracking files when a task requires file updates.

Mitigation: Review proposed file changes before relying on them for finance close work, and keep source files under normal workspace access controls.

Risk: Incorrect scheduler selection could create unwanted reminders or ongoing watches.

Mitigation: Follow the task's stated scheduler mode exactly and use heartbeat only for periodic awareness and cron only for exact-time follow-ups.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/finance-accrual-rollforward-coordinator)
- [ClawHub publisher profile](https://clawhub.ai/user/terrycarter1985)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown or local file edits with concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use saved memory, scheduling instructions, and local reconciliation or issue-tracking files when the active task requires them.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
