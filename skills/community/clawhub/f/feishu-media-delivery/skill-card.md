## Description:

Delivers already-generated images and videos to Feishu/Lark users and chats using Feishu image and media message flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhy2015](https://clawhub.ai/user/zhy2015)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and multimodal agent operators use this skill to deliver existing image and MP4 outputs to Feishu/Lark users without guessing the required image or media message protocol.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper scripts can upload arbitrary readable local files to a caller-supplied Feishu recipient.

Mitigation: Do not allow untrusted prompts to choose recipient IDs or file paths; restrict execution to an approved generated-media directory and trusted recipients.

Risk: The Feishu app secret is read from an environment-selected or default local secret file.

Mitigation: Protect the secret file, scope the Feishu app permissions, and keep secret-path configuration outside untrusted agent control.

Risk: The Node dependency set should be reviewed before production use.

Mitigation: Pin or update dependencies and review the lockfile as part of release approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhy2015/skills/feishu-media-delivery)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with bash command snippets; helper scripts return JSON Feishu responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Feishu app credentials and a trusted recipient open_id plus local image or MP4 path.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
