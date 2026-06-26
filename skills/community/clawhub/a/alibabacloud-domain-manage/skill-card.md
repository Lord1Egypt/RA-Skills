## Description: <br>
Queries Alibaba Cloud domain details, domain lists, advanced search results, and instance ID lookups through Aliyun CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud operators, and account administrators use this skill to inspect Alibaba Cloud domain inventory and domain status without performing domain write operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses the local Aliyun CLI with the user's configured Alibaba Cloud identity to read domain inventory and details. <br>
Mitigation: Use a dedicated read-only RAM user or role and grant only the domain query permissions documented by the skill. <br>
Risk: The workflow can change local Aliyun CLI setup by enabling automatic plugin installation, updating plugins, enabling AI-mode, and suggesting remote CLI installation or update commands. <br>
Mitigation: Review installation, plugin update, and AI-mode commands before execution, and install Aliyun CLI through a trusted and verifiable method. <br>
Risk: Domain detail responses can include registrant contact information such as name and email. <br>
Mitigation: Avoid displaying registrant name or email unless needed for the user's request. <br>


## Reference(s): <br>
- [Related Commands](references/related-commands.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [Credential Check](references/credential-check.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Aliyun CLI Guide](https://help.aliyun.com/zh/cli/) <br>
- [QueryDomainList API](https://help.aliyun.com/zh/dws/developer-reference/api-domain-2018-01-29-querydomainlist) <br>
- [QueryAdvancedDomainList API](https://help.aliyun.com/zh/dws/developer-reference/api-domain-2018-01-29-queryadvanceddomainlist) <br>
- [QueryDomainByDomainName API](https://help.aliyun.com/zh/dws/developer-reference/api-domain-2018-01-29-querydomainbydomainname) <br>
- [QueryDomainByInstanceId API](https://help.aliyun.com/zh/dws/developer-reference/api-domain-2018-01-29-querydomainbyinstanceid) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, API call results] <br>
**Output Format:** [Markdown summaries with inline shell commands and Alibaba Cloud domain query results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Displays only data returned by Alibaba Cloud API responses and may include pagination details, domain status, dates, DNS servers, registrant type, and related domain metadata.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
