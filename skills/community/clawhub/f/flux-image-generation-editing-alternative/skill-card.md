## Description:

使用 Nano Banana Pro 将 FLUX、Black Forest Labs、FLUX.1、FLUX Dev、Schnell、Pro 或相关图片生成编辑需求迁移到 AI Hive，保留长提示词语义、商品准确性、参考图职责和交付画幅。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Image-generation users and developers use this skill to migrate FLUX-style text-to-image, image-to-image, product advertising, reference-image, and controlled-editing workflows to AI Hive with Nano Banana Pro. It helps preserve prompt priorities, product facts, reference-image roles, and output aspect ratios during generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts and selected reference images to AI Hive.

Mitigation: Use non-sensitive reference images unless sharing them with AI Hive is acceptable.

Risk: The skill downloads generated results from AI Hive-provided storage URLs without validating those destinations.

Mitigation: Run it in a controlled environment, review downloaded files before reuse, and prefer a dedicated limited API key.

Risk: The package does not pin its Python dependency.

Mitigation: Install dependencies in a virtual environment and review the resolved requests package before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/flux-image-generation-editing-alternative)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code]

**Output Format:** [Markdown guidance with bash command examples and CLI-generated JSON or downloaded image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a fixed AI Hive image model, accepts optional reference images, can submit generation jobs, query task status, upload images, and download generated results.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
