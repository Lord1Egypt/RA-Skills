## Description: <br>
Use when you need to query, add, and update DNS records via aliyun-cli, including CNAME setup for Function Compute custom domains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to query, add, and update Alibaba Cloud DNS records with aliyun-cli and prepare Function Compute custom domain CNAME records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DNS record additions or changes can misroute traffic or disrupt domain resolution. <br>
Mitigation: Confirm the domain, RR, record type, value, region, and whether the task is mutating; run a minimal read-only query first and require explicit confirmation before add or update commands. <br>
Risk: Cloud credentials can be exposed or over-permissioned during CLI configuration and command execution. <br>
Mitigation: Use a dedicated least-privilege RAM credential, prefer environment variables or secure local configuration, and avoid pasting long-lived secrets into chat or evidence files. <br>
Risk: Installing aliyun-cli from a remote archive introduces supply-chain and version drift risk. <br>
Mitigation: Verify the CLI source or pin a trusted release where possible before installation. <br>


## Reference(s): <br>
- [Official source list](references/sources.md) <br>
- [Install Alibaba Cloud CLI on Linux](https://help.aliyun.com/zh/cli/install-cli-on-linux) <br>
- [Alidns AddDomainRecord API](https://help.aliyun.com/zh/dns/api-alidns-2015-01-09-adddomainrecord) <br>
- [Alidns DescribeSubDomainRecords API](https://help.aliyun.com/zh/dns/api-alidns-2015-01-09-describesubdomainrecords) <br>
- [Function Compute custom domain names](https://www.alibabacloud.com/help/en/functioncompute/fc/user-guide/configure-custom-domain-names) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and command parameter guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include read-only DNS queries, mutating DNS command proposals, validation notes, and saved evidence paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
