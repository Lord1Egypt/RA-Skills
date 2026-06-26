## Description: <br>
Discover and reconcile Alibaba Cloud product catalogs from Ticket System, Support & Service, and BSS OpenAPI; fetch OpenAPI product/version/API metadata; and summarize API coverage to plan new skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to collect Alibaba Cloud product catalogs, map products to OpenAPI metadata, and generate coverage or gap reports for planning new skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill queries Alibaba Cloud metadata and product APIs using provided credentials. <br>
Mitigation: Use narrowly scoped read-only or temporary Alibaba Cloud credentials before running the bundled scripts. <br>
Risk: Endpoint environment variables could be pointed at unexpected hosts. <br>
Mitigation: Keep endpoint variables pointed at official Alibaba Cloud domains before execution. <br>
Risk: Generated inventory and metadata files may reveal cloud product and API context. <br>
Mitigation: Review generated files before sharing them outside the intended audience. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cinience/alicloud-platform-openapi-product-api-discovery) <br>
- [Publisher profile](https://clawhub.ai/user/cinience) <br>
- [OpenAPI Metadata Endpoints](references/openapi-meta.md) <br>
- [Product Source APIs](references/product-sources.md) <br>
- [Alibaba Cloud OpenAPI metadata product list](https://api.aliyun.com/meta/v1/products.json?language=EN_US) <br>
- [Alibaba Cloud OpenAPI API docs metadata pattern](https://api.aliyun.com/meta/v1/products/{ProductCode}/versions/{Version}/api-docs.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and generated JSON or Markdown inventory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated files are directed under output/ and may include product lists, API metadata summaries, joined coverage reports, and skill gap reports.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
