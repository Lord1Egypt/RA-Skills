## Description:

Compress images for web usage with smart quality reduction and resizing to fit a target file size, supporting JPEG, PNG, WebP, BMP, TIFF, and GIF inputs with WebP output by default.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to compress single images or batches of web assets into smaller WebP, JPEG, or PNG outputs while preserving originals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optimized outputs may overwrite existing destination files when a custom output path or repeated batch run reuses the same name.

Mitigation: Check destination paths before running compression and keep originals or backups for important assets.

Risk: The skill writes local image files during compression.

Mitigation: Run it in a project workspace or virtual environment with the minimum filesystem access needed.

Risk: Dependency behavior can vary across Pillow versions.

Mitigation: Pin Pillow when reproducible compression results are required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-web-image-optimizer)
- [Publisher profile](https://clawhub.ai/user/freedompixels)
- [AISoBrand](https://aisobrand.com)
- [AISoBrand free diagnosis](https://aisobrand.com/free-diagnosis.html)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Files, Configuration]

**Output Format:** [Markdown guidance with bash commands and local image file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces optimized image files and CLI status summaries; image metadata is stripped during compression.]

## Skill Version(s):

1.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
