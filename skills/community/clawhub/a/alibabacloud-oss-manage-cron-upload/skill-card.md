## Description:

Helps agents plan, validate, and execute recurring local-folder uploads to Alibaba Cloud OSS using aliyun CLI integrated ossutil commands, cron or Task Scheduler configuration, and least-privilege RAM guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to configure recurring incremental uploads from a local folder to an Alibaba Cloud OSS bucket and verify CLI credentials, bucket prerequisites, upload commands, scheduler setup, and cleanup boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide cloud and local mutations, including bucket creation, object upload, optional object deletion, and scheduler persistence.

Mitigation: Run it only with a least-privilege Alibaba Cloud profile, review generated OSS and scheduler commands before applying them, and require explicit user confirmation for bucket creation or cleanup.

Risk: CLI installation and plugin setup may fetch or enable tooling outside the skill package.

Mitigation: Verify downloaded CLI binaries through trusted Alibaba Cloud distribution channels and avoid broad global auto-plugin installation unless operationally required.

Risk: Placeholder local data could be created or uploaded if the real source path is missing.

Mitigation: Confirm the real absolute local source path exists before upload testing and do not create or upload substitute data unless the user explicitly approves that test scope.

## Reference(s):

- [Acceptance Criteria](references/acceptance-criteria.md)
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md)
- [RAM Policies for OSS Scheduled Local Sync](references/ram-policies.md)
- [Related APIs and CLI Commands](references/related-apis.md)
- [Verification Method for OSS Scheduled Local Sync](references/verification-method.md)
- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-oss-manage-cron-upload)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Alibaba Cloud OSS and local scheduler changes; live commands require validated user parameters and an existing least-privilege Alibaba Cloud CLI profile.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
