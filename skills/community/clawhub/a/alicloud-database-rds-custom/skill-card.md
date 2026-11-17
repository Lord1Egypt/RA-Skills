## Description:

Queries Alibaba Cloud RDS Custom (RC) instances and related resources with the aliyun CLI and RDS APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chucklong](https://clawhub.ai/user/chucklong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to prepare aliyun CLI commands and guidance for inspecting Alibaba Cloud RDS Custom instances, attributes, disks, snapshots, metrics, KubeConfig, node pools, and VNC URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to configure Alibaba Cloud credentials that may be powerful if the account is not scoped.

Mitigation: Use a least-privilege Alibaba Cloud RAM user limited to the specific read-only RDS Custom APIs required for the task.

Risk: Some supported queries can return sensitive operational material such as KubeConfig, VNC URLs, private IPs, VPC IDs, or AccessKey-related configuration.

Mitigation: Treat returned credentials, access URLs, network identifiers, and configuration files as sensitive and avoid sharing them in logs or public outputs.

Risk: The documented CLI installation path includes a curl-to-bash installer.

Mitigation: Verify the installer independently or use an approved installation method before running it.

## Reference(s):

- [DescribeRCInstances API Reference](references/api-docs.md)
- [Alibaba Cloud CLI Documentation](https://help.aliyun.com/product/29987.html)
- [RDS API Documentation](https://help.aliyun.com/document_detail/26223.html)
- [DescribeRCInstances OpenAPI Portal](https://api.aliyun.com/api?product=Rds&api=DescribeRCInstances)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON/jq examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include aliyun CLI invocations that call Alibaba Cloud RDS APIs and parse JSON responses with jq.]

## Skill Version(s):

1.14.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
