## Description:

Distill finished work into the right OpenClaw knowledge layer by deciding whether results belong in daily logs, the experience bank, playbooks, reusable skills, multiple layers, or no long-term record.

This skill is ready for commercial/non-commercial use.

## Publisher:

[traceme](https://clawhub.ai/user/traceme)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill after completing a task to decide what should be captured as dated evidence, reusable experience, workflow playbook content, a reusable skill, or nothing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose or write long-term knowledge files, which could preserve private details, credentials, temporary debugging output, or inaccurate lessons if used without review.

Mitigation: Review proposed files and draft content before executing writes, especially when the completed task involved private details, credentials, or temporary debugging output.

## Reference(s):

- [Experience Distiller Decision Rules](references/decision-rules.md)
- [Distill Invocation Template](references/template.md)
- [Distill Invocation Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown recommendation block with draft content bullets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include exact file paths to create or update when the user asks it to execute writes.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
