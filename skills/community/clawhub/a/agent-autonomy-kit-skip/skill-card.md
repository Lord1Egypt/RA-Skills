## Description:

Helps agents keep working from a task queue and proactive heartbeat instead of waiting for prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayakolin](https://clawhub.ai/user/ayakolin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to set up proactive work routines, task queues, heartbeat behavior, handoff notes, and scheduling patterns for autonomous agent progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent unattended execution can allow broad queued tasks to run with insufficient human review.

Mitigation: Restrict which tasks may be queued, control who can edit the queue, define budgets and stop conditions, and review task scope before enabling scheduled work.

Risk: External posting, agent spawning, and scheduled cron examples may expand operational impact if enabled by default.

Mitigation: Disable external posting and agent spawning until explicitly configured, set the correct timezone, and document how to list and remove every scheduled job.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ayakolin/skills/agent-autonomy-kit-skip)
- [ClawHub Publisher Profile](https://clawhub.ai/user/ayakolin)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes queue and heartbeat templates plus scheduling examples for unattended agent work.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
