## Description:

输入一张图像，对其中的手机进行检测，输出图片中所有目标的检测框、置信度和标签。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xby-skill](https://clawhub.ai/user/xby-skill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to send an image URL or base64 image data to a phone-detection service and receive detected phone labels, confidence scores, and bounding boxes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends image URLs or full image contents to an external Xiaobenyang API.

Mitigation: Avoid sensitive images unless the publisher's data handling terms are acceptable for the use case.

Risk: The security summary reports insecure plaintext API key persistence.

Mitigation: Use a restricted or disposable API key and prefer secure secret storage before deployment.

Risk: The security summary reports mismatched configuration from another service.

Mitigation: Review configuration names, defaults, and service identifiers before installation.

Risk: Dependencies are version-ranged rather than pinned.

Mitigation: Pin and review dependencies in controlled environments before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xby-skill/skills/cellphone-detection)
- [Xiaobenyang API Key Site](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [Markdown summary of JSON detection results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns phone labels, confidence scores, and bounding boxes from an external API.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
