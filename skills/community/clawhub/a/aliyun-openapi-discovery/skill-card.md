## Description: <br>
Use when discovering and reconciling Alibaba Cloud product catalogs from Ticket System, Support & Service, and BSS OpenAPI; fetch OpenAPI product/version/API metadata; and summarize API coverage to plan new skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to collect and reconcile Alibaba Cloud product catalogs, retrieve OpenAPI metadata, and produce product-to-API coverage or gap reports for planning skill generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated Alibaba Cloud API requests can expose broad cloud privileges if run with long-lived or over-scoped credentials. <br>
Mitigation: Use explicit least-privilege or short-lived credentials and run the scripts in a controlled workspace. <br>
Risk: Generated product metadata can influence local output paths when fetching per-product API documentation. <br>
Mitigation: Review or sanitize generated product metadata before large API-documentation fetches, and keep generated files confined to the documented output directory. <br>
Risk: OpenAPI metadata discovery can make many network requests and produce large local reports. <br>
Mitigation: Use dry-run filters such as OPENAPI_META_MAX_PRODUCTS, OPENAPI_META_PRODUCTS, and OPENAPI_META_VERSIONS before broad discovery runs. <br>


## Reference(s): <br>
- [Product Source APIs](references/product-sources.md) <br>
- [OpenAPI Metadata Endpoints](references/openapi-meta.md) <br>
- [Alibaba Cloud OpenAPI product metadata endpoint](https://api.aliyun.com/meta/v1/products.json?language=EN_US) <br>
- [Aliyun Openapi Discovery on ClawHub](https://clawhub.ai/cinience/aliyun-openapi-discovery) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON files] <br>
**Output Format:** [Markdown guidance with inline shell commands; bundled scripts generate JSON and Markdown reports under output/.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated artifacts include product lists, product-to-API mappings, API count summaries, and coverage or gap reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
