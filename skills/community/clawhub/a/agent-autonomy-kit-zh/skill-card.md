## Description:

Helps configure AI agents to use task queues, proactive heartbeats, and scheduled OpenClaw runs for autonomous work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayakolin](https://clawhub.ai/user/ayakolin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up task queues, heartbeat routines, and OpenClaw schedules so agents can keep making progress between human prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill promotes unattended autonomous work through persistent cron runs and mutable task queues.

Mitigation: Install only in controlled workspaces where autonomous file edits, token spend, team-channel posts, and scheduled OpenClaw runs are acceptable.

Risk: Scheduled runs may continue without enough scope, approval, or stop controls.

Mitigation: Before enabling cron examples, add explicit task approval, restrict writable paths and tools, define resource and time limits, and document how to list, disable, and remove schedules.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ayakolin/skills/agent-autonomy-kit-zh)
- [Skill Homepage](https://github.com/itskai-dev/agent-autonomy-kit)
- [Agent Autonomy Kit Repository](https://github.com/reflectt/agent-autonomy-kit)
- [Agent Memory Kit](https://github.com/reflectt/agent-memory-kit)
- [Agent Team Kit](https://github.com/reflectt/agent-team-kit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON5-style configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes QUEUE.md and HEARTBEAT.md templates for agent work tracking.]

## Skill Version(s):

1.0.2 (source: release evidence; artifact frontmatter reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
