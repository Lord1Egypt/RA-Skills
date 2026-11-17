## Description:

输入一张图像，对其中的手势进行检测，输出图片中所有目标的检测框、置信度和标签。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to detect hand gestures in an image supplied as a URL or base64 data. It returns detected target boxes, labels, and confidence values through the Xiaobenyang API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image URLs or full base64 image data are sent to a remote Xiaobenyang API.

Mitigation: Use only non-sensitive images and confirm that sending the image data to Xiaobenyang is acceptable for the user or organization.

Risk: The API key is stored in a local plaintext .env file.

Mitigation: Use a dedicated low-privilege API key and check .env file contents and permissions before and after use.

Risk: Endpoint configuration can be changed, which could redirect image data and credentials.

Mitigation: Run only in trusted workspaces and verify configuration before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/gesture-detection)
- [ALinkLab publisher profile](https://clawhub.ai/user/alinklab)
- [Xiaobenyang API key site](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown summary of JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are based on raw remote API responses and may include bounding boxes, confidence scores, and labels.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
