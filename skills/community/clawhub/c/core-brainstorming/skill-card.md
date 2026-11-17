## Description:

Core Brainstorming helps agents explore user intent, requirements, and design before creative work through a structured collaborative dialogue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tlreal](https://clawhub.ai/user/tlreal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and agent users use this skill to turn vague feature or behavior ideas into validated design notes before implementation. It guides the agent to inspect project context, ask one focused question at a time, compare alternatives, and present design sections for user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to create repository files and make git commits after design validation.

Mitigation: Use it with an agent setup that asks before writing files, stages only the intended design document, shows diffs before commits, and confirms before invoking follow-on planning skills.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance, code, shell commands, configuration]

**Output Format:** [Conversational guidance and Markdown design documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a design document under docs/plans and request follow-on implementation planning.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
