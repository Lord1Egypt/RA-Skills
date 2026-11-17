## Description:

Generates images with Aliyun Tongyi Wanxiang when the user prompt starts with the dedicated trigger phrase "千问画个图".

This skill is ready for commercial/non-commercial use.

## Publisher:

[roykingw](https://clawhub.ai/user/roykingw)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn short Chinese image requests into expanded prompts, call Aliyun Tongyi Wanxiang, and receive the saved local image path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide a cloud API key in chat and stores it permanently in a plaintext local file.

Mitigation: Use a dedicated low-privilege Alibaba or DashScope key with spending limits, avoid real long-lived credentials in chat, and replace plaintext key storage before routine use.

Risk: The skill installs the Python requests dependency at runtime if it is missing.

Mitigation: Review and preinstall dependencies in a controlled environment, or remove runtime package installation before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/roykingw/skills/aliyun-image-generator)
- [Aliyun Bailian Console](https://bailian.console.aliyun.com/)
- [DashScope Text-to-Image API Endpoint](https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Plain text or Markdown with shell commands and local image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates PNG images through Aliyun Tongyi Wanxiang and reports the saved local path.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
