## Description:

Downloads files such as videos, images, documents, and audio from Feishu messages to local storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cindypapa](https://clawhub.ai/user/cindypapa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to download Feishu message attachments for local editing, archiving, content publishing, or AI processing workflows. It supports message URLs or explicit message IDs and file keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe filenames can write or overwrite files outside the intended download folder.

Mitigation: Reject absolute paths and parent-directory components, constrain writes to the resolved output directory, and prevent unintended overwrites.

Risk: Large or stalled downloads can consume excessive time, bandwidth, or disk space.

Mitigation: Add request timeouts, download size limits, and storage checks before installing broadly.

Risk: Feishu app credentials grant access to message resources.

Mitigation: Use a narrowly scoped Feishu app secret and run the skill in a workspace where downloaded files cannot damage important local data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cindypapa/skills/feishu-message-download)
- [Publisher profile](https://clawhub.ai/user/cindypapa)
- [Feishu Open Platform documentation](https://open.feishu.cn/document/ukTMukTMukTM/uEjNwUjLxYDM14SM2ATN)
- [Feishu Message API](https://open.feishu.cn/document/ukTMukTMukTM/uYjNwUjL2YDM14iN2ATN)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with Python and shell examples; downloaded files are written to local storage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, requests, Feishu app credentials, and message resource permissions.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
