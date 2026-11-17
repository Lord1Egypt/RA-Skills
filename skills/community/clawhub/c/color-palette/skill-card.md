## Description:

Extract a color palette from an image and return HEX/RGB values with optional swatch image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qrost](https://clawhub.ai/user/qrost)

### License/Terms of Use:

MIT

## Use Case:

Designers, architects, and agents use this skill to extract dominant colors from local image files for design tools, mood boards, and quick visual reference workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded or local images may contain sensitive visual information or metadata.

Mitigation: Use temporary or OpenClaw media paths for generated swatches and remove temporary files when they are no longer needed.

Risk: Unpinned Python dependencies may change behavior across installations.

Mitigation: Install the skill in an isolated Python environment and pin reviewed dependency versions before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qrost/skills/color-palette)
- [Publisher profile](https://clawhub.ai/user/qrost)
- [Publisher GitHub profile](https://github.com/QROST)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Plain text HEX/RGB palette with optional PNG swatch image]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The palette size is configurable from 1 to 20 colors.]

## Skill Version(s):

1.1.1 (source: server release evidence, skill frontmatter, and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
