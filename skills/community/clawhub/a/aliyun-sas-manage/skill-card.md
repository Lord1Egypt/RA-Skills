## Description: <br>
Use when managing Alibaba Cloud Security Center (Sas) via OpenAPI/SDK, including Security Center resource operations, configuration updates, status queries, and troubleshooting Sas API or security workflow issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud security operators use this skill to discover Alibaba Cloud Security Center Sas APIs, plan inventory or configuration operations, call APIs through official tooling, and verify results with describe or list operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use Alibaba Cloud credentials and guide Security Center configuration changes. <br>
Mitigation: Use least-privilege credentials, confirm the region, resource IDs, and exact API action before any mutating operation. <br>
Risk: Saved outputs may contain sensitive cloud security details. <br>
Mitigation: Review and clean up files under output/aliyun-sas-manage/ when they contain security findings, resource identifiers, or API response details. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/cinience/aliyun-sas-manage) <br>
- [OpenAPI product page](https://api.aliyun.com/product/Sas) <br>
- [Sas API list metadata](https://api.aliyun.com/meta/v1/products/Sas/versions/2021-01-14/api-docs.json) <br>
- [Sas single API definition metadata](https://api.aliyun.com/meta/v1/products/Sas/versions/2021-01-14/apis/{ApiName}/api.json) <br>
- [sources.md](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, API calls, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated artifacts may include JSON API metadata and Markdown API lists.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated files are directed to output/aliyun-sas-manage/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
