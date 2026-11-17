## Description:

Feishu Messaging.Bak helps agents send Feishu messages, look up chats and group members, and use Feishu Open Platform examples for related messaging workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[make453](https://clawhub.ai/user/make453)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send Feishu messages, find chat or group member identifiers, and troubleshoot failed message delivery through Feishu Open Platform APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled executable scripts contain hardcoded Feishu application credentials.

Mitigation: Remove and rotate embedded secrets before use, and require users to provide their own least-privilege Feishu credentials through environment variables or a secret manager.

Risk: Scripts can access contact-directory or profile data and may print employee identifiers, emails, phone numbers, or token fragments.

Mitigation: Document required permissions, limit credentials to the minimum Feishu scopes needed, and redact personal or credential-derived data from logs.

Risk: Running the scripts against a real Feishu tenant may send messages or upload content using the configured app.

Mitigation: Review target tenant, recipient identifiers, and app permissions before execution; test only in an approved tenant or sandbox.

## Reference(s):

- [Feishu Open Platform API documentation](https://open.feishu.cn/document/server-docs/api-call-guide/server-api-list)
- [ClawHub skill page](https://clawhub.ai/make453/skills/feishu-messaging-bak)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with API examples, code snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Feishu API calls or commands that send messages, retrieve user details, or inspect chat membership when executed.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog; artifact _meta.json reports 0.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
