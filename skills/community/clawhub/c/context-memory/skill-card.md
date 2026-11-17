## Description:

Helps an agent maintain persistent context by using workspace memory files and a structured task-start workflow for reading, executing, and saving important information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[long57777](https://clawhub.ai/user/long57777)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to give agents a repeatable memory workflow for long-running collaboration, frequent task switching, user preferences, tool notes, and lessons learned.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages agents to save and reload personal details, project history, corrections, workflow rules, and tool notes.

Mitigation: Use it only in workspaces where persistent memory is appropriate, and keep secrets, tokens, private emails, and sensitive client data out of memory files.

Risk: Automatic memory writes may preserve inaccurate, stale, or overly broad instructions.

Mitigation: Require explicit confirmation before memory writes and periodically review or delete memory files.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance with memory file templates and workflow rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide an agent to create or update workspace memory files.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
