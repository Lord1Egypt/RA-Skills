## Description:

Helps agents keep working from task queues, heartbeat routines, and recurring schedules instead of waiting for prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[123oo123442](https://clawhub.ai/user/123oo123442)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to set up persistent task queues, proactive heartbeat routines, and scheduled work so agents can make progress between human prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended agents can continue work from shared queues or recurring schedules without active human prompting.

Mitigation: Use a dedicated workspace, restrict writable paths and tools, require approval for sensitive or external actions, control who can edit the task queue, limit team-channel posting, and document how to list and remove scheduled jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/123oo123442/skills/agent-autonomy-kit-1-0-0)
- [Artifact README](artifact/README.md)
- [Proactive heartbeat template](artifact/templates/HEARTBEAT.md)
- [Task queue template](artifact/templates/QUEUE.md)
- [Skill homepage](https://github.com/itskai-dev/agent-autonomy-kit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, configuration snippets, and reusable templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes task queue and heartbeat templates; may recommend recurring scheduled jobs for autonomous operation.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
