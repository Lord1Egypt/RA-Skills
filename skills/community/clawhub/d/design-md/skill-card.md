## Description:

Helps an agent create, update, and apply a project-level DESIGN.md design and brand specification so generated UI follows the project's visual system.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmy1006-sudo](https://clawhub.ai/user/zmy1006-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and coding-agent users use this skill to create or maintain a root-level DESIGN.md and guide UI generation against a documented brand, layout, typography, color, and component system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or overwrite a project DESIGN.md, which may replace existing design documentation if changes are not reviewed.

Mitigation: Check whether DESIGN.md already exists and review proposed additions or edits before allowing file writes.

## Reference(s):

- [DESIGN.md template](references/design-md-template.md)
- [VoltAgent awesome-design-md](https://github.com/VoltAgent/awesome-design-md)
- [Google Stitch DESIGN.md overview](https://stitch.withgoogle.com/docs/design-md/overview/)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Code, Configuration]

**Output Format:** [Markdown guidance and project file content, sometimes accompanied by UI code or configuration recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a project DESIGN.md after reviewing product positioning, existing design assets, and requested design changes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
