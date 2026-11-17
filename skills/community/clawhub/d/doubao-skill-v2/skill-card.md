## Description:

Provides Bash commands for using Volcengine ARK Doubao APIs to generate images, edit images, generate videos, and check generation task status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenkangwei](https://clawhub.ai/user/wenkangwei)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to invoke Doubao image and video generation workflows from an agent or shell environment. It supports text-to-image, image editing, text-to-video, asynchronous task tracking, and local media downloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Volcengine ARK API key, and the security guidance warns that unsafe handling could expose the user's Volcengine account.

Mitigation: Use a restricted, rotatable ARK key; do not paste or share full ARK_API_KEY values; and prefer a safer secret store over common shell startup files.

Risk: Prompts, image URLs, task metadata, and generated media URLs are sent to Volcengine.

Mitigation: Avoid submitting sensitive or confidential content unless the user has approved that third-party processing.

Risk: The skill promotes watermark-removal examples.

Mitigation: Use watermark-removal workflows only for content the user owns or is explicitly authorized to modify.

Risk: Security guidance recommends avoiding exposure to untrusted prompts until JSON encoding is fixed.

Mitigation: Limit use to trusted prompts and image URLs, and review input handling before exposing the wrapper to untrusted users.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wenkangwei/skills/doubao-skill-v2)
- [Volcengine ARK API Documentation](https://www.volcengine.com/docs/82379/1520757?lang=zh#y2hhTyHB)
- [Volcengine ARK Console](https://console.volcengine.com/ark)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [JSON responses, local media files, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return task IDs, generated media URLs, and local paths under data/.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata; artifact frontmatter/config report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
