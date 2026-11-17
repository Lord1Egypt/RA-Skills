## Description:

Feishu Video Message helps agents upload local or remote videos to Feishu chats as playable media messages with optional cover image and duration metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vivila-yxx](https://clawhub.ai/user/vivila-yxx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a Feishu chat workflow needs to send a local video file or a trusted remote video URL to the current chat. It is suited for Feishu/OpenClaw deployments that can provide the required chat identifier, Feishu credentials, Python runtime, and ffmpeg tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary remote video URLs and forward the downloaded content to Feishu using local app credentials.

Mitigation: Use only trusted public HTTPS video URLs until URL allowlisting, private-network blocking, and redirect validation are enforced.

Risk: Remote video downloads may bypass the documented 30 MB size expectation because evidence.security notes no strong size limit.

Mitigation: Pre-check source size and content type before invocation, and enforce a deployment-level download size cap.

Risk: The skill reads local Feishu app credentials from ~/.openclaw/openclaw.json and can send media to the supplied destination.

Mitigation: Restrict credentials to the minimum required Feishu app scope and pass only explicit current-chat receive IDs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vivila-yxx/skills/feishu-video-message)
- [Feishu Upload Image API](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/image/create)
- [Feishu Upload File API](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/file/create)
- [Feishu Send Message API](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/create)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Command-line invocation with Feishu media message side effects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, ffmpeg, ffprobe, network access, Feishu credentials from ~/.openclaw/openclaw.json, and an explicit receive-id.]

## Skill Version(s):

1.0.2 (source: server release metadata, SKILL.md frontmatter, clawdis.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
