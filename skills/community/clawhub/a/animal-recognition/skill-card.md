## Description:

对含有动物的图像进行标签识别，无需任何额外输入，输出动物的类别标签。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xby-skill](https://clawhub.ai/user/xby-skill)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit an animal image by URL or base64 data and receive animal category labels from the xiaobenyang.com API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images, image URLs, base64 image data, and API credentials are sent to xiaobenyang.com infrastructure.

Mitigation: Use only images, URLs, and API keys that are approved for that service; avoid sensitive photos and internal URLs.

Risk: The API key is stored as plaintext in a local .env file.

Mitigation: Protect the workspace from sharing or commits that include .env, and rotate the key if exposure is possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xby-skill/skills/animal-recognition)
- [XiaoBenYang API Key Portal](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [JSON tool result summarized as concise text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an image URL or base64-encoded image and an XBY_APIKEY before calling the remote API.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
