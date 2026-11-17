## Description:

Alibabacloud Video Forge guides agents through Alibaba Cloud Media Processing Service workflows for video upload, media probing, cover snapshots, multi-resolution transcoding, content moderation, and output retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, media operations teams, and content platform engineers use this skill to standardize video assets on Alibaba Cloud by uploading source media to OSS, submitting MPS snapshot/transcoding/moderation jobs, polling job status, and retrieving processed outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer and plugin update steps can run unverified latest code or automatically install Aliyun CLI plugins.

Mitigation: Review install sources before use, avoid curl-to-bash and unverified latest binary installers, and avoid enabling automatic CLI plugin installation unless the environment explicitly allows it.

Risk: Cloud actions can use broad permissions and include recursive or forceable OSS deletion.

Mitigation: Use a dedicated low-privilege RAM role scoped to one OSS bucket or prefix where possible, avoid full-access policy examples, preview deletes with dry-run, and do not use force for recursive deletes.

Risk: Credential and environment loading can expose or mix sensitive Alibaba Cloud settings if reused across shells or projects.

Mitigation: Use the Alibaba Cloud default credential chain, never print or read raw credentials, and keep only required Alibaba Cloud settings in a dedicated config environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-video-forge)
- [Capability Overview](references/capability-overview.md)
- [Security Guidelines](references/security-guidelines.md)
- [RAM Permission Policies](references/ram-policies.md)
- [Script Parameter Reference](references/params.md)
- [Script Usage Examples](references/scripts-detail.md)
- [Verification Method](references/verification-method.md)
- [CLI Installation Guide](references/cli-installation-guide.md)
- [SDK Installation Guide](references/sdk-installation.md)
- [Troubleshooting](references/troubleshooting.md)
- [Alibaba Cloud MPS RAM Authorization Overview](https://help.aliyun.com/zh/mps/developer-reference/api-mts-2014-06-18-overview)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code, JSON, Files]

**Output Format:** [Markdown guidance with inline shell commands, Python script invocations, optional JSON responses, and generated or downloaded media files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Alibaba Cloud OSS object paths, MPS job IDs, task status summaries, content moderation results, signed URLs, and locally downloaded media artifacts.]

## Skill Version(s):

0.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
