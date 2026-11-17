## Description:

Quality assurance skill that helps an agent record task context, confirm plans, verify deliverables against user requirements, and reflect on prior errors or feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[webray1983](https://clawhub.ai/user/webray1983)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to make an assistant keep task notes, confirm execution plans, re-check deliverables against the original requirements, and extract lessons from previous mistakes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently record and reuse detailed conversation and task history without strong user-control or privacy limits.

Mitigation: Review before installing, avoid sharing secrets while active, and add explicit opt-in, redaction, retention, deletion, and trust-boundary rules before broad use.

Risk: Stored notes may preserve stale, incorrect, or overly broad task context that can affect later assistant behavior.

Mitigation: Require the agent to compare recalled context against the current user request and ask for confirmation when requirements conflict.

Risk: The bundled memory script writes local diary, document, experience, and index files under a fixed workspace path.

Mitigation: Review the storage path and file permissions before running the script, and adjust them to the intended environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/webray1983/skills/double-check-skill)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Files]

**Output Format:** [Markdown guidance with shell command examples and local memory files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent local notes and indexes about conversations and tasks.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
