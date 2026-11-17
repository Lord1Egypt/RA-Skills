## Description:

Image replicate tool: analyzes the visuals, composition, colors, lighting, and style of the source image, builds a replicate prompt, and hands it off to Seedream 4.5 to generate a new image in the same style. 图像仿写工具：分析原图的视觉效果、构图、色彩、光影和风格，生成重绘提示词，并交给 Seedream 4.5 生成具有相同风格的新图像。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to analyze a reference image, create a prompt that reflects its visual style, and request a newly generated image through dLazy's hosted service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan could not verify the declared image workflow, reported a mismatch involving login behavior, and had unavailable resources.

Mitigation: Review the skill’s purpose and installation details before use if these scan uncertainties matter to you.

Risk: Prompts and local image files supplied to the skill are sent to dLazy-hosted services for processing.

Mitigation: Only submit prompts and images that are appropriate to upload to dLazy’s services.

## Reference(s):

- [Repository link listed in skill metadata](https://github.com/dlazy-ai/cli)
- [dLazy CLI on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy website](https://dlazy.com)
- [ClawHub release page](https://clawhub.ai/dlazyai/skills/dlazy-image-replicate)

## Skill Output:

**Output Type(s):** [Images, JSON, Shell commands]

**Output Format:** [Generated image assets with a JSON response containing output URLs or asynchronous task status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated assets are hosted by dLazy; asynchronous requests may first return a task identifier.]

## Skill Version(s):

1.3.42 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
