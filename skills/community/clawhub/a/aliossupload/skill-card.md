## Description:

阿里云 OSS 文件上传工具。支持单文件上传，适用于将本地文件上传到阿里云 OSS 并获取访问链接。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerryxn](https://clawhub.ai/user/jerryxn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users can use this skill to upload explicitly named local files to an Alibaba Cloud OSS bucket and receive the resulting object URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload local files to Alibaba Cloud OSS using configured credentials, which may expose secrets or regulated data if file paths or bucket access are not reviewed.

Mitigation: Use a RAM access key limited to the intended bucket and actions, review each file path before upload, and avoid uploading secrets or regulated data.

Risk: Returned object URLs may be inaccessible or unintentionally public depending on bucket ACL and object policy.

Mitigation: Verify bucket ACLs, object policies, and URL exposure before sharing returned links.

Risk: Running the Python script directly with credentials can create or upload a test object.

Mitigation: Run direct script tests only against a controlled bucket and remove generated test objects after validation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jerryxn/skills/aliossupload)
- [jerryxn ClawHub Publisher Profile](https://clawhub.ai/user/jerryxn)
- [Alibaba Cloud OSS Documentation](https://help.aliyun.com/product/31815.html)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python and shell snippets; runtime upload calls return JSON-like dictionaries containing status, URL, object name, size, elapsed time, and speed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Alibaba Cloud OSS credentials and bucket configuration through environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata, clawhub.yaml, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
