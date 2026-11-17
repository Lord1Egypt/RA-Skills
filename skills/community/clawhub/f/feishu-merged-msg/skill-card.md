## Description:

Fetch and parse Feishu merged/forwarded messages (合并转发消息). Activate when a Feishu message shows "Merged and Forwarded Message" with no readable content, or when you need to retrieve sub-messages from a merge_forward message type.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deadblue22](https://clawhub.ai/user/deadblue22)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to retrieve unreadable Feishu merge_forward messages, parse their sub-messages, and summarize forwarded conversation threads for users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu app credentials may be exposed because the skill reads local OpenClaw configuration and passes app_id and app_secret to a shell script.

Mitigation: Install only when credential access is acceptable; prefer a safer version that avoids printing appSecret, avoids command-line secret arguments, and limits credential use to the requested message retrieval task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deadblue22/skills/feishu-merged-msg)
- [Feishu tenant access token endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu message retrieval endpoint](https://open.feishu.cn/open-apis/im/v1/messages/{message_id})

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, JSON, Markdown, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON response parsing]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include summarized conversation text, sender details, mentions, and notes about inaccessible image_key references.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
