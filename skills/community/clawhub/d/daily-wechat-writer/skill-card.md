## Description:

Generates and uploads daily sincere, concise WeChat articles on trending AI and human-interest topics with matched AI images, triggered at 10 AM or on command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robertstarry-gif](https://clawhub.ai/user/robertstarry-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and operators use this skill to receive daily Chinese topic pitches, generate WeChat article drafts with section-matched images, and upload selected drafts for review. It supports scheduled daily operation and manual topic selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Markdown image references can cause local files or unrestricted remote downloads to be transmitted to WeChat.

Mitigation: Use only trusted Markdown, review every image URL and local image path before upload, and run the skill in a restricted environment.

Risk: Credential-file use, scheduling behavior, and simulated parts of the writing workflow may not be clear to operators.

Mitigation: Confirm credential storage, scheduled execution, and the actual draft-generation path before enabling routine use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/robertstarry-gif/skills/daily-wechat-writer)
- [Publisher profile](https://clawhub.ai/user/robertstarry-gif)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and console text with generated article drafts, topic choices, image references, and upload status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require WeChat credentials and a Google Imagen API key; generated article drafts should be reviewed before publication.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
