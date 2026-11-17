## Description:

Use when you need to query, add, and update DNS records via aliyun-cli, including CNAME setup for Function Compute custom domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to query and change Alibaba Cloud DNS records through aliyun-cli, including CNAME setup for Function Compute custom domains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unverified mutable aliyun-cli binary.

Mitigation: Review before installing, and use a pinned version with checksum verification when possible.

Risk: DNS record additions or updates can disrupt production resolution.

Mitigation: Require explicit confirmation and rollback notes before mutating operations, then verify results with a bounded read-only query.

Risk: Alibaba Cloud credentials may be over-scoped or exposed during CLI configuration.

Mitigation: Use least-privilege credentials scoped to the intended DNS zone, preferably through temporary environment variables or a dedicated temporary profile.

## Reference(s):

- [Official source list](references/sources.md)
- [aliyun-cli installation](https://help.aliyun.com/zh/cli/install-cli-on-linux)
- [Alidns AddDomainRecord API](https://help.aliyun.com/zh/dns/api-alidns-2015-01-09-adddomainrecord)
- [Alidns DescribeSubDomainRecords API](https://help.aliyun.com/zh/dns/api-alidns-2015-01-09-describesubdomainrecords)
- [Function Compute custom domain configuration](https://www.alibabacloud.com/help/en/functioncompute/fc/user-guide/configure-custom-domain-names)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Text]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save command outputs, API response summaries, and key operation parameters under output/aliyun-dns-cli/.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
