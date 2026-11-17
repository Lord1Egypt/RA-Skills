## Description:

输入一张图像，对其中的电动自行车进行检测，输出图片中所有目标的检测框、置信度和标签。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to send an image URL or base64-encoded image to a remote API and receive e-bike detection labels, bounding boxes, and confidence values.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image content or image URLs are sent to the Xiaobenyang remote API.

Mitigation: Avoid submitting sensitive images and review the service's data handling before use.

Risk: The API key may be stored in a plaintext .env file.

Mitigation: Use a scoped or revocable key and protect or remove the .env file after use.

Risk: The release evidence reports stale unrelated Gaokao configuration remnants.

Mitigation: Ask the publisher to remove unrelated configuration before relying on the skill in a managed environment.

Risk: Dependencies are not locked in the artifact.

Mitigation: Install in an isolated environment and pin dependencies during deployment review.

## Reference(s):

- [Xiaobenyang service](https://xiaobenyang.com)
- [Xiaobenyang API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [Text summary derived from raw JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Xiaobenyang API key and an image URL or base64-encoded image.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
