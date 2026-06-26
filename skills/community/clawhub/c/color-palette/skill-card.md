## Description: <br>
Extract a color palette from an image and return HEX/RGB values with optional swatch image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QROST](https://clawhub.ai/user/QROST) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Designers, architects, and agents use this skill to extract dominant colors from reference images for design tools, mood boards, or visual palette handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local Python image-processing script on image files provided to the agent. <br>
Mitigation: Install only when local script execution is acceptable, process trusted or sandboxed images, and review the image paths passed to the command. <br>
Risk: The skill can write an optional swatch image to a caller-provided output path. <br>
Mitigation: Write swatch files only to intended media or temporary directories and avoid ambiguous output paths. <br>
Risk: The skill depends on Pillow for image handling. <br>
Mitigation: Pin dependencies where appropriate and keep Pillow updated before processing untrusted images. <br>


## Reference(s): <br>
- [Color Palette Generator on ClawHub](https://clawhub.ai/QROST/color-palette) <br>
- [Publisher profile](https://clawhub.ai/user/QROST) <br>
- [Publisher homepage](https://github.com/QROST) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files] <br>
**Output Format:** [Plain text HEX/RGB palette lines with an optional PNG swatch file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts an image path, a color count from 1 to 20, and an optional output path for the swatch PNG.] <br>

## Skill Version(s): <br>
1.1.1 (source: SKILL.md frontmatter, clawhub.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
