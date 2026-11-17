## Description:

Submit ready PyFlink code to Alibaba Cloud Realtime Compute for Apache Flink by routing storage, uploading artifacts, creating a Python deployment, and verifying the saved configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill to prepare Alibaba Cloud Flink Python deployments from already-built PyFlink artifacts, select workspace storage and engine settings, and verify the resulting deployment. It is intended for deployment submission workflows, not SQL authoring or deletion-only operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review warns that installer and update commands are unverified before execution.

Mitigation: Review the Aliyun CLI installation or update path before running it; prefer a pinned, verified CLI installation.

Risk: The security review warns that broader cloud permissions may be granted than a creation-only workflow needs.

Mitigation: Use least-privilege RAM policies for the current operation, limiting creation workflows to DescribeVvpInstances, CreateDeployment, GetDeployment, and ListEngineVersionMetadata when needed.

Risk: Alibaba Cloud credentials and deployment responses can contain sensitive values.

Mitigation: Configure credentials outside the agent conversation, do not print AK/SK values, and rely on the helper's sensitive-field redaction for API output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-flink-python-job-submission)
- [Aliyun CLI Installation](references/cli-installation-guide.md)
- [Python Deployment Configuration](references/create-deployment.md)
- [RAM Policies for Flink Python Job Submission](references/ram-policies.md)
- [Storage Routing and Artifact Upload](references/storage-routing.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call a bundled Python helper that emits JSON responses with sensitive values redacted.]

## Skill Version(s):

0.0.1 (source: release evidence and references/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
