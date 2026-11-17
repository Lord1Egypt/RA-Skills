## Description:

A communication framework that asks an agent to structure replies around goals and options, command-and-result execution, and a short outcome review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[markma84](https://clawhub.ai/user/markma84)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to make collaborative work easier to audit by separating brief planning rationale, execution evidence, and retrospective review. It is useful when a consistent think-execute-review response pattern is desired.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to run a bundled Python license-check script before showing skill content.

Mitigation: Review the script before use and run it only where reading local OpenClaw license metadata is acceptable; prefer platform-enforced licensing when available.

Risk: The skill imposes a fixed response structure that may conflict with task-specific or user-directed formatting.

Mitigation: Use the three-part format only when it helps the task, and let explicit user or workflow formatting requirements take priority.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/markma84/skills/3steps-to-wisdom)
- [Publisher profile](https://clawhub.ai/user/markma84)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown text, optionally including shell commands and command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Applies a three-part response structure: think, execute, and review.]

## Skill Version(s):

2.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
