## Description:

1-Click WOA helps an agent create WeChat Official Account draft articles from Markdown or text by retrieving a token, uploading configured images, creating the draft, and generating an HTML fallback when draft submission fails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanbo00701](https://clawhub.ai/user/yanbo00701)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and content teams use this skill to prepare WeChat Official Account drafts from supplied article content and configured image assets. It is intended for accounts where the user can provide WeChat AppID and AppSecret credentials and review the resulting draft before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive WeChat AppID and AppSecret credentials.

Mitigation: Store credentials with owner-only permissions and rotate secrets if they may have been exposed.

Risk: The skill uploads configured images and article content automatically with weak safeguards.

Mitigation: Confirm the target account, article content, and image set before running the workflow.

Risk: Fallback HTML can carry untrusted article content into a browser or publishing workflow.

Mitigation: Avoid opening fallback HTML generated from untrusted input and review the file before copying it into WeChat.

Risk: The security guidance says to expect WeChat draft creation and not to rely on the workflow for real Markdown conversion.

Mitigation: Review the generated draft or fallback HTML before publishing and verify formatting manually.

## Reference(s):

- [1-Click WOA setup guide](references/SETUP.md)
- [1-Click WOA troubleshooting guide](references/TROUBLESHOOTING.md)
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com/)
- [ClawHub skill page](https://clawhub.ai/yanbo00701/skills/1-click-woa)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration; script execution returns plain-text status and may generate an HTML fallback file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May upload configured images and create a WeChat draft; successful runs report a media_id and preview link.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
