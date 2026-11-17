## Description:

输入一张图像，对其中的人/宠物/车/火焰/纸箱进行检测，输出图片中所有目标的检测框、置信度和标签。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xby-skill](https://clawhub.ai/user/xby-skill)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to send an image URL or base64-encoded image to a remote object detection API and receive labels, confidence values, and bounding boxes for people, pets, cars, fire, and cartons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image URLs or full base64 image data are sent to the XiaoBenYang remote API.

Mitigation: Avoid sensitive or private images unless the user accepts that remote processing path.

Risk: The XiaoBenYang API key is stored in a local plaintext .env file.

Mitigation: Use a disposable or tightly scoped API key and review local .env file permissions before use.

Risk: The release evidence reports mismatched, under-scoped API configuration.

Mitigation: Verify the endpoint and MCP tool configuration before installation or operational use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xby-skill/skills/daily-object-detection)
- [XiaoBenYang API Key Portal](https://xiaobenyang.com)
- [XiaoBenYang MCP API Endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, configuration guidance]

**Output Format:** [Markdown text summarizing JSON detection results from a remote API.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key; image input is provided as either a URL or a base64 string.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
