## Description:

GPT Image 2.5 Sunburst, the precision tier of OpenAI's GPT Image 2.5 series, for text-to-image and image editing. Built for detailed creative work where fine detail, in-image text and composition matter; supports reference images, aspect ratios up to 21:9 and quality up to max.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can request detailed image generation or edit images with text prompts and optional reference images. The skill returns generated image assets and result metadata through the dLazy service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports medium confidence and partial analysis, with some referenced paths or package details unavailable and a login step left unexplained.

Mitigation: Review the CLI authentication and service details before installing, and proceed only if comfortable with the login flow.

Risk: Reference images supplied from local paths are uploaded to dLazy media storage for processing.

Mitigation: Avoid submitting sensitive images unless your data-handling requirements permit uploading them to dLazy.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/dlazyai/skills/dlazy-gpt-image-2-5-sunburst)
- [dLazy CLI repository (referenced in skill metadata)](https://github.com/dlazy-ai/cli)
- [dLazy CLI on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy service](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Images, JSON]

**Output Format:** [Generated image files and JSON response metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts up to five reference images; supports aspect ratios from auto through 21:9, quality settings from low through max, and asynchronous jobs.]

## Skill Version(s):

1.2.34 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
