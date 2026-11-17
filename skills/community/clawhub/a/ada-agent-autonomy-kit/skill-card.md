## Description:

Stop waiting for prompts. Keep working.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanford](https://clawhub.ai/user/seanford)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure proactive task queues, heartbeat routines, scheduled work, and daily handoff notes for agents that should keep making progress between human prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages persistent autonomous scheduled work, which can continue acting without timely human review.

Mitigation: Enable cron or heartbeat examples only when the workspace and tools are restricted, task queues are writable only by trusted users or agents, and time and token limits are set.

Risk: Ready queue items may be acted on before they have been reviewed for priority, safety, or authorization.

Mitigation: Review tasks before moving them to Ready, keep human requests first, and require escalation for blocked or high-impact tasks.

Risk: Scheduled jobs can persist after they are no longer wanted.

Mitigation: Track configured cron jobs and keep a documented process to list and remove them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seanford/skills/ada-agent-autonomy-kit)
- [Publisher profile](https://clawhub.ai/user/seanford)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON5 configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes task queue and heartbeat templates; no API calls or credentials are required.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
