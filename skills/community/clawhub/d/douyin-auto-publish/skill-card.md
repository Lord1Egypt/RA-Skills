## Description:

Helps an OpenClaw agent upload and publish videos to the Douyin Creator Platform after the user provides the file path, title, visibility, and explicit pre-publication confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[l1angjy](https://clawhub.ai/user/l1angjy)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and operators use this skill to guide an agent through uploading a local video to Douyin, filling in title and visibility settings, and publishing only after explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish through a logged-in Douyin creator account.

Mitigation: Require the agent to show the file name, title, and visibility and obtain explicit user confirmation before every publish.

Risk: A persistent browser profile can retain account access between sessions.

Mitigation: Use the sandbox browser target when stronger isolation is needed, accepting that the user may need to log in each time.

Risk: Unsafe file-staging instructions may be risky for unusual or untrusted file paths.

Mitigation: Use only trusted local video paths and verify the staged file before upload.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/l1angjy/skills/douyin-auto-publish)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [Douyin Creator Platform](https://creator.douyin.com/creator-micro/home)
- [Douyin upload page](https://creator.douyin.com/creator-micro/content/upload)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with browser-tool actions and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided video path, title, visibility selection, and explicit confirmation before publishing.]

## Skill Version(s):

2.2.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
