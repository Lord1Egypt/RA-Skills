## Description: <br>
Alibaba Cloud DNS (Alidns) CLI skill. Use to query, add, and update DNS records via aliyun-cli, including CNAME setup for Function Compute custom domains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure engineers use this skill to inspect and change Alibaba Cloud DNS records with aliyun-cli, including CNAME setup for Function Compute custom domains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change live Alibaba Cloud DNS records. <br>
Mitigation: Manually confirm each domain, record name, type, value, and region before running mutating commands. <br>
Risk: The workflow uses Alibaba Cloud credentials. <br>
Mitigation: Use a RAM user or role limited to the required DNS zones and actions, and prefer environment variables or a secure credential flow over pasting long-lived secrets into shell commands. <br>
Risk: The skill installs and runs aliyun-cli from a download source. <br>
Mitigation: Verify the CLI download source before installation when possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cinience/alicloud-network-dns-cli) <br>
- [Official source list](references/sources.md) <br>
- [Install Alibaba Cloud CLI on Linux](https://help.aliyun.com/zh/cli/install-cli-on-linux) <br>
- [Alidns AddDomainRecord API](https://help.aliyun.com/zh/dns/api-alidns-2015-01-09-adddomainrecord) <br>
- [Alidns DescribeSubDomainRecords API](https://help.aliyun.com/zh/dns/api-alidns-2015-01-09-describesubdomainrecords) <br>
- [Function Compute custom domain CNAME guidance](https://www.alibabacloud.com/help/en/functioncompute/fc/user-guide/configure-custom-domain-names) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create command outputs and evidence files under output/alicloud-network-dns-cli/.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
