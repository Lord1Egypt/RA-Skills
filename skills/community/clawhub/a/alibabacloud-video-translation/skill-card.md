## Description:

Guides agents through Alibaba Cloud IMS video translation workflows for subtitle extraction, subtitle translation, and speech-synthesis translation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and media operations teams use this skill to prepare Alibaba Cloud OSS inputs, choose subtitle or speech translation options, submit IMS jobs, poll for completion, and retrieve translated video or subtitle outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Videos, subtitles, credentials, and signed URLs may expose sensitive content if handled carelessly.

Mitigation: Treat media, subtitles, credentials, and signed URLs as sensitive; share signed URLs only when needed and with short expirations.

Risk: Alibaba Cloud credentials and broad OSS permissions can grant more access than the video translation workflow requires.

Mitigation: Use a dedicated least-privileged RAM user or role, restrict OSS access to specific input and output buckets, avoid root account keys, and prefer temporary credentials.

Risk: Automatically installing CLI plugins or running generated shell commands can introduce supply-chain or execution risk.

Mitigation: Review dependencies, plugins, and generated commands before execution, and enable automatic plugin installation only in trusted environments.

Risk: Cloud processing may send user media and subtitle data to Alibaba Cloud services.

Mitigation: Use only non-confidential or organization-approved media for Alibaba Cloud processing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-video-translation)
- [Workflow Details](artifact/references/workflow-details.md)
- [API Parameters for Video Translation](artifact/references/api-parameters.md)
- [CLI Command Templates](artifact/references/cli-commands.md)
- [RAM Policies for Video Translation Skill](artifact/references/ram-policies.md)
- [Troubleshooting Guide for Video Translation Skill](artifact/references/troubleshooting.md)
- [Aliyun CLI Installation and Configuration Guide](artifact/references/cli-installation-guide.md)
- [Alibaba Cloud Video Translation Parameters](https://help.aliyun.com/zh/ims/use-cases/introduction-and-examples-of-video-translation-parameters)
- [Alibaba Cloud CLI Documentation](https://help.aliyun.com/zh/cli/)
- [IMS Video Translation Product Page](https://help.aliyun.com/zh/ims/video-translation)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, code, configuration]

**Output Format:** [Markdown guidance with inline shell commands and optional Python CLI usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Alibaba Cloud job IDs, status summaries, SRT subtitle content, translated media URLs, and signed URL retrieval guidance.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
