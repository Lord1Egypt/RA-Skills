## Description:

通过 Flyelep AI 接口将图片中的商品替换为指定商品，同时保留原图背景与光影。

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyelepai](https://clawhub.ai/user/flyelepai)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要制作商品展示图的用户，在保留原场景和光影的同时，将图片中的商品替换为目标商品。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence rates the skill suspicious because scanners report a mismatch between its stated image-editing purpose and reported behavior.

Mitigation: Review the reported upload destination and the skill's behavior before installing.

Risk: The security evidence notes a possible data-loss risk in the Windows workflow; the scan was partial and some local references could not be resolved.

Mitigation: Review the Windows temporary-file workflow before use, and account for the scan's incomplete coverage.

## Reference(s):

- [ClawHub product-replace skill release](https://clawhub.ai/flyelepai/skills/flyelep-product-replace)
- [Flyelep product replacement API](https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/productReplace)
- [Flyelep image upload API](https://www.flyelep.cn/prod-api/poster-design/api/v1/file/upload)

## Skill Output:

**Output Type(s):** [API Calls, Image URLs, Guidance]

**Output Format:** [HTTP POST requests with JSON or multipart form data; a JSON response containing result image URL(s)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided source and target image URLs, prompt, and API key; returns image URL(s) for direct presentation.]

## Skill Version(s):

1.0.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
