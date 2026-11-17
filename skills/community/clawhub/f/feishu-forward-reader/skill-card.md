## Description:

读取和解析飞书合并转发消息 (merge_forward) 的详细内容，以便在默认仅显示 "Merged and Forwarded Message" 时获取原始消息内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[konce](https://clawhub.ai/user/konce)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to retrieve and parse Feishu merged-forward messages they are authorized to view. It helps turn Feishu API responses into readable text or JSON when forwarded messages otherwise appear only as a placeholder.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Feishu app secrets and message-read access, which can expose sensitive chat contents if used in shared or logged environments.

Mitigation: Prefer environment variables or a protected secret store, avoid command-line secrets in shared shells, and retrieve only messages the user is authorized to view.

Risk: The required Feishu message-read permission can grant broad access to messages available to the app.

Mitigation: Use the narrowest feasible Feishu app permissions and review authorization before installing or running the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/konce/skills/feishu-forward-reader)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON, with shell command examples in Markdown instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Feishu message_id and Feishu app credentials with message-read permissions; optional user-name lookup can be disabled.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
