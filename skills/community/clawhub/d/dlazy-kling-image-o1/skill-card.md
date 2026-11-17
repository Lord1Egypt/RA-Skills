## Description:

Generate images with the Kling o1 model from text prompts or reference images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate or edit images with Kling o1 using a text prompt and optional reference images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reported partial coverage, including an unresolved CLI package, and could not clearly connect the login step to the image-generation purpose.

Mitigation: Before installing or signing in, verify that the CLI and login flow are from the expected provider and are needed for this skill.

Risk: Prompts and supplied local image files are sent to dLazy's hosted API and media storage.

Mitigation: Avoid sending sensitive prompts or images unless your organization's policies allow processing them by this service.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-kling-image-o1)
- [dLazy CLI project (listed in skill metadata)](https://github.com/dlazy-ai/cli)
- [dLazy CLI on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy API key dashboard](https://dlazy.com/dashboard/organization/api-key)
- [dLazy website](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Images, JSON]

**Output Format:** [Image URLs or saved image files with structured JSON result metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports text-to-image and image-to-image generation; results can be returned asynchronously.]

## Skill Version(s):

1.3.40 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
