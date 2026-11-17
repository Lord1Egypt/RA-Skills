## Description:

Turn text into spoken Feishu (Lark) voice messages. Use when the agent should speak in a Feishu group, send voice alerts or announcements, or reply with a playable voice note instead of text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richerlv](https://clawhub.ai/user/richerlv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Cyber Horn to convert an agent's text into a Feishu voice message for group announcements, alerts, or voice-note replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends text and generated audio through external TTS and Feishu services using configured credentials.

Mitigation: Use only with approved Feishu, Edge TTS, or ElevenLabs data flows, and avoid sending secrets, personal data, or regulated content unless that use is approved.

Risk: A default Feishu chat ID can route generated voice messages to an unintended destination if configured incorrectly.

Mitigation: Set FEISHU_DEFAULT_CHAT_ID carefully, prefer explicit chat IDs for sensitive messages, and verify the destination before production use.

Risk: Compromised or over-privileged Feishu credentials could allow unwanted message posting.

Mitigation: Configure a least-privilege Feishu app, protect FEISHU_APP_ID and FEISHU_APP_SECRET, and rotate credentials according to operational policy.

Risk: Pinned dependencies may become outdated before production deployment.

Mitigation: Review and update dependency pins before deploying the skill in a production environment.

## Reference(s):

- [Cyber Horn ClawHub page](https://clawhub.ai/richerlv/skills/cyber-horn)
- [richerlv publisher profile](https://clawhub.ai/user/richerlv)
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu file upload API](https://open.feishu.cn/open-apis/im/v1/files)
- [Feishu message create API](https://open.feishu.cn/open-apis/im/v1/messages)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API calls]

**Output Format:** [CLI arguments and status text; the skill sends a playable Feishu voice message through external services.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Feishu credentials, FFmpeg, and network access to Edge TTS or ElevenLabs and Feishu.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
