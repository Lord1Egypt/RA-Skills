## Description: <br>
Cloudflare R2 S3 兼容存储工具，支持配置 API 密钥、上传文件并获取公开访问地址。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chao-eng](https://clawhub.ai/user/chao-eng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure Cloudflare R2 credentials, upload local files to an R2 bucket, list stored objects, delete objects, and retrieve public URLs for uploaded files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploads can be public by default. <br>
Mitigation: Use private mode or set default public access to false unless the object is intended for public access; avoid uploading sensitive files to public buckets. <br>
Risk: The delete command can remove bucket objects without an additional safety prompt. <br>
Mitigation: Require clear human confirmation before deletion and use an R2 token scoped only to the intended bucket. <br>
Risk: R2 access keys are required for operation. <br>
Mitigation: Use a dedicated least-privilege R2 token and keep secrets out of version control. <br>


## Reference(s): <br>
- [Configuration example](references/config_example.env) <br>
- [ClawHub skill page](https://clawhub.ai/chao-eng/cloudflare-r2-s3) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Cloudflare R2 account credentials and boto3; uploads are public by default unless private mode is selected.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
