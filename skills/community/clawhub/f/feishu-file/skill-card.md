## Description:

Send local files to Feishu chats. Supports uploading and sending any file type as a Feishu file message.

This skill is ready for commercial/non-commercial use.

## Publisher:

[franklu0819-lang](https://clawhub.ai/user/franklu0819-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to upload a chosen local file to Feishu and send it to a user, group, or email receiver from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user may accidentally upload a secret, private file, or unintended path to Feishu.

Mitigation: Confirm the file path before invocation and avoid sending credentials, private documents, or other sensitive local files unless the transfer is intended.

Risk: A file may be sent to the wrong Feishu receiver or receiver type.

Mitigation: Verify the receiver ID and receiver type before sending, especially when overriding the configured default receiver.

Risk: Feishu app credentials can authorize file upload and message sending.

Mitigation: Use a tightly scoped Feishu app configuration and protect FEISHU_APP_ID and FEISHU_APP_SECRET as secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/franklu0819-lang/skills/feishu-file)
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu file upload API](https://open.feishu.cn/open-apis/im/v1/files)
- [Feishu message send API](https://open.feishu.cn/open-apis/im/v1/messages)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Configuration]

**Output Format:** [Terminal text from a Bash script, with JSON Feishu API responses shown on failure.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, FEISHU_APP_ID, FEISHU_APP_SECRET, and a local file path; accepts optional receiver ID and receiver type.]

## Skill Version(s):

1.0.1 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
