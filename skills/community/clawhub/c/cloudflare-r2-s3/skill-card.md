## Description:

Cloudflare R2 S3 兼容存储工具，支持配置 API 密钥、上传文件并获取公开访问地址。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chao-eng](https://clawhub.ai/user/chao-eng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure Cloudflare R2 or another S3-compatible storage service, upload local files, list bucket objects, delete objects, and retrieve public URLs when sharing stored assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded files may be publicly accessible by default.

Mitigation: Avoid uploading secrets or private documents, and use --private or public=False when files should not be shared publicly.

Risk: The tool can write to and delete objects from the configured R2 bucket without built-in delete confirmation.

Mitigation: Use a dedicated bucket with a restricted R2 token and manually confirm object names before deleting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chao-eng/skills/cloudflare-r2-s3)
- [Configuration Example](references/config_example.env)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return public object URLs and JSON-like upload, list, delete, or connection-test results.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
