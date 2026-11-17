## Description:

Automatically record and analyze user behavior patterns from conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chefroger](https://clawhub.ai/user/chefroger)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users can use this skill to record conversation topics, analyze behavior patterns from local conversation memory, and generate behavior reports. It supports manual tracking and optional scheduled analysis for users who explicitly opt in.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill profiles OpenClaw conversation memory and stores durable behavior data.

Mitigation: Install only when this profiling is expected, inspect generated behavior files periodically, and delete them when they are no longer needed.

Risk: Cron or heartbeat automation can update behavior records repeatedly without a fresh prompt each time.

Mitigation: Prefer manual runs unless scheduled tracking has been explicitly enabled by the user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chefroger/skills/behavior-tracker)
- [Publisher profile](https://clawhub.ai/user/chefroger)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown reports, JSON behavior profile files, and shell commands for manual or scheduled runs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write behavior-patterns.json, behavior-report.md, and behavior-last-check.json under the OpenClaw workspace memory directory when run.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
