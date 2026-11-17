## Description:

Alibaba Cloud DNS (Alidns) CLI skill. Use to query, add, and update DNS records via aliyun-cli, including CNAME setup for Function Compute custom domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to query, add, and update Alibaba Cloud DNS records with aliyun-cli, including CNAME setup for Function Compute custom domains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unverified latest aliyun-cli release can introduce supply-chain risk.

Mitigation: Use a verified, pinned aliyun-cli release where possible before installation.

Risk: Passing Alibaba Cloud access-key secrets directly in command-line arguments can expose credentials.

Mitigation: Prefer least-privilege, short-lived credentials supplied through environment variables or a safer credential store.

Risk: Mutating DNS records can disrupt domain routing or Function Compute custom-domain setup.

Mitigation: Confirm the DNS target, record type, TTL, propagation impact, and rollback steps before any add or update operation.

## Reference(s):

- [Official source list](references/sources.md)
- [aliyun-cli installation](https://help.aliyun.com/zh/cli/install-cli-on-linux)
- [Alidns AddDomainRecord API](https://help.aliyun.com/zh/dns/api-alidns-2015-01-09-adddomainrecord)
- [Alidns DescribeSubDomainRecords API](https://help.aliyun.com/zh/dns/api-alidns-2015-01-09-describesubdomainrecords)
- [Function Compute custom domain CNAME guidance](https://www.alibabacloud.com/help/en/functioncompute/fc/user-guide/configure-custom-domain-names)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce command outputs and API response summaries under output/alicloud-network-dns-cli/ when executed.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
