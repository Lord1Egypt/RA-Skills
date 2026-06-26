## Description: <br>
Use when managing Alibaba Cloud AIContent (AiContent) via OpenAPI/SDK, including listing assets, creating or updating generation configurations, checking task status, and troubleshooting failed content jobs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Alibaba Cloud AIContent resources through OpenAPI or SDK workflows, including API discovery, generation configuration changes, task status checks, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Alibaba Cloud credentials and can guide create, update, modify, or set operations on AIContent resources. <br>
Mitigation: Use least-privilege Alibaba Cloud credentials, confirm region and resource identifiers, and review each mutating action before execution. <br>
Risk: Saved outputs may contain operational metadata or API response details. <br>
Mitigation: Treat files under output/aliyun-aicontent-generate/ as sensitive, limit sharing, and remove retained responses when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cinience/aliyun-aicontent-generate) <br>
- [OpenAPI Product Page: AiContent](https://api.aliyun.com/product/AiContent) <br>
- [AiContent API List Metadata](https://api.aliyun.com/meta/v1/products/AiContent/versions/20240611/api-docs.json) <br>
- [AiContent Single API Metadata Template](https://api.aliyun.com/meta/v1/products/AiContent/versions/20240611/apis/{ApiName}/api.json) <br>
- [sources.md](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated JSON or Markdown API inventory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves command outputs and API response summaries under output/aliyun-aicontent-generate/ when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
