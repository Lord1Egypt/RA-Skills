## Description:

Rapidly spawn and configure specialized sub-agents with Research, Coding, and Analysis templates plus automated workspace setup and instruction delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keyserkazi1](https://clawhub.ai/user/keyserkazi1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create specialized sub-agent workspaces for coding, research, and analysis tasks, including inbox, outbox, workspace folders, and a starter SKILL.md.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup script can write outside the intended agents directory if given a crafted agent name.

Mitigation: Run the script only with trusted, simple agent names using letters, numbers, underscores, or hyphens, and avoid running it where unintended file creation or overwrite would matter.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Code]

**Output Format:** [Markdown guidance with inline shell commands and generated SKILL.md content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local agent workspace files under agents/<name> when the setup script is run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
