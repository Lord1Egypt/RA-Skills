## Description:

为电商运营、商家和内容团队生成或修复 Seedance 2.5 销售视频节拍，围绕商品事实、主张来源、连续性和平台安全区组织提示词与 CLI 调用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce teams, merchants, agencies, and content operators use this skill to plan, preview, submit, and check product sales-video generation or repair jobs. It supports beat-by-beat sales-video creation and fact-preserving repair for channels such as Taobao, Tmall, JD, Douyin, Xiaohongshu, Amazon, TikTok Shop, Instagram, Shopify, Reels, Shorts, and product listing videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys can be exposed through shell history or weak local handling.

Mitigation: Use AI_HIVE_API_KEY or a protected config workflow, install in a virtual environment, and prefer pinned dependencies when available.

Risk: Media files supplied to generation or repair commands may be uploaded to AI Hive.

Mitigation: Use preview mode before submission and provide only product images or videos that are approved and intended for upload.

Risk: Generated sales videos can imply unsupported product claims, altered product facts, or channel-policy issues.

Mitigation: Require approved claim or offer sources, continuity locks, explicit reject rules, and a final review against the target platform's current publishing policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ecommerce-viral-sales-video-generation-editing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and optional JSON preview output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preview mode can show the selected model, prompt, media inputs, and params before upload; execution may create AI Hive video tasks and save MP4 results.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
