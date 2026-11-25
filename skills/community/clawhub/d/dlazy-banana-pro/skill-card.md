## Description:

Generate and edit images with Nano Banana Pro using text-to-image and image-to-image workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can request AI image generation or image editing with text prompts and optional reference images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and supplied local images may be sent to dLazy's hosted service for generation.

Mitigation: Do not submit confidential prompts or images unless they are approved for that service.

Risk: The security review was partial and noted an unexplained CLI login operation and whitespace padding in the Chinese guide.

Mitigation: Review the login behavior and padded guide section before execution, and confirm that CLI authentication is intended.

## Reference(s):

- [dLazy](https://dlazy.com)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)

## Skill Output:

**Output Type(s):** [Images, JSON]

**Output Format:** [Generated image assets with JSON result metadata and hosted URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports text-to-image and image-to-image; image size and aspect ratio are configurable.]

## Skill Version(s):

1.2.48 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
