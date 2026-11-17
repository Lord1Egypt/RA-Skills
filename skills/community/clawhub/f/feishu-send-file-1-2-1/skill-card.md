## Description:

Sends local files or images through a Feishu/Lark bot by uploading ordinary files through the file API and images through the image API before sending the corresponding message type.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kururu111](https://clawhub.ai/user/kururu111)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when normal Feishu/Lark messaging tools send a local path as text instead of delivering the file or image itself. It provides command-line scripts for uploading the local asset, then sending the resulting file_key or image_key to a user or chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to pass Feishu/Lark app secrets on the command line, where local process listings, shell history, or automation logs may expose them.

Mitigation: Use an app with only the required messaging and upload scopes, and adapt execution to read secrets from a protected environment variable, secret manager, or hidden prompt.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kururu111/skills/feishu-send-file-1-2-1)
- [Feishu Open Platform](https://open.feishu.cn)
- [Lark Open Platform](https://open.larksuite.com)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Guidance]

**Output Format:** [Markdown with inline bash commands and Python script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local command invocations that call Feishu/Lark APIs and print upload and message status.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact skill.json version 1.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
