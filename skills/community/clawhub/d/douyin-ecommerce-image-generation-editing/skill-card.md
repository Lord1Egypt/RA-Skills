## Description:

为抖音电商、抖店和直播间生成与编辑商品卡主图、SKU 图、卖点证明图、直播商品贴片及千川广告图片，并支持参考图保真与 AI Hive 自动生成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce operators, designers, and developers use this skill to generate or edit Douyin e-commerce product card images, SKU image sets, selling-point proof images, live-commerce overlays, and Qianchuan ad test creatives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, selected product images, and the API key are sent to the configured AI Hive service.

Mitigation: Install only when the AI Hive service is trusted, avoid sensitive product media unless approved, and protect ~/.ai-hive/config.json and AI_HIVE_API_KEY as credentials.

Risk: The API base URL is configurable, so a custom endpoint could receive credentials and uploaded media.

Mitigation: Use the default endpoint or only set a custom base URL after confirming the host is fully trusted.

Risk: The security verdict is suspicious because the endpoint can receive API keys and uploaded media without clear host scoping or warning.

Mitigation: Review the skill and dependency installation in an isolated environment before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/douyin-ecommerce-image-generation-editing)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key access](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash commands; runtime commands return JSON task data and downloaded image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports reference images, batch image generation, routing mode selection, model parameters, output directory selection, and submit-only mode.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact CHANGELOG top entry is 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
