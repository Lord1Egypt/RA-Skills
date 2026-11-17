## Description:

Process and convert images with resize, crop, compress, and format conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run local image processing tasks such as resizing, cropping, compressing, converting formats, creating thumbnails, and applying simple filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image processing can overwrite an input file when no explicit output path is provided.

Mitigation: Pass an explicit --output path and keep backups of important source images before processing.

Risk: Unpinned or untrusted Pillow installations can add dependency and supply-chain risk.

Mitigation: Install Pillow from a trusted, pinned dependency source where possible.

Risk: Extreme resize, crop, blur, or quality values may produce unusable outputs or unexpected resource use.

Mitigation: Review parameters before batch operations and test on a copy before processing large directories.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dinghaibin/skills/dinghaibin-image-processor)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write processed image files locally; Pillow is required for full functionality.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
