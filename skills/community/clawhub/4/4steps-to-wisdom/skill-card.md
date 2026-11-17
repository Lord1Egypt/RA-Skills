## Description:

A structured five-step communication method that guides an agent to listen, think, say, do, and see so reasoning, action, and review are visible to the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[markma84](https://clawhub.ai/user/markma84)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users apply this skill when they want responses to follow a fixed listen, think, say, do, and see cycle. It is intended to externalize reasoning, show command-and-result execution, and close each task with review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill tries to control every response through a strict five-step communication style.

Mitigation: Use it only where that response structure is desired, and disable it for tasks that need a different interaction pattern.

Risk: The artifact describes automatically storing decisions, execution results, and reflections in memory.

Mitigation: Disable or manually approve memory writes, especially for sensitive work, and filter reasoning, commands, outputs, and stored memories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/markma84/skills/4steps-to-wisdom)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown responses with structured sections and optional command/result blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include visible reasoning structure, execution results, and post-task reflections.]

## Skill Version(s):

3.0.0 (source: server release metadata, changelog dated 2026-04-13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
