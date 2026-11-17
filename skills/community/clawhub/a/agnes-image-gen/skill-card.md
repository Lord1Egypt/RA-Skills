## Description:

Agnes Image Gen helps agents generate and edit images with Agnes AI, supporting text-to-image and image-to-image prompts, size selection, endpoint failover, and local result saving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiuwu2495](https://clawhub.ai/user/jiuwu2495)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request creative, marketing, product visualization, social media, and image transformation assets through Agnes text-to-image or image-to-image workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill ships with and automatically uses a hardcoded Agnes API key.

Mitigation: Remove the embedded key, rotate it as compromised, and require a user-provided key through a secure environment variable or explicit per-run configuration.

Risk: Prompts and selected local images are sent to Agnes servers for generation or editing.

Mitigation: Warn users before use and avoid sending confidential prompts, private images, or regulated data unless the deployment has approved Agnes for that data.

Risk: Generated outputs may be saved locally and returned image URLs may be time-limited.

Mitigation: Disclose saved file locations, apply local file handling policy, and download required results promptly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiuwu2495/skills/agnes-image-gen)
- [Agnes AI](https://agnes-ai.com)
- [Agnes image generations endpoint](https://apihub.agnes-ai.com/v1/images/generations)
- [Agnes image generations fallback endpoint](https://apihub.agnes-ai.cn/v1/images/generations)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON API responses, generated image URLs, and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save generated PNG files locally and may return time-limited image URLs or base64 image data.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
