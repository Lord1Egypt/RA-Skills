## Description:

AIPing Media helps an agent generate images and videos through the AIPing API, download generated media locally, and send native image or video messages through Feishu with CDN links as a fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haoruilee](https://clawhub.ai/user/haoruilee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users can use this skill to add image and video generation workflows that save media under /tmp and optionally deliver the results to Feishu users or chats. It is suited for media generation tasks where configured AIPing and Feishu credentials are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses AIPing and Feishu credentials and can send generated media to Feishu recipients.

Mitigation: Install only when Feishu delivery is expected, store app credentials carefully, and use explicit recipient IDs for each send operation.

Risk: The skill can fetch media from URLs before uploading to Feishu.

Mitigation: Avoid passing arbitrary or untrusted URLs as media sources; prefer locally generated media paths when possible.

Risk: Generated files left in /tmp may contain sensitive media content.

Mitigation: Treat /tmp outputs as sensitive and remove generated files after they are no longer needed.

## Reference(s):

- [AIPing Media ClawHub page](https://clawhub.ai/haoruilee/skills/aiping-media)
- [AIPing supported models](references/models.md)
- [AIPing API](https://aiping.cn/api/v1)
- [Feishu Open API](https://open.feishu.cn/open-apis)

## Skill Output:

**Output Type(s):** [JSON, Files, API Calls, Shell commands, Configuration guidance]

**Output Format:** [JSON responses with local media paths, Feishu delivery status, and fallback CDN URLs; documentation includes Markdown and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media is downloaded to /tmp by default; Feishu delivery requires configured app credentials and explicit recipient identifiers.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
