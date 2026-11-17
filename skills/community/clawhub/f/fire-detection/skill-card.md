## Description:

检测各类通用场景中出现的火焰，最佳使用场景：安防摄像头、交通摄像头视角。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xby-skill](https://clawhub.ai/user/xby-skill)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to detect fire in images from general scenes, especially security-camera and traffic-camera views. It accepts either an image URL or a base64-encoded image and returns the remote API response for presentation to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends image URLs or base64 image data to a remote image-analysis service.

Mitigation: Use it only with images that are approved for sharing with the remote service, and avoid sensitive security-camera or traffic footage unless that data sharing is acceptable.

Risk: The security review notes local plaintext .env storage for the API key.

Mitigation: Prefer a secure secret mechanism for API keys instead of allowing persistent plaintext storage.

Risk: The security review notes stale gaokao and school-search leftovers in the artifact.

Mitigation: Review the artifact before installation and ask the publisher to remove unrelated leftovers before production deployment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/xby-skill/skills/fire-detection)
- [XiaoBenYang API key site](https://xiaobenyang.com)
- [XiaoBenYang remote API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, Text, JSON, Guidance]

**Output Format:** [Markdown summary of JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an API key and sends image input to a remote service.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
