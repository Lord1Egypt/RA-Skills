## Description:

Converts JPG or PNG images into round Android app icons and generates mdpi, hdpi, xhdpi, xxhdpi, and xxxhdpi PNG outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[starclimber](https://clawhub.ai/user/starclimber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and app teams use this skill to turn supplied JPG or PNG artwork into a complete Android mipmap icon set with circular masking and density-specific PNG files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing dependencies into the system Python environment can create package-management conflicts.

Mitigation: Use a dedicated Python virtual environment and avoid --break-system-packages unless a reviewer explicitly accepts that tradeoff.

Risk: Writing generated icons into an existing Android project can replace files with the same generated icon filenames.

Mitigation: Confirm the intended output directory before running the script, especially when targeting project mipmap directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/starclimber/skills/androidiconmaker)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated PNG files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces icon_mdpi.png, icon_hdpi.png, icon_xhdpi.png, icon_xxhdpi.png, and icon_xxxhdpi.png in the selected output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
