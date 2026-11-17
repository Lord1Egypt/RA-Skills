## Description:

Generate color palettes and get color suggestions via the Colormind.io API, including listing models and generating palettes with optional locked colors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boilerrat](https://clawhub.ai/user/boilerrat)

### License/Terms of Use:


## Use Case:

Developers, designers, and agents use this skill to generate Colormind color palettes, list available models, lock selected RGB colors, or derive a palette from an image sample.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Palette inputs and image-derived color values are sent to colormind.io over unencrypted HTTP.

Mitigation: Use only non-sensitive palettes and images, and avoid confidential designs, proprietary brand colors, or private images.

Risk: Processing untrusted image files with ImageMagick can expose the runtime to image parser vulnerabilities.

Mitigation: Use a recent patched ImageMagick version, process only trusted files when possible, and add sandboxing and explicit approval for image workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/boilerrat/skills/colormind)
- [Colormind API endpoint](http://colormind.io/api/)
- [Colormind model list endpoint](http://colormind.io/list/)
- [Artifact security notes](artifact/SECURITY.md)
- [Artifact changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [JSON palette data with optional Markdown palette summaries and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Palette generation can use a selected model and optional locked RGB color slots; image sampling requires Node.js, Python 3, and ImageMagick convert.]

## Skill Version(s):

1.1.1 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
