## Description:

MCP服务器提供从本地文件、URL提取图像并转换为base64格式的功能，适用于LLM分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to route image inputs from local files, web URLs, or base64 payloads to the XiaoBenYang API for LLM-oriented visual analysis and conversion workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted images, image URLs, base64 payloads, and local path strings are sent to an external XiaoBenYang API.

Mitigation: Avoid using the skill with screenshots, documents, IDs, credentials, private URLs, sensitive project paths, or other confidential material unless appropriate privacy disclosures and consent controls are in place.

Risk: The required service API key is stored in a local plaintext .env file.

Mitigation: Use a dedicated low-privilege API key, restrict local file permissions, rotate the key if exposed, and remove it from .env when the skill is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/extract-image)
- [XiaoBenYang service](https://xiaobenyang.com)
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON, Guidance]

**Output Format:** [Markdown summary of JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key and may return raw upstream API payloads.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
