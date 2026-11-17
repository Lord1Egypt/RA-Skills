## Description:

Enlarges images without loss through the Flyelep AI tool API, supporting single-image and batch processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyelepai](https://clawhub.ai/user/flyelepai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to upscale one or more images through Flyelep and receive links to the processed images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images are sent to Flyelep for processing; local uploads return links described as temporary public URLs.

Mitigation: Use only images you are authorized to share, avoid sensitive images, and use upload links promptly rather than retaining them.

Risk: The API requires a Flyelep secret key.

Mitigation: Obtain the key from the user at runtime and keep it out of skill files, repositories, and persistent configuration.

Risk: ClawScan reported a possible mismatch between the skill's stated purpose and demonstrated behavior; its analysis was partial.

Mitigation: Review the skill and test it with non-sensitive images before relying on it. Treat the scanner verdict as a review warning, not proof of malicious intent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flyelepai/skills/flyelep-image-enlarge)
- [Flyelep image enlargement API](https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/enlarge)
- [Flyelep image upload API](https://www.flyelep.cn/prod-api/poster-design/api/v1/file/upload)
- [Flyelep developer platform](https://www.flyelep.cn/controlboard)

## Skill Output:

**Output Type(s):** [Text, Image URLs]

**Output Format:** [JSON response containing URLs for successfully enlarged images]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch results may contain fewer URLs than inputs when individual images fail; supports up to 20 images per request.]

## Skill Version(s):

1.0.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
