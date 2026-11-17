## Description:

对包含主体物体的图像进行标签识别，输出主体物体的类别标签，目前已经覆盖了5万多类的物体类别。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to recognize the primary object in an image by sending either an image URL or Base64 image data to the Xiaobenyang API and receiving category labels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys are stored in plaintext .env files, which can be exposed in shared workspaces.

Mitigation: Use non-sensitive workspaces, restrict file access, and rotate the API key if the .env file may have been exposed.

Risk: Images and API keys are sent to Xiaobenyang's API, and XBY_GAOKAO_BASE_URL can change the API origin.

Mitigation: Use only images suitable for third-party processing and review any XBY_GAOKAO_BASE_URL override before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/general-recognition)
- [Xiaobenyang API key site](https://xiaobenyang.com)
- [Xiaobenyang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Guidance]

**Output Format:** [JSON API response summarized as concise text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XBY_APIKEY and accepts an image URL or Base64-encoded image data.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
