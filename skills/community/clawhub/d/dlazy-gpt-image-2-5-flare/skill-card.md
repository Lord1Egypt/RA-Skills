## Description:

GPT Image 2.5 Flare is the speed tier in the GPT Image 2.5 series for text-to-image generation and image editing, with reference-image support, aspect ratios up to 21:9, and quality up to max.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users can generate images from prompts or edit images using reference images through the dLazy service. It supports quick everyday and higher-volume image generation with selectable aspect ratios and quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence notes a possible mismatch between the image-generation description and reviewed material, and is incomplete.

Mitigation: Review the pinned CLI package and sign-in flow, and confirm the dLazy service is intended before using it.

Risk: Prompts and local reference images are sent to dLazy's hosted API and media storage for processing.

Mitigation: Avoid sending prompts or images that contain information you are not comfortable sharing with the dLazy service.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/dlazyai/skills/dlazy-gpt-image-2-5-flare)
- [dLazy CLI project (listed in skill metadata)](https://github.com/dlazy-ai/cli)
- [dLazy CLI on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Images, JSON]

**Output Format:** [JSON result with generated image URLs and metadata; optionally saves image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports up to 5 reference images, selectable aspect ratio and quality, and asynchronous task results.]

## Skill Version(s):

1.2.34 (source: evidence.json release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
