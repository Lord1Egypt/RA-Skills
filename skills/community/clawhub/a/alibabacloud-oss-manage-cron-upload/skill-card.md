## Description: <br>
Alibaba Cloud OSS scheduled local-folder sync skill using aliyun CLI, including integrated ossutil commands for incremental upload. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to validate prerequisites, run Alibaba Cloud OSS incremental upload commands, and configure local cron or Task Scheduler jobs for recurring local-folder backups to OSS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can configure recurring uploads from a local path to Alibaba Cloud OSS. <br>
Mitigation: Review the exact local source path, OSS bucket, prefix, schedule, log path, and generated script before installation or execution. <br>
Risk: The workflow requires Alibaba Cloud credentials and cloud storage permissions. <br>
Mitigation: Use a dedicated least-privilege RAM identity, keep credential setup outside the agent session, and avoid printing or entering secrets in chat or commands. <br>
Risk: Bucket creation and test-object cleanup can require broader OSS permissions such as PutBucket or DeleteObject. <br>
Mitigation: Grant PutBucket only when bucket creation is confirmed, and grant or use DeleteObject only when explicit cleanup is requested. <br>
Risk: The security scan flagged under-scoped test-file and credential-setup guidance. <br>
Mitigation: Do not allow substitute test folders, test uploads, or credential setup steps unless the user explicitly requests and reviews them. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/sdk-team/alibabacloud-oss-manage-cron-upload) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md) <br>
- [RAM Policies for OSS Scheduled Local Sync](references/ram-policies.md) <br>
- [Related APIs and CLI Commands](references/related-apis.md) <br>
- [Verification Method for OSS Scheduled Local Sync](references/verification-method.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Code] <br>
**Output Format:** [Markdown with inline bash, cron, and Windows scheduler command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires confirmed OSS region, bucket, prefix, local source path, schedule, maximum age window, operating system, and bucket existence status.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
