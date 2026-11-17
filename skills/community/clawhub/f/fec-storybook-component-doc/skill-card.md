## Description:

Helps developers document and preview UI component states in Storybook, with optional interaction checks and visual baselines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bovinphang](https://clawhub.ai/user/bovinphang)

### License/Terms of Use:

MIT

## Use Case:

Frontend developers use this skill to create and review Storybook stories, MDX documentation, isolated component previews, and component-level checks for design systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running example setup commands may change project dependencies or configuration.

Mitigation: Review commands, pin package versions where practical, and run them only in the intended project.

Risk: An inline Chromatic project token could be exposed in shell history.

Mitigation: Keep Chromatic tokens in environment variables or CI secrets instead of inline commands.

## Reference(s):

- [Storybook component documentation examples](references/story-patterns.md)
- [ClawHub skill release](https://clawhub.ai/bovinphang/skills/fec-storybook-component-doc)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with Storybook configuration and story examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Component-level documentation and previews; cross-page testing requires a separate workflow.]

## Skill Version(s):

2.9.0 (source: ClawHub release, package.json, README.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
