## Description:

GPT Image 2.5 Sunburst, the precision tier of OpenAI's GPT Image 2.5 series, for text-to-image and image editing. Built for detailed creative work where fine detail, in-image text and composition matter; supports reference images, aspect ratios up to 21:9 and quality up to max.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative users use this skill to generate images from text prompts or edit images with reference images, choosing an aspect ratio and quality level for the result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports a mismatch between the image-generation description and the skill's login and authentication operations.

Mitigation: Review the dLazy CLI authentication flow and confirm those operations are expected before use.

Risk: Local reference images are uploaded to dLazy media storage for processing.

Mitigation: Only submit images you are authorized to share, and avoid confidential or sensitive images.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/dlazyai/skills/dlazy-gpt-image-2-5-sunburst)
- [dLazy CLI repository linked in skill metadata](https://github.com/dlazy-ai/cli)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Images, JSON metadata]

**Output Format:** [Image files returned through a JSON response with image URLs and metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports text prompts, up to five reference images, multiple aspect ratios, and selectable quality; asynchronous requests can return a task identifier before the images are ready.]

## Skill Version(s):

1.2.31 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
