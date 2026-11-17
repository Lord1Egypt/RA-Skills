## Description:

使用智谱AI的CogView模型生成图片，支持中文提示词自动翻译为英文、自定义图片尺寸，并在首次使用时引导用户配置智谱API密钥。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yzh-q](https://clawhub.ai/user/yzh-q)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request image generation through Zhipu AI CogView, including Chinese prompts that should be translated and submitted with a supported image size.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and translated prompts may be sent to the external Zhipu CogView API.

Mitigation: Do not include secrets, confidential business information, or sensitive personal data in prompts.

Risk: The skill references a PowerShell script that may not be present in every installed package or runtime environment.

Mitigation: Verify that scripts/generate_image.ps1 is available before relying on the skill for image generation.

Risk: Generated image URLs may expire after about 24 hours.

Mitigation: Save required generated assets promptly when retention is needed.

## Reference(s):

- [Zhipu AI Open Platform](https://open.bigmodel.cn/)
- [ClawHub skill page](https://clawhub.ai/yzh-q/skills/cogview-image-gen)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with PowerShell command examples, configuration guidance, and generated image URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated image URLs are described as temporary and valid for about 24 hours.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
