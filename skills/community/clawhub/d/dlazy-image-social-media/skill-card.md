## Description:

A structured skill for multi-platform social-media content creation across Instagram, TikTok, YouTube, LinkedIn, Xiaohongshu, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and social media teams use this skill to plan platform-specific visuals, layouts, and copy for posts, carousels, and thumbnails. It can guide image generation through the dLazy CLI and return generated image links alongside the content plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review has medium confidence because a referenced artifact was not fully inspected.

Mitigation: Review the install details and unresolved references before installing if you need more assurance.

Risk: The skill sends prompts and supplied media to dLazy-hosted APIs; local media paths may be uploaded to its media storage.

Mitigation: Avoid sending sensitive prompts or media unless their use with the dLazy service is appropriate for your context.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-image-social-media)
- [dLazy CLI project reference](https://github.com/dlazy-ai/cli)
- [dLazy CLI on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Image-generation prompts, Generated images and links]

**Output Format:** [Structured Markdown with platform checks, layout plans, short in-image copy, separate captions, and generated image links or assets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [In-image headlines are kept under 10 words; captions are returned separately. Platform-specific aspect ratios and safe areas guide the design.]

## Skill Version(s):

1.3.42 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
