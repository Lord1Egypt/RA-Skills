## Description:

Send messages and files to Feishu (Lark) via Open API. Supports text, markdown, any file format, and images. Use when user needs to send notifications, reports, or any content to Feishu/Lark groups or chats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhendexuebuhui](https://clawhub.ai/user/zhendexuebuhui)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to send selected notifications, reports, text, markdown, local files, and images to configured Feishu/Lark chats from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured Feishu credentials could be exposed if stored in an untrusted environment file or copied into prompts, logs, or shared files.

Mitigation: Keep the Feishu app secret in a trusted environment file and avoid passing untrusted --env paths.

Risk: Text, images, or local files could be sent to the wrong chat or disclosed when that sharing was not intended.

Mitigation: Verify the destination chat ID before sending sensitive material and do not send secrets or private files unless disclosure is intended.

## Reference(s):

- [Feishu Open Platform](https://open.feishu.cn/app)
- [Feishu Open APIs](https://open.feishu.cn/open-apis)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code]

**Output Format:** [Markdown usage guidance with Python and shell command examples; runtime sends Feishu/Lark messages and returns API or CLI status output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FEISHU_APP_ID, FEISHU_APP_SECRET, and FEISHU_CHAT_ID or an explicit chat ID before messages or files can be sent.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
