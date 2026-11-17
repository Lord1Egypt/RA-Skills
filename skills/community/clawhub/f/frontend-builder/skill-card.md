## Description:

Generates production-ready React TSX frontend components from natural-language UI goals for non-programmers, including setup instructions and dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h4gen](https://clawhub.ai/user/h4gen)

### License/Terms of Use:


## Use Case:

External users, developers, and non-programmers use this skill to turn UI requirements for dashboards, landing pages, admin screens, and similar interfaces into a copy-pasteable React TypeScript component with setup guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned remote CLI install commands may change behavior between runs.

Mitigation: Review or pin the ClawHub and shadcn CLI versions before executing setup commands.

Risk: The broad update command can update every installed skill, not only this skill's dependencies.

Mitigation: Run broad updates only when intended and review the resulting skill changes before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/h4gen/skills/frontend-builder)
- [Inspected upstream skills](artifact/references/inspected-skills.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline TypeScript TSX and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Usually produces one self-contained TSX component plus setup commands, assumptions, and adaptation notes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
