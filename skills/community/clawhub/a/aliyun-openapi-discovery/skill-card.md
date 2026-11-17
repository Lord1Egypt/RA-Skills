## Description:

Discovers and reconciles Alibaba Cloud product catalogs from Ticket System, Support & Service, BSS OpenAPI, and OpenAPI metadata so agents can plan product-to-API coverage and skill gap reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to collect Alibaba Cloud product lists, retrieve OpenAPI product/version/API metadata, merge catalogs, and generate coverage or gap reports for skill planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send signed Alibaba Cloud requests to endpoint values supplied through environment variables.

Mitigation: Use short-lived, least-privilege Alibaba Cloud credentials and verify every endpoint environment variable before running scripts.

Risk: Untrusted product metadata files or broad workspace access can affect local outputs.

Mitigation: Run the skill from a controlled workspace, keep generated files under output/, and avoid untrusted metadata inputs.

## Reference(s):

- [Product Source APIs](references/product-sources.md)
- [OpenAPI Metadata Endpoints](references/openapi-meta.md)
- [Alibaba Cloud OpenAPI product metadata](https://api.aliyun.com/meta/v1/products.json?language=EN_US)
- [Alibaba Cloud OpenAPI API docs metadata](https://api.aliyun.com/meta/v1/products/{ProductCode}/versions/{Version}/api-docs.json)
- [Alibaba Cloud OpenAPI API definition metadata](https://api.aliyun.com/meta/v1/products/{ProductCode}/versions/{Version}/apis/{ApiName}/api.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with bash command examples; bundled Python scripts generate JSON and Markdown output files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated artifacts are expected under output/; OpenAPI metadata fetches can be filtered by product, version, or maximum product count.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
