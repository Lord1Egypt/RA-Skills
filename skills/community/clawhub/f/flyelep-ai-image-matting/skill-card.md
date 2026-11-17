## Description:

Removes image backgrounds through the Flyelep AI tool API for single images or batches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyelepai](https://clawhub.ai/user/flyelepai)

### License/Terms of Use:

MIT-0

## Use Case:

People preparing product or other images can use the skill to remove backgrounds and receive processed image URLs, for one image or a batch of up to 20. It requires an API key supplied by the user and image URLs that the service can access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that images may be sent to third-party hosting and returned at public URLs; the scan is partial and does not establish the full behavior.

Mitigation: Consider the privacy exposure before using sensitive images. Send only images you are comfortable sharing with the service, and do not treat the partial scan as assurance that all behavior was assessed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/flyelepai/skills/flyelep-ai-image-matting)
- [Flyelep AI image matting API](https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/aiImageMatting)
- [Flyelep developer platform](https://www.flyelep.cn/controlboard)

## Skill Output:

**Output Type(s):** [Image URLs, Guidance]

**Output Format:** [Text containing returned image URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch results include successful images and may contain fewer URLs than the number of input images.]

## Skill Version(s):

1.0.5 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
