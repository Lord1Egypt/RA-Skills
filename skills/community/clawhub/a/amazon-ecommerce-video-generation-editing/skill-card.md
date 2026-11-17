## Description:

Create and edit Amazon product videos, listing demos, storefront brand clips and advertising video assets for Amazon商品视频, Listing Video, Product Detail Page video, Sponsored Brands Video, Amazon Store, 开箱, 安装演示, 功能说明 and cross-border localization, with support for text/image/reference-to-video, editing, extension and AI Hive delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, marketplace operators and ecommerce creative teams use this skill to generate, edit, localize and review product-first Amazon listing, storefront and advertising video assets. It emphasizes source-sheet accuracy, supported claims, marketplace-ready text and rights checks before upload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials can be sent to a configurable service endpoint.

Mitigation: Use a dedicated low-privilege AI Hive API key and set a custom base URL only when the endpoint is controlled and trusted.

Risk: Generated downloads can overwrite files if task metadata or result origins are malicious.

Mitigation: Run the skill in an isolated workspace, use a dedicated output directory, and prefer no-download mode until task origin and filename handling are validated.

Risk: Generated product videos may introduce unsupported claims, certifications, rankings, discounts or marketplace-specific text.

Mitigation: Review outputs against the merchant-approved source sheet, current marketplace requirements, approved copy and media rights before upload.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/amazon-ecommerce-video-generation-editing)
- [AI Hive API base URL referenced by the skill](https://ai-hive.iclip.cn/api)
- [AI Hive API access page referenced by the skill](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI-generated task JSON or downloaded media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can submit video generation or editing tasks, poll task status, upload media inputs and download generated video or image outputs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
