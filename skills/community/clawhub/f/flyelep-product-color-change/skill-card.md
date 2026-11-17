## Description:

通过 Flyelep AI 工具接口识别图片中的商品并进行换色处理。

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyelepai](https://clawhub.ai/user/flyelepai)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要处理商品展示图的用户：当用户要求只更改商品颜色时，智能体可调用 Flyelep 接口生成换色图片并返回结果链接。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image data is uploaded to Flyelep, and the security review advises caution because the scan is partial.

Mitigation: Confirm Flyelep is the intended destination and obtain the user's approval before uploading an image.

Risk: The instructions use and remove a fixed temporary payload filename.

Mitigation: Check for an existing payload_temp.json before writing or deleting it, or use a unique temporary filename.

## Reference(s):

- [Flyelep Product Color Change API](https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/productColorChange)

## Skill Output:

**Output Type(s):** [API Calls, Text]

**Output Format:** [JSON API request and returned image URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a URL for the recolored image.]

## Skill Version(s):

1.0.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
