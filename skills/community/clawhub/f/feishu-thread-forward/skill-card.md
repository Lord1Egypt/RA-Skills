## Description:

Forward Feishu thread or topic content to a user, group, or topic through the Feishu Open API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deadblue22](https://clawhub.ai/user/deadblue22)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to forward Feishu thread-level conversations when a topic must be shared or cross-posted to another user, group, or topic while preserving thread context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu thread content may be forwarded to an unintended or unauthorized audience.

Mitigation: Verify the source thread, destination ID, and audience authorization before executing the forward request.

Risk: Feishu app credentials could be exposed or over-privileged.

Mitigation: Use least-privilege Feishu app credentials and keep app IDs, secrets, and access tokens out of prompts, logs, and copied outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deadblue22/skills/feishu-thread-forward)
- [Feishu thread forward API](https://open.feishu.cn/open-apis/im/v1/threads/{thread_id}/forward?receive_id_type={type})
- [Feishu message retrieval API](https://open.feishu.cn/open-apis/im/v1/messages/{message_id})
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Feishu thread or message identifiers, a target receive ID, receive ID type, and Feishu app credentials.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
