## Description:

Schedule delayed tasks between OpenClaw agents - set reminders, chain tasks, coordinate agents on a delay.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ktech99](https://clawhub.ai/user/ktech99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw agent users use this skill to enqueue reminders, delayed follow-ups, and post-task checks that should wake a target agent later instead of running immediately.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a persistent user-level daemon that can wake agents and deliver queued text as system events.

Mitigation: Install only after reviewing the daemon behavior, and keep the LaunchAgent removal path available if the skill is no longer needed.

Risk: Queued task text can be injected into agent system events through local queue files and the authenticated local plugin route.

Mitigation: Restrict who can write to ~/.openclaw/queue files, review allowed targets in targets.json, and cancel unexpected queued tasks before they fire.

## Reference(s):

- [Async Queue Protocol](references/PROTOCOL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON queue records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces delayed queue items with ISO 8601 run times and TTL values for a local OpenClaw queue.]

## Skill Version(s):

1.0.6 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
