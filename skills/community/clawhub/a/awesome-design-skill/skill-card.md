## Description:

awesome-design-skill helps agents apply a user-specified UI design style by selecting a bundled brand-inspired design system and copying its DESIGN.md guidance into the working project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouchang1988](https://clawhub.ai/user/zhouchang1988)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill when they want an agent to follow a specific UI style, list available design styles, inspect a style guide, or restyle an existing page while preserving its function and content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Applying a style can overwrite an existing DESIGN.md in the target project.

Mitigation: Check for an existing DESIGN.md before applying a style, or copy the selected guide into a temporary location first.

Risk: Path-like style names could select unintended filesystem paths.

Mitigation: Use known style names from the style list and avoid values containing slashes or '..'.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhouchang1988/skills/awesome-design-skill)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)
- [VoltAgent awesome-design-md inspiration project](https://github.com/VoltAgent/awesome-design-md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown design guidance files, concise text responses, and shell command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or overwrite DESIGN.md in the target directory when applying a style.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
