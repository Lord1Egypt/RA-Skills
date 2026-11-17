## Description:

Generates and edits ecommerce main product image candidates with Nano Banana Pro using product evidence, channel constraints, SKU controls, and single-variable testing guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators, marketplace sellers, and developers use this skill to create white-background, scene, SKU, and A/B-test product image candidates while preserving product facts and platform-review constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote API response fields can influence local downloads and file paths.

Mitigation: Review the skill before installing, prefer an isolated Python environment, and avoid running it in sensitive networks or directories until result URL validation and safe filename containment are added.

Risk: Reference images provided to generation commands are uploaded to AI Hive.

Mitigation: Use only an AI Hive account and images that are intended for upload, and review command inputs before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ecommerce-bestseller-main-image-generation-editing)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive account and API key page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline bash commands and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses fixed Nano Banana Pro image generation through AI Hive and can save generated results to a local output directory.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
