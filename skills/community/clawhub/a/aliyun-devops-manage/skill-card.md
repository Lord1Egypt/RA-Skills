## Description: <br>
Use when managing Alibaba Cloud DevOps (Yunxiao 2020) via OpenAPI/SDK, including project/repository/pipeline resource discovery, read-only inspection, and safe change planning before mutating operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to inspect Alibaba Cloud DevOps projects, repositories, pipelines, work items, tests, releases, and API metadata. It supports read-only inventory, evidence collection, and safe planning before approved mutating operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Alibaba Cloud credentials and can access DevOps resources. <br>
Mitigation: Use least-privilege or read-only credentials where possible, prefer environment variables, and keep generated outputs private and out of source control. <br>
Risk: Create, update, run, or stop operations can change Alibaba Cloud DevOps resources. <br>
Mitigation: Require explicit owner approval, confirm target scope and change window, run read-only discovery first, and prepare a rollback plan before mutating operations. <br>
Risk: Network calls to Alibaba Cloud OpenAPI and metadata endpoints may expose request context or retrieve live service data. <br>
Mitigation: Install and run the SDK only when working with intended Alibaba Cloud DevOps resources, and record key parameters needed for reproducible evidence. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cinience/aliyun-devops-manage) <br>
- [DevOps product page in API Explorer](https://api.aliyun.com/product/devops) <br>
- [DevOps OpenAPI metadata](https://api.aliyun.com/meta/v1/products/devops/versions/2021-06-25/api-docs.json) <br>
- [DevOps product metadata](https://api.aliyun.com/meta/v1/products) <br>
- [Alibaba Cloud API Explorer](https://api.aliyun.com/) <br>
- [Alibaba Cloud DevOps documentation](https://www.alibabacloud.com/help/en/yunxiao) <br>
- [API quick map](references/api_quick_map.md) <br>
- [Operation templates](references/templates.md) <br>
- [Source list](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, markdown] <br>
**Output Format:** [Markdown with inline shell commands and generated local evidence files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate API metadata, command output, and response summaries under output/aliyun-devops-manage/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
