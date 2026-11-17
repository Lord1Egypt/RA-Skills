## Description:

Uploads local files to Alibaba Cloud OSS and generates temporary signed access URLs using Aliyun OSS credentials supplied through environment variables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chengjiaxiongkf](https://clawhub.ai/user/chengjiaxiongkf)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to upload selected local files to Alibaba Cloud Object Storage Service and return temporary signed URLs for controlled file sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chosen local files are uploaded to Alibaba Cloud OSS.

Mitigation: Use the skill only when OSS upload is intended, avoid sensitive files unless sharing is approved, and confirm the target bucket and object key before upload.

Risk: OSS AccessKeys are required in environment variables.

Mitigation: Use least-privileged AccessKeys, keep secrets out of prompts and logs, and rotate credentials according to the user's cloud security policy.

Risk: Temporary signed URLs can expose uploaded objects for their validity period.

Mitigation: Use private buckets, choose short expirations, and share signed URLs only with intended recipients.

Risk: A misconfigured endpoint or bucket could send data to the wrong OSS location.

Mitigation: Verify the HTTPS Aliyun OSS endpoint and bucket name before running upload or URL generation commands.

## Reference(s):

- [Aliyun OSS configuration guide](references/config.md)
- [Aliyun OSS regions and endpoints](https://help.aliyun.com/document_detail/31837.html)
- [Alibaba Cloud console](https://www.aliyun.com/)
- [ClawHub skill page](https://clawhub.ai/chengjiaxiongkf/skills/aliyun-oss-upload)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and returned URL text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns temporary signed URLs; default expiry is 3600 seconds.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
