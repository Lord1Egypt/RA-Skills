## Description:

Uploads files, images, videos, and attachments to Feishu or Lark Bitable and returns a file_token, using direct upload for files up to 20MB and chunked upload for larger files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billzhuang6569](https://clawhub.ai/user/billzhuang6569)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to upload authorized files to Feishu or Lark Bitable when they need a reusable Drive file_token for later attachment-field updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu App Secret can be exposed through shell history or process inspection when passed with --app-secret.

Mitigation: Prefer a secret manager or tightly controlled environment variables, and avoid placing secrets directly in command lines.

Risk: Tenant access token prefixes and upload responses may appear in execution logs.

Mitigation: Restrict access to logs, redact sensitive output, and remove token-prefix logging before broad deployment.

Risk: The script can upload local files to Feishu using supplied credentials.

Mitigation: Run it only for files the user is authorized to upload and confirm the target Bitable parent node before execution.

## Reference(s):

- [Feishu Open Platform](https://open.feishu.cn)
- [ClawHub skill page](https://clawhub.ai/billzhuang6569/skills/feishu-bitable-upload)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Text]

**Output Format:** [Markdown with inline bash commands and terminal text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a Feishu file_token after successful upload; requires Feishu App ID, App Secret, and Bitable parent node inputs.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
