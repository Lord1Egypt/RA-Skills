## Description:

Batch image processing tool for compressing, resizing, watermarking, format conversion, and renaming images from a local folder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run local batch image workflows for ecommerce images, social media assets, ID photos, and blog images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that a rename filename-handling flaw can write outside the intended output folder.

Mitigation: Run the skill only on copied image folders or with an explicit output directory, and avoid prefix or date-format values containing slashes, backslashes, absolute paths, or '..'.

Risk: The skill depends on Pillow for local image processing.

Mitigation: Install Pillow from a trusted, pinned environment where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-batch-image-editor)
- [AISoBrand](https://aisobrand.com)
- [AISoBrand free diagnosis](https://aisobrand.com/free-diagnosis.html)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Files, Guidance]

**Output Format:** [Markdown guidance with bash commands; the bundled Python script produces processed image files and console status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes local image folders with Pillow; output defaults to an output or renamed subdirectory when no explicit output directory is provided.]

## Skill Version(s):

1.2.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
