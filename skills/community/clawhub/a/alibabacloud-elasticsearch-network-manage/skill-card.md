## Description:

Alibaba Cloud Elasticsearch Instance Network Management Skill for managing Elasticsearch instance network configurations, including network triggering, Kibana PVL network, white IP lists, HTTPS settings, and Kibana SSO authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to manage Alibaba Cloud Elasticsearch network access, Kibana private network settings, whitelists, HTTPS, and Kibana SSO through Aliyun CLI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supply-chain exposure from shell-based CLI installation and automatic plugin update flows.

Mitigation: Use a verified package-manager or signed and pinned Aliyun CLI installation path, and avoid global automatic plugin installation.

Risk: Overbroad cloud permissions can allow unintended Elasticsearch network changes.

Mitigation: Scope RAM permissions to one confirmed instance and one approved action where possible, and prefer temporary or role-based credentials.

Risk: Network, allowlist, SSO, or HTTPS changes can expose services or weaken access controls.

Mitigation: Require explicit confirmation before public exposure, allowlist replacement, SSO changes, or disabling HTTPS.

## Reference(s):

- [Acceptance Criteria](references/acceptance-criteria.md)
- [Aliyun CLI Installation and Configuration Guide](references/cli-installation-guide.md)
- [RAM Policies](references/ram-policies.md)
- [Related APIs](references/related-apis.md)
- [Verification Method](references/verification-method.md)
- [TriggerNetwork API Documentation](https://help.aliyun.com/zh/es/developer-reference/api-triggernetwork)
- [EnableKibanaPvlNetwork API Documentation](https://help.aliyun.com/zh/es/developer-reference/api-enablekibanapvlnetwork)
- [DisableKibanaPvlNetwork API Documentation](https://help.aliyun.com/zh/es/developer-reference/api-disablekibanapvlnetwork)
- [ModifyWhiteIps API Documentation](https://help.aliyun.com/zh/es/developer-reference/api-modifywhiteips)
- [OpenHttps API Documentation](https://help.aliyun.com/zh/es/developer-reference/api-openhttps)
- [CloseHttps API Documentation](https://help.aliyun.com/zh/es/developer-reference/api-closehttps)
- [UpdateKibanaSso API Documentation](https://api.aliyun.com/document/elasticsearch/2017-06-13/UpdateKibanaSso)
- [DescribeInstance API Documentation](https://help.aliyun.com/zh/es/developer-reference/api-describeinstance)
- [Aliyun CLI Documentation](https://help.aliyun.com/zh/cli/)
- [Aliyun CLI Repository](https://github.com/aliyun/aliyun-cli)
- [RAM Policy Overview](https://help.aliyun.com/document_detail/93732.html)
- [Elasticsearch Authorization Information](https://help.aliyun.com/document_detail/169951.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and Aliyun CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation for instance, region, network, whitelist, VPC, security group, HTTPS, and SSO changes.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
