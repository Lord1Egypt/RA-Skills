## Description:

Batch Image Processor Pro helps agents produce bulk image-processing instructions for compression, cropping, watermarking, format conversion, renaming, resizing, color adjustment, and EXIF cleanup workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bingze00000](https://clawhub.ai/user/bingze00000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and content teams can use this skill to ask an agent for batch image-processing commands for ecommerce, social-media, and photo optimization workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch operations can alter many images at once, including metadata such as EXIF data.

Mitigation: Process copies or use a separate output directory, then inspect sample results before applying changes to a full image set.

Risk: The skill content is primarily Chinese-language, which can lead to parameter misunderstandings for non-Chinese readers.

Mitigation: Have a Chinese-reading reviewer confirm commands and parameters before using the skill in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bingze00000/skills/batch-image-processor-pro)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language command patterns for image directory, output directory, quality, watermark, size, and format settings.]

## Skill Version(s):

1.0.0 (source: evidence release and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
