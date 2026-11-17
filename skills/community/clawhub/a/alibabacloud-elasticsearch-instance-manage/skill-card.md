## Description:

Alibaba Cloud Elasticsearch Instance & Config Management Skill for managing Elasticsearch instance lifecycle, instance-side configuration, analyzer dictionaries, Kibana settings, cluster YML configuration, and plugins through the Aliyun CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to generate and verify Aliyun CLI workflows for Alibaba Cloud Elasticsearch instance lifecycle, configuration, plugin, snapshot, dictionary, and upgrade operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote CLI setup and automatic plugin updates can install or change local tooling unexpectedly.

Mitigation: Review setup manually, avoid piping remote installers into bash, and prefer pinned, verified Aliyun CLI and plugin versions.

Risk: Generated commands can perform broad cloud administration changes, including password, billing, restart, plugin, YML, and upgrade operations.

Mitigation: Use least-privilege RAM permissions for only the modules needed and require explicit confirmation before state-changing commands.

Risk: Snapshot and dictionary workflows can expose sensitive data if OSS buckets or credentials are handled poorly.

Mitigation: Use restricted OSS access or service-role access where possible, and rely on environment variables or configured CLI profiles without exposing access keys in conversation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-elasticsearch-instance-manage)
- [Instance lifecycle APIs](references/instance-manage.md)
- [Instance configuration APIs](references/config-manage.md)
- [Plugin management APIs](references/plugin-manage.md)
- [RAM permission policies](references/ram-policies.md)
- [Verification methods](references/verification-method.md)
- [Aliyun CLI installation guide](references/cli-installation-guide.md)
- [Alibaba Cloud Elasticsearch product page](https://www.aliyun.com/product/bigdata/elasticsearch)
- [Alibaba Cloud Elasticsearch API reference](https://next.api.aliyun.com/product/elasticsearch)
- [Alibaba Cloud CLI documentation](https://help.aliyun.com/zh/cli/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require user-provided region, instance identifiers, configured Alibaba Cloud credentials, and review before state-changing operations.]

## Skill Version(s):

0.0.5 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
