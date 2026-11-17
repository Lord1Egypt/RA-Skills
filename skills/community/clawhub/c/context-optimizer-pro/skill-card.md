## Description:

Monitors token usage in long sessions, extracts key information, and creates continuation sessions to manage context limits automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericgogogogogo](https://clawhub.ai/user/ericgogogogogo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to monitor long-running OpenClaw sessions, extract unfinished work, decisions, preferences, and important files, and prepare a continuation prompt when context approaches its limit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect and carry private conversation history into continuation sessions.

Mitigation: Review extracted content before reuse, redact secrets and sensitive user data, and limit what history can be copied.

Risk: Automatic splitting or scheduled monitoring can move session context without enough user control.

Mitigation: Keep a human review step before enabling cron or automatic spawning, and define clear thresholds and retention limits.

## Reference(s):

- [Context Auto-Split](references/auto-split.md)
- [Context Optimizer Cron Template](references/cron-usage.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown continuation summaries with inline shell commands and optional JSON analysis output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Continuation content may include extracted session history, decisions, tasks, preferences, and file paths.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
