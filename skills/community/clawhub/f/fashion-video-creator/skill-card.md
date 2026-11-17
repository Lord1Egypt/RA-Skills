## Description:

Generates fashion e-commerce video assets, including virtual model image prompts, Seedance 2.0 video prompts, dialogue, scene guidance, and Jimeng operator SOPs for single or batch workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, e-commerce operators, and developers use this skill to assemble virtual fashion showcase assets: model-generation prompts, Seedance video prompts, dialogue scripts, camera and scene choices, and step-by-step Jimeng operating guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable API keys may be exposed if pasted into chat.

Mitigation: Provide credentials through a local environment variable or secret manager, use a low-scope key with quotas, and rotate any key previously shared in conversation.

Risk: Prompts and product details may be sent to an external image generation service.

Mitigation: Avoid confidential product plans, personal data, and real-person likeness requests unless the user has approved that external processing.

Risk: Generated fashion assets may not preserve garment color, pattern, texture, or style accurately.

Mitigation: Use the skill's generated quality checklist and review model images, video prompts, upload order, and brand-preservation constraints before publishing.

## Reference(s):

- [Model Presets & Realism System](references/model-presets.md)
- [Seedance Prompt Assembly Rules](references/prompt-assembly.md)
- [Dialogue Library](references/dialogue-library.md)
- [Seedream API Call Specifications](references/seedream-api.md)
- [Volcano Engine Ark API Endpoint](https://ark.cn-beijing.volces.com)
- [Jimeng Video Generation Platform](https://jimeng.jianying.com)
- [ClawHub Skill Page](https://clawhub.ai/dingtom336-gif/skills/fashion-video-creator)

## Skill Output:

**Output Type(s):** [text, markdown, image, shell commands, configuration, guidance]

**Output Format:** [Markdown with generated prompts, SOP steps, configuration details, and optional code or shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include single-task or batch outputs, degraded prompt-only mode when image generation fails, and operator quality checklists.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
