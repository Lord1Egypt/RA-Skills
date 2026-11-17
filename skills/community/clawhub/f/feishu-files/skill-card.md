## Description:

A simple skill for sending files to Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bingothreed](https://clawhub.ai/user/bingothreed)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to send local image or video files through Feishu by obtaining a tenant access token, uploading media, and sending the resulting message.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to read Feishu app credentials and use bearer tokens in shell commands.

Mitigation: Use a tightly scoped Feishu app, avoid running as root, and prefer a token workflow that does not expose app secrets or bearer tokens in command arguments or logs.

Risk: The skill can send a local file to the wrong Feishu recipient or send the wrong file.

Mitigation: Confirm the exact recipient open_id and file path before each send.

Risk: The skill relies on broad curl commands against Feishu upload and message APIs.

Mitigation: Review commands before execution and grant only the upload and message-sending permissions required for the intended workflow.

## Reference(s):

- [OpenClaw Feishu channel documentation](https://docs.openclaw.ai/channels/feishu)
- [Feishu message API explorer](https://open.feishu.cn/api-explorer/cli_a937fd6055791bca?apiName=create&project=im&resource=message&version=v1)
- [ClawHub skill page](https://clawhub.ai/bingothreed/skills/feishu-files)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Feishu app configuration, a recipient open_id, and a local file path.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
