## Description: <br>
Uploads local files to Alibaba Cloud OSS and can generate temporary signed access URLs for stored objects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chengjiaxiongkf](https://clawhub.ai/user/chengjiaxiongkf) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to upload selected local files to an Alibaba Cloud OSS bucket and share them through temporary signed URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload selected local files to an Aliyun OSS bucket. <br>
Mitigation: Confirm each file is intended for upload before running the skill, and use a private bucket unless public access is explicitly required. <br>
Risk: Broad or long-lived Aliyun credentials could expose more OSS access than the workflow needs. <br>
Mitigation: Use dedicated least-privilege RAM credentials or temporary STS credentials scoped to the required bucket and actions. <br>
Risk: Signed URLs can grant temporary access to uploaded objects. <br>
Mitigation: Keep signed URL expirations short and share generated links only with intended recipients. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chengjiaxiongkf/aliyun-oss-upload) <br>
- [Aliyun OSS Configuration Guide](references/config.md) <br>
- [Alibaba Cloud OSS regions and endpoints](https://help.aliyun.com/document_detail/31837.html) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Text] <br>
**Output Format:** [Markdown with inline shell commands and plain-text URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return temporary signed OSS URLs; the default expiry is 3600 seconds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
