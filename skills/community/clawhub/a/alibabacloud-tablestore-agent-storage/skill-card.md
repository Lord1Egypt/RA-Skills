## Description:

Helps developers build and manage Alibaba Cloud Tablestore knowledge bases with the tablestore-agent-storage Python SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure Alibaba Cloud credentials and Tablestore resources, then create, connect, populate, retrieve from, and optionally sync knowledge bases backed by Tablestore and OSS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud credentials may be stored locally or exposed through configuration handling.

Mitigation: Use temporary or least-privilege Alibaba Cloud credentials, prefer the default credential chain, and avoid saving AK/SK or STS tokens in project JSON.

Risk: Installer guidance includes privileged or curl-to-shell patterns.

Mitigation: Verify installer sources and downloaded artifacts before running privileged installation commands.

Risk: Scheduled sync can repeatedly move local files into cloud storage if configured incorrectly.

Mitigation: Enable scheduled sync only after confirming the directory, OSS bucket, sync command, frequency, and removal procedure.

Risk: Automatic plugin installation can install dependencies without deliberate review.

Mitigation: Keep automatic plugin installation disabled unless the operator has reviewed the plugins and source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-tablestore-agent-storage)
- [Credentials Configuration](references/credentials.md)
- [Tablestore Instance Operations](references/tablestore-instance.md)
- [RAM Permissions](references/ram-policies.md)
- [Metadata Reference](references/metadata.md)
- [Alibaba Cloud CLI Installation Guide](references/aliyun-cli-installation-guide.md)
- [Tablestore CLI Installation Guide](references/tablestore-cli-installation-guide.md)
- [ossutil Installation Guide](references/ossutil-installation-guide.md)
- [Alibaba Cloud CLI documentation](https://help.aliyun.com/zh/cli/)
- [Tablestore CLI documentation](https://help.aliyun.com/zh/tablestore/developer-reference/tablestore-cli)
- [ossutil documentation](https://help.aliyun.com/zh/oss/developer-reference/ossutil-overview/)
- [Alibaba Cloud Credentials for Python](https://help.aliyun.com/zh/sdk/developer-reference/v2-manage-python-access-credentials)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, JSON configuration examples, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create configuration, sync script, and sync cache files under tablestore_agent_storage/ when the user opts into those workflows.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
