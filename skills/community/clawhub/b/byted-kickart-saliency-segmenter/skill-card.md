## Description:

Performs image cutout and background removal by uploading image files to Volcengine services, polling batch segmentation jobs, and returning subject and mask outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to remove image backgrounds and generate subject and mask outputs for uploaded JPEG, PNG, or WEBP images. It supports single-image and batch workflows through local files, URLs, or ZIP inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide cloud AK/SK credentials through chat and may print credential-related environment values.

Mitigation: Do not paste secrets into chat; require environment- or secret-manager-based credentials and redact credential values from all user-visible output and logs.

Risk: The skill can execute server-supplied update commands during version checks.

Mitigation: Disable automatic command execution and allow only verified, publisher-signed update commands after explicit review.

Risk: Dependencies are partly unpinned or range-pinned.

Mitigation: Install only from a reviewed lockfile or pinned dependency set before deployment.

Risk: The skill can register or mutate account package state with weak user control.

Mitigation: Document account changes clearly and require explicit user approval before package registration or account-state mutation.

Risk: Authorization data and request or response details may be written to local logs.

Mitigation: Redact authorization headers and sensitive payload fields before logging, and restrict log retention and access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-kickart-saliency-segmenter)
- [Volcengine IAM key management](https://console.volcengine.com/iam/keymanage)
- [Volcengine Kickart package management](https://console.volcengine.com/kickart/fusion/setting/combobuy?tab=combo)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON status data, and local image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes batch result JSON under /tmp/openclaw/byted-kickart-saliency-segmenter/output and downloads subject.png and mask.png files under ~/.openclaw/media/outbound/<task_id>/.]

## Skill Version(s):

1.0.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
