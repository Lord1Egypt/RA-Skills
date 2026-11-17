## Description:

Cn Image Watermark adds text or logo watermarks to local images, with batch processing, nine-position placement, and opacity controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content operators, and brand teams use this skill to add visible ownership or anti-reposting watermarks to local image files. It is suited for social images, cover art, product photos, and batches of images that need consistent text or logo marks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch mode recursively scans the selected input folder and writes generated images to the selected output directory.

Mitigation: Review input and output paths before batch use, and run on a small sample folder before processing a large image set.

Risk: Batch mode may need a bug fix before it works as documented.

Mitigation: Validate batch behavior locally before relying on it for production workflows; use single-image text or logo commands when batch output is not confirmed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-image-watermark)
- [AISoBrand](https://aisobrand.com)

## Skill Output:

**Output Type(s):** [shell commands, JSON, files, guidance]

**Output Format:** [Markdown guidance with shell commands; CLI commands return JSON status and write watermarked image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes caller-provided local image paths and can recursively scan a chosen input folder for batch watermarking.]

## Skill Version(s):

1.2.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
