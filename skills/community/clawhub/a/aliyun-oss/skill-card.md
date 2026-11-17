## Description:

阿里云OSS文件上传工具 - 安全、高效的文件上传和临时链接生成

This skill is ready for commercial/non-commercial use.

## Publisher:

[jixsonwang](https://clawhub.ai/user/jixsonwang)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to upload selected local files to Aliyun OSS, create object paths, search by filename, and return temporary or standard access URLs for sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload arbitrary readable local files to Aliyun OSS.

Mitigation: Restrict the agent to explicit user-selected files or approved workspace paths before upload.

Risk: Long-lived AK/SK credentials in the config file can expose the bucket if mishandled.

Mitigation: Use a tightly scoped Aliyun RAM user or STS credentials, protect the config file with strict permissions, and rotate credentials.

Risk: Public-read object ACLs or shared URLs can expose uploaded content beyond the intended audience.

Mitigation: Avoid public-read ACLs by default and use short-lived access URLs only when sharing is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jixsonwang/skills/aliyun-oss)
- [Publisher profile](https://clawhub.ai/user/jixsonwang)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Plain text status messages and JSON-like upload or search results containing OSS object paths and URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include presigned URLs, standard object URLs, file sizes, and error details.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
