## Description:

Convert PNG images into circular PNG avatars with transparent corners.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charmingzuo](https://clawhub.ai/user/charmingzuo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to create circular PNG avatars, profile photos, icons, and other round image assets from user-selected PNG files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A missing or floating Pillow dependency can make results less reproducible across environments.

Mitigation: Install the dependency in a virtual environment and pin Pillow for sensitive or reproducible workflows.

Risk: The helper script can overwrite an existing output file when overwrite behavior is explicitly enabled.

Mitigation: Keep overwriting user-directed and review the output path before running with force behavior.

Risk: The script processes local image paths supplied by the user.

Mitigation: Provide only PNG image paths that are intended for processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charmingzuo/skills/circle-png-image)
- [Publisher profile](https://clawhub.ai/user/charmingzuo)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [PNG file output with Markdown or text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are PNG images with an alpha channel; optional fit, size, and overwrite settings affect the generated file.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
