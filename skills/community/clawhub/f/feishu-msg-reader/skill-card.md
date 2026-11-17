## Description:

Fetches Feishu message content by message_id, with optional thread context for replies and interactive-card fallback text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deadblue22](https://clawhub.ai/user/deadblue22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to retrieve Feishu message content by message ID, inspect parsed message bodies, and gather thread context when a replied-to message or interactive card placeholder lacks enough detail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Thread retrieval can transiently fetch nearby unrelated messages from the same Feishu chat.

Mitigation: Use the skill only in workspaces where this access is appropriate, and review thread-mode output before sharing or acting on it.

Risk: Passing a tenant access token with --token can expose credentials through local shell history or process listings.

Mitigation: Prefer configured Feishu app credentials or environment variables, and use a least-privileged Feishu app.

Risk: Interactive-card messages only expose fallback or degraded text through the Feishu message API.

Mitigation: Use --thread to inspect surrounding text or post messages when fallback content is incomplete.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/deadblue22/skills/feishu-msg-reader)
- [Feishu Open API Base](https://open.feishu.cn/open-apis)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [JSON from the helper script, with Markdown usage guidance in the skill instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The JSON output may include parsed content for a single message, raw API responses, or a chronological thread array when --thread is used.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
