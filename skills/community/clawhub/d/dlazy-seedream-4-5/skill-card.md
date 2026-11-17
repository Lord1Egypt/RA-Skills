## Description:

Generate high-quality images with Doubao Seedream 4.5, supporting text-to-image and image-to-image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users can generate images from text prompts or transform reference images with Seedream 4.5 through the dLazy CLI. The skill returns generated image URLs and can save image files locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment was benign with medium confidence but incomplete; it could not connect the reported login flow to the image-generation purpose, and some references were unresolved.

Mitigation: Review the linked CLI package and verify its login and generation behavior before providing an API key.

Risk: Prompts and any local reference images are sent to dLazy hosted services for generation.

Mitigation: Avoid submitting sensitive prompts or images, and review dLazy's service terms before use.

## Reference(s):

- [dLazy CLI repository (listed in skill metadata)](https://github.com/dlazy-ai/cli)
- [dLazy CLI on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy homepage](https://dlazy.com)
- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-seedream-4-5)

## Skill Output:

**Output Type(s):** [Images, JSON]

**Output Format:** [JSON result metadata with generated image URLs; optional image files saved locally.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image generation may complete asynchronously; generated files are hosted by dLazy unless saved locally.]

## Skill Version(s):

1.3.40 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
