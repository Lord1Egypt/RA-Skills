## Description:

使用 Nano Banana Pro 将 Adobe Firefly、Adobe Express 或生成式图片编辑需求迁移为 AI Hive 工作流，覆盖生成扩展、区域替换、背景重构、品牌色适配和 Campaign 变体。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use this skill to turn Adobe Firefly-style image generation and editing requests into AI Hive Nano Banana Pro workflows for expansion, object removal, background reconstruction, brand-color adaptation, and campaign variants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, selected reference images, and the AI Hive API key are sent to the AI Hive service.

Mitigation: Use non-sensitive, approved images and prompts; keep the API key in an environment variable or protected config file; rotate the key if exposure is suspected.

Risk: API responses can choose unvalidated upload and download network destinations.

Mitigation: Run the skill in a virtual environment on a network with limited access to private services, and review generated task links before using outputs in production.

Risk: Image edits can alter protected areas, logos, text, product details, or brand facts.

Mitigation: Compare outputs against the approved reference images, check protected regions and brand elements, and run small batches before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/adobe-firefly-image-generation-editing-alternative)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill submits image generation tasks, can upload approved reference images, and may download generated image files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
