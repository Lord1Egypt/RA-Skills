## Description:

Time-windowed autonomous task queue. Autonomy works only during specific time windows (e.g., 8 AM - 8 PM UTC), while cron jobs run overnight. Separates concerns by time - day = autonomy, night = maintenance. Use when you want predictable work schedule, controlled token budget, and clear temporal separation between autonomous work and scheduled maintenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luciusrockwing](https://clawhub.ai/user/luciusrockwing)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to run autonomous queue work only during configured UTC time windows while keeping overnight heartbeats in standby. It is intended for predictable scheduling, token-budget control, urgent-task overrides, and separation between active work and maintenance jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent work logs, checkpoint memories, GOALS.md updates, and .learnings entries may capture sensitive or unrelated private context.

Mitigation: Restrict writable paths and add deployment rules forbidding secrets, credentials, personal data, and unrelated private context in persistent memory or goal-tracking files.

Risk: Urgent overrides allow work outside the configured autonomy window.

Mitigation: Require approval or narrowly defined criteria before treating tasks as urgent, and review urgent-task labels before deployment.

Risk: Autonomous queue execution can continue during active windows without enough local operational boundaries.

Mitigation: Configure explicit session duration, token-budget, queue-empty, and human-active stop conditions before enabling scheduled heartbeats.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/luciusrockwing/skills/autonomy-windowed)
- [README](README.md)
- [Heartbeat Template](templates/HEARTBEAT.md)
- [Queue Template](templates/QUEUE.md)
- [Checkpoint Formats](references/checkpoints.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown templates and procedural guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defines UTC autonomy windows, heartbeat behavior, queue states, checkpoint formats, urgent overrides, and work-session logging conventions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
