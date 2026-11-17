## Description:

Save or resume task context, record work history, and compress long records for a new session or agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snowsonz](https://clawhub.ai/user/snowsonz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to continue, save, inspect, tidy, compress, and archive handoff task records across sessions while keeping current task state in workspace files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence reports that implicit invocation is enabled even though handoff actions are intended for explicit user requests.

Mitigation: Consider disabling implicit invocation before deployment, or require explicit user confirmation before loading the handoff workflow or changing task records.

Risk: The skill can store task records in .agents/tasks and includes maintenance commands for legacy cleanup.

Mitigation: Review saved handoff content for sensitive details and inspect install, setup, migration, or cleanup commands before running them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/snowsonz/skills/agent-handoff-skill)
- [Task Handoff Protocol](PROTOCOL.md)
- [Handoff Maintenance](references/protocol.md)
- [Cross-Client Compatibility](references/compatibility.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown task records with inline shell commands when maintenance is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update task records under .agents/tasks when explicitly asked to save, resume, tidy, compress, or archive handoff work.]

## Skill Version(s):

0.4.1 (source: server release evidence and VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
