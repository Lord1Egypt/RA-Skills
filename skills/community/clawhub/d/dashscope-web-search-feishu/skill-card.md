## Description:

Searches the web with DashScope Qwen and can send requested image results into Feishu chats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oreo992](https://clawhub.ai/user/oreo992)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to answer requests that need current web information, including optional image searches for Feishu conversations. It supports quick search, deeper retrieval, site filters, freshness filters, and Feishu image delivery when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to DashScope and image content can be uploaded to Feishu.

Mitigation: Use the skill only when that data sharing is acceptable for the conversation and organization.

Risk: The Feishu image pipeline was flagged for unsafe network and token-storage practices.

Mitigation: Before image-mode deployment, re-enable TLS verification, validate image URLs, enforce response size and type checks, and store tokens in a private per-user cache.

Risk: Image mode can send content directly to a Feishu chat.

Mitigation: Require clear user confirmation and a verified chat identifier before sending images.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oreo992/skills/dashscope-web-search-feishu)
- [DashScope](https://dashscope.aliyuncs.com/)
- [DashScope Console](https://dashscope.console.aliyun.com/)
- [Feishu Open Platform](https://open.feishu.cn/app/)
- [OpenClaw](https://github.com/nicepkg/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with citation markers, optional Markdown image references, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text mode returns sourced web-search answers; image mode can upload and send image results to Feishu when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
